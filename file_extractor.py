#!/usr/bin/python
#-*-coding:utf-8*

#file_extractor.py
#Role:extracts data from static data files

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

DEFAULT_ENCODING_PY = DEFAULT_ENCODING_WEB = "utf-8"
FILE_TYPES = [("HyperText Mark-Up Language file", "*.html" ),
              ("Cascade Style Sheet", "*.css"),
              ("JavaScript", "*.js"),
              ("All","*.*")]
######----Constantes longues et extracteurs-----######
#This will not be used anymore:
def table_with_textfile(NomDuDocument,NbColonnes,Tableau=None):
    """Remove this soon when all constants are normalized"""
    if Tableau is None:
        Tableau = []
    ManqueAide = "Il n'y a pas encore d'aide ici"
    LigneS = codecs.open(NomDuDocument,'r',"utf-8").readlines()
    Ligne = LigneS.pop(0).strip("\ufeff")#enlever éventuellement la signature utf-8
    i = -1
    while True:
        #print(Ligne.strip())
        if Ligne[0] != "#":
            Tableau.append([])
            i += 1
            for cols in range(NbColonnes):
                try:
                    TexteCol = ((Ligne.split(";"))[cols]).strip()
                except IndexError:
                    TexteCol = ManqueAide
                finally:
                    if not(TexteCol):
                        TexteCol = ManqueAide
                    Tableau[i].append(TexteCol)
        try:
            Ligne = LigneS.pop(0)
        except IndexError:
            break
    return Tableau



staticf = "Constantes/"
#extract and store
def json_file_to_object(directory_name="", file_name=""):
    """Reads a json file and returns its equivalent python object."""
    file_path = os.path.normpath(os.path.join(directory_name,file_name))
    return json.loads(codecs.open(file_path,'r',"utf-8").read())

def load_local_strings(lang="fr"):
    """returns additional description in selected language."""
    return (json_file_to_object(staticf+lang, lang+"_html5_elements.json"),
            json_file_to_object(staticf+lang, lang+"_html5_attributes.json"),
            json_file_to_object(staticf+lang, lang+"_css_selectors.json")
            )

def object_to_json_file(data, directory_name="", file_name=""):
    """Stores data in json format in the given path."""
    file_path = os.path.normpath(os.path.join(directory_name,file_name))
    print ("saving",file_path)
    codecs.open(file_path,'w',"utf-8").write(
                    json.dumps(data,sort_keys=True, indent=4,
                               separators=(',',':'))
                    )
    
ENCODINGS = table_with_textfile(os.path.normpath(os.path.join("Constantes","encodings.txt")),3)



ELEMENTS = json_file_to_object(staticf,"htmlelements.json")
ATTRIBUTES = json_file_to_object(staticf,"html5_attributes.json")
GENERAL_ATTRIBUTES_LIST = json_file_to_object(staticf,"html5_general_attributes.json")

CSS_SELECTORS = json_file_to_object(staticf,"css_selectors.json")

(LOCAL_ELEMENTS, LOCAL_ATTRIBUTES,
 LOCAL_CSS_SELECTORS)               = load_local_strings("fr")



def store_change_in_source(data_holder,lang="fr"):
    """Saves the source file so that it has the same value as the current variable."""    
    if data_holder is ELEMENTS: #id(data_holder) == id(ELEMENTS)
        object_to_json_file(data_holder,staticf,"htmlelements.json")
    elif data_holder is ATTRIBUTES:
        object_to_json_file(data_holder,staticf,"html5_attributes.json")
    elif data_holder is GENERAL_ATTRIBUTES_LIST:
        object_to_json_file(data_holder,staticf,"html5_general_attributes.json")
    elif data_holder is CSS_SELECTORS:
        object_to_json_file(data_holder,staticf,"css_selectors.json")
    elif data_holder is LOCAL_ELEMENTS:
        object_to_json_file(data_holder,staticf+lang, lang+"_html5_elements.json")
    elif data_holder is LOCAL_ATTRIBUTES:
        object_to_json_file(data_holder,staticf+lang, lang+"_html5_attributes.json")
    elif data_holder is LOCAL_CSS_SELECTORS:
        object_to_json_file(data_holder,staticf+lang, lang+"_css_selectors.json")
                

if __name__ == '__main__':
    pass
