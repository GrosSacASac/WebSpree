#!/usr/bin/python
#-*-coding:utf-8*

#Options_class.py
#Role:class defintion to keep extra data alive

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
import json
def _(l_string):
    #print("local language: "+l_string)
    return l_string

class Options():
    """Options is a class designed to read, add and change informations in a JSON file with a dictionnary in it.

    The entire object works even if the file is missing since it re-creates it.
    If present it must respect the JSON format: e.g. keys must be strings and so on.
    If something corrupted the file, just destroy the file or call read_file method to remake it.
    If the file is not accessible,
         default values will always be given and updating a value has no effect."""
    
    def __init__(self,directory_name="Cache",file_name="options.json",imported_default_values=None):
        #json file
        self.option_file_path=os.path.normpath(os.path.join(directory_name,file_name))
        self.directory_name=os.path.normpath(directory_name)
        self.file_name=file_name
        #self.parameters_json_file={'sort_keys':True, 'indent':4, 'separators':(',',':')}
        #the default data
        if imported_default_values is None:
            self.default_values={}
        else:
            self.default_values=imported_default_values
            for key in self.default_values:
                self.read_file(read_this_key_only=key)
            
        
    def read_file(self,read_this_key_only=False,for_update=False):
        """returns the value for the given key or a dictionary if the key is not given.

        returns the default value(s) if it s impossible to reach the file as wanted
        returns None if the key doesnt exist in the default values
        don t use for_update argument. It is just there for intern methods"""
        text_in_file = self.__read_raw_text()
        if not(text_in_file):#file could not be read properly
            option_dict=self.default_values
            if for_update:
                return None
        else:
            option_dict = self.__text_to_dict(text_in_file)
            if not(option_dict):
                option_dict=self.default_values
                
        if read_this_key_only:
            if read_this_key_only in option_dict:
                return option_dict[read_this_key_only]
            else:
                #if the value is not there it should be written for the next time
                if read_this_key_only in self.default_values:
                    self.add_option_to_file(read_this_key_only,self.default_values[read_this_key_only])
                    return self.default_values[read_this_key_only]
                else:
                    #impossible because there is not default value so the value isn t meant to be here
                    return None
        else:
            return option_dict

    def add_option_to_file(self,key,value):#or update
        """Adds or updates an option(key and value) to the json file.

The option must exists in the default_values of the object
and there should be no problem for reading and writing the file."""
        
        option_dict=self.read_file(for_update=True)
        if option_dict is not None:
            if key in self.default_values:
                option_dict[key]=value
            try:
                codecs.open(self.option_file_path,'w',"utf-8").write(\
                    json.dumps(option_dict,sort_keys=True, indent=4, separators=(',',':')))
            except IOError:#permission error
                pass#updating a file that is not accessible is impossible


    def __read_raw_text(self):
        if os.path.exists(self.option_file_path):
            text_in_file=codecs.open(self.option_file_path,'r',"utf-8").read()
        else:
            text_in_file=""#if the file is not there we re-make one with default values
        if text_in_file=="":#same if the file is empty
            if self.__insert_all_default_values():
                text_in_file=codecs.open(self.option_file_path,'r',"utf-8").read()
            else:
                text_in_file=False
        return text_in_file

    def __text_to_dict(self, text_in_file):
        try:
            option_dict=json.loads(text_in_file)
        except ValueError:
            #if the json file is broken we re-make one with default values
            if self.__insert_all_default_values():
                text_in_file = self.__read_raw_text()
                option_dict=json.loads(text_in_file)
            else:
                option_dict=False
        return option_dict
    
    def __insert_all_default_values(self):
        """Recreate json file with default values.

    called if the document is empty or non-existing or corrupted."""
        possible=True
        try:
            if os.path.isdir(self.directory_name):
                codecs.open(self.option_file_path,'w',"utf-8").write(\
                json.dumps(self.default_values,sort_keys=True, indent=4, separators=(',',':')))
            else:
                os.mkdir(self.directory_name)#Create the directory
                self.__insert_all_default_values()#succes
        except IOError:#permission error
                print("Access denied to write in %s" % (os.path.abspath(self.option_file_path)))
                possible=False
        return possible

class InterfaceOptions():
    def __init__(self):
        pass
    def set_option(self,option_name,value):
        self.options_file_object.add_option_to_file(option_name,value)
    def get_option(self,option_name):
        return self.options_file_object.read_file(read_this_key_only=option_name)

DEFAULT_VALUES={\
#editing global
    "translate_html_level": 1,\
    "indent_size":2,\
    "indent_style":" ",\
    "footer_bonus":False,\
#editing local (read only to set a default value)
    "html_version":5.0,\
    "document_language":"fr",\
#history
    "last_html_document_title":_("Titre"),\
    "last_css_document_title":_("Titre"),\
    "previous_files_opened":[],\
#app
    "license_accepted_and_read":False,\
    "app_language":"fr",\
    "developper_interface":False,\
#tutorials
    "tutorial_progress":{}\
    }
#demo
if __name__ == '__main__':
    option_file_object=Options()
    print(option_file_object.__doc__)
    print("\n",option_file_object.read_file())
    option_file_object.add_option_to_file("non-existing-key","test")#this should have no effect
    
    option_file_object.add_option_to_file("translate_html_level","0")#this should have an effect
    print("value of translate_html_level:",option_file_object.read_file("translate_html_level"))
    print(option_file_object.read_file())
