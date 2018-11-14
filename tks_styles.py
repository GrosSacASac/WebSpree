#!/usr/bin/python
#-*-coding:utf-8*

#tks_styles.py
#Role: describes how widgets should look like in the main app
#Static data now but it may change 


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

######----Le style-----######
Po='Arial 12 bold'#


#Entrées
ENTRY_FONT='CourrierNewNormal 11'#Pas utilisé
ENTRY_COLOR='black'#Couleur symbolique
ENTRY_BACK_COLOR='white'#Couleur de fond
ENTRY_STYLE={'fg':ENTRY_COLOR,'bg':ENTRY_BACK_COLOR,'font':ENTRY_FONT}

#Label
PoLabel='Arial 14 bold'
CLabel='#397106'#Couleur symbolique
CFLabel='#e1e1e1'#Couleur de fond
LABEL_STYLE={'font':PoLabel,'fg':CLabel,'bg':CFLabel}

#Label d'aide
HELP_LABEL_FONT='Times 12'
HELP_LABEL_COLOR='black'#Couleur symbolique
CFA='#e1e1e1'#Couleur de fond
JustificationA='left'
HELP_LABEL_STYLE={'font':HELP_LABEL_FONT,'fg':HELP_LABEL_COLOR,'bg':CFA,'justify':JustificationA}

#RadioButton
PoRadioButton='Arial 12 bold'
CRadioButton='dark blue'#Couleur symbolique
CFRadioButton=CFLabel#Couleur de fond
RADIOBUTTON_STYLE={'font':PoRadioButton,'fg':CRadioButton,'bg':CFRadioButton}

#Listbox
PoListbox='Arial 10'
CListbox='black'#Couleur symbolique
CFListbox='white'#Couleur de fond
LISTBOX_STYLE={'font':PoListbox,'fg':CListbox,'bg':CFListbox}

#tkk Treeview
#TREEVIEW_STYLE1={'selectmode':'browse','height':25}
#In every widget creation I insert the corresponding widget-style which is  a dictionnary as you can see
#after the master or parent. But this doesn t work with ttk widgets. Here s the error:
#TTK.Treeview.__init__(self,master,kw)
#TypeError: __init__() takes from 1 to 2 positional arguments but 3 were given
#solution 1: take use of the style object
# mystyle=TTK.Style()
#solution 2: Find a trick to send (master,style_dic,other) as (master,kw)
#no importance for now ,just copy parameter 1 by 1 in Treeview init

#Label Frame
PoFrame='Arial 13'
CFrame='black'#Couleur symbolique
FRAME_BACK_COLOR=CFLabel#Couleur de fond
EppaisseurCadres=5
StyleContour='ridge'
FRAME_STYLE={'font':PoFrame,'fg':CFrame,'bg':FRAME_BACK_COLOR,'borderwidth':EppaisseurCadres}

#Frame
FRAME_STYLE_2={'bg':FRAME_BACK_COLOR,'borderwidth':EppaisseurCadres}
COLOURS_A=["#ffd0d0","#ffffd0","#d0ffd0","#d0d0ff", "#af2222"]#eye friendly
COLOURS_B=["#ffe2e2","#ffffe2","#e2ffe2","#e2e2ff", "#af2222"]#light

#todo let user choose his own set of coulours

#Fen
WINDOW_BACK_COLOR=FRAME_BACK_COLOR
MAIN_TITLE="WebSpree"
MAIN_TITLE_2="WebSpree*"
LOGO1_PATH="Images/icos/AutoHLogo.ico"
