#!/usr/bin/python
#-*-coding:utf-8*

#Text__classes.py
#Role: define objects containing documents

#Walle Cyril
#20/02/2014

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
##by sending an email to the following adress:capocyril@hotmail.com
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

import codecs
import os
import webbrowser
#import json


from character_translator import html5, html5reci,minimum_translation
from Options_class import *

class Text_(InterfaceOptions):
    """base Text_ class

with InterfaceOptions
"""
    def __init__(self,options_file_object,content="",saved=True,path="",encoding_py="utf-8"):
        self.__content=content
        self.__saved=saved
        self.__path=path
        self.__encoding_py=encoding_py
        
        #Parent data
        self.options_file_object=options_file_object#do not touch this directly use interface methods

    def is_saved(self):
        return self.__saved

    def set_save_path(self,new_path):
        self.__path=new_path

    def get_save_path(self):
        return self.__path

    def get_encoding(self):
        return self.__encoding_py
    
    def set_encoding(self,new_encoding_py):
        self.__encoding_py=new_encoding_py

    def save_in_file(self):
        codecs.open(self.__path,'w',self.__encoding_py).write(self.__content)
        self.__saved=True

    def save_in_file_to_test(self):
        """saves file in Cache folder with self-chosen name and returns path to that file."""
        file_name="essay-{}.{}".format(self.doctype,self.extension)
        file_path=os.path.join("Cache",file_name)
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
        self.__saved=False
        self.__content=new_content
    
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

class Text_HTML(Text_):
    def __init__(self,options_file_object,content="",saved=True,path="",encoding_py="utf-8",w3c_encoding="utf-8",version=5.0,document_language="fr"):
        Text_.__init__(self,options_file_object,content,saved,path,encoding_py)
        
        #specific addition for HTML
        self.w3c_encoding=w3c_encoding
        self.version=version
        self.document_language=document_language
        
        self.doctype="HTML{}".format(version)
        self.extension="html"
        
        #editing data
        self.element_still_not_closed_list=[]
        self.instant_indenting_level=0
        self.current_direction=0
        self.last_selected_element="p"
        self.last_selected_element_is_void=False
        #helps to indent properly
        self.current_translation_needed=True
        #help to detect if we need translation (e.g for display content)
        # or to protect tags themselves (e.g. for <p>)
        self.insertion=None
             
#editing methods
    def html_to_normal_char(self,html_conversion):
        #not used yet
        #uses dictionnaire html5
        if html_conversion[0]=='&':
            if html_conversion[1::] in html5:
                normal_char=html5[html_conversion[1::]]
            else:
                normal_char=html_conversion
        else:#Not a keyword
            normal_char=html_conversion
        return normal_char

    def normal_char_to_html(self,normal_char):
        level=self.get_option("translate_html_level")
        if level==1:
            translator=minimum_translation
        elif level==10:
            translator=html5reci
            
        if normal_char in translator:
            html_conversion=translator[normal_char]
            if html_conversion[0] !='&':
                html_conversion='&'+html_conversion
            if html_conversion[-1] !=';':
                html_conversion += ';'
            if html_conversion=="&<br />;":
                html_conversion="<br />"
            return html_conversion
        else:
            return normal_char

    def add_indent_and_line(self, text, first=False):
        indented_text="\n"
        if first:
            indented_text=""
        for _ in range(self.instant_indenting_level+self.current_direction):
            indented_text+=(self.get_option("indent_size") * self.get_option("indent_style"))
            
        if not(self.current_translation_needed) or self.get_option("translate_html_level")==0:
            indented_text+=text
        else:
            for chars in text:
                indented_text+=self.normal_char_to_html(chars)
                if self.normal_char_to_html(chars)=="<br />":#Ce if rend la prévisualisation plus lisible
                    indented_text+="\n"
                    for _ in range(self.instant_indenting_level+self.current_direction):
                        indented_text+=(self.get_option("indent_size") * self.get_option("indent_style"))
        self.current_direction=0
        self.current_translation_needed=True
        return indented_text

#editing macros with border effect
    def open_close_void_element(self,lone_element,attributes=""):
        self.current_translation_needed=False
        return "<"+lone_element+attributes+"/>"

    def open_element(self,lone_element,attributes=""):
        opening_tag="<"+lone_element+attributes+">"
        closing_tag="</"+lone_element+">"
        self.element_still_not_closed_list.append(closing_tag)
        self.instant_indenting_level += 1
        self.current_direction=-1
        self.current_translation_needed=False
        return opening_tag

    def close_element(self,closing_tag=""):
        if not closing_tag:
            closing_tag=self.element_still_not_closed_list.pop()
        else:
            closing_tag="</"+closing_tag+">"
        self.instant_indenting_level -= 1
        self.current_translation_needed=False
        return closing_tag#len(self.element_still_not_closed_list)>0

#editing super macros with direct border effect on the text
    def add_to_text(self,text):
        """adds the text to our current_text_html.

        if insertion is not None the text is inserted on the position value of insertion"""
        #to do also make possible to write and visualize in real time but not here
        if ((self.insertion is None) or (self.insertion>len(self))):        #insertion out of bound or None is appending
            insertion=len(self)
        else:
            insertion=self.insertion
        self.text="%s%s%s" % (self[0:insertion],text,self[insertion:])
        if insertion==self.insertion:
            self.insertion+=len(text)
        
    def add_standard_beginning(self):
        beginning=""
        previous_insertion=self.insertion
        previous_translate=self.get_option("translate_html_level")
        self.set_option("translate_html_level",0)
        self.insertion=None
        if self.version==5.0:
            beginning+= self.add_indent_and_line("<!DOCTYPE html>",first=True)
            beginning+=self.add_indent_and_line(self.open_element("html"," lang=\"{}\"".format(self.document_language)))
            beginning+=self.add_indent_and_line(self.open_element("head"))
            beginning+=self.add_indent_and_line(self.open_close_void_element("meta"," charset=\"{}\"".format(self.get_w3c_encoding())))
            beginning+=self.add_indent_and_line(self.open_close_void_element("link"," rel=\"stylesheet\" href=\"{}\"".format("coming_style.css")))
            beginning+=self.add_indent_and_line(self.open_element("title"))
            beginning+=self.add_indent_and_line(self.get_option("last_html_document_title"))
            beginning+=self.add_indent_and_line(self.close_element())#title close
            beginning+=self.add_indent_and_line(self.close_element())#head close
            beginning+=self.add_indent_and_line(self.open_element("body"))
        elif self.version==4.0:
             pass#complete here ...
            
        self.add_to_text(beginning)

        #revert effects
        self.insertion=previous_insertion
        self.set_option("translate_html_level",previous_translate)

    #settings
    def get_w3c_encoding(self):
        return self.w3c_encoding

    def set_w3c_encoding(self,new_w3c_encoding):
        self.w3c_encoding=new_w3c_encoding
        
    #testing
    def test_file_with_browser(self):
        webbrowser.open(self.save_in_file_to_test(),new=2)#new=2 to open in a new tab if possible


class Text_CSS(Text_):
    def __init__(self,content="",saved=True,path="",encoding_py="utf-8"):
        Text_.__init__(self,content,saved,path,encoding_py)
        
        #specific addition for CSS
        self.doctype="CSS"
        self.extension="css"
        
if __name__ == '__main__':
    pass
