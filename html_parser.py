#!/usr/bin/python
#-*-coding:utf-8*

#html_parser.py
#Role:HTML and CSS parser 

#Walle Cyril
#2015-12-02

##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##WebSpree
##Copyright (C) 2014 Walle Cyril
##
##WebSpree is free software: you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##WebSpree is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with WebSpree. If not, see <http://www.gnu.org/licenses/>.
##
##If you have questions concerning this license you may contact via email Walle Cyril
##by sending an email to the following adress:capocyril [ (a ] hotmail.com
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
r"""
Original file:C:\Python33\Lib\html\parser.py
"""

# This file is based on sgmllib.py, but the API is slightly different.

# XXX There should be a way to distinguish between PCDATA (parsed
# character data -- the normal case), RCDATA (replaceable character
# data -- only char and entity references and end tags are special)
# and CDATA (character data -- only end tags are special).
def do_nothing(a,b,c):
                pass
try:
    import _markupbase
except ImportError:
    import markupbase as _markupbase
import re
import warnings


##DATA##
from file_extractor import *
from Text__classes import *

# Regular expressions used for parsing

interesting_normal = re.compile('[&<]')
incomplete = re.compile('&[a-zA-Z#]')

entityref = re.compile('&([a-zA-Z][-.a-zA-Z0-9]*)[^a-zA-Z0-9]')
charref = re.compile('&#(?:[0-9]+|[xX][0-9a-fA-F]+)[^0-9a-fA-F]')

starttagopen = re.compile('<[a-zA-Z]')
piclose = re.compile('>')
commentclose = re.compile(r'--\s*>')
tagfind = re.compile('([a-zA-Z][-.a-zA-Z0-9:_]*)(?:\s|/(?!>))*')
# see http://www.w3.org/TR/html5/tokenization.html#tag-open-state
# and http://www.w3.org/TR/html5/tokenization.html#tag-name-state
tagfind_tolerant = re.compile('[a-zA-Z][^\t\n\r\f />\x00]*')
# Note:
#  1) the strict attrfind isn't really strict, but we can't make it
#     correctly strict without breaking backward compatibility;
#  2) if you change attrfind remember to update locatestarttagend too;
#  3) if you change attrfind and/or locatestarttagend the parser will
#     explode, so don't do it.
attrfind = re.compile(
    r'\s*([a-zA-Z_][-.:a-zA-Z_0-9]*)(\s*=\s*'
    r'(\'[^\']*\'|"[^"]*"|[^\s"\'=<>`]*))?')
attrfind_tolerant = re.compile(
    r'((?<=[\'"\s/])[^\s/>][^\s/=>]*)(\s*=+\s*'
    r'(\'[^\']*\'|"[^"]*"|(?![\'"])[^>\s]*))?(?:\s|/(?!>))*')
locatestarttagend = re.compile(r"""
  <[a-zA-Z][-.a-zA-Z0-9:_]*          # tag name
  (?:\s+                             # whitespace before attribute name
    (?:[a-zA-Z_][-.:a-zA-Z0-9_]*     # attribute name
      (?:\s*=\s*                     # value indicator
        (?:'[^']*'                   # LITA-enclosed value
          |\"[^\"]*\"                # LIT-enclosed value
          |[^'\">\s]+                # bare value
         )
       )?
     )
   )*
  \s*                                # trailing whitespace
""", re.VERBOSE)
locatestarttagend_tolerant = re.compile(r"""
  <[a-zA-Z][-.a-zA-Z0-9:_]*          # tag name
  (?:[\s/]*                          # optional whitespace before attribute name
    (?:(?<=['"\s/])[^\s/>][^\s/=>]*  # attribute name
      (?:\s*=+\s*                    # value indicator
        (?:'[^']*'                   # LITA-enclosed value
          |"[^"]*"                   # LIT-enclosed value
          |(?!['"])[^>\s]*           # bare value
         )
         (?:\s*,)*                   # possibly followed by a comma
       )?(?:\s|/(?!>))*
     )*
   )?
  \s*                                # trailing whitespace
""", re.VERBOSE)
endendtag = re.compile('>')
# the HTML 5 spec, section 8.1.2.2, doesn't allow spaces between
# </ and the tag name, so maybe this should be fixed
endtagfind = re.compile('</\s*([a-zA-Z][-.a-zA-Z0-9:_]*)\s*>')


class HTMLParseError(Exception):
    """Exception raised for all parse errors."""

    def __init__(self, msg, position=(None, None)):
        assert msg
        self.msg = msg
        self.lineno = position[0]
        self.offset = position[1]

    def __str__(self):
        result = self.msg
        if self.lineno is not None:
            result = result + ", at line %d" % self.lineno
        if self.offset is not None:
            result = result + ", column %d" % (self.offset + 1)
        return result


class HTMLParser(_markupbase.ParserBase):
    """Find tags and other markup and call handler functions.

        p = HTMLParser();p.feed(data);p.close()

    Start tags are handled by calling self.handle_starttag() or
    self.handle_startendtag(); end tags by self.handle_endtag().  The
    data between tags is passed from the parser to the derived class
    by calling self.handle_data() with the data as argument (the data
    may be split up in arbitrary chunks).  Entity references are
    passed by calling self.handle_entityref() with the entity
    reference as the argument.  Numeric character references are
    passed to self.handle_charref() with the string containing the
    reference as the argument.
    """
    VOID_ELEMENTS_5 = ("br", "hr", "img", "input", "link",
                       "meta","area", "base", "col", "command",
                       "embed", "keygen", "param", "source",
                       "track", "wbr")
    
    CDATA_CONTENT_ELEMENTS = ("script", "style")

    def __init__(self, strict=False, for_color=None):
        """Initialize and reset this instance.

        If strict is set to False (the default) the parser will parse invalid
        markup, otherwise it will raise an error.  Note that the strict mode
        is deprecated.
        """
        self.doctype_first = True
        self.declaration = ""
        self.start_list = []
        self.end_list = []
        self.content_list = []
        self.key_attribute_list = []
        self.value_attribute_list = []
        #dynamic_start_list contains opened tags at the moment you look it
        #if the document is valid it should be empty at the end
        self.dynamic_start_list = []
        self.close_before_error_list = []
        self.must_parent_errors = []

        if for_color:
            self.painter = for_color#function
        else:
            #most elegant way to do it ?
            self.painter = do_nothing        
        if strict:
            warnings.warn("The strict mode is deprecated.",
                          DeprecationWarning, stacklevel=2)
        self.strict = strict
        self.reset()

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        self.rawdata = ''
        self.lasttag = '???'
        self.interesting = interesting_normal
        self.cdata_elem = None
        _markupbase.ParserBase.reset(self)

    def feed(self, data):
        r"""Feed data to the parser.

        Call this as often as you want, with as little or as much text
        as you want (may include '\n').
        """
        self.rawdata = self.rawdata + data
        self.goahead(0)

    def close(self):
        """Handle any buffered data."""
        self.goahead(1)

    def error(self, message):
        raise HTMLParseError(message, self.getpos())

    __starttag_text = None

    def get_starttag_text(self):
        """Return full source of start tag: '<...>'."""
        return self.__starttag_text

    def set_cdata_mode(self, elem):
        self.cdata_elem = elem.lower()
        self.interesting = re.compile(r'</\s*{}\s*>'.format(self.cdata_elem), re.IGNORECASE)

    def clear_cdata_mode(self):
        self.interesting = interesting_normal
        self.cdata_elem = None

    # Internal -- handle data as far as reasonable.  May leave state
    # and data to be processed by a subsequent call.  If 'end' is
    # true, force handling all data as if followed by EOF marker.
    def goahead(self, end):
        rawdata = self.rawdata
        self.i = 0
        n = len(rawdata)
        while self.i < n:
            match = self.interesting.search(rawdata, self.i) # < or &
            if match:
                j = match.start()
            else:
                if self.cdata_elem:
                    break
                j = n
            if self.i < j:
                self.handle_data(rawdata[self.i:j])
            self.i = self.updatepos(self.i, j)
            if self.i == n: break
            startswith = rawdata.startswith
            if startswith('<', self.i):
                if starttagopen.match(rawdata, self.i): # < + letter
                    end_i = self.parse_starttag()
                    # future use len(self.dynamic_start_list) to add coulour itensity for more nested stuff
                    self.painter(self.i,end_i, "element")
                elif startswith("</", self.i):
                    end_i = self.parse_endtag()
                    self.painter(self.i,end_i, "element")
                elif startswith("<!--", self.i):
                    end_i = self.parse_comment(self.i)
                    self.painter(self.i,end_i, "comment")
                elif startswith("<?", self.i):
                    end_i = self.parse_pi(self.i)
                elif startswith("<!", self.i):
                    if self.strict:
                        end_i = self.parse_declaration(self.i)#! method not found !!!
                    else:
                        end_i = self.parse_html_declaration()
                        self.painter(self.i,end_i, "html_declaration")
                elif (self.i + 1) < n:
                    self.handle_data("<")
                    end_i = self.i + 1
                else:
                    break
                if end_i < 0:
                    if not end:
                        break
                    if self.strict:
                        self.error("EOF in middle of construct")
                    end_i = rawdata.find('>', self.i + 1)
                    if end_i < 0:
                        end_i = rawdata.find('<', self.i + 1)
                        if end_i < 0:
                            end_i = self.i + 1
                    else:
                        end_i += 1
                    self.handle_data(rawdata[self.i:end_i])
                self.i = self.updatepos(self.i, end_i)
            elif startswith("&#", self.i):
                match = charref.match(rawdata, self.i)
                if match:
                    name = match.group()[2:-1]
                    self.handle_charref(name)
                    end_i = match.end()
                    if not startswith(';', end_i-1):
                        end_i = end_i - 1
                    self.i = self.updatepos(self.i, end_i)
                    continue
                else:
                    if ";" in rawdata[self.i:]: #bail by consuming &#
                        self.handle_data(rawdata[0:2])
                        self.i = self.updatepos(self.i, 2)
                    break
            elif startswith('&', self.i):
                match = entityref.match(rawdata, self.i)
                if match:
                    name = match.group(1)
                    self.handle_entityref(name)
                    end_i = match.end()
                    if not startswith(';', end_i-1):
                        end_i = end_i - 1
                    self.i = self.updatepos(self.i, end_i)
                    continue
                match = incomplete.match(rawdata, self.i)
                if match:
                    # match.group() will contain at least 2 chars
                    if end and match.group() == rawdata[i:]:
                        if self.strict:
                            self.error("EOF in middle of entity or char ref")
                        else:
                            end_i = match.end()
                            if end_i <= self.i:
                                end_i = n
                            self.i = self.updatepos(self.i, self.i + 1)
                    # incomplete
                    break
                elif (self.i + 1) < n:
                    # not the end of the buffer, and can't be confused
                    # with some other construct
                    self.handle_data("&")
                    self.i = self.updatepos(self.i, self.i + 1)
                else:
                    break
            else:
                assert 0, "interesting.search() lied"
        # end while
        if end and self.i < n and not self.cdata_elem:
            self.handle_data(rawdata[self.i:n])
            self.i = self.updatepos(self.i, n)
        self.rawdata = rawdata[self.i:]

    # Internal -- parse html declarations, return length or -1 if not terminated
    # See w3.org/TR/html5/tokenization.html#markup-declaration-open-state
    # See also parse_declaration in _markupbase
    def parse_html_declaration(self):
        if self.i > 2:
            #Doctype declaration at the wrong place
            self.doctype_first = False
        rawdata = self.rawdata
        assert rawdata[self.i : self.i+2] == '<!', ('unexpected call to '
                                        'parse_html_declaration()')
        if rawdata[self.i:self.i+4] == '<!--':
            # this case is actually already handled in goahead()
            return self.parse_comment(self.i)
        elif rawdata[self.i:self.i+3] == '<![':
            return self.parse_marked_section(self.i)
        elif rawdata[self.i:self.i+9].lower() == '<!doctype':
            # find the closing >
            gtpos = rawdata.find('>', self.i+9)
            if gtpos == -1:
                return -1
            self.handle_decl(rawdata[self.i+2:gtpos])
            return gtpos+1
        else:
            return self.parse_bogus_comment(self.i)

    # Internal -- parse bogus comment, return length or -1 if not terminated
    # see http://www.w3.org/TR/html5/tokenization.html#bogus-comment-state
    def parse_bogus_comment(self, i, report=1):
        rawdata = self.rawdata
        assert rawdata[i:i+2] in ('<!', '</'), ('unexpected call to '
                                                'parse_comment()')
        pos = rawdata.find('>', i+2)
        if pos == -1:
            return -1
        if report:
            self.handle_comment(rawdata[i+2:pos])
        return pos + 1

    # Internal -- parse processing instr, return end or -1 if not terminated
    def parse_pi(self):
        rawdata = self.rawdata
        assert rawdata[self.i:self.i+2] == '<?', 'unexpected call to parse_pi()'
        match = piclose.search(rawdata, self.i+2) # >
        if not match:
            return -1
        j = match.start()
        self.handle_pi(rawdata[self.i+2: j])
        j = match.end()
        return j

    # Internal -- handle starttag, return end or -1 if not terminated
    def parse_starttag(self):
        self.__starttag_text = None
        endpos = self.check_for_whole_start_tag(self.i)
        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        self.__starttag_text = rawdata[self.i:endpos]

        # Now parse the data between i+1 and j into a tag and attrs
        attrs = []
        match = tagfind.match(rawdata, self.i+1)
        assert match, 'unexpected call to parse_starttag()'
        end_i = match.end()
        self.lasttag = tag = match.group(1).lower()
        while end_i < endpos:
            if self.strict:
                m = attrfind.match(rawdata, end_i)
            else:
                m = attrfind_tolerant.match(rawdata, end_i)
            if not m:
                break
            attrname, rest, attrvalue = m.group(1, 2, 3)
            if not rest:
                attrvalue = None
            elif attrvalue[:1] == '\'' == attrvalue[-1:] or \
                 attrvalue[:1] == '"' == attrvalue[-1:]:
                attrvalue = attrvalue[1:-1]
            if attrvalue:
                attrvalue = self.unescape(attrvalue)
            attrs.append((attrname.lower(), attrvalue))
            between = end_i + len(attrname)
            self.painter(end_i, between,"attribute")
            self.painter(between, m.end(), "attribute_value")
            end_i = m.end()

        end = rawdata[end_i:endpos].strip()
        if end not in (">", "/>"):
            lineno, offset = self.getpos()
            if "\n" in self.__starttag_text:
                lineno = lineno + self.__starttag_text.count("\n")
                offset = len(self.__starttag_text) \
                         - self.__starttag_text.rfind("\n")
            else:
                offset = offset + len(self.__starttag_text)
            if self.strict:
                self.error("junk characters in start tag: %r"
                           % (rawdata[end_i:endpos][:20],))
            self.handle_data(rawdata[self.i:endpos])
            
            return endpos
        
        if (end.endswith('>') and tag in self.VOID_ELEMENTS_5) or end.endswith('/>'):
            # XHTML-style empty tag: <span attr="value" />
            
            self.handle_startendtag(tag, attrs)
            
        else:
            self.handle_starttag(tag, attrs)
            if tag in self.CDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode(tag)
        return endpos

    # Internal -- check to see if we have a complete starttag; return end
    # or -1 if incomplete.
    def check_for_whole_start_tag(self, i):
        rawdata = self.rawdata
        if self.strict:
            m = locatestarttagend.match(rawdata, i)
        else:
            m = locatestarttagend_tolerant.match(rawdata, i)
        if m:
            j = m.end()
            next_ = rawdata[j:j+1]
            if next_ == ">":
                return j + 1
            if next_ == "/":
                if rawdata.startswith("/>", j):
                    return j + 2
                if rawdata.startswith("/", j):
                    # buffer boundary
                    return -1
                # else bogus input
                if self.strict:
                    self.updatepos(i, j + 1)
                    self.error("malformed empty start tag")
                if j > i:
                    return j
                else:
                    return i + 1
            if next_ == "":
                # end of input
                return -1
            if next_.isalpha() or next_ in "=/":
                # end of input in or before attribute value, or we have the
                # '/' from a '/>' ending
                return -1
            if self.strict:
                self.updatepos(i, j)
                self.error("malformed start tag")
            if j > i:
                return j
            else:
                return i + 1
        raise AssertionError("we should not get here!")

    # Internal -- parse endtag, return end or -1 if incomplete
    def parse_endtag(self):
        rawdata = self.rawdata
        assert rawdata[self.i:self.i+2] == "</", "unexpected call to parse_endtag"
        match = endendtag.search(rawdata, self.i+1) # >
        if not match:
            return -1
        gtpos = match.end()
        match = endtagfind.match(rawdata, self.i) # </ + tag + >
        if not match:
            if self.cdata_elem is not None:
                self.handle_data(rawdata[self.i:gtpos])
                return gtpos
            if self.strict:
                self.error("bad end tag: %r" % (rawdata[self.i:gtpos],))
            # find the name: w3.org/TR/html5/tokenization.html#tag-name-state
            namematch = tagfind_tolerant.match(rawdata, self.i+2)
            if not namematch:
                # w3.org/TR/html5/tokenization.html#end-tag-open-state
                if rawdata[self.i:self.i+3] == '</>':
                    return self.i+3
                else:
                    return self.parse_bogus_comment(self.i)
            tagname = namematch.group().lower()
            # consume and ignore other stuff between the name and the >
            # Note: this is not 100% correct, since we might have things like
            # </tag attr=">">, but looking for > after that name should cover
            # most of the cases and is much simpler
            gtpos = rawdata.find('>', namematch.end())
            self.handle_endtag(tagname)
            return gtpos+1

        elem = match.group(1).lower() # script or style
        if self.cdata_elem is not None:
            if elem != self.cdata_elem:
                self.handle_data(rawdata[i:gtpos])
                return gtpos

        self.handle_endtag(elem.lower())
        self.clear_cdata_mode()
        return gtpos

    # Overridable -- finish processing of start+end tag: <tag.../>
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)
        

    # Overridable -- handle start tag
    def handle_starttag(self, tag, attrs):
         #if attrs:
            #attrs.insert(0,tag)
        #print(tag,self.i)
        if attrs:
            i1=len(self.key_attribute_list)
            i2=len(self.value_attribute_list)
            self.key_attribute_list.append([])
            self.value_attribute_list.append([])
            for attr in attrs:
                self.key_attribute_list[i1].append(attr[0])
                self.value_attribute_list[i2].append(attr[1])
        else:
            self.key_attribute_list.append(None)
            self.value_attribute_list.append(None)
        html_element = html_element_from_name(tag)
        if html_element is not None: # found in saved, documented text
            must_parent = html_element["parent"]#in file extractor
            must_parents = must_parent.split(",")
            for parent in must_parents:
                if parent in self.dynamic_start_list or must_parent == "root":
                    break
            else :#this block executes if the for block hasn t broke
                #the must parent is not open or missing (<li> needs <ul> or <ol> open before)
                self.must_parent_errors.append([",".join(must_parents), tag])
        self.start_list.append(tag)
        self.dynamic_start_list.append(tag)

    # Overridable -- handle end tag
    def handle_endtag(self, tag):
        if self.dynamic_start_list[-1] != tag:
            #nested tags: the last closed is not the same as last opened
            self.close_before_error_list.append([self.dynamic_start_list[-1],tag])
            self.painter(self.i,self.i+len(tag)+2, "error")
            if tag in self.dynamic_start_list:
                self.dynamic_start_list.remove(tag)
        else:
            self.dynamic_start_list.pop(-1)
        self.end_list.append(tag)

    # Overridable -- handle character reference
    def handle_charref(self, name):
        pass

    # Overridable -- handle entity reference
    def handle_entityref(self, name):
        pass

    # Overridable -- handle data
    def handle_data(self, data):
        stripped_data = data.strip()
        if stripped_data:
            try:
                i = j = 0
                while self.start_list[-i-1] == self.end_list[-j-1]:
                    i = i + 1
                    j = j + 1
                container = self.start_list[-i-1]
            except IndexError:
                container = ""
            self.content_list.append([container, stripped_data])
        else:
           pass#self.content_list.append("") 

    # Overridable -- handle comment
    def handle_comment(self, data):
        pass

    # Overridable -- handle declaration
    def handle_decl(self, decl):
        self.declaration = decl

    # Overridable -- handle processing instruction
    def handle_pi(self, data):
        pass

    def unknown_decl(self, data):
        if self.strict:
            self.error("unknown declaration: %r" % (data,))

    # Internal -- helper to remove special character quoting
    def unescape(self, s):
        if '&' not in s:
            return s
        def replaceEntities(s):
            s = s.groups()[0]
            try:
                if s[0] == "#":
                    s = s[1:]
                    if s[0] in ['x','X']:
                        c = int(s[1:].rstrip(';'), 16)
                    else:
                        c = int(s.rstrip(';'))
                    return chr(c)
            except ValueError:
                return '&#' + s
            else:
                from html.entities import html5
                if s in html5:
                    return html5[s]
                elif s.endswith(';'):
                    return '&' + s
                for x in range(2, len(s)):
                    if s[:x] in html5:
                        return html5[s[:x]] + s[x:]
                else:
                    return '&' + s

        return re.sub(r"&(#?[xX]?(?:[0-9a-fA-F]+;|\w{1,32};?))",
                      replaceEntities, s, flags=re.ASCII)
#CSS regular expressions
    #" " space 32
    #\b backspace 8
    #\t tab 9
    #\r carriage return 13
    #\n Linefeed NewLine Unix 10
    #\f Form feed New Page 12
anything_start = re.compile(r"[^ \t\n\r\f]+")
selector_word = re.compile(r"([^{} \t\n\r\f]+[ \t\n\r\f]*)+")
atrule_word = re.compile(r"@[^{}:]+")
comment_long = re.compile(r"/\*[^(\*/)]*\*/")

#http://www.w3.org/TR/css3-selectors/#whitespace
"space"  "tab" "line feed"  "carriage return" "form feed" 
valid_whitespace = re.compile(r"[ \t\n\r\f]")
brace_start = re.compile(r"{")
property_word = re.compile(r"""[^:{}]+""")
property_value_separator = re.compile(r":")
#value_word = re.compile("[^;]+") #this ends too soon in e.g content: "Ok; not ok";
value_word = re.compile(r"""[^";{}]+""")
literal_word = re.compile(r"""[^"]*""")
literal_start_or_end = re.compile(r"""["']""")
value_end = re.compile(r";")
brace_end = re.compile(r"}")

class CSSParseError(Exception):
    """Exception raised for all parse errors."""

    def __init__(self, msg="", position=None):
        assert msg
        self.msg = str(msg)
        self.position = position

    def __str__(self):
        result = self.msg
        if self.position is not None:
            result = "{}, at {}".format(result, self.position)
        return result
    
IN_TEXT = 0
AFTER_AT_RULE = 2
AFTER_SELECTOR = 4
IN_RULE = 5
IN_PROPERTY = 6
AFTER_PROPERTY = 7
IN_VALUE = 10
IN_VALUE_QUOTE = 11
IN_VALUE_QUOTE_SINGLE = 12
AFTER_VALUE = 14
AFTER_PROPERTY_VALUE_SEPARATOR = 15
TOO_MANY_OPEN_BRACKETS = "TOO_MANY_OPEN_BRACKETS"
VALUE_END_MISSING = "VALUE_END_MISSING"

class CSSParser(_markupbase.ParserBase):
    """Parses CSS Text.

    If you already have a parsed object use existing_CSSText to append the incoming parsed data to it
    strict if you want to raise Errors (and stop the parsing) as soon as something unexpected shows up
    for_color should be a function(a,b,c) that alters the apparence of your text.

    Use .feed(text) to add raw text data to be parsed
    Use .parse() to do the parsing
    Use .x to use the results that are interesting for you

    reset() not implemented yet
    
    """
    
    
    def __init__(self, css_text=None, strict=False, for_color=None):
        """Initialize and reset this instance.

        """
        self.reset()
        if css_text is None:
            css_text = CSSText()
        self.css_text = css_text
        self.tree = [self.css_text]
        if for_color:
            self.painter = for_color#function
        else:
            #most elegant way to do it ?
            self.painter = do_nothing
        

    def reset(self):
        """Reset this instance. Loses all unprocessed data."""
        self.state = IN_TEXT
        self.rawdata = ''
        self.warnings = []
        self.set_anything_mode()
        self.error_list = []
        _markupbase.ParserBase.reset(self)

    def feed(self, data):
        r"""Feed data to the parser.

        Call this as often as you want, with as little or as much text
        as you want (may include '\n').
        """
        self.rawdata = self.rawdata + data


    def set_anything_mode(self):
        self.searching = anything_start
        
    # Internal -- handle data as far as reasonable.  May leave state
    # and data to be processed by a subsequent call.
    def parse(self):
        """Main loop, scans the text until a fatal error or end.

Everytime a significant css object is detected, the specific handler is called.
Those handlers are overridable.
"""
        rawdata = self.rawdata # holds the text
        self.i = 0 # character index where we are looking at
        length = len(rawdata) 
        while self.i < length:
            match = anything_start.search(rawdata, self.i)
            if not match:
                # 
                return
            #else:
            j = match.start()
            first_letter = rawdata[j]
            if first_letter == "@" and self.state == IN_TEXT:
                self.i = self.parse_at_rule(j)
            elif first_letter == "{":
                self.i = self.start_block(j)
            elif first_letter == "}":
                self.i = self.end_block(j)
            else:
                self.i = self.parse_this(j)

            assert self.i is not None, "self.i should be the index not None"
                
    def parse_this(self, start):
        if self.state == IN_TEXT:
            return self.parse_selector(start)
        elif self.state == IN_RULE:
            return self.parse_property(start)
        elif self.state == AFTER_PROPERTY:
            return self.parse_property_value_separator(start)
        elif self.state == AFTER_PROPERTY_VALUE_SEPARATOR:
            return self.parse_value(start)
        elif self.state == AFTER_VALUE:
            return self.parse_after_value(start)
        
    def parse_selector(self, start):
        match = selector_word.search(self.rawdata, start)
        if match is None:
            return start + 1 #here you can do better performance 
        else:
            self.state = AFTER_SELECTOR
            self.searching = brace_start
            self.handle_selector(match.group())
            return match.end()     
        
    def parse_property(self, start):
        match = property_word.search(self.rawdata, start)
        self.state = AFTER_PROPERTY
        self.searching = property_value_separator
        self.handle_property(match.group())
        return match.end()        
       
    def parse_property_value_separator(self, start):
        match = property_word.search(self.rawdata, start)
        if match is None:
            self.property_value_separator_missing()
        else:
            self.state = AFTER_PROPERTY_VALUE_SEPARATOR
            self.searching = value_word
            return start + 1
        
    def parse_value(self, start):
        match = value_word.search(self.rawdata, start)
        self.handle_value(match.group())
        self.state = AFTER_VALUE#will search for ;
        self.searching = value_end
        return match.end()

    def parse_after_value(self, start):
        match = value_end.search(self.rawdata, start)
        if match is None:
            #self.value_end_missing()#not fatal error
            self.warning( VALUE_END_MISSING, start)
        self.state = IN_RULE
        self.searching = property_word
        return (start + 1)
    
    def parse_at_rule(self, start):
        match = atrule_word.search(self.rawdata, start)
        atrule_string = match.group()[1::]
        #only keyframes, no there are other atrules !
        if atrule_string.split(" ")[0].strip() == "keyframes":
            keyframe_name = atrule_string.split(" ")[1].strip()
            self.add_to_tree(CSSKeyframes(keyframe_name))
            self.state = AFTER_AT_RULE
        return match.end()
    
    def warning(self, message, position):
        self.warnings.append(message, position)

    def missing_brace_start(self):
        raise CSSParseError(self.i)

    def missing_brace_end(self):
        raise CSSParseError(self.i)
    
    def value_end_missing(self):
        raise CSSParseError(self.i)

    def property_value_separator_missing(self):
        raise CSSParseError(self.i)
    
    # Overridable
    def handle_selector(self, selector):
        self.add_to_tree(CSSRule(CSSSelector(selector.strip().split(u" "))))
    
    # Overridable
    def handle_property(self, property_,):
        self.add_to_tree(CSSPropertyValue(property_.strip()))
    
    # Overridable
    def handle_value(self, value):
        self.tree[-1].value = value.strip()
        self.close_last_sub_tree() #success we have a property and a value
    
    # Overridable
    def handle_rule(self, rule):
        pass
        
    # Overridable
    def handle_keyframe(self, keyframe):
        pass
        
    # Overridable
    def handle_x(self, x):
        pass
        

    def handle_comment(self, comment):
        pass

    # Overridable -- handle declaration
    def handle_decl(self, declaration):
        pass

    # Overridable -- handle processing instruction
    def handle_pi(self, data):
        pass

    #methods used in overridable methods
    def add_to_tree(self, css_object):
        self.tree[-1].append(css_object)
        self.tree.append(css_object)

    def close_last_sub_tree(self):
        return self.tree.pop()

    def start_block(self, start):
        if self.state == AFTER_SELECTOR:
            self.state = IN_RULE
            self.searching = property_word
            
        elif self.state == IN_RULE:
            self.warning(TOO_MANY_OPEN_BRACKETS, start)
            
        elif self.state == AFTER_AT_RULE:
            self.state = IN_TEXT
            self.searching = anything_start
        return start + 1
    
    def end_block(self, start):
        if self.state == IN_RULE:
            self.state = IN_TEXT
            self.searching = anything_start
        self.close_last_sub_tree()
        return start + 1


if __name__=='__main__':
    a=r"""

<html lang="?"><!DOCTYPE html>
    <head>
        <meta charset="utf-8">
        <title>C</title>
    </head>
    <body hey>
        <p>bonjour</p>
        <footer>
            <p>er weiss nit wat er schreiben muss</footer></p>
            dans footer
            <a target="here" href="https://www.jssuperheroes.inputoutput/">b</a>
    </body>
</html>
"""
    p = HTMLParser()
    p.feed(a)
    p.close()
##    print("Declaration at the right place:",p.doctype_first and p.declaration)
##    print("Document:", p.declaration + "\n")
##    print("start", p.start_list)
##    print("end", p.end_list)
##    print("\nattribute list",p.key_attribute_list)
##    print("value list", p.value_attribute_list)
##    print("\ndata",p.content_list)
##    print("\n\n")
##    start = p.start_list[:]
##    end = p.end_list[:]
##    finished = False
##    print(start,"\n")
##    print(end,"\n")
##    print("close x before y (x,y): ",p.close_before_error_list)
##    if len(start) != len(end):
##        print("Some not closed or not opened")
    
    #generic css text to test the parser
    css_text = r"""

    @keyframes yo
    {
    a{color:blue;}
    b{hello:false;}
}

rule1 {
                    property1: value1;
    property2: value2;
}"""

    #css parser should not have different result for different whitespacing
    import time
    a= time.time()
    css_parser = CSSParser()
    css_parser.feed(css_text)
    css_parser.parse()
    print(css_parser.css_text)
    print(time.time() - a)
