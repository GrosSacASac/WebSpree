#!/usr/bin/python
#-*-coding:utf-8*

#WebSpree.py
#Role: main file

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

try:
    import os
    #import os.path useless ?
except Exception as e:
    print("Do you see this ? #problem with Mac still dont know where it comes from",e)
    pass
import time
import platform
import webbrowser

##DATA##
#from file_extractor import*
##GUI##
from GraphicalUserInterfaceTk import *
##TEXT AND STRINGS##
from Text__classes import *
##OPTIONS##
from Options_class import *
##LOG##
from log_writer import log_writer
##parser##

def _(l_string):
    return l_string

DEFAULT_ENCODING_PY = DEFAULT_ENCODING_WEB = "utf-8"
def get_time(time_modell="%d/%m/%Y\n%H:%M:%S"):
    return time.strftime(time_modell)

def title_from_path(path):
    return os.path.splitext(os.path.basename(path))[0]


class WebSpree(InterfaceOptions):#Model
    """ Bridge between all. Single instance only.

creating a copy of this object starts the app."""
    def __init__(self):
        #options
        self.options_file_object = Options(imported_default_values=DEFAULT_VALUES)
        #do not touch this directly use interface methods
        
        #we create 1 html tab. Each tab is an instance of FileDocument class
        #each tab is stored as 1 element of this list
        
        #this is the variable to know which one the user is currently editing
        self.selected_tab = 0
        
        self.graphical_user_interface_tk = GraphicalUserInterfaceTk(self)
        self.tabs_html = []
##        for path in self.get_option("previous_files_opened"):
##            try:
##                self.edit_file(path)
##            except Exception as E:
##                print(E)
##                pass#file not found or something
        for path in self.get_option("previous_files_opened"):
            self.edit_file(path)
            
        if not self.tabs_html:#nothing opened so we provide a blank "new" file
            self.start_mod = "newtab"
            self._start_new_session()
        self.graphical_user_interface_tk._start()
        
    def create_document(self, selected_tab, title, text=u"", path=u""):
        self.graphical_user_interface_tk.new_html_tab(selected_tab, title)
        current_text_html = FileDocument(self.options_file_object,content=text,
                                      saved=True, path=path,
                                      encoding_py=DEFAULT_ENCODING_PY,
                                      document_language="fr", # !
                                      gui_link=self.graphical_user_interface_tk)
        self.tabs_html.append(current_text_html)
        current_text_html.start()
        
    def _start_new_session(self):
        self.selected_tab = len(self.tabs_html)
        if self.start_mod == "standard":
            self.create_document(self.selected_tab, self.get_option("last_html_document_title"))
            self.tabs_html[selected_tab].add_standard_beginning()
            
        elif self.start_mod == "blank":
            self.create_document(self.selected_tab, self.get_option("last_html_document_title"))

        elif self.start_mod == "open":
            self.graphical_user_interface_tk.edit_file_dialog()
            #perhaps check if correctly opened here and update some data
            #but then Ctrl+N hotkey misses something
            
        elif self.start_mod == "newtab":
            self.create_document(self.selected_tab, _("nouveau"))
                     
    def edit_file(self,file_path):
        if not os.path.isfile(file_path):
            return #we stop here because the file has been lost        
        #print("edit_file:", file_path)
        self.selected_tab = len(self.tabs_html)
        text_in_file = codecs.open(file_path,'r','utf-8').read()
        #set other usefull data here
        self.set_option("last_html_document_title",title_from_path(file_path))
        self.create_document(self.selected_tab, self.get_option("last_html_document_title"),
                             text=text_in_file, path=file_path)       

        
        #todo
        #change the way it sniffs out the encoding  and redo this method
        
    def _save_html_file_as(self,file_path):
        tab_index = self.selected_tab
        current_text_html = self.tabs_html[tab_index]
        if self.get_option("footer_bonus"):
            optional_bonus = ("<!-- Document produit avec WebSpree\n{}\n{} -->".format(get_time(),"Fait par Cyril Walle\ncapocyril [ (a ] hotmail.com"))
            current_text_html.add_to_text(optional_bonus)
        
        #if os.path.splitext(file_path)[1] != ".html":
            #file_path=os.path.splitext(file_path)[0]+".html"
        #TODO Let user choose other extension if he/she really wants to have a forced extension
        
        current_text_html.save_path = file_path
        current_text_html.save_in_file()
        self.graphical_user_interface_tk.html_text_tabs.tab(tab_index,text=title_from_path(file_path))
        return True#only when success

    def save_html_file(self,*event):
        current_text_html = self.tabs_html[self.selected_tab]
        if current_text_html.save_path:
            current_text_html.save_in_file()
            return True
        else:#ask for a new path
            return self.graphical_user_interface_tk._save_file_dialog()
            
        
    def save_file_totest(self):#Try with CTRL+Shift+T
        current_text_html = self.tabs_html[self.selected_tab]
        if current_text_html.saved or self.save_html_file():
            current_text_html.test_file_with_browser()
        
    def guess_dir(self):
        current_text_html = self.tabs_html[self.selected_tab]
        last_path = current_text_html.save_path
        if last_path:
            return os.path.dirname(last_path)
        else:
            return os.path.expanduser('~')
        
    def validate_document(self):
        results = self.tabs_html[self.selected_tab].parse()
        messages = []
        if len(results) > 1:
            messages.append(_(u"Faites des documents uniques, ne mélangez pas html, css et js"))
            messages.append(str(len(results)))
        else:
            result = results[0][0]
            if self.tabs_html[self.selected_tab].inlines[0][0] == "html":
                parsed_html = result
                if not parsed_html.declaration:
                    messages.append(_(u"Déclaration du type de document introuvable, insérez <!DOCTYPE html>"))
                if not parsed_html.doctype_first:
                    messages.append(_(u"La déclaration du type de document doit se trouver en haut du document"))
                for should,closed in parsed_html.close_before_error_list:
                    messages.append(_(u"Vous devez fermer {} avant {}").format(should,closed))
                if len(parsed_html.start_list) > len(parsed_html.end_list):
                    messages.append(_(u"Il faut fermer toutes les balises !"))
                for parent,child in parsed_html.must_parent_errors:
                    messages.append(_(u"Les balises {} doivent êtres contenus dans des balises {}").format(child,parent))
            #elif
            
        return messages        

    def return_fragment(self, wanted="html"):
        for inline in self.tabs_html[self.selected_tab].inlines:
            if inline[0] == wanted:
                return inline[1]
        else:
            print("wanted fragment not found")
        


if __name__ == '__main__':
    log_writer("platform", platform.platform())
    log_writer("python_build", platform.python_build())
    WebSpreeInstance=WebSpree()
