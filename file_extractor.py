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
    ManqueAide="Il n'y a pas encore d'aide ici"
    LigneS=codecs.open(NomDuDocument,'r',"utf-8").readlines()
    Ligne=LigneS.pop(0).strip("\ufeff")#enlever éventuellement la signature utf-8
    i=-1
    while True:
        #print(Ligne.strip())
        if Ligne[0]!="#":
            Tableau.append([])
            i=i+1
            for cols in range(NbColonnes):
                try:
                    TexteCol=((Ligne.split(";"))[cols]).strip()
                except IndexError:
                    TexteCol=ManqueAide
                finally:
                    if not(TexteCol):
                        TexteCol=ManqueAide
                    Tableau[i].append(TexteCol)
        try:
            Ligne=LigneS.pop(0)
        except IndexError:
            break
    return Tableau



def dictionary_with_textfile(NomDuDocument,TailleMin=0,Dic=None):
    if Dic is None:
        Dic = {}
    #Vide="Il n'y a pas encore de liens entre l'élément et ses attributs spécifiques"
    Vide="Remplissez les Constantes!"
    LigneS=codecs.open(NomDuDocument,'r',"utf-8").readlines()
    Ligne=LigneS.pop(0).strip("\ufeff")#enlever éventuellement la signature utf-8
    i=-1
    while True:
        #print(Ligne.strip())
        if Ligne[0]!="#":
            Clef=Ligne.split(";")[0].strip()
            ValeurT=[]
            for attribut in ((Ligne.split(";")[1]).strip()).split(","):
                if attribut:
                    ValeurT.append(attribut.strip())
            if TailleMin>len(ValeurT):
                for manquants in range(TailleMin-len(ValeurT)):
                    ValeurT.append(Vide)
            Dic[Clef]=ValeurT
        try:
            Ligne=LigneS.pop(0)
        except IndexError:
            break
    return Dic

def dictionary_with_json_file(directory_name, file_name):
    option_file_path=os.path.normpath(os.path.join(directory_name,file_name))
    ManqueAide="Il n'y a pas encore d'aide ici"
    text_in_file=codecs.open(NomDuDocument,'r',"utf-8").read()
    #Ligne=LigneS.pop(0).strip("\ufeff")#enlever éventuellement la signature utf-8(BOM)
    Dic=json.loads(text_in_file)
    return Dic

#New extractors:s
def json_file_to_object(directory_name="", file_name=""):
    file_path=os.path.normpath(os.path.join(directory_name,file_name))
    return json.loads(codecs.open(file_path,'r',"utf-8").read())

def load_local_strings(lang="fr"):
    return (json_file_to_object("Constantes/"+lang, lang+"_html5_elements.json"),\
            json_file_to_object("Constantes/"+lang, lang+"_html5_attributes.json"))

ENCODINGS=table_with_textfile(os.path.normpath(os.path.join("Constantes","encodings.txt")),3)
Balises=table_with_textfile("Constantes/balises.txt",3)#obso new 1
GENERAL_ATTRIBUTES=table_with_textfile("Constantes/attributsall.txt",4)
LINK_ELEMENT_TO_ATTRIBUTES=dictionary_with_textfile("Constantes/Liens_Balises_Attributs_Spe.txt",0)#obso new1
#en cle, les balises et en valeurs, les n noms d'attributs
LINK_ATTRIBUTE_TO_VALUES=dictionary_with_textfile("Constantes/Attributs_Spe.txt",3)
#en cle, les attributs et en valeurs, le nomfr; valeur défaut;aide

#NEW
ELEMENTS=json_file_to_object("Constantes","html5_elements.json")
ATTRIBUTES=json_file_to_object("Constantes","html5_attributes.json")
GENERAL_ATTRIBUTES_LIST=json_file_to_object("Constantes","html5_general_attributes.json")

LOCAL_ELEMENTS, LOCAL_ATTRIBUTES=load_local_strings("fr")


#-------------------------------------------------------------------------------------
if __name__ == '__main__':#essay
    try:
        from tkinter import*#3.X
        from tkinter.ttk import Treeview
    except ImportError:
        from Tkinter import*#2.X
        from ttk import Treeview
    def update_Label_demo(*event):
        item=T.selection()[0]
        Info2['text']=str(T.item(item,'values'))
    def update_Label_demo2(*event):
        item2=T2.selection()[0]
        Info3['text']=str(T2.item(item2,'values'))
    def update_Label_demo3(*event):
        item3=T3.selection()[0]
        Info4['text']=str(T3.item(item3,'values'))
    def update_Label_demo4(*event):
        item4=T4.selection()[0]
        Info5['text']=str(T4.item(item4,'values'))
    root = Tk()
   
    T=Treeview(root,selectmode="browse")
    for nom,valeur,aide in Balises:
        if nom[0:3]=="---":
            NomMenu=nom[3::]
            id=T.insert("",'end',text=NomMenu)
            continue
        T.insert(id,'end', text=nom,values=(nom,valeur,aide))
    T.grid(row=0,column=0)
    T.bind("<Double-Button-1>",update_Label_demo)
    Info2=Label(root,text='0',bg='white',font="Arial 15 bold",fg='black',wrap=400)
    Info2.grid(row=1,column=0)#Sortie
    
    T2=Treeview(root,selectmode="browse")
    for Attribut, defaut,aide,NomFr in GENERAL_ATTRIBUTES:
        T2.insert("",'end', text=NomFr,values=(Attribut, defaut,aide,NomFr))
    T2.grid(row=0,column=1)
    T2.bind("<Double-Button-1>",update_Label_demo2)
    Info3=Label(root,text='0',bg='white',font="Arial 15 bold",fg='black',wrap=400)
    Info3.grid(row=1,column=1)#Sortie

    T3=Treeview(root,selectmode="browse")
    for cles in LINK_ELEMENT_TO_ATTRIBUTES:
        id=T3.insert("",'end',text=cles)
        for ele in LINK_ELEMENT_TO_ATTRIBUTES[cles]:
            T3.insert(id,'end', text=ele,values=(ele))
    T3.grid(row=2,column=0)
    T3.bind("<Double-Button-1>",update_Label_demo3)
    Info4=Label(root,text='0',bg='white',font="Arial 15 bold",fg='black',wrap=400)
    Info4.grid(row=3,column=0)#Sortie

    T4=Treeview(root,selectmode="browse")
    for cles in LINK_ATTRIBUTE_TO_VALUES:
        id=T4.insert("",'end',text=cles)
        for ele in LINK_ATTRIBUTE_TO_VALUES[cles]:
            T4.insert(id,'end', text=ele,values=(ele))
    T4.grid(row=2,column=1)
    T4.bind("<Double-Button-1>",update_Label_demo4)
    Info5=Label(root,text='0',bg='white',font="Arial 15 bold",fg='black',wrap=400)
    Info5.grid(row=3,column=1)#Sortie

    root.mainloop()
