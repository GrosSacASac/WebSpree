#!/usr/bin/python
#-*-coding:utf-8*

#css_parser.py
#Role: CSS parser 

#Walle Cyril
#2015-08-19

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

#todo maybe replace all _repr_ by _str_ or vice versa
def do_nothing(*anything):
    pass
try:
    import _markupbase
except ImportError:
    import markupbase as _markupbase
import re

class CSSSelector(object):
    """Stores the filters, together they form an CSSSelector.

filter1 filter2 filtern"""
    
    def __init__(self,filters=None):
        if filters is None:
            filters = ["*"]
            #should the default selector be void or general ?
        self.filters = filters
        
    def __repr__(self):
        return u"{}".format(u" ".join(self.filters))
    
class CSSPropertyValue(object):
    """Stores an attribute and a value.

attr: value;"""
    
    def __init__(self,property_="",value=u""):
        self.property_ = property_
        self.value = value
        
    def __repr__(self):
        return u"{}: {};".format(self.property_, self.value)
    
class CSSRule(object):
    r"""A CSSRule is composed of 1 CSSSelector and n CSSPropertyValues.

Here's the output of __repr__ method
    CSSSelector {
            CSSPropertyValue1
            CSSPropertyValue2
            ...
            CSSPropertyValueN
        }"""

    def __init__(self, css_selector=None, css_property_values=None):
        if css_selector is None:
            css_selector = CSSSelector()
        self.css_selector = css_selector
        if css_property_values is None:
            css_property_values = []
        self.css_property_values = css_property_values

    def append(self,css_property_value):
        """adds a new property-value pair to the rule.
If the property is already there, we only overwrite the old value."""
        for s_css_property_value in self.css_property_values:
            if s_css_property_value.property_ == css_property_value.property_:
                s_css_property_value.value = css_property_value.value
                break
        else: #the property is new to the rule
            self.css_property_values.append(css_property_value)
        
    def __repr__(self):
        return u"{} {{\n    {}\n}}".format(
            self.css_selector,
            "\n    ".join(pv.__repr__() for pv in self.css_property_values))
    
class CSSKeyframes(object):
    r"""A CSSKeyframes is composed of a name and n CSSRules(with x% selectors each).

Here's the output of __repr__ method:

@keyframes Name {
    CSSSelector1 {
            CSSPropertyValue1
            ...
            CSSPropertyValueN
        }
    CSSSelector2 {
            CSSPropertyValue1
            ...
            CSSPropertyValueN
        }
}
        """

    def __init__(self, name=u"", css_rules=None):
        self.name = name
        if css_rules is None:
            css_rules = []
        self.css_rules = css_rules
        
    def __repr__(self):
        return u"@keyframes {} {{\n    {}\n}}".format(
            self.name,
            "\n    ".join(list(map(repr,self.css_rules))))
            #"\n    ".join(rule.__repr__() for rule in self.css_rules))
    
    def __str__(self):
        return u"@keyframes {} {{\n    {}\n}}".format(
            self.name,
            "\n    ".join(list(map(repr,self.css_rules))))
            #"\n    ".join(rule.__repr__() for rule in self.css_rules))
        
    def append(self, css_rule):
        """adds a new rule to the group.
If the selector is already there, we instead update that old rule by appending each property-value."""
        for s_css_rule in self.css_rules:
            if s_css_rule.css_selector == css_rule.css_selector:
                for new_css_property_value in css_rule.css_property_values:
                    s_css_rule.append(new_css_property_value)#see CSSRule to see what happens
                break
        else: #the property is new to the rule
            self.css_rules.append(css_rule)

class CSSHolder(object):        
    """Stores rules, keyframes, etc."""
    
    def __init__(self):
        self.content_list = []
            
    def __str__(self):
        return "\n".join(list(map(repr,self.content_list)))

        
    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        elif isinstance(other, self.__class__):
            return str(self) == str(other)
        else:
            return self == other

    def append(self, x):
        self.content_list.append(x)
        #todo check if the selector ? or thing is alreaddy taken
        
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

#http://www.w3.org/TR/selectors4/#case-sensitive
#"space"  "tab" "line feed"  "carriage return" "form feed"
valid_whitespace = re.compile(r"[ \t\n\r\f]")#\v exluded
brace_start = re.compile(r"{")
property_word = re.compile(r"""[^;:{}]+""")
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
VALUE_END_MISSING = "VALUE_END_MISSING(;)"
MISSING_START_BRACE = "MISSING_START_BRACE"
NOT_CLOSED_RULES = "NOT_CLOSED_RULES"


class CSSParser(_markupbase.ParserBase):
    """Parses CSS Text.

    If you already have a parsed object use existing_CSSText to append the incoming parsed data to it
    strict if you want to raise Errors (and stop the parsing) as soon as something unexpected shows up

    Use .feed(text) to add raw text data to be parsed
    Use .parse() to do the parsing
    Use .x to use the results that are interesting for you
    .css_text should be an interesting object
    Or in 1 line  p = CSSParser().feed(css_text).parse()
    
    """
    
    
    def __init__(self, css_text=None, strict=False):
        """Initialize and reset this instance.

        """
        self.reset()
        if css_text is None:
            css_text = CSSHolder()
        self.css_text = css_text
        self.tree = [self.css_text]
        self.color_codes_with_location = []
        
    def color(self, start, end, color_code):
        self.color_codes_with_location.append(((start, end), color_code))

    def reset(self):
        """Reset this instance. Loses all unprocessed data."""
        self.state = IN_TEXT
        self.rawdata = ''
        self.warnings = []
        self.set_anything_mode()
        self.error_list = []
        self.block_started = 0
        _markupbase.ParserBase.reset(self)

    def feed(self, data):
        r"""Feed data to the parser.

        """
        self.rawdata = self.rawdata + data
        return self


    def set_anything_mode(self):
        self.searching = anything_start
        
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
                return self.end_parse()
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
        return self.end_parse()

    def end_parse(self):
        end = len(self.rawdata)-1
        if self.state != IN_TEXT:
            self.warning(NOT_CLOSED_RULES, end)
        if self.state == AFTER_VALUE:
            self.warning(VALUE_END_MISSING, end)
        if self.state != IN_TEXT:
            self.warning(NOT_CLOSED_RULES, end)
        return self
                
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
            self.handle_selector(match.group(), match.start(), match.end())
            return match.end()     
        
    def parse_property(self, start):
        match = property_word.search(self.rawdata, start)
        self.state = AFTER_PROPERTY
        self.searching = property_value_separator
        self.handle_property(match.group(), match.start(), match.end())
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
        self.handle_value(match.group(), match.start(), match.end())
        self.state = AFTER_VALUE#will search for ;
        self.searching = value_end
        return match.end()

    def parse_after_value(self, start):
        match = value_end.search(self.rawdata, start)
        if match is None:
            #self.value_end_missing()#not fatal error
            self.warning(VALUE_END_MISSING, start)
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
        self.warnings.append((message, position))

    def missing_brace_start(self):
        raise CSSParseError(self.i)

    def missing_brace_end(self):
        raise CSSParseError(self.i)
    
    def value_end_missing(self):
        raise CSSParseError(self.i)

    def property_value_separator_missing(self):
        raise CSSParseError(self.i)
    
    # Overridable
    def handle_selector(self, selector, start, end):
        self.color(start, end, "selector")
        self.add_to_tree(CSSRule(CSSSelector(selector.strip().split(u" "))))
    
    # Overridable
    def handle_property(self, property_, start, end):
        self.color(start, end, "property_")
        self.add_to_tree(CSSPropertyValue(property_.strip()))
    
    # Overridable
    def handle_value(self, value, start, end):
        self.color(start, end, "value")
        self.tree[-1].value = value.strip()
        self.close_last_sub_tree()
    
    # Overridable
    def handle_rule(self, rule):
        pass
        
    # Overridable
    def handle_keyframe(self, keyframe):
        pass
        
    # Overridable
    def handle_x(self, x):
        pass
        
    # Overridable
    def handle_comment(self, comment):
        pass

    # Overridable -- handle declaration
    def handle_decl(self, declaration):
        pass

    def is_css(self):
        """Is it css ?"""
        # what is the best way to guess if it is css ?
        START_RATIO = 100
        return len(self.error_list) < 2 and self.block_started > int(len(self.rawdata)/START_RATIO)

    # methods used in overridable methods
    def add_to_tree(self, css_object):
        
        if self.tree:
            self.tree[-1].append(css_object)
        #else what would it mean to land here ?
        self.tree.append(css_object)

    def close_last_sub_tree(self):
        return self.tree.pop()

    def start_block(self, start):
        self.block_started += 1
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
        elif self.state == AFTER_SELECTOR:
            self.warning(MISSING_START_BRACE, start)
            self.state = IN_TEXT
            self.searching = anything_start
        self.close_last_sub_tree()
        return start + 1


if __name__=='__main__':
    import unittest
    import time
    
            
    class TestCSSParser(unittest.TestCase):

        def setUp(self):
            self.css_text = r"""

    @keyframes keyframenameislong
    {
    a{color:blue;}
    b{hello:false;}
}

rule1 a > g{
                    property1: value1;
    property2: value2;
}"""

        def test_speed(self):
            t = time.time()
            css_parser = CSSParser() .feed(self.css_text) .parse()
            self.assertGreaterEqual(1.0, time.time() - t, msg = "parser is a bit too slow")

            # should raise an exception for an immutable sequence
            # self.assertRaises(TypeError, random.shuffle, (1,2,3))

        def test_consistent(self):
            css_parser1 = CSSParser() .feed(self.css_text) .parse()
            css_parser2 = CSSParser() .feed(str(css_parser1.css_text)) .parse()
            css_parser3 = CSSParser() .feed(self.css_text+"     ") .parse()
            self.assertEqual(css_parser1.css_text,
                             css_parser2.css_text,
                             "parsing parsed text should have no effect")
            self.assertEqual(css_parser1.css_text,
                             css_parser3.css_text,
                             "css parser should not have different result for different whitespacing")
          
        def test_guess_is_css(self):
            
            css_parser1 = CSSParser() .feed(self.css_text) .parse()
            self.assertTrue(css_parser1.is_css())
            
            css_parser2 = CSSParser() .feed("bla bla bla not c s s ") .parse()
            self.assertFalse(css_parser2.is_css())
            
        def test_unparsable_css(self):
            """Expect the parser to stop completly, it makes no sense to continue"""
            pass
        
        def test_wrong_but_parsable_css(self):
            """we expect the parser to warn but not stop because the errors are easy to ignore and continue"""
            bad_css = "a b:c;} d{e:f"
            css_parser1 = CSSParser() .feed(bad_css) .parse()
            
            self.assertIn((MISSING_START_BRACE, 6), css_parser1.warnings)
            self.assertIn((NOT_CLOSED_RULES,len(bad_css)-1), css_parser1.warnings)
            self.assertIn((VALUE_END_MISSING,len(bad_css)-1), css_parser1.warnings)
            
            # css_parser1.state
    unittest.main()
