#!/usr/bin/python
#-*-coding:utf-8*

#tutorial.py
#Role:Manage,open and close tutorials


#2014-11-09

##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##WebSpree

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
##If you have questions concerning this license you may contact
##by opening an issue
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
        
    

def do_verification(model, document, expressions):
    """See \Documentation\specifications\technical_spec.md to know."""
    text = document.text
    fail_messages = model.validate_document()
    parsed_html = model.tabs_html[model.selected_tab].parse()[0][0] # and css ?
    if fail_messages:
        return fail_messages #Document must be valid html
    #expression can be [["t","c","1"],["html","head","meta","title","body","p"]]
    for expression in expressions:
        descriptors = expression[0]
        targets = expression[1]
        if descriptors[0] == "t": #tag
            m1 = _("balise ouvrante %s manquante.(Voulu: %d. Trouvé: %d)")
            m2 = _("balise fermante %s manquante.(Voulu: %d. Trouvé: %d)")
            x = 1 # we search at least one time)
            if len(descriptors)>1:
                x = int(descriptors[-1])
            for tag in targets:
                if parsed_html.start_list.count(tag) < x:
                    fail_messages.append(m1 % (tag,x,
                        parsed_html.start_list.count(tag)))
                if parsed_html.end_list.count(tag) < x:
                    fail_messages.append(m2 % (tag,x,
                        parsed_html.end_list.count(tag)))
                    
        elif descriptors[0] == "a":#attribute
            attribute_name = descriptors[1]
            value= ""
            if len(descriptors) > 2:
                value = descriptors[2]
            count = 0
            value_missed = 0
            #impossible to count directly because there is no direct access
            #for each set of attribute, if there are any , if name in this list
            for i,keylist in enumerate(parsed_html.key_attribute_list):
                if ((isinstance(keylist,list) and attribute_name in keylist) and
                    (not(targets) or parsed_html.start_list[i] in targets)):#and not None
                    if (not (value)) or (value in parsed_html.value_attribute_list[i]):
                        break
            else:
                fail_messages.append(_(u"attribut %s manquant.(%s)") % (attribute_name,value))
                
        elif descriptors[0] == "r":#raw (without parsing)
            if len(descriptors) > 1 and descriptors[1] == "o":
                for target in targets:
                    if text.find(target) == -1:
                        fail_messages.append(_("contenu %s non trouvé") % (target))
            else:
                for target in targets:
                    if re.search(target, text) is None:
                        fail_messages.append(_("expression régulière %s n'a pas connecté avec le document") % (target))
        
        elif descriptors[0] == "d":#data
            tag = descriptors[1]
            if len(descriptors) > 2 and descriptors[2] == "o":
                for pair in parsed_html.content_list:
                    if (tag == "any" or pair[0] == tag) and search_content in pair[1]:
                        break
                else:
                    fail_messages.append(_(u"{}  n'a pas été trouvé\
dans l'élément {}").format(search_content,tag))
            else:
                for pair in parsed_html.content_list:
                    if (tag == "any" or pair[0] == tag) and re.search(targets[0], pair[1]):
                        break
                else:        
                    fail_messages.append(_(u"{} expression régulière n'a pas connecté dans l'élément {}").format(targets[0],tag))
                
    return fail_messages

def verify(model):
    self = model
    if self.current_verification is None:
        return #  no tutorial selected
    fail_messages = do_verification(model, self.tabs_html[self.selected_tab],
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
