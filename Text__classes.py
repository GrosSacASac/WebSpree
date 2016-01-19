#!/usr/bin/python
#-*-coding:utf-8*

"""Text__classes.py
Role: define objects containing documents

Authors: Walle Cyril
Last-edit: 2015-05-25
"""
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

import codecs
import os
import webbrowser
#import json

from html_parser import *
from css_parser import *
from character_translator import html5, html5reci,minimum_translation
from Options_class import *

def _(l_string):
    return l_string

#export FileDocument, HTMLFragment, CSSFragment, JSFragment
STANDARD_BEGINNING_HTML = u"""<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>  </title>
    </head>
    <body>
       
        
    </body>
</html>"""

def raw_insert(base, new, position=None):
    """Inserts str into str after character at position position.

    if position is not given concatenation happens"""
            
    if not new or not isinstance(new, str):
        return base
    length = len(base)
    if position is None or position >= length:
        return base + new
    else:
        return u"{}{}{}".format(base[0:position], new, base[position::])
    
def raw_remove(base, from_, to_):
    """removes"""
    assert 0 <= from_ <= to_
    if not base:
        return base
    return u"{}{}".format(base[0:from_], base[to_::])
    
class CommonFragment():
    """holds what doesn t change.

defines insert append remove find replace"""
    def __init__(self, text=u""):
        self.text = text

    def insert(self, string, position=None):
        self.text = raw_insert(self.text, string, position)
            
    def append(self, string):
        self.insert(string)

    def remove(self, from_, to_):
        self.text = raw_remove(self.text, from_, to_)

    def __len__(self):
        return len(self.text)

    def find(self, *args):
        return self.text.find(*args)

    def replace(self, *args):
        self.text = self.text.replace(*args)
            
class HTMLFragment(CommonFragment):
    """Stores an html text and has methods to edit it."""
    def __init__(self, text=u"", document_language="en", doctype="html"):
        CommonFragment.__init__(self,text=text)
        #specific addition for HTML
        self.document_language = document_language
        self.doctype = doctype

        #editing data
        # get self.element_still_not_closed_list = []
        # get self.current_direction = 0
        #helps to indent properly
        self.current_translation_needed = True
        #help to detect if we need translation (e.g for display content)
        # or to protect tags themselves (e.g. for <p>)
        self.insertion = None

        
    def parse(self):
        parser = HTMLParser()
        parser.feed(self.text)
        parser.close()
        return parser # parser is an object with results
            
                   
    #editing methods
    def html_to_normal_char(self,html_conversion):
        #not used yet
        #uses dictionnaire html5
        if html_conversion[0] == '&':
            if html_conversion[1::] in html5:
                normal_char = html5[html_conversion[1::]]
            else:
                normal_char = html_conversion
        else:#Not a keyword
            normal_char = html_conversion
        return normal_char

    def normal_char_to_html(self,normal_char,tr_level):
        
        if tr_level == 1:
            translator = minimum_translation
        elif tr_level == 10:
            translator = html5reci
            
        if normal_char in translator:
            html_conversion = translator[normal_char]
            if html_conversion[0] !='&':
                html_conversion = '&'+html_conversion
            if html_conversion[-1] !=';':
                html_conversion += ';'
            if html_conversion == "&<br />;":
                html_conversion = "<br>"
            return html_conversion
        else:
            return normal_char


  #editing macros with border effect
    def open_close_void_element(self,lone_element,attributes=""):
        """Adds < > to the arguments.

<br /> is an syntax error silently ignored in latest spec
<br> is correct syntax"""
        self.current_translation_needed = False
        return "<"+lone_element+attributes+">"

    def open_element(self,lone_element,attributes=""):
        self.current_direction = -1
        self.current_translation_needed = False
        return "<"+lone_element+attributes+">"

    def close_element(self,closing_tag=""):
        self.current_translation_needed = False
        return "</"+closing_tag+">"

#editing macros
        
    def add_standard_beginning(self):
        return  STANDARD_BEGINNING_HTML


    @property
    def w3c_encoding(self):
        #todo return encoding as it should appear in the meta charset
        return self.encoding

    @w3c_encoding.setter
    def w3c_encoding(self,new_w3c_encoding):
        #todo convert to python usable encoding string
        self.encoding = new_w3c_encoding
           
        
    def __add__(self,other):
        assert False, "not implemented"

    def __radd__(self,other):
        assert False, "not implemented"
        
    def __str__(self):
        return self.text
    
    def __repr__(self):
        return str(self)

    #def __getitem__(self, key):
    #    return deprecated
    
    def __len__(self):
        return len(self.text)
    

            
class CSSFragment(CommonFragment):        
    """Stores a parsed css text

and has methods to edit it fast."""
    
    def __init__(self,text=u""):
        CommonFragment.__init__(self,text=text)
        #specific addition for CSS
        self.doctype = "CSS"
        self.content_list = []
##   
##    def insert(self, to_add, position=None):
##        """Adds the given object to the css text, delegating it to special methods."""
##        CommonFragment.insert(self, to_add, position)#
##        
##        place_method = self.content_list.insert
##        if position is None or position >= len(self.text):
##            def eater(f): #append only takes 1 argument
##                def eaten(ignored,stays):
##                    return f(stays)
##                return eaten
##            place_method = eater(self.content_list.append)
##        place_method(position,to_add)
##        if isinstance(to_add, str):
##            
##            self.parse()
##        
##        #if self.tk_text:
##            #self.tk_text.tk_copy_text(self.text)
            

    def __repr__(self):
        return "\n".join(list(map(repr,self.content_list)))

    def parse(self):
        parser = CSSParser()
        parser.feed(self.text).parse()
        self.content_list = parser.css_text.content_list
        # parsed css structure
        # is kept for faster future changes on the css
        return parser # parser is an object with results
        
    def __eq__(self, other):
        if isinstance(other, str):
            return repr(self) == other
        elif isinstance(other, self.__class__):
            return repr(self) == repr(other)
        else:
            return self == other
            

fragments = {"html": HTMLFragment,
             "css": CSSFragment
            }

class FileDocument(InterfaceOptions):
    """Represents a file.

Uses HTMLFragment, CSSFragment, JSFragment"""
    def __init__(self, options_file_object, content=u"", saved=True, path="",
                 encoding_py="utf-8", document_language="en", gui_link=None,
                 doctype="html"):

        #specific addition for HTML
        self.document_language = document_language
        self.doctype = doctype

        #html can be a mixture of css and js (inline) in any order, in any way
        #to ease the internal implementation, html itself is considered inlined
        self.initial_content = content
        self.inlines = []
        self.__saved = saved
        self.save_path = path
        self.encoding = encoding_py
        self.gui_link = gui_link
        #if self.tk_text:
            # self.tk_text.tk_insert_text(where, inserted_text)
            # self.tk_text.tk_delete_text(from_, to_)
            # self.tk_text.reset_undo()

        self.last_find_index = -1
        #Parent data
        self.options_file_object = options_file_object#do not touch this directly use interface methods

    def start(self):
        """Separate init to put the object in a list that is used by methods in start."""
        self.text = self.initial_content #calls setter
        del self.initial_content
    
        if self.gui_link:
            self.gui_link.reset_undo()
        
    @property
    def text(self):
        #complete_text (str)
        complete_text = u""
        for inline in self.inlines:
                complete_text += inline[1].text
        return complete_text

    @text.setter
    def text(self, content):
        #example
        #self.inlines = [
        #   [doctype1, content1]
        #   [doctype2, content2]
        #   [doctype3, content3]
        #   ]
        self.parse(first=True, text=content) #will set inlines
        self.gui_link.tk_copy_text(content)


    def insert(self, string, position=None):
        if not string:
            return
        if position is None:
            self.inlines[-1][1].text += string
            position = len(self.text)
        else:
            travelled = 0
            for inline in self.inlines:
                if position < (travelled + len(inline[1].text)):
                    local_position = position - travelled
                    inline[1].text = u"".join((inline[1].text[0:local_position],
                                          string,
                                          inline[1].text[local_position::]))
                    break
                travelled += len(inline[1].text)
            else:
                self.inlines[-1][1].text += string
        self.gui_link.tk_insert_text(string, position)
     
    def append(self, string):
        self.insert(string)           

    def remove(self, start, end):
        assert start <= end
        if start == end:
            return
        travelled = 0
        for inline in self.inlines:
            local_start = start - travelled
            local_end = end - travelled            
            if start == end:  # 1
                if end < (travelled + len(inline[1].text)):
                    inline[1].text = u""
                else:
                    inline[1].text = inline[1].text[local_end::]
            elif start < (travelled + len(inline[1].text)):
                if end < (travelled + len(inline[1].text)):

                    
                    inline[1].text = u"".join((inline[1].text[0:local_start],
                                          inline[1].text[local_end::]))
                    break
                else:
                    inline[1].text = inline[1].text[0:local_start]
                    start = end  # 1
            travelled += len(inline[1].text)
        self.gui_link.tk_delete_text(start, end)
                
        def is_empty_text(a):
            return bool(a[1].text)
        
        self.inlines = list(filter(is_empty_text, self.inlines))
        # self.tk_text.tk_delete_text(start, start+length)
    
    def delete(self, start, length):
        assert False
        
    def find(self, string, start=-2):
        if start == -2 :
            if self.last_find_index == -1:
                start = 0
            elif self.last_find_index != -1:
                start = self.last_find_index + len(string)
        self.last_find_index = self.text.find(string, start)
        return self.last_find_index

    def replace(self, old, new, max_repeat=None):
        """replace all, max_repeat set to an int to replace less"""
        where = i = 0
        while where != -1:
            where = self.find(old)
            if where != -1:
                self.remove(where, where + len(old))
                self.insert(new, where)
            i += 1
            if i == max_repeat:
                break
        return self.text
            
    
                
    def parse(self, first=False, text=u""):
        """Parses the raw text, then puts the resulted fragments into its respective Fragment object.

See Documentation/how_to_parse.svg for more infos. 
Or, if first==False then immediately calls the parser of each fragment.

returns results, a list with many informations. See parsers to know what informations."""
        position = 0
        results = [] #parse result, position

        if first:
            parser = HTMLParser()
            parser.feed(text)
            parser.close()
            if parser.is_html():
                if parser.cutpoints:
                    self.inlines = [["html", HTMLFragment(text=text[0:parser.cutpoints[0][0]])]]
                    i = 0
                    for cutpoint in parser.cutpoints:
                        if parser.parsedinline[i][0] == "style":
                            fragmentype = "css"
                            parser.parsedinline[i][0] = fragmentype
                        #else ...
                        parser.parsedinline[i][1] = fragments[fragmentype](text=parser.parsedinline[i][1])    
                        self.inlines.append(parser.parsedinline[i])
                        if i+1 == len(parser.cutpoints):
                            #end
                            self.inlines.append(["html", HTMLFragment(text=text[cutpoint[1]:])])
                        else:
                            self.inlines.append(["html", HTMLFragment(text=text[cutpoint[1]:parser.cutpoints[i+1][0]])]) 
                        i += 1
                else:
                    self.inlines = [["html", HTMLFragment(text=text)]]
            else:
                #if is css ...
                self.inlines = [["css", CSSFragment(text=text)]]
        # else could be removed
        # but would do work twice
        else:
            for fragment in self.inlines:
                 results.append((fragment[1].parse(), position))
                 position += len(fragment[1].text)
        
            return results
    

    def save_in_file(self):
        codecs.open(self.save_path,'w',self.encoding).write(self.text)
        self.__saved = True
        
    #testing
    def test_file_with_browser(self):
        webbrowser.open(self.save_path,new=2)#new=2 to open in a new tab if possible
        
    @property
    def saved(self):
        return self.__saved

    @property
    def save_path(self):
        return self.__path

    @save_path.setter
    def save_path(self,new_path):
        self.__path = new_path

    @property
    def encoding(self):
        return self.__encoding_py
    
    @encoding.setter
    def encoding(self,new_encoding_py):
        assert new_encoding_py
        self.__encoding_py = new_encoding_py
        
    @property
    def w3c_encoding(self):
        #todo return encoding as it should appear in the meta charset
        return self.encoding

    @w3c_encoding.setter
    def w3c_encoding(self,new_w3c_encoding):
        #todo convert to python usable encoding string
        self.encoding = new_w3c_encoding
           
        
    def __add__(self,other):
        assert False, "not implemented"

    def __radd__(self,other):
        assert False, "not implemented"
        
    def __str__(self):
        return self.text
    
    def __repr__(self):
        return str(self)

    #def __getitem__(self, key):
    #    return deprecated
    
    def __len__(self):
        return len(self.text)


        
    
if __name__ == '__main__':
    html = "<html></html>"
    css = "* {a:b;}"
    js = "alert('hi');"
    
    import unittest
    import time
    
    BIG = 10
    class TestHTMLFragment(unittest.TestCase):

        def setUp(self):
            """do not remove"""
            self.html = "<html></html>"
            self.css = "* {a:b;}"
            self.js = "alert('hi');"
            self.t = HTMLFragment()
            
        def test_append(self):
            self.t.append(self.html)
            self.assertEqual(self.t.text, self.html)
            
        def test_big_append(self):
            for i in range(BIG):
                self.t.append(self.html)
                self.assertEqual(self.t.text, self.html * (i + 1))
            
        def test_insert(self):
            self.t.insert(self.html,5)
            self.assertEqual(self.t.text, self.html)
            
        def test_big_insert(self):
            for i in range(BIG):
                self.t.insert(self.html,5)
                self.t.insert(self.css,0)
                self.t.insert(self.js,7)
            
            
        def test_remove(self):
            self.t.insert(self.html)
            self.t.remove(3,5)
            self.assertEqual(self.t.text, "<ht></html>")
            
        def test_big_remove(self):
            self.t.insert(self.html * int((BIG / 10)))
            for i in range(BIG):
                self.t.remove(3,5)
            self.assertEqual(self.t.text, "<ht")
            
        def test_find(self):
            native_string = self.html
            self.t.append(self.html)
            searching = "html"
            
            self.assertEqual(self.t.find(searching), native_string.find(searching))
            native_string += self.css
            self.t.append(self.css)
            searching = "*"
            self.assertEqual(self.t.find(searching), native_string.find(searching))
            
            native_string += self.js
            self.t.append(self.js)
            searching = "alert"
            self.assertEqual(self.t.find(searching), native_string.find(searching))
            
            native_string += self.html
            self.t.append(self.html)
            searching = "html"
            self.assertEqual(self.t.find(searching, 15), native_string.find(searching, 15))
            
            searching = "cannot find"
            self.assertEqual(self.t.find(searching, 0), native_string.find(searching, 0))
            
        def test_replace(self):
            native_string = self.html
            self.t.append(self.html)
            old = "html"
            new = "body"
            self.t.replace(old, new)
            native_string = native_string.replace(old, new)
            self.assertEqual(self.t.text, native_string)

        
    unittest.main()
