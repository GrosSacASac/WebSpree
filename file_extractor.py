#!/usr/bin/python
#-*-coding:utf-8*

#file_extractor.py
#Role:extracts data from static data files

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

DEFAULT_ENCODING_PY = DEFAULT_ENCODING_WEB = "utf-8"

######----Constantes longues et extracteurs-----######
#This will not be used anymore:
def table_with_textfile(NomDuDocument,NbColonnes,Tableau=None):
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
            i = i+1
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
#New extractors:s
def json_file_to_object(directory_name="", file_name=""):
    file_path = os.path.normpath(os.path.join(directory_name,file_name))
    return json.loads(codecs.open(file_path,'r',"utf-8").read())

def load_local_strings(lang="fr"):
    return (json_file_to_object(staticf+lang, lang+"_html5_elements.json"),
            json_file_to_object(staticf+lang, lang+"_html5_attributes.json"),
            json_file_to_object(staticf+lang, lang+"_css_selectors.json")
            )

ENCODINGS = table_with_textfile(os.path.normpath(os.path.join("Constantes","encodings.txt")),3)


ELEMENTS = json_file_to_object(staticf,"html5_elements.json")
ATTRIBUTES = json_file_to_object(staticf,"html5_attributes.json")
GENERAL_ATTRIBUTES_LIST = json_file_to_object(staticf,"html5_general_attributes.json")

CSS_SELECTORS = json_file_to_object(staticf,"css_selectors.json")

(LOCAL_ELEMENTS, LOCAL_ATTRIBUTES,
 LOCAL_CSS_SELECTORS)               = load_local_strings("fr")


#-------------------------------------------------------------------------------------
if __name__ == '__main__':#essay
    pass
