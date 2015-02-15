#!/usr/bin/python
#-*-coding:utf-8*

#Text__classes.py
#Role: define objects containing documents

#Walle Cyril
#2014-11-09

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
from character_translator import html5, html5reci,minimum_translation
from Options_class import *

def _(l_string):
    return l_string

class Text_(InterfaceOptions):
    """base Text_ class

with InterfaceOptions
"""
    def __init__(self,options_file_object,content="",saved=True,path="",encoding_py="utf-8",
                 gui=None):
        self.__content = ""
        self.insertion = None
        self.tk_text = gui
        if content:
            self.add_to_text(content)
        if self.tk_text:
            self.tk_text.reset_undo()
        self.__saved = saved
        self.__path = path
        self.__encoding_py = encoding_py
        #if self.tk_text:
            # self.tk_text.tk_insert_text(where, inserted_text)
            # self.tk_text.tk_delete_text(from_, to_)
            # self.tk_text.reset_undo()

        self.last_find_index = -1
        #Parent data
        self.options_file_object = options_file_object#do not touch this directly use interface methods

    def is_saved(self):
        return self.__saved

    def set_save_path(self,new_path):
        self.__path = new_path

    def get_save_path(self):
        return self.__path

    def get_encoding(self):
        return self.__encoding_py
    
    def set_encoding(self,new_encoding_py):
        self.__encoding_py = new_encoding_py

    def save_in_file(self):
        codecs.open(self.__path,'w',self.__encoding_py).write(self.__content)
        self.__saved = True

    def save_in_file_to_test(self):
        """saves file in Cache folder with self-chosen name and returns path to that file."""
        file_name = "essay-{}.{}".format(self.doctype,self.extension)
        file_path = os.path.join("Cache",file_name)
        codecs.open(file_path,'w',self.__encoding_py).write(self.__content)
        return file_path
      
    @property
    def text(self):
        return self.read()
    
    @text.setter
    def text(self, value):
        self.__overwrite_content(value)
    
    #@text.deleter#not needed for now
        
    def read(self):
        """returns the content."""
        return self.__content

    def __overwrite_content(self,new_content):
        self.__saved = False
        self.__content = new_content
    
    def __add__(self,other):
        if isinstance(other,str):
            return self.__content + other

    def __radd__(self,other):
        if isinstance(other,str):
            return other + self.__content
        
    def __repr__(self):
        return self.read()

    def __getitem__(self, key):
        return self.read().__getitem__(key)
    
    def __len__(self):
        return len(self.read())

    def add_to_text(self,text):
        """adds the text to our text.

        if insertion is not None the text is inserted on the position value of insertion"""
        #to do write and see in real time
        if ((self.insertion is None) or (self.insertion>len(self))):#insertion out of bound or None is appending
            insertion = len(self)
        else:
            insertion = self.insertion
        self.text = "".join((self[0:insertion], text, self[insertion:]))
        if self.tk_text:
            self.tk_text.tk_insert_text(insertion, text)
        if insertion == self.insertion:
            self.insertion += len(text)
        else:
            self.insertion = None
            
    #def insert(self, index, text):
    def delete(self, start, length):
        self.text = "".join((self[0:start], self[start+length:]))
        self.insertion = start
        if self.tk_text:
            self.tk_text.tk_delete_text(start, start+length)
        
    def find(self, string, start=-2):
        if start == -2 :
            if self.last_find_index == -1:
                start = 0
            elif self.last_find_index != -1:
                start = self.last_find_index + len(string)
        self.last_find_index = self.read().find(string, start)
        return self.last_find_index

    def replace(self,old, new, count=-1):
        #count is ignored for now
        where = self.find(old)
        if where != -1:
            self.delete(where,len(old))
            self.add_to_text(new)
        
                                 
class Text_HTML(Text_):
    """Stores an html text and has methods to edit it."""
    def __init__(self,options_file_object,content="",saved=True,path="",encoding_py="utf-8",
                 w3c_encoding="utf-8",version=5.0,document_language="fr",
                 gui=None):
        Text_.__init__(self,options_file_object,content,saved,path,encoding_py,
                 gui=gui)

        #specific addition for HTML
        self.w3c_encoding = w3c_encoding
        self.version = version
        self.document_language = document_language
        
        self.doctype = "HTML{}".format(version)
        self.extension = "html"

        #html can contain css and js (inline)
        self.inline = {}
        #self.inline = {(index_start, index_end): "extension",
        #               (index_start, index_end): "extension"}
        
        #editing data
        self.element_still_not_closed_list = []
        self.instant_indenting_level = 0
        self.current_direction = 0
        #helps to indent properly
        self.current_translation_needed = True
        #help to detect if we need translation (e.g for display content)
        # or to protect tags themselves (e.g. for <p>)
        self.insertion = None
             
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

    def add_indent_and_line(self, text, first=False):
        if text == "":
            return ""
        #else:
        tr_level = self.get_option("translate_html_level")
        indented_text = "\n"
        if first:
            indented_text = ""
        for i in range(self.instant_indenting_level+self.current_direction):
            indented_text += (self.get_option("indent_size") * self.get_option("indent_style"))
            
        if not(self.current_translation_needed) or tr_level == 0:
            indented_text += text
        else:
            for character in text:
                new = self.normal_char_to_html(character,tr_level)
                indented_text += new
                if new == "<br />":#Ce if rend la prévisualisation plus lisible
                    indented_text += "\n"
                    for i in range(self.instant_indenting_level+self.current_direction):
                        indented_text += (self.get_option("indent_size") * self.get_option("indent_style"))
        self.current_direction = 0
        self.current_translation_needed = True
        return indented_text

#editing macros with border effect
    def open_close_void_element(self,lone_element,attributes=""):
        self.current_translation_needed = False
        return "<"+lone_element+attributes+">"

    def open_element(self,lone_element,attributes=""):
        opening_tag = "<"+lone_element+attributes+">"
        closing_tag = "</"+lone_element+">"
        self.element_still_not_closed_list.append(closing_tag)
        self.instant_indenting_level += 1
        self.current_direction = -1
        self.current_translation_needed = False
        return opening_tag

    def close_element(self,closing_tag=""):
        if not closing_tag:
            closing_tag = self.element_still_not_closed_list.pop()
        else:
            closing_tag = "</"+closing_tag+">"
        self.instant_indenting_level -= 1
        self.current_translation_needed = False
        return closing_tag#len(self.element_still_not_closed_list)>0

#editing super macros with direct border effect on the text
        
    def add_standard_beginning(self):
        beginning = ""
        previous_insertion = self.insertion
        previous_translate = self.get_option("translate_html_level")
        self.set_option("translate_html_level",0)
        self.insertion = None
        if self.version == 5.0:
            beginning += self.add_indent_and_line("<!DOCTYPE html>",first=True)
            beginning += self.add_indent_and_line(self.open_element("html"," lang=\"{}\"".format(self.document_language)))
            beginning += self.add_indent_and_line(self.open_element("head"))
            beginning += self.add_indent_and_line(self.open_close_void_element("meta"," charset=\"{}\"".format(self.get_w3c_encoding())))
            beginning += self.add_indent_and_line(self.open_close_void_element("link"," rel=\"stylesheet\" href=\"{}\"".format("coming_style.css")))
            beginning += self.add_indent_and_line(self.open_element("title"))
            beginning += self.add_indent_and_line(self.get_option("last_html_document_title"))
            beginning += self.add_indent_and_line(self.close_element())#title close
            beginning += self.add_indent_and_line(self.close_element())#head close
            beginning += self.add_indent_and_line(self.open_element("body"))
        elif self.version == "HTML 4.01 Strict":
            beginning +=  self.add_indent_and_line("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">",first=True)
            beginning += self.add_indent_and_line(self.open_element("html"," lang=\"{}\"".format(self.document_language)))
            beginning += self.add_indent_and_line(self.open_element("head"))
            beginning += self.add_indent_and_line(self.open_close_void_element("meta"," charset=\"{}\"".format(self.get_w3c_encoding())))
            beginning += self.add_indent_and_line(self.open_close_void_element("link"," rel=\"stylesheet\" href=\"{}\"".format("coming_style.css")))
            beginning += self.add_indent_and_line(self.open_element("title"))
            beginning += self.add_indent_and_line(self.get_option("last_html_document_title"))
            beginning += self.add_indent_and_line(self.close_element())#title close
            beginning += self.add_indent_and_line(self.close_element())#head close
            beginning += self.add_indent_and_line(self.open_element("body"))
        elif self.version == "HTML 4.01 Transitional":
            pass
            
        self.add_to_text(beginning)
        if self.tk_text:
            self.tk_text.reset_undo()

        #revert effects
        self.insertion = previous_insertion
        self.set_option("translate_html_level",previous_translate)

    #settings
    def get_w3c_encoding(self):
        return self.w3c_encoding

    def set_w3c_encoding(self,new_w3c_encoding):
        self.w3c_encoding = new_w3c_encoding
        
    #testing
    def test_file_with_browser(self):
        webbrowser.open(self.get_save_path(),new=2)#new=2 to open in a new tab if possible
        
    def validate(self,parsed_html=None):
        fail_messages = []
        if parsed_html is None:
            parsed_html = HTMLParser()
            parsed_html.feed(self.read())
            parsed_html.close()
            
        
        if not parsed_html.declaration:
            fail_messages.append(_(u"Déclaration du type de document introuvable, insérez <!DOCTYPE html>"))
        if not parsed_html.doctype_first:
            fail_messages.append(_(u"La déclaration du type de document doit se trouver en haut du document"))
        for should,closed in parsed_html.close_before_error_list:
            fail_messages.append(_(u"Vous devez fermer {} avant {}").format(should,closed))
        if len(parsed_html.start_list) > len(parsed_html.end_list):
            fail_messages.append(_(u"Il faut fermer toutes les balises !"))
        for parent,child in parsed_html.must_parent_errors:
            fail_messages.append(_(u"Les balises {} doivent êtres contenus dans des balises {}").format(child,parent))
            
        
        return fail_messages
    
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
                s_css_property_value.value = ss_property_value.value
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
    def __str__(sef):
        print("repr")
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
            
class CSSText(Text_):
    """Stores a css text and has methods to edit it."""
    
    def __init__(self,content=u"",saved=True,path=u"",encoding_py="utf-8"):
        Text_.__init__(self,None,content,saved,path,encoding_py)
        
        #specific addition for CSS
        self.doctype = "CSS"
        self.extension = "css"
        self.reset()

    def reset(self):
        self.content_list = []
        
    def append(self,to_add):
        """Adds the given object to the css text, delegating it to special methods."""
        if isinstance(to_add, str):
            self.add_to_text(to_add)
            self.parse()
        else:
            self.content_list.append(to_add)
        if self.tk_text:
            self.tk_text.tk_copy_text(self.text)
            

    def __repr__(self):
        return "\n".join(list(map(repr,self.content_list)))

    def parse(self):
        #...
        self.text = self.__repr__()
            
    def validate(self,parsed_css=None):
        fail_messages = []
        if parsed_css is None:
            pass
if __name__ == '__main__':
    t = Text_HTML(None,content="",saved=True,path="",encoding_py="utf-8",
                 w3c_encoding="utf-8",version=5.0,document_language="en",
                 gui=None)
    assert isinstance(t[:], str)
    t.add_to_text("The most important thing in your life is to always finish wha")
    assert t[:] == "The most important thing in your life is to always finish wha"
    t.replace("finish", "begin")#exist
    assert t[:] == "The most important thing in your life is to always begin wha"
    t.replace("honey", "butter")#not exist
    assert t[:] == "The most important thing in your life is to always begin wha"
    t.replace("in", "out")#multi
    assert t[:] == "The most important thoutg in your life is to always begin wha"
    t.replace("in", "out")#multi
    assert t[:] == "The most important thoutg out your life is to always begin wha"
    t.replace("in", "out")#multi
    assert t[:] == "The most important thoutg out your life is to always begout wha"
    t.delete(8, 10)
    assert t[:] == "The most thoutg out your life is to always begout wha"
    t.add_to_text(" text")
    assert t[:] == "The most text thoutg out your life is to always begout wha"
    
    
