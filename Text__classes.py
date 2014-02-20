#!/usr/bin/python
#-*-coding:utf-8*

#Text__classes.py

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

class Text_():
    """base Text_ class"""
    def __init__(self,content="",saved=True,path="",encoding_py="utf-8"):
        self.__content=content
        self.__saved=saved
        self.__path=path
        self.__encoding_py=encoding_py

    def is_saved(self):
        return self.__saved

    def set_save_path(self,new_path):
        self.__path=new_path

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
    def __init__(self,content="",saved=True,path="",encoding_py="utf-8",w3c_encoding="utf-8",version=5.0):
        Text_.__init__(self,content,saved,path,encoding_py)
        
        #specific addition for HTML
        self.version=version
        self.w3c_encoding=w3c_encoding
        self.doctype="HTML{}".format(version)
        self.extension="html"

    def get_w3c_encoding(self):
        return self.w3c_encoding
    
    def set_w3c_encoding(self,new_w3c_encoding):
        self.w3c_encoding=new_w3c_encoding

    def test_file_with_browser(self):
        webbrowser.open(self.save_in_file_to_test(),new=2)#new=2 to open in a new tab if possible

##    perhaps insert  add_to_text1 in this kind of object


class Text_CSS(Text_):
    def __init__(self,content="",saved=True,path="",encoding_py="utf-8"):
        Text_.__init__(self,content,saved,path,encoding_py)
        
        #specific addition for CSS
        self.doctype="CSS"
        self.extension="css"
        
if __name__ == '__main__':
    pass
