#!/usr/bin/python
#-*-coding:utf-8*

#log_writer.py
#Role:write information about the system, screen resolution and more in a log file
#no information about the work itself should be written in a log file only information to help debugging

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
import json

def log_writer(key,value):
    #look data
    directory_name="Cache"
    file_name="journal.json"
    file_path=os.path.normpath(os.path.join(directory_name,file_name))
    if os.path.exists(file_path):
        text_in_file=codecs.open(file_path,'r',"utf-8").read()
        try:
            data=json.loads(text_in_file)
        except ValueError: #if the json file is broken 
            data={}
    else:
        data={}

    #update data
    data[key]=value
    try:
        codecs.open(file_path,'w',"utf-8").write(\
            json.dumps(data, separators=(',',':')))
    except IOError:
        pass

