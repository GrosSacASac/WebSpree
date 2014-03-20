#!/usr/bin/python
#-*-coding:utf-8*

#tutorial.py
#Role:Manage,open and close tutorials

#Walle Cyril
#14/03/2014

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
import re
import webbrowser

from custom_parser import*

def _(l_string):
    #print("local language: "+l_string)
    return l_string

def detect_existing_tutorials():
    """reads tuto/tuto.json to return a list of installed tutorials."""
    file_path=os.path.normpath(os.path.join("tuto","tuto.json"))
    tutorials=json.loads(codecs.open(file_path,'r',"utf-8").read())
    name_and_foldername=[]
    for tutorial in tutorials:
        name_and_foldername.append([tutorial["name"],\
                                                        tutorial["folder"]])
    return name_and_foldername#a list with doubles

def start_tutorial(folder,GUItk):
    """Opens home page of the tutorial + returns the verification."""
    index_path=os.path.normpath(os.path.join("tuto",folder,"index.html"))
    verification_path=os.path.normpath(os.path.join("tuto",folder,"verification.json"))
    webbrowser.open_new_tab(index_path)
    verification=json.loads(codecs.open(verification_path,'r',"utf-8").read())
    GUItk.html_window.prepare_verification()#enable "check" button
    GUItk.lock_tutorial()
    GUItk.model.current_verification=verification
    GUItk.model.index_path=index_path
    GUItk.model.tfolder=os.path.normpath(os.path.join("tuto",folder))
    GUItk.model.tfolderw=folder
    GUItk.model.current_step=0

def do_verification(html,expressions):
    parsed_html = HTMLParser2()
    parsed_html.feed(html)
    parsed_html.close()
    fail_messages=[]
    for expression in expressions:
        x=1#default we search at least one time
        search_reg_expr=True
        d=False#see d
        
        if expression[0]=="{":#prefix
            end_format=expression.find("}")
            search_type_format=expression[1:end_format].split(":")
            search_what=search_type_format[0][0]
            search_content=expression[end_format+1:]
            
            if search_what=="t":#tag
                """{t:x}tag1,tag2,...,tagn"""
                m1=_("balise ouvrante %s manquante.(Voulu: %d. Trouvé: %d")
                m2=_("balise fermante %s manquante.(Voulu: %d. Trouvé: %d")
                if len(search_type_format)>1:
                    x=int(search_type_format[1])
                close_strict=False
                if len(search_type_format[0])>1 and search_type_format[0][1]=="c":#must be closed
                    close_strict=True
                tags=search_content.split(",")
                for tag in tags:
                    if not (parsed_html.start_list.count(tag)>=x):
                        fail_messages.append(m1 % (tag,x,parsed_html.start_list.count(tag)))
                    if close_strict and not(parsed_html.end_list.count(tag)>=x):
                        fail_messages.append(m2 % (tag,x,parsed_html.start_list.count(tag)))
                        
            elif search_what=="a":#attribute
                """{a:attribute_name:x}tag1,tag2,...,tagn:value or None"""
                tags=search_content.split(":")[0].split(",")
                value=search_content.split(":")[1]
                attribute_name=search_type_format[1]
                if len(search_type_format)>1:
                    x=int(search_type_format[2])
                count=0
                value_missed=0
                #impossible to count directly because there is no direct access
                #for each set of attribute, if there are any , if name in this list
                for i,keylist in enumerate(parsed_html.key_attribute_list):
                    if isinstance(keylist,list):#and not None
                        if attribute_name in keylist:
                            if not tags[0] or parsed_html.start_list[i] in tags:
                                if (not (value)) or (value and value in parsed_html.value_attribute_list):
                                    count+=1
                                elif value:
                                    value_missed+=1
                if not(count>=x):
                    fail_messages.append(_("attribut %s manquant. Voulus: %d Trouvés: %d") % (attribute_name,x,count))
                    if value_missed>0:
                        fail_messages.append(_("    valeur attendu:%s ") % (value))
                        
            elif search_what=="r":#raw (without parsing)
                """"{r}" will search in raw mode (without parsing html)"""
                if len(search_type_format[0])>1 and search_type_format[0][1]=="o":
                    search_reg_expr=False
                    if html.find(search_content)==-1:
                        fail_messages.append(_("contenu %s non trouvé") % (search_content))
                else:
                    if re.search(search_content, html) is None:
                        fail_messages.append(_("expression régulière %s n'a pas connecté avec le document") % (search_content))
            
            elif search_what=="d":#data
                """{d:tag:x}expression        d for data tag is ignored for now"""
                
                tag=search_type_format[1]
                if tag=="any":
                    pass
                if len(search_type_format)>2:
                    x=int(search_type_format[2])
                if len(search_type_format[0])>1 and search_type_format[0][1]=="o":
                    search_reg_expr=False
                if search_reg_expr:
                    found=False
                    for content in parsed_html.content_list:
                        if re.search(search_content, content):
                            found=True
                            break
                    if not found:
                        fail_messages.append(_("%s expression régulière n'a pas connecté") % (search_content))
                else:
                    if not search_content in parsed_html.content_list:
                        fail_messages.append(_("%s pas trouvé") % (search_content))
                #d=True#link to the next, take d away when elif search_what=="d": is ready
                                

            
        if expression[0]!="{" or d:#
            """No prefix will be searched as data as non regular expression same as {do:any:1}expression"""
            if expression in parsed_html.content_list:
                pass
            else:
                fail_messages.append(_("%s pas trouvé") % (expression))
    #do stuff
    del parsed_html#maybe useless
    return fail_messages

def verify(model):
    self=model
    fail_messages=do_verification(self.tabs_html[self.selected_tab].text,\
                    self.current_verification[self.current_step]["verification"])

    success= not (fail_messages)
    finished=False
    messages=[""]
    links=[("","")]
    if success:
        after=self.current_verification[self.current_step]["afterthis"]
        if not(after=="END"):
            self.current_step += 1
            messages=["Bravo, vous pouvez aller à la prochaine étape (étape #%d)" % (self.current_step+1)]
            links=[(os.path.join(self.tfolder,after),_("prochaine étape"))]
        else:
            messages=[_("Bravo,vous avez terminé ce tutoriel")]
            finished=True
            links=[(self.index_path,_("revenir au départ"))]
            tutorial_finished=self.get_option("tutorial_finished")
            if not self.tfolderw in tutorial_finished:
                tutorial_finished.append(self.tfolderw)
                self.set_option("tutorial_finished",tutorial_finished)
            
            
    else:
        current=self.current_verification[self.current_step]["this"]
        links=[(os.path.join(self.tfolder,current),_("étape courante"))]
        messages=[_("Des erreurs (%d) ont été trouvés lors de la verification:") % (len (fail_messages))]+fail_messages
        if self.current_verification[self.current_step]["show_solution"]:
            links.append((os.path.join(self.tfolder,"solution_"+self.current_verification[self.current_step]["this"]),_("solution")))
        else:
            pass
            
                  
    self.graphical_user_interface_tk.html_window.feedback_verification(messages,links,finished)
#-------------------------------------------------------------------------------------
if __name__ == '__main__':
    print(detect_existing_tutorials())
