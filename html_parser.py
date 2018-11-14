#!/usr/bin/python
#-*-coding:utf-8*

#html_parser.py
#Role:HTML parser 


#2015

##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##WebSpree

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
##If you have questions concerning this license you may contact
##by opening an issue
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
r"""
Original file:C:\Python33\Lib\html\parser.py
"""

# This file is based on sgmllib.py, but the API is slightly different.

# XXX There should be a way to distinguish between PCDATA (parsed
# character data -- the normal case), RCDATA (replaceable character
# data -- only char and entity references and end tags are special)
# and CDATA (character data -- only end tags are special).


def do_nothing(*anything):
    pass
try:
    import _markupbase
except ImportError:
    import markupbase as _markupbase
import re
import warnings


# DATA
from file_extractor import *
from css_parser import *


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

    def __init__(self, strict=False):
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
        self.cutpoints = []
        self.parsedinline = []
        self.key_attribute_list = []
        self.value_attribute_list = []
        # dynamic_start_list contains opened tags at the moment you look it
        # if the document is valid it should be empty at the end
        self.dynamic_start_list = []
        self.close_before_error_list = []
        self.must_parent_errors = []

        self.color_codes_with_location = [] # [((5,13),"code"), ...]  
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

    def color(self, start, end, color_code):
        self.color_codes_with_location.append(((start, end), color_code))
        
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
                    # future use len(self.dynamic_start_list) to add coulour itensity variation
                    self.color(self.i, end_i, "element")
                elif startswith("</", self.i):
                    end_i = self.parse_endtag()
                    self.color(self.i, end_i, "element")
                elif startswith("<!--", self.i):
                    end_i = self.parse_comment(self.i)
                    self.color(self.i, end_i, "comment")
                elif startswith("<?", self.i):
                    end_i = self.parse_pi(self.i)
                elif startswith("<!", self.i):
                    if self.strict:
                        end_i = self.parse_declaration(self.i)# ! method not found !!!
                    else:
                        end_i = self.parse_html_declaration()
                        self.color(self.i, end_i, "html_declaration")
                elif (self.i + 1) < n:
                    self.handle_data("<") #warning < alone
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
                    self.handle_data("&") #warning
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
            # Doctype declaration at the wrong place
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
            self.color(end_i, between,"attribute")
            self.color(between, m.end(), "attribute_value")
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

    def is_html(self):
        return bool(self.start_list or self.end_list or self.declaration)
    
    # Overridable -- finish processing of start+end tag: <tag.../>
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)
        

    # Overridable -- handle start tag
    def handle_starttag(self, tag, attrs):
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
        try:
            html_element = ELEMENTS[tag] # found in saved, documented text
            #in file extractor
            must_parents = html_element["parent"]
            for parent in must_parents:
                if parent in self.dynamic_start_list or must_parents[0] == "root":
                    break
            else :#this block executes if the for block hasn t broke
                #the must parent is not open or missing (<li> needs <ul> or <ol> open before)
                self.must_parent_errors.append([",".join(must_parents), tag])
        except KeyError:
            pass
        except AttributeError:
            print("warning must parent must be a comma separated list with []")
        self.start_list.append(tag)
        self.dynamic_start_list.append(tag)

    # Overridable -- handle end tag
    def handle_endtag(self, tag):
        if self.dynamic_start_list:
            if self.dynamic_start_list[-1] != tag:
                #nested tags: the last closed is not the same as last opened
                self.close_before_error_list.append([self.dynamic_start_list[-1],tag])
                self.color(self.i,self.i+len(tag)+2, "error")
                if tag in self.dynamic_start_list:
                    self.dynamic_start_list.remove(tag)
                    # removes first occurrence
                    # maybe better to remove last
            else:
                self.dynamic_start_list.pop(-1)
            
        else:
            #doc starts with a closed tag
            self.color(self.i,self.i+len(tag)+2, "element")
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
            if self.dynamic_start_list:
                container = self.dynamic_start_list[-1]
            else:
                container = ""
            if container == "style":
                #print("inline css detected")
                #print("raw:\n", stripped_data)
                self.cutpoints.append([self.i, self.i + len(data)])
                self.parsedinline.append([container, data])
                #CSSParser().feed(stripped_data).parse()
                #print("parsed:\n", stripped_data)
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
    
if __name__=='__main__':
    import unittest
    import time
    class TestHTMLParser(unittest.TestCase):

        def setUp(self):
            self.bad_html_text = r"""
<html lang="en"><!DOCTYPE html>
    <head>
        <meta charset="utf-8">
        <title>C</title></head>    <body hey><p>bonjour</p>    <footer>
            <p>er weiss nit wat er schreiben muss</footer></p>
            µµµµµµùùùùù are these ùµ in p or in footer ? -->[?]
            <a target="here" href="https://www.jssuperheroes.inputoutput/">b</a>    </body></html>
"""
            self.mixed_html = r"""<!doctype html><html>
	<head>
		<title>t$***$y</title>
		<style>
			body { margin: 1em; }
			canvas { width: 100%; height: 100% }
		</style>
	</head>
	<body>
		<script src="good.js"></script>
		<script>
			var bad = "a";
		</script>
	</body>
</html>"""

        def test_parse(self):
            p = HTMLParser()
            p.feed(self.bad_html_text)
            p.close()
            self.assertFalse(p.doctype_first and p.declaration, "Declaration is not at the right place:")
            self.assertEqual(p.declaration, "DOCTYPE html")
            self.assertEqual(len(p.start_list), len(p.end_list))
            self.assertEqual(p.key_attribute_list[0][0], "lang")
            self.assertEqual(p.value_attribute_list[0][0], "en")
            self.assertEqual(p.content_list[0],['title', 'C'])
            #print(p.content_list) [?]
            self.assertEqual(p.close_before_error_list,[['p', 'footer']])


        def test_consistent(self):
            pass

        def test_guess_is_html(self):
            
            p = HTMLParser()
            p.feed(self.bad_html_text)
            p.close()
            self.assertTrue(p.is_html())
            
            p = HTMLParser()
            p.feed("this is definitly not h t m l{x:b;}")
            p.close()
            self.assertFalse(p.is_html())
            
            
        def test_unparsable_html(self):
            """here we expect the parser to stop completly because it makes no sense to continue"""
            pass
        
        def test_wrong_but_parsable_html(self):
            """Warn but not stop because the errors are easy to ignore and continue"""
            pass
        
        def test_parse_html_with_inline_extensions(self):
            p = HTMLParser()
            p.feed(self.mixed_html)
            p.close()
            
            

    unittest.main()
