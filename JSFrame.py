#!/usr/bin/python
#-*-coding:utf-8*

#JSFrame.py
#Role: Define the JS specific tools in tkinter

#Walle Cyril
#2017-11-09

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

#import tkinter ...
try:#3.X
    import tkinter as tk
    import tkinter.ttk  as ttk
    import tkinter.filedialog as filedialog
    import tkinter.messagebox as messagebox
    import tkinter.font as tkfont
except ImportError:#2.X
    import Tkinter as tk
    import ttk as ttk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
    import tkFont as tkfont

import webbrowser
import time

from tutorial import*
##DATA##
from file_extractor import*
##STYLES##
from tks_styles import*
##LOG##
#from log_writer import log_writer
##TOOLS##
from tks_widgets_1 import *

def _(l_string):
    #print("local language: "+l_string)
    return l_string


class JSFrame(tk.Frame):
    """CSS  frame."""

    def __init__(self, parent, master_window, model, adapted_height):
        tk.Frame.__init__(self,parent)
        self.model = model
        self.master_window = master_window

        commandsAndLabels = [
            [self.insert_import, _(u"Import")],
            [self.insert_export, _(u"Export")],
            [self.insert_function, _(u"Fonction")],
            [self.insert_iife, _(u"IIFE")],
            [self.insert_if_else_else_if, _(u"If else...")],
            [self.insert_class, _(u"Classe")]
        ]
        i = 0
        for command, label in commandsAndLabels:
            button_i=ttk.Button(self, text=label,command=command)
            button_i.grid(row=i,column=0,sticky='nw')
            i += 1


    def insert_function(self):

        self.insert_text("""const FUNCTION = function () {
    
};""")
        
    def insert_class(self):

        self.insert_text("""const CLASS = class {
    constructor (x) {
        this.x = x
    }
};""")
        
    def insert_if_else_else_if(self):

        self.insert_text("""if (CONDITIONA) {

} else if (CONDITIONB) {

} else {

}""")
    def insert_import(self):
        self.insert_text("""import {AAA, BBB}  from "./EXAMPLE.js";""")

    def insert_export(self):
        self.insert_text("""export {AAA, BBB};""")

    def insert_iife(self):

        self.insert_text("""(function () {
   // function body 
}());""")
            
    def insert_text(self, text):
        tab_index = self.model.selected_tab
        cursor_position = self.master_window.get_cursor_position()
        current_object=self.model.tabs_html[tab_index]
        current_object.insert(text + "\n", cursor_position)

    def save_file_to_test_control(self,*event):
        self.model.save_file_totest()
        
