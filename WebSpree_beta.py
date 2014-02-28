#!/usr/bin/python
#-*-coding:utf-8*

#WebSpree.py
#Role: main file

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
try:#3.X
    from tkinter import*
    import tkinter.ttk  as TTK
    import tkinter.filedialog as FileDialog
    import tkinter.messagebox as MessageBox
    import tkinter.font as TKFonts
except ImportError:#2.X
    from Tkinter import*
    import ttk as TTK
    import tkFileDialog as FileDialog
    import tkMessageBox as MessageBox
    import tkFont as TKFonts
    #from math import abs


import webbrowser
import os
import time
import platform

from Options_class import *
from log_writer import log_writer
from Text__classes import*
from file_extractor import*
from tks_styles import*

#from tks_widgets_1 import*

def _(l_string):
    #print("local language: "+l_string)
    return l_string

def get_time(time_modell="%d/%m/%Y\n%H:%M:%S"):
    return time.strftime(time_modell)

class GraphicalUserInterfaceTk(Tk):
    """tkinter interface for WebSpree.

graphic user interface, view and controller
begin: methods that changes something important
middle: intern methods
end: lesser important methods with visual effects but not much more"""

#methods that changes something important --------------###############################
    
    def __init__(self,model):
        Tk.__init__(self)
        self.model=model
        self.title(MAIN_TITLE)
        #self.attributes('-fullscreen', 1)#, '-topmost', 1)fullscreen #doesnt exist everywhere
        #self.geometry('1700x600+0+0')#static size is bad, it doesn t adapt
        self.configure(bd=1,bg=WINDOW_BACK_COLOR)
        #self.iconbitmap(LOGO1_PATH)#problems here, icon should be insert when freezing the app not here
        self.protocol("WM_DELETE_WINDOW", self.intercept_close)

        self.bind("<Control-Shift-T>",self.save_file_to_test_control)
        self.bind("<Control-Shift-S>",self._save_file_dialog)
        self.bind("<Control-s>",self.model.save_html_file)
        self.bind("<Control-o>",self.edit_file_dialog)
        self.bind("<Control-n>",self.new_file)
        

        self.bind("<Control-plus>",self.change_size)
        self.bind("<Control-minus>",self.change_size)
        self.bind("<Control-0>",self.change_size)
        
        
        self.HTML5_PHOTO_ICO = PhotoImage(file="images/icos/HTML5_Badge_32.gif")#image is ready for tkinter
        self.CSS3_PHOTO_ICO = PhotoImage(file="images/icos/CSS3_Badge_32.gif")#image is ready for tkinter
        self.JS_PHOTO_ICO = PhotoImage(file="images/icos/js32.gif")
        intern_root=Frame(self)#this is almost the root

        
        #print(mystyle.theme_names())
        #mystyle.theme_use('clam')
        self.group_app_tabs=TTK.Notebook(intern_root)#this contains every tab,html,css,...
        self.group_app_tabs.enable_traversal()
        self.current_font=TKFonts.Font(family='helvetica', size=-12)
        mystyle=TTK.Style()
        mystyle.configure('.',font=self.current_font)
        
        self.frame_of_frames_html=Frame(self.group_app_tabs)#html frame
        self.frame_of_frames_css=Frame(self.group_app_tabs)#css frame
        self.frame_of_frames_js=Frame(self.group_app_tabs)#js frame
        
        self.group_app_tabs.add(self.frame_of_frames_html,text="HTML",image=self.HTML5_PHOTO_ICO,compound='left',underline=0)
        self.group_app_tabs.add(self.frame_of_frames_css,text="CSS",image=self.CSS3_PHOTO_ICO,compound='left',underline=0)
        self.group_app_tabs.add(self.frame_of_frames_js,text="JavaScript",image=self.JS_PHOTO_ICO,compound='left',underline=0)
        Label(self.frame_of_frames_js,text='coming soon ...').pack()
        Label(self.frame_of_frames_css,text='coming soon ...').pack()
        
        #-HTML- Frames
        #elements and help
        frame_element_master=Frame(self.frame_of_frames_html,FRAME_STYLE_2,bg=COLOURS_A[0])
        self.frame_element_notebook=TTK.Notebook(frame_element_master)
        self.frame_element_notebook.grid(row=0,column=0,sticky='nsw')
        
        self.frame_element=Frame(self.frame_element_notebook,FRAME_STYLE_2)#elements
        self.frame_element_help=Frame(self.frame_element_notebook,FRAME_STYLE_2)#help elements
        self.frame_element_notebook.add(self.frame_element,text=_("1. Balises"),sticky='swen')
        self.frame_element_notebook.add(self.frame_element_help,text=_("Aides"),sticky='swen')
        
        
        #attributes and help
        frame_attribute_master=Frame(self.frame_of_frames_html,FRAME_STYLE_2,bg=COLOURS_A[1])#attributes
        self.frame_attribute_notebook=TTK.Notebook(frame_attribute_master)
        self.frame_attribute_notebook.grid(row=0,column=0,sticky='nsw')
        
        self.frame_attribute=Frame(self.frame_attribute_notebook,FRAME_STYLE_2)#attributes
        self.frame_attribute_help=Frame(self.frame_attribute_notebook,FRAME_STYLE_2)#help attributes
        self.frame_attribute_notebook.add(self.frame_attribute,text=_("2. Choisir les attributs"),sticky='swen')
        self.frame_attribute_notebook.add(self.frame_attribute_help,text=_("Aides"),sticky='swen')

        
        frame_2_user_input=LabelFrame(self.frame_of_frames_html, FRAME_STYLE,text=_("3. Saisir Contenu"),bg=COLOURS_A[2])#Buttons et saisies
        frame_3_html_box=LabelFrame(self.frame_of_frames_html, FRAME_STYLE,text=_("4.Code HTML"),bg=COLOURS_A[3])#Preview
        self.autoclose_element_check_variable=BooleanVar(value=True)
        self.insertion_tk_var=BooleanVar(value=False)
        #frame_element_notebook.add(frame_attribute,text="Attributs")


        
        self.elements_in_treeviews_lift = TTK.Scrollbar(self.frame_element)
        self.elements_in_treeview=TTK.Treeview(self.frame_element,selectmode='browse',columns=("local name","element"),height=21,\
                                             yscrollcommand=self.elements_in_treeviews_lift.set,padding=0,takefocus=True,\
                                             displaycolumns=(0))#,show='tree'
        self.elements_in_treeview.heading("#0",text=_("Traduction"))
        self.elements_in_treeview.heading("local name",text=_("Code"))
        self.elements_in_treeview.bind('<<TreeviewSelect>>',self.update_choice1)
        self.elements_in_treeviews_lift.config(command=self.elements_in_treeview.yview)
        #_List of elements:
        for couple in ELEMENTS:
            function=self.elements_in_treeview.insert("",'end',text=couple[0])
            for ele in couple[1]:
                self.elements_in_treeview.insert(function,'end', text=LOCAL_ELEMENTS[ele]["translation"],value=ele)

        self.elements_in_treeview.grid(row=0,column=0,columnspan=2,sticky='nsw')#sticky remplit colle l'objet vers le n w e ou sud
        self.elements_in_treeviews_lift.grid(row=0,column=2,sticky='nsw')#sticky remplit colle l'objet vers le n w e ou sud

        #Help
        self.element_help_and_tip=Label(self.frame_element,HELP_LABEL_STYLE, text=_("Seléctionnez une balise pour avoir de l'aide..."), wrap=400,anchor='nw',fg='#2220dd')
        self.element_help_and_tip.grid(row=1,column=0,columnspan=3,sticky='nsw')
        self.element_help_and_tip.bind("<ButtonRelease-1>", self.see_more_help_and_details)
        self.more_help_2=Button(self.frame_attribute, text=_("Plus d'aide"),anchor='center')
        self.more_help_2.grid(row=2,column=0,sticky='nswe',columnspan=2)
        self.more_help_2.bind("<ButtonRelease-1>", self.see_more_help_and_details)
        self.more_help=Button(self.frame_element, text=_("Plus d'aide"),anchor='center')
        self.more_help.grid(row=2,column=0,sticky='nswe',columnspan=3)
        self.more_help.bind("<ButtonRelease-1>", self.see_more_help_and_details)
        self.leave_help=Button(self.frame_element_help, text=_("Quitter l'aide"),anchor='center')
        self.leave_help.grid(row=1,column=0,sticky='nswe')
        self.leave_help.bind("<ButtonRelease-1>", self.see_more_help_and_details)
        self.leave_help_2=Button(self.frame_attribute_help, text=_("Quitter l'aide"),anchor='center')
        self.leave_help_2.grid(row=1,column=0,sticky='nswe')
        self.leave_help_2.bind("<ButtonRelease-1>", self.see_more_help_and_details)

        self.help_in_treeview_elements=TTK.Treeview(self.frame_element_help,selectmode='browse',columns=("key","value"),height=21,\
                                                    padding=0,takefocus=True,displaycolumns=(0,1))#,show='tree'
        self.help_in_treeview_elements.grid(row=0,column=0,sticky='nswe')
        self.help_in_treeview_elements.column('#0', width=0)#take away the icon column
        self.help_in_treeview_elements.heading("key",text=_("Propriété"))
        self.help_in_treeview_elements.heading("value",text=_("Valeur"))
        self.help_in_treeview_elements.insert("", 'end', iid="description", values=(_("description"),_("Ancre ou lien")))
        self.help_in_treeview_elements.insert("description", 'end', iid="description_full", values=(_("description"),_("Ancre ou lien...")))

        #HyperW3C=Hyperlien(master,"www.w3c.org",LABEL_STYLE,text="Site du World Wide Web Consortium",justify='left')
        #HyperW3C.pack(side='left',fill='y')

        

        #_List of attributes:
        
        self.general_attributes_treeview=TTK.Treeview(self.frame_attribute,selectmode='browse',height=21,columns=("real","local"),displaycolumns=(1),show='headings')
        self.general_attributes_treeview.heading("local",text=_("Général"))
        self.general_attributes_treeview.grid(row=0,column=0,sticky='w')
        for general_attribute in GENERAL_ATTRIBUTES_LIST:
            self.general_attributes_treeview.insert("",'end',values=(general_attribute,LOCAL_ATTRIBUTES[general_attribute]["translation"]))
        self.general_attributes_treeview.bind('<<TreeviewSelect>>',self.add_attribute,"")
        
        
        self.specific_attributes_treeview=TTK.Treeview(self.frame_attribute,selectmode='browse',height=21,columns=("real","local"),displaycolumns=(1),show='headings')
        self.specific_attributes_treeview.heading("local",text=_("Spécifique"))
        #self.specific_attributes_treeview.tag_configure("specific_attribute")
        self.specific_attributes_treeview.grid(row=0,column=1,sticky='w')
        self.specific_attributes_treeview.bind('<<TreeviewSelect>>',self.add_attribute,"")

        self.attribute_help_and_tip=Label(self.frame_attribute,HELP_LABEL_STYLE, text=_("Seléctionnez un attribut pour avoir de l'aide"), wrap=400,anchor='nw',fg='#2220dd')
        self.attribute_help_and_tip.grid(row=1,column=0,columnspan=2,sticky='nsw')
        self.attribute_help_and_tip.bind("<ButtonRelease-1>", self.see_more_help_and_details)
        
        
        

        help_label_for_content=Label(frame_2_user_input,LABEL_STYLE, text=_("Ecrivez le contenu"))
        help_label_for_content.grid(row=0,column=0,sticky='nw')
        help_label_for_attribute=Label(frame_2_user_input,LABEL_STYLE, text=_("Placez les attributs"))
        help_label_for_attribute.grid(row=2,column=0,sticky='nw')

        self.content_area_form=Text(frame_2_user_input,ENTRY_STYLE,width=20,height=10)
        self.content_area_form.grid(row=1,column=0,sticky='nw')
        self.attribute_area_form=Text(frame_2_user_input,ENTRY_STYLE,width=16,height=10)
        self.attribute_area_form.grid(row=3,column=0,sticky='nw')
        #self.content_area_form.bind('<KeyRelease>',write_in_real_time)

        self.confirm_add_button=TTK.Button(frame_2_user_input, text=_("Confirmer"),command=self.confirm_write)
        self.confirm_add_button.grid(row=4,column=0,sticky='nw')

        self.close_last_element_button=TTK.Button(frame_2_user_input, text=_("Fermer la dernière\nbalise ouverte"), command=self.confirm_close_element)
        self.close_last_element_button.grid(row=5,column=0,sticky='nw')

        auto_close_checkbutton=TTK.Checkbutton(frame_2_user_input, text=_("Auto Fermeture"),variable=self.autoclose_element_check_variable )
        auto_close_checkbutton.grid(row=6,column=0,sticky='nw')


        self.main_scrollbar = TTK.Scrollbar(frame_3_html_box)
        self.main_text_field=Text(frame_3_html_box,yscrollcommand=self.main_scrollbar.set,state='normal',height=35,undo=True,font=self.current_font)#,bg='black',fg='white')
        self.main_scrollbar.config(command=self.main_text_field.yview)
        self.main_scrollbar.grid(row=0,column=1,sticky='nsw')
        self.main_text_field.grid(row=0,column=0,sticky='nsw')
        #Indicateur = InformationBubble(parent=main_text_field,texte="Vous pouvez éditer ici directement si vous ça vous chante")

        self.main_text_field.bind("<KeyRelease>", self.so_you_decided_to_write_html_directly)

        frame_3_html_box_1=LabelFrame(frame_3_html_box, text="Outils", relief='ridge', borderwidth=1,bg=WINDOW_BACK_COLOR)#
        RadioFin=TTK.Radiobutton(frame_3_html_box_1, text=_("Ecrire à la fin"),variable=self.insertion_tk_var, value=False, command=self.switch_writing_place )
        RadioFin.grid(row=0,column=0,sticky='nw')
        RadioIns=TTK.Radiobutton(frame_3_html_box_1, text=_("Insèrer au curseur"),variable=self.insertion_tk_var, value=True,command=self.switch_writing_place )
        RadioIns.grid(row=1,column=0,sticky='nw')

        self.insertion_cursor=Scale(frame_3_html_box_1,resolution=1, from_=0, to=16, tickinterval=2,length=200,state='active'
                       ,orient='horizontal', relief='groove', showvalue=1,sliderlength=30, troughcolor='green')
        frame_3_html_box_1.grid(row=1,column=0,sticky='e')
        
        if self.model.get_option("developper_interface"):
            leave_button=TTK.Button(frame_3_html_box, text="Quitter",command=self._end )
            leave_button.grid(row=2,column=0,sticky='')

        


        ######----Menus-----######
        FILEMENU={}
        FILEMENU["name"]=_("Fichier")
        FILEMENU["command"]=[{'label':_("Nouveau [Ctrl+N]"),'command':self.new_file},\
                             {'label':_("Ouvrir [Ctrl+O]"),'command':self.edit_file_dialog},\
                             {'label':_("Enregistrer [Ctrl+S]"),'command':lambda: self.model.save_html_file()},\
                             {'label':_("Enregistrer sous[Ctrl+Shift+S]"),'command':lambda: self._save_file_dialog()},\
                             {'label':_("Essayer ! [Ctrl+Shift+T]"),'command':lambda: self.save_file_to_test_control()}]
        FILEMENU["radiobutton"]=[]

        EDITMENU={}
        EDITMENU["name"]=_("Edition")
        EDITMENU["command"]=[]
        EDITMENU["radiobutton"]=[]

        VIEWMENU={}
        VIEWMENU["name"]=_("Vue")
        VIEWMENU["command"]=[{'label':_("Pas de Zoom[Ctrl+0]"),'command':lambda: self.change_size("0")},\
                             {'label':_("Zoom +[Ctrl+ +]"),'command':lambda: self.change_size("plus")},\
                             {'label':_("Zoom -[Ctrl+ -]"),'command':lambda: self.change_size("minus")}]
        VIEWMENU["radiobutton"]=[]

        self.translate_html_level_tk_var=IntVar(value=self.model.get_option("translate_html_level"))
        if self.model.get_option("indent_style")=="\t":
            self.indent_size_tk_var=IntVar(value=-1)
        else:
            self.indent_size_tk_var=IntVar(value=self.model.get_option("indent_size"))
        OPTIONMENU={}
        OPTIONMENU["name"]=_("Options")
        OPTIONMENU["command"]=[]
        OPTIONMENU["radiobutton"]=[{'label':_("Remplacer tout caractère spécial"),\
                                    'command':self.set_translation,'value':10,"variable":self.translate_html_level_tk_var},\
                                   {'label':_("Remplacer le minimum"),\
                                    'command':self.set_translation,'value':1,"variable":self.translate_html_level_tk_var},\
                                   {'label':_("Remplacer aucun caractère spécial"),\
                                    'command':self.set_translation,'value':0,"variable":self.translate_html_level_tk_var},\
                                   {'label':_("Indenter avec 2 espaces"),\
                                    'command':self.set_indent_size,'value':2,"variable":self.indent_size_tk_var},\
                                   {'label':_("Indenter avec 3 espaces"),\
                                    'command':self.set_indent_size,'value':3,"variable":self.indent_size_tk_var},\
                                   {'label':_("Indenter avec 4 espaces"),\
                                    'command':self.set_indent_size,'value':4,"variable":self.indent_size_tk_var},\
                                   {'label':_("Indenter avec 8 espaces"),\
                                    'command':self.set_indent_size,'value':8,"variable":self.indent_size_tk_var},\
                                   {'label':_("Indenter avec des tabulations"),\
                                    'command':self.set_indent_size,'value':-1,"variable":self.indent_size_tk_var}]
        #([{'label':_("Compact"),'command':self.change_mapping,'value':True,"variable":self.small_layout},
                                    #{'label':_("Etendu"),'command':self.change_mapping,'value':False,"variable":self.small_layout}])
        HELPMENU={}
        HELPMENU["name"]=_("Aide")
        HELPMENU["command"]=([
                              {'label':_("Lisez_moi"),'command':lambda: webbrowser.open("Documentation\Lisez_moi.html",new=2)},
                              {'label':_("To-do"),'command':lambda: webbrowser.open("Documentation\To_do.html",new=2)},
                              {'label':_("Patch notes"),'command':lambda: webbrowser.open("Documentation\Patch_Notes.html",new=2)},
                              {'label':_("Version"),'command':lambda: webbrowser.open("Documentation\Version.html",new=2)},
                              {'label':_("LICENSE"),'command':lambda: self.view_license(already_accepted=True)}])
        HELPMENU["radiobutton"]=[]
        #start file doesn t work on every platform use webbrowser
        ALL_MENUS=[FILEMENU,EDITMENU,VIEWMENU, OPTIONMENU, HELPMENU]
        top=self.winfo_toplevel()#for macs menu to render as users are used to
        self.Menus_tk=Menu(top)
        top['menu']=self.Menus_tk
        sub_menu_list=[]
        #All_MENU_ITEM_OPTION={'activebackground':"blue"}
        
        #This loop creates the menus described just before. from dicts to menus of menus
        for index,submenu in enumerate(ALL_MENUS):
            sub_menu_list.append(Menu(self.Menus_tk,tearoff=0))#,tearoff=0 disables the popopable menu item with the dottet bar
            self.Menus_tk.add_cascade(label=submenu["name"], menu=sub_menu_list[index],underline=0)
            for command_ in submenu["command"]:
                sub_menu_list[len(sub_menu_list)-1].add_command(label=command_["label"], command=command_["command"],activebackground="blue")
            for radiobutton_ in submenu["radiobutton"]:
                sub_menu_list[len(sub_menu_list)-1].add_radiobutton(label=radiobutton_["label"], command=radiobutton_["command"],\
                                                                    variable=radiobutton_["variable"],value=radiobutton_["value"],activebackground="blue")


    
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        intern_root.grid(row=0,column=0,sticky='snew')
        intern_root.columnconfigure(0,weight=2)
        intern_root.rowconfigure(0,weight=2)

        self.group_app_tabs.grid(row=0,column=0,sticky='nswe')
        self.group_app_tabs.columnconfigure(0,weight=3)
        self.group_app_tabs.rowconfigure(0,weight=3)



        
        frame_element_master.grid(row=0,column=0,sticky='nsw')
        frame_attribute_master.grid(row=0,column=1,sticky='nsw')
        frame_2_user_input.grid(row=0,column=2,sticky='nsw')
        frame_3_html_box.grid(row=0,column=3,sticky='nsw',rowspan=2)
        #self.grid_columnconfigure(0,weight=0)
    def _prepare_new_session(self):#view
        self.Contexte=Toplevel(self,bd=1,bg=WINDOW_BACK_COLOR)
        self.Contexte.title(_("Commencer"))
        self.Contexte.geometry('700x600+200+200')
        self.Contexte.grab_set()
        self.Contexte.focus_set()
        self.Contexte.focus_force()#force focus
        
        frame_title=LabelFrame(self.Contexte, FRAME_STYLE,text=_("Titre du document"))
        self.title_tk_var=StringVar(value=self.model.get_option("last_html_document_title"))
        Entry(frame_title,ENTRY_STYLE,textvariable=self.title_tk_var).pack()

        
        self.new_doc_radiobutton_var=IntVar(value=0)
        frame_where_to_start=LabelFrame(self.Contexte, FRAME_STYLE,text=_("Document"))
        new_doc_radiobutton=TTK.Radiobutton(frame_where_to_start, text=_("Commencer un nouveau document standard"),value=0,variable=self.new_doc_radiobutton_var)
        new_doc_radiobutton.pack(anchor="w")
        new_blank_doc_radiobutton=TTK.Radiobutton(frame_where_to_start,text=_("Commencer un nouveau document vierge"), value=-1,variable=self.new_doc_radiobutton_var)
        new_blank_doc_radiobutton.pack(anchor="w")
        edit_doc_radiobutton=TTK.Radiobutton(frame_where_to_start, text=_("Modifier un document existant"),value=1,variable=self.new_doc_radiobutton_var)
        edit_doc_radiobutton.pack(anchor="w")
        
        #to do change this barbar method to control encoding properly
        self._which_encoding_var=StringVar(value=self.model.current_text_html.get_encoding()+";"+self.model.current_text_html.get_w3c_encoding())
        frame_which_encoding=LabelFrame(self.Contexte, FRAME_STYLE,text=_("Encodage(beta)"))
        for encotext,pyencodings,standardenco in ENCODINGS:
            encoding_radiobutton=TTK.Radiobutton(frame_which_encoding, text=encotext,value=pyencodings+";"+standardenco,variable=self._which_encoding_var)
            encoding_radiobutton.pack(anchor='w')

        self.indent_style_tk_var=StringVar(value=self.model.get_option("indent_style"))
        self.indent_size_tk_var_2=IntVar(value=self.model.get_option("indent_size"))
        frame_indentation=LabelFrame(self.Contexte, FRAME_STYLE,text=_("Indentation"))
        indent_style_radiobutton=TTK.Radiobutton(frame_indentation, text=_("Espaces"),value=" ",variable=self.indent_style_tk_var)
        indent_style_radiobutton.pack(anchor='w')
        indent_style_radiobutton2=TTK.Radiobutton(frame_indentation, text=_("Tabulations"),value="\t",variable=self.indent_style_tk_var)
        indent_style_radiobutton2.pack(anchor='w')
        for i in range(1,9):
            indent_size_radiobutton=TTK.Radiobutton(frame_indentation, text=str(i),value=i,variable=self.indent_size_tk_var_2)
            indent_size_radiobutton.pack(anchor='w')

        frame_submit=LabelFrame(self.Contexte, FRAME_STYLE,text=_("Valider"))
        accept_and_begin=TTK.Button(frame_submit, text=_("Confirmer[Entrée]"), command=self._confirm_new_session)
        accept_and_begin.grid(row=0,column=0)
        cancel=TTK.Button(frame_submit, text=_("Annuler"), command=self.Contexte.destroy)
        cancel.grid(row=1,column=0)

        
        frame_title.grid(row=0,column=0,sticky='w')
        frame_where_to_start.grid(row=1,column=0,sticky='nswe')
        frame_which_encoding.grid(row=1,column=1,sticky='nswe')
        frame_indentation.grid(row=2,column=0,sticky='nswe')
        frame_submit.grid(row=2,column=1,sticky='nswe')


        self.Contexte.bind("<Return>",self._confirm_new_session)

        
    def _confirm_new_session(self,*event):#controller
        self.model.set_option("last_html_document_title",self.title_tk_var.get())
        self.model.set_option("indent_style",self.indent_style_tk_var.get())
        if self.indent_style_tk_var.get()=="\t":
            size=1
            self.indent_size_tk_var.set(-1)
        else:
            size=self.indent_size_tk_var_2.get()
            self.indent_size_tk_var.set(size)
        self.model.set_option("indent_size",size)
            
        self.model.start_mod=self.new_doc_radiobutton_var.get()
        self.model._start_new_session()

        #this should be passe via start new session method-------
        new_encoding_py , new_w3c_encoding = (self._which_encoding_var.get().split(";"))
        self.model.current_text_html.set_encoding(new_encoding_py)
        self.model.current_text_html.set_w3c_encoding(new_w3c_encoding)
        #this should be passe via start new session method-------
        
        if (self.model.current_text_html.element_still_not_closed_list):
            self.close_last_element_button['state']='normal'
        else:
            self.close_last_element_button['state']='disabled'
        self.Contexte.destroy()
        
    def add_attribute(self,event):
        selected_item_id=event.widget.selection()[0]
        attribute=(event.widget.item(selected_item_id,'value'))[0]
        attribute_details=ATTRIBUTES[attribute]
        attribute_local_details=LOCAL_ATTRIBUTES[attribute]
        if not attribute in self.attribute_area_form.get('1.0', 'end'+'-1c'):
            self.attribute_area_form.insert('end',"{}=\"{}\"\n".format(attribute,attribute_details["default_value"]))
            
        self.attribute_help_and_tip['text']=(_("Attribut {}:\n{}").\
                                             format(attribute,attribute_local_details["description"]))[0:60]+"..."
        
    def update_choice1(self,*event):
        selected_item_id=self.elements_in_treeview.selection()[0]
        if not self.elements_in_treeview.get_children(selected_item_id):#we do nothing if user opened a folder(who has childs)
            element_tag=(self.elements_in_treeview.item(selected_item_id,'value'))[0]
            self.model.current_text_html.last_selected_element=element_tag
            

            previous=self.content_area_form['state']
            self.content_area_form['state']='normal'
            self.content_area_form.delete('1.0', 'end'+'-1c')#Mettre en option
            self.content_area_form['state']=previous
            self.attribute_area_form.delete('1.0', 'end'+'-1c')
            
            
            self.elements_in_treeview.heading("local name",text=_("Code: ")+element_tag)
            self.element_help_and_tip['text']=(("<%s>\n%s") %\
                                                              (element_tag,LOCAL_ELEMENTS[element_tag]["description"]))[0:60]+"..."
            
            _i=self.specific_attributes_treeview.get_children()
            for item in _i:
                self.specific_attributes_treeview.delete(item)#delete all items in specific_attributes_treeview before
            for couple in ELEMENTS:
                for ele in couple[1]:
                    if ele==element_tag:
                        self.model.current_text_html.last_selected_element_is_void=couple[1][ele]["void"]
                        self.content_area_form['state']='normal'
                        if self.model.current_text_html.last_selected_element_is_void:
                            self.content_area_form.insert('end',_("Les éléments vides n'ont pas de contenu"))
                            self.content_area_form['state']='disabled'
                        #todo add must attributes somewhere
                        for attribute in couple[1][ele]["specific_attributes"]:
                                self.specific_attributes_treeview.insert("",'end',values=(attribute,LOCAL_ATTRIBUTES[attribute]["translation"]))#,tags="specific_attribute")
                                
                        break


                
    def confirm_write(self):
        element_tag=self.model.current_text_html.last_selected_element
        attributes_with_spaces=self.attribute_area_form.get('1.0', 'end'+'-1c').strip()
        if attributes_with_spaces!="":
            attributes_with_spaces=" "+attributes_with_spaces.replace("\n"," ")
        
        if self.model.current_text_html.last_selected_element_is_void:
            text_to_add=self.model.current_text_html.add_indent_and_line(self.model.current_text_html.open_close_void_element(element_tag,attributes_with_spaces))
        else:
            text_to_add=self.model.current_text_html.add_indent_and_line(self.model.current_text_html.open_element(element_tag, attributes_with_spaces))
            text_to_add+=self.model.current_text_html.add_indent_and_line(self.content_area_form.get('1.0', 'end'+'-1c'))
            if self.autoclose_element_check_variable.get():
                text_to_add+=self.model.current_text_html.add_indent_and_line(self.model.current_text_html.close_element())
        self.model.current_text_html.add_to_text(text_to_add)
        self.tk_copy_text(self.model.current_text_html)
        
        if not self.model.current_text_html.element_still_not_closed_list:
            self.close_last_element_button['state']='disabled'
        else:
            self.close_last_element_button['state']='active'###
    #todo here put the cursor at the end of what is just added

    
            
    def so_you_decided_to_write_html_directly(self,event):
        if self.model.current_text_html.text!=self.main_text_field.get('1.0', 'end'+'-1c'):
            self.model.current_text_html.text=self.main_text_field.get('1.0', 'end'+'-1c')
            
    def switch_writing_place(self):#todo redesign this old thing
        if self.insertion_tk_var.get():
            line_before=self.main_text_field.get('insert'+'-1l', 'insert')
            #CTabulations=line_before.count(indent_var_changed)
            self.insertion_cursor.grid(row=2,column=0,sticky='nw')
            #self.insertion_cursor.set(CTabulations)            
            before_cursor_text=self.main_text_field.get('1.0', 'insert')
            self.model.current_text_html.insertion=len(before_cursor_text)
        else:
            self.insertion_cursor.grid_forget()
            self.model.current_text_html.insertion=None
        
                   
##    def write_in_real_time(self,*event):#TODO
##        try:
##            self.main_text_field.delete("hi")
##        except IndexError:
##            pass
        
    def confirm_close_element(self):
        if self.model.current_text_html.element_still_not_closed_list:#there is something to close
            text_to_add=self.model.current_text_html.add_indent_and_line(self.model.current_text_html.close_element())
            self.model.current_text_html.add_to_text(text_to_add)
            self.tk_copy_text(self.model.current_text_html)
        else:
            pass
        if self.model.current_text_html.element_still_not_closed_list:#there is still something to close
            pass
        else:
            self.close_last_element_button['state']='disabled'
        
#Intern methods called by other or by changing an option --------------###############################
            
    def new_file(self,*event):
        if self.model.current_text_html.is_saved():
            self._prepare_new_session()
        else:
            Reponse=MessageBox.askyesnocancel(title=_("Attention"), message=_("Voulez vous sauvegarder avant de commencer un nouveau document ?"))#True False ou None 
            if Reponse:                                                      # Oui
                if self.model.save_html_file():
                    self._mark_as_not_modified()
                    self._prepare_new_session()
            elif Reponse is None: pass                             # Annuler
            else :
                self._prepare_new_session()                       #Non
    
    def edit_file_dialog(self,*event):
        file_path=FileDialog.askopenfilename(defaultextension=".html",filetypes=[("HyperText Mark-Up Language file", "*.html" ),])
        #to-do double check if the file exist here because it could have been deleted during the time the user chooses the file
        if file_path:
            self.model.edit_file(file_path)


    def _save_file_dialog(self,*event):
        NomDuFichier=FileDialog.asksaveasfilename(defaultextension=".html",filetypes=[("HyperText Mark-Up Language file", "*.html" ),],\
                                                  initialfile=self.model.get_option("last_html_document_title"))
        
        if NomDuFichier != "":
            if self.model._save_html_file_as(NomDuFichier):
                self._mark_as_not_modified()
                return True
        return False
    
    def save_file_to_test_control(self,*event):#Try with CTRL+Shift+T
        self.model.save_file_totest()
        
    def _start(self):
        if not self.model.get_option("license_accepted_and_read"):
            self.view_license(already_accepted=False)
        log_writer("width",self.winfo_screenwidth())
        log_writer("height",self.winfo_screenheight())
        self.mainloop()

    def _end(self):
        self.destroy()
        
    def tk_copy_text(self,text_to_copy):
        self._mark_as_modified()
        self.main_text_field.delete('1.0', 'end'+'-1c')
        self.main_text_field.insert('end',text_to_copy)
        self.main_text_field.yview("moveto","1.0")
        
    def set_translation(self):
        self.model.set_option("translate_html_level",self.translate_html_level_tk_var.get())

    def set_indent_size(self):
        if self.indent_size_tk_var.get()== -1:
            self.model.set_option("indent_size",1)
            self.model.set_option("indent_style","\t")
        else:
            self.model.set_option("indent_size",self.indent_size_tk_var.get())
            self.model.set_option("indent_style"," ")
        
    

    def intercept_close(self): # intercept_close
        try:
            if not self.model.current_text_html.is_saved():
                Reponse=MessageBox.askyesnocancel(title=_("Attention"), message=_("Voulez vous sauvegarder avant de quitter ?"))#True False ou None 
                if Reponse:                                                      # Oui
                    if self.model.save_html_file():
                        self.destroy()
                elif Reponse==None: pass                             # Annuler
                else :
                    self.destroy()                                              # Non
            else:
                self.destroy()
        except AttributeError:#caused when the windows creation process was interrupted because the
            #current_text_html.is_saved() attribute is created after the windows
            #solution: just le the user close the windows since nothing can be lost
            self.destroy()

#Mostly visual and not important --------------###############################
            
    def see_more_help_and_details(self,event):
        def toogle_index(i):#0 becomes 1 and 1 becomes
            return int(not i)
        w=event.widget
        group=w.nametowidget(w.nametowidget(w.winfo_parent()).winfo_parent())
        current_tab=w.nametowidget(w.winfo_parent())
        not_current_tab_as_index=toogle_index(group.index(current_tab))
        group.select(not_current_tab_as_index)
        #redirect to the correct help tab
        
     
    def _mark_as_modified(self):
        self.title(MAIN_TITLE_2)

    def _mark_as_not_modified(self):
        self.title(MAIN_TITLE)

    def change_size(self,event):
        #treeview is growing, even with control- fix it with something like that
        #self.elements_in_treeview['width']=25
        try:
            equivalent=event.keysym#when someone zooms with keyboard
        except AttributeError:
            equivalent=event#zoom with something else 
        if equivalent== '0':
            self.current_font['size']= -12
            self.elements_in_treeview['height']=21
        elif equivalent == 'plus':
            if self.current_font['size'] > -50:
                self.current_font['size'] -= 1
                self.elements_in_treeview['height']+=1
        elif equivalent == 'minus':
            if self.current_font['size'] < -6:
                self.current_font['size'] += 1
                self.elements_in_treeview['height']-=1
                
    def view_license(self,already_accepted=False):
        license_window=Toplevel(self,bd=1,bg=WINDOW_BACK_COLOR)
        license_window.title("LICENSE")
        LICENSE=codecs.open("LICENSE.txt",'r','utf-8').read()
        license_text=Text(license_window)
        license_text.grid(column=0,row=0)
        license_text.insert('end',LICENSE)
        
        LICENSE_NOTICE=codecs.open("Documentation/notice_license.txt",'r','utf-8').read()
        License_notice_text=Text(license_window)
        License_notice_text.grid(column=1,row=0)
        License_notice_text.insert('end',LICENSE_NOTICE)
        license_window.lift()
        
        if not already_accepted:
            license_window.grab_set()
            license_window.focus_set()
            license_window.focus_force()#force focus
            def accept(self):
                self.model.set_option("license_accepted_and_read",True)
                license_window.destroy()
                self._prepare_new_session()

            def refuse(self):
                self.model.set_option("license_accepted_and_read",False)
                self._end()
            
            license_window.protocol("WM_DELETE_WINDOW", lambda:refuse(self))
            
            accept_button=Button(license_window,text=_("Accepter"),command=lambda:accept(self))
            accept_button.grid(column=0,row=1)
            refuse_button=Button(license_window,text=_("Refuser"),command=lambda:refuse(self))
            refuse_button.grid(column=0,row=2)
        











class WebSpree(InterfaceOptions):#Model
    """ Object containing html css and javaScript file.

creating a copy of this object starts the app."""
    def __init__(self):
        #options
        default_values={\
            #editing global
                "translate_html_level": 1,\
                "indent_size":2,\
                "indent_style":" ",\
                "footer_bonus":False,\
            #editing local (read only to set a default value)
                "html_version":5.0,\
                "document_language":"fr",\
            #history
                "last_html_document_title":_("Titre"),\
                "last_css_document_title":_("Titre"),\
            #app
                "license_accepted_and_read":False,\
                "app_language":"fr",\
                "developper_interface":False\
                }
        
        self.options_file_object=Options(imported_default_values=default_values)#do not touch this directly use interface methods
        
        
        #start
        self.graphical_user_interface_tk=GraphicalUserInterfaceTk(self)
        self.current_text_html=Text_HTML(self.options_file_object,content="",saved=True,path="",encoding_py=DEFAULT_ENCODING_PY,\
                                         w3c_encoding=DEFAULT_ENCODING_WEB,version=5.0,document_language="fr")
        self.graphical_user_interface_tk._start()
        
    def _start_new_session(self):
        #self.start_mod=-2#0:standard, -1: blank, 1:open -2 nothing
        if self.start_mod==0:
            self.current_text_html=Text_HTML(self.options_file_object,content="",saved=True,path="",encoding_py=DEFAULT_ENCODING_PY,\
                                         w3c_encoding=DEFAULT_ENCODING_WEB,version=5.0,document_language="fr")
            self.current_text_html.add_standard_beginning()
            self.graphical_user_interface_tk.tk_copy_text(self.current_text_html)
        elif self.start_mod==-1:
            self.current_text_html=Text_HTML(self.options_file_object,content="",saved=True,path="",encoding_py=DEFAULT_ENCODING_PY,\
                                         w3c_encoding=DEFAULT_ENCODING_WEB,version=5.0,document_language="fr")
            self.graphical_user_interface_tk.tk_copy_text(self.current_text_html)
        elif self.start_mod==1:
            self.graphical_user_interface_tk.edit_file_dialog()
            #perhaps check if correctly opened here and update some data
            #but then Ctrl+N hotkey misses something
         
    def edit_file(self,file_path):
        ContenuExistant=open(file_path,'r').read()
        #set other usefull data here
        self.current_text_html=Text_HTML(self.options_file_object,content=ContenuExistant,saved=True,path=file_path,encoding_py=DEFAULT_ENCODING_PY,\
                                         w3c_encoding=DEFAULT_ENCODING_WEB,version=5.0,document_language="fr")
        
        self.graphical_user_interface_tk.tk_copy_text(self.current_text_html)
        #todo
        #change the way it sniffs out the encoding  and redesign this method
        
    def _save_html_file_as(self,file_path):
        if self.get_option("footer_bonus"):
            optional_bonus=("<!-- Document produit avec WebSpree\n{}\n{} -->".format(get_time(),"Fait par Cyril Walle\ncapocyril@hotmail.com"))
            self.current_text_html.add_to_text(optional_bonus)
            self.graphical_user_interface_tk.tk_copy_text(self.current_text_html)
        
        if os.path.splitext(file_path)[1]!=".html":
            file_path=os.path.splitext(file_path)[0]+".html"
        #TODO Let user choose other extension if he/she really wants to have a forced extension
        
        self.current_text_html.set_save_path(file_path)
        self.current_text_html.save_in_file()
        return True#only when success

    def save_html_file(self,*event):
        if self.current_text_html.get_save_path():
            self.current_text_html.save_in_file()
            return True
        else:#ask for a new path
            if self.graphical_user_interface_tk._save_file_dialog():
                return True
            
        
    def save_file_totest(self):#Try with CTRL+T
        self.current_text_html.test_file_with_browser()


if __name__=='__main__':
    log_writer("platform", platform.platform())
    log_writer("python_build", platform.python_build())
    WebSpreeInstance=WebSpree()

##except Exception as E:
##    log_writer("error",str(E))
##    #os.chdir(path)to change cwd
##    print(os.getcwd())
##    print(E)
##    a=input("erreur veuillez l'indiquer sur le site.\
##    Vous retrouverez peut-être l'erreur dans Cache/journal.json")
