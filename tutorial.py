#!/usr/bin/python
#-*-coding:utf-8*

#tutorial.py
#Role:Manage,open and close tutorials

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
import re
import webbrowser

from html_parser import*

def _(l_string):
    return l_string

def detect_existing_tutorials():
    """Reads all tuto/*name*/tuto.json to return a list of installed tutorials.

The list contains doubles in this format (dict_info, *name*)"""
    info_and_foldername = []
    tuto_folder = "tuto"
    for folder in os.listdir(tuto_folder):
        if os.path.isdir(os.path.join(tuto_folder, folder)):
            file_path = os.path.join(tuto_folder, folder, "tuto.json")
            if os.path.isfile(file_path):
                infos = json.loads(codecs.open(file_path,'r',"utf-8").read())
                info_and_foldername.append([infos, folder])
                

    return info_and_foldername

def start_tutorial(folder,gui_tk):
    """Opens home page of the tutorial + returns the verification."""
    gui_tk.lock_tutorial()
    model = gui_tk.model
    model.index_path = os.path.normpath(os.path.join("tuto",
                                                     folder,"index.html"))
    verification_path = os.path.normpath(os.path.join("tuto",
                                                      folder,"verification.json"))
    verification = json.loads(codecs.open(verification_path,'r',"utf-8").read())
    model.current_verification = verification
    model.tutorial_path = os.path.normpath(os.path.join("tuto",folder))
    model.tutorial_folder_name = folder
    
    tutorial_progress = model.get_option("tutorial_progress")
    if folder in tutorial_progress:
        model.current_step = tutorial_progress[folder]["current"]
        if model.current_step !=0:
            webbrowser.open_new_tab(os.path.normpath(os.path.join(
                "tuto",folder,model.current_verification[model.current_step]["this"])))
    else:
        model.current_step = 0
    if model.current_step == 0:
        webbrowser.open_new_tab(model.index_path)
        
    

def do_verification(document,expressions):
    html = document.text
    parsed_html = HTMLParser()
    parsed_html.feed(html)
    parsed_html.close()
    fail_messages = document.validate(parsed_html)
    if fail_messages:
        return fail_messages #Document must be valid html
    #else:
    for expression in expressions:
        #fail_messages = [] 
        x = 1 # we search at least one time
        search_reg_expr = True
        
        if expression[0] == "{":#prefix
            end_format = expression.find("}")
            search_type_format = expression[1:end_format].split(":")
            search_what = search_type_format[0][0]
            search_content = expression[end_format+1:]
            
            if search_what == "t":#tag
                """{t(c):x}tag1,tag2,...,tagn"""
                m1 = _("balise ouvrante %s manquante.(Voulu: %d. Trouvé: %d)")
                m2 = _("balise fermante %s manquante.(Voulu: %d. Trouvé: %d)")
                if len(search_type_format)>1:
                    x = int(search_type_format[1])
                close_strict = False
                if len(search_type_format[0])>1 and search_type_format[0][1]=="c":#must be closed
                    close_strict = True
                tags = search_content.split(",")
                for tag in tags:
                    if parsed_html.start_list.count(tag) < x:
                        fail_messages.append(m1 % (tag,x,
                                                   parsed_html.start_list.count(tag)))
                    if close_strict and parsed_html.end_list.count(tag) < x:
                        fail_messages.append(m2 % (tag,x,
                                                   parsed_html.end_list.count(tag)))
                        
            elif search_what == "a":#attribute
                """{a:attribute_name:x}tag1,tag2,...,tagn:value or None"""
                tags = search_content.split(":")[0].split(",")
                value = "".join(search_content.split(":")[1:])
                attribute_name = search_type_format[1]
                if len(search_type_format)>1:
                    x = int(search_type_format[2])
                count = 0
                value_missed = 0
                #impossible to count directly because there is no direct access
                #for each set of attribute, if there are any , if name in this list
                for i,keylist in enumerate(parsed_html.key_attribute_list):
                    if (isinstance(keylist,list) and attribute_name in keylist)\
                        and (not tags[0] or parsed_html.start_list[i] in tags):#and not None
                        if (not (value)) or (value in parsed_html.value_attribute_list[i]):
                            count+=1
                        elif value:
                            value_missed+=1
                if count < x :
                    fail_messages.append(_("attribut %s manquant. Voulus: %d Trouvés: %d") % (attribute_name,x,count))
                    if value_missed > 0:
                        fail_messages.append(_("valeur attendu:%s ") % (value))
                        
            elif search_what=="r":#raw (without parsing)
                """"{r}" will search in raw mode (without parsing html)"""
                if len(search_type_format[0]) > 1\
                   and search_type_format[0][1] == "o":
                    search_reg_expr = False
                    if html.find(search_content) == -1:
                        fail_messages.append(_("contenu %s non trouvé") % (search_content))
                elif re.search(search_content, html) is None:
                    fail_messages.append(_("expression régulière %s n'a pas connecté avec le document") % (search_content))
            
            elif search_what == "d":#data
                """{d:tag:x}expression  """
                found = 0
                tag = search_type_format[1]                
                if len(search_type_format) > 2:
                    x = int(search_type_format[2])
                if len(search_type_format[0]) > 1 and search_type_format[0][1] == "o":
                    search_reg_expr = False
                if search_reg_expr:
                    for pair in parsed_html.content_list:
                        if (tag=="any" or pair[0]==tag)\
                            and re.search(search_content, pair[1]):
                            found += 1
                            
                    if found < x:
                        fail_messages.append(_(u"{} expression régulière n'a pas connecté\
 dans l'élément {} (Voulu {};Trouvés {})").format(search_content,tag,x,found))
                else:
                    for pair in parsed_html.content_list:
                        if (tag == "any" or pair[0] == tag)\
                            and search_content in pair[1]:
                            found += 1
                    if found < x:
                        fail_messages.append(_(u"{}  n'a pas été trouvé\
dans l'élément {} (Voulu {};Trouvés {})").format(search_content,tag,x,found))
    

        else: # expression[0] != "{":
            """No prefix will be searched as data as non regular expression same as {do:any:1}expression"""
            if expression not in parsed_html.content_list:
                fail_messages.append(_("%s pas trouvé") % (expression))
    return fail_messages

def verify(model):
    self = model
    fail_messages = do_verification(self.tabs_html[self.selected_tab],\
                    self.current_verification[self.current_step]["verification"])

    success = not (fail_messages)
    finished = False
    messages = [""]
    links = [("","")]
    if success:
        after = self.current_verification[self.current_step]["afterthis"]
        tutorial_progress = self.get_option("tutorial_progress")
        if after.lower() != "end":
            self.current_step += 1
            messages = ["Bravo, vous pouvez aller à la prochaine étape (étape #%d)" % (self.current_step+1)]
            links = [(os.path.join(self.tutorial_path,after),_("prochaine étape"))]
            if self.tutorial_folder_name not in tutorial_progress:
                tutorial_progress[self.tutorial_folder_name] = {"current":self.current_step, "finished":finished}
                
            else:
                tutorial_progress[self.tutorial_folder_name]["current"] = self.current_step
                
        else:
            messages = [_("Bravo,vous avez terminé ce tutoriel")]
            finished = True
            links = [(self.index_path,_("revenir au départ"))]
            tutorial_progress[self.tutorial_folder_name] = {"current":0, "finished":finished}
        self.set_option("tutorial_progress", tutorial_progress)
            
            
    else:
        current = self.current_verification[self.current_step]["this"]
        links = [(os.path.join(self.tutorial_path,current),_("étape courante"))]
        messages = [_("Des erreurs (%d) ont été trouvés lors de la verification:") % (len (fail_messages))]+fail_messages
        if self.current_verification[self.current_step]["show_solution"]:
            links.append((os.path.join(self.tutorial_path,"solution_"+self.current_verification[self.current_step]["this"]),_("solution")))
        else:
            pass
        
                  
    self.graphical_user_interface_tk.feedback_verification(messages,links,finished)
#-------------------------------------------------------------------------------------
if __name__ == '__main__':
    print(detect_existing_tutorials())
