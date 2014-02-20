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


import webbrowser
import os
import time


from Options_class import Options
from Text__classes import*
from file_extractor import*
from tks_styles import*
from html5custom import html5, html5reci
#from tks_widgets_1 import*

def _(l_string):
    #print("local language: "+l_string)
    return l_string

def get_time(time_modell="%d/%m/%Y\n%H:%M:%S"):
    return time.strftime(time_modell)

class InterfaceTk(Tk):#view and controller
    """easy tkinter"""
    def __init__(self,model):
        Tk.__init__(self)
        self.model=model
        self.title(MAIN_TITLE)
        #self.attributes('-fullscreen', 1)#, '-topmost', 1)fullscreen
        self.wm_state(newstate="zoomed")#maximize windows size
        self.geometry('1700x600+0+0')
        self.configure(bd=1,bg=WINDOW_BACK_COLOR)
        self.iconbitmap(LOGO1_PATH)
        self.protocol("WM_DELETE_WINDOW", self.intercept_close)

        self.bind("<Control-t>",self.save_file_to_test_control)
        self.bind("<Control-s>",self._save_file_dialog)

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
        self.current_font=TKFonts.Font(family='helvetica', size=-18)
        mystyle=TTK.Style()
        mystyle.configure('.',font=self.current_font)
        
        self.frame_of_frames_html=Frame(self.group_app_tabs)#html frame
        self.frame_of_frames_css=Frame(self.group_app_tabs)#css frame
        self.frame_of_frames_txt=Frame(self.group_app_tabs)#txt frame
        
        self.group_app_tabs.add(self.frame_of_frames_html,text="HTML",image=self.HTML5_PHOTO_ICO,compound='left',underline=0)
        self.group_app_tabs.add(self.frame_of_frames_css,text="CSS",image=self.CSS3_PHOTO_ICO,compound='left',underline=0)
        self.group_app_tabs.add(self.frame_of_frames_txt,text="JavaScript",image=self.JS_PHOTO_ICO,compound='left',underline=0)
        Text(self.frame_of_frames_txt,font=self.current_font).pack()
        Label(self.frame_of_frames_css,text='coming soon ...').pack()
        
        #-HTML- Frames
        F0=Frame(self.frame_of_frames_html)
        optimize_space_tab_group_for_html=TTK.Notebook(F0)
        optimize_space_tab_group_for_html.grid(column=0,row=0,sticky='nswe')
        F1=LabelFrame(optimize_space_tab_group_for_html, FRAME_STYLE,text=_("1. Choisir une Balise"))#Balises
        F1Options=LabelFrame(self.frame_of_frames_html, FRAME_STYLE,text=_("2. Choisir les attributs"))#Options
        F2=LabelFrame(self.frame_of_frames_html, FRAME_STYLE,text=_("3. Saisir Contenu"))#Buttons et saisies
        F3=LabelFrame(self.frame_of_frames_html, FRAME_STYLE,text=_("4.Code HTML"))#Preview
        F4=LabelFrame(self.frame_of_frames_html, FRAME_STYLE,text=_("0. Aides"))#Terminer
        self.autoclose_element_check_variable=BooleanVar(value=False)
        self.insertion_tk_var=BooleanVar(value=False)
        optimize_space_tab_group_for_html.add(F1,text=_("Balises"))
        #optimize_space_tab_group_for_html.add(F1Options,text="Attributs")


        
        self.elements_in_treeviews_lift = TTK.Scrollbar(F1)
        self.elements_in_treeview=TTK.Treeview(F1,selectmode='browse',columns=("local name","element"),height=25,\
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

        self.elements_in_treeview.grid(row=1,column=0,sticky='nsw')#sticky remplit colle l'objet vers le n w e ou sud
        self.elements_in_treeviews_lift.grid(row=1,column=1,sticky='nsw')#sticky remplit colle l'objet vers le n w e ou sud


        #_List of attributes:
        
        self.general_attributes_treeview=TTK.Treeview(F1Options,selectmode='browse',height=21)
        self.general_attributes_treeview.heading("#0",text=_("Général"))
        self.general_attributes_treeview.grid(row=0,column=0,sticky='w')
        for general_attribute in GENERAL_ATTRIBUTES_LIST:
            self.general_attributes_treeview.insert("",'end', text=LOCAL_ATTRIBUTES[general_attribute]["translation"],value=general_attribute)
        self.general_attributes_treeview.bind('<<TreeviewSelect>>',self.add_attribute,"")
        
        
        self.specific_attributes_treeview=TTK.Treeview(F1Options,selectmode='browse',height=21)
        self.specific_attributes_treeview.heading("#0",text=_("Spécifique"))
        self.specific_attributes_treeview.tag_configure("specific_attribute")
        self.specific_attributes_treeview.grid(row=0,column=1,sticky='w')
        self.specific_attributes_treeview.bind('<<TreeviewSelect>>',self.add_attribute,"")

        help_label_for_content=Label(F2,LABEL_STYLE, text=_("Ecrivez le contenu"))
        help_label_for_content.grid(row=0,column=0,sticky='nw')
        help_label_for_attribute=Label(F2,LABEL_STYLE, text=_("Placez les attributs"))
        help_label_for_attribute.grid(row=2,column=0,sticky='nw')

        self.content_area_form=Text(F2,ENTRY_STYLE,width=20,height=10)
        self.content_area_form.grid(row=1,column=0,sticky='nw')
        self.attribute_area_form=Text(F2,ENTRY_STYLE,width=16,height=10)
        self.attribute_area_form.grid(row=3,column=0,sticky='nw')
        #self.content_area_form.bind('<KeyRelease>',write_in_real_time)

        self.confirm_add_button=TTK.Button(F2, text=_("Confirmer"))
        self.confirm_add_button.grid(row=4,column=0,sticky='nw')

        self.close_last_element=TTK.Button(F2, text=_("Fermer la dernière\nbalise ouverte"), command=self.confirm_close_element)
        self.close_last_element.grid(row=5,column=0,sticky='nw')

        auto_close_checkbutton=TTK.Checkbutton(F2, text=_("Auto Fermeture"),variable=self.autoclose_element_check_variable )
        auto_close_checkbutton.grid(row=6,column=0,sticky='nw')



        self.main_scrollbar = TTK.Scrollbar(F3)
        self.main_text_field=Text(F3,yscrollcommand=self.main_scrollbar.set,state='normal',height=35,undo=True,font=self.current_font)#,bg='black',fg='white')
        self.main_scrollbar.config(command=self.main_text_field.yview)
        self.main_scrollbar.grid(row=0,column=1,sticky='nsw')
        self.main_text_field.grid(row=0,column=0,sticky='nsw')
        #Indicateur = InformationBubble(parent=main_text_field,texte="Vous pouvez éditer ici directement si vous ça vous chante")

        self.main_text_field.bind("<ButtonRelease-1>", self.switch_writing_place)
        self.main_text_field.bind("<KeyRelease>", self.switch_writing_place)

        F3_1=LabelFrame(F3, text="Outils", relief='ridge', borderwidth=1,bg=WINDOW_BACK_COLOR)#
        RadioFin=TTK.Radiobutton(F3_1, text=_("Ecrire à la fin"),variable=self.insertion_tk_var, value=False, command=self.switch_writing_place )
        RadioFin.grid(row=0,column=0,sticky='nw')
        RadioIns=TTK.Radiobutton(F3_1, text=_("Insèrer au curseur"),variable=self.insertion_tk_var, value=True,command=self.switch_writing_place )
        RadioIns.grid(row=1,column=0,sticky='nw')

        self.insertion_cursor=Scale(F3_1,resolution=1, from_=0, to=16, tickinterval=2,length=200,state='active'
                       ,orient='horizontal', relief='groove', showvalue=1,sliderlength=30, troughcolor='green')
        F3_1.grid(row=1,column=0,sticky='e')
        leave_button=TTK.Button(F3, text="Quitter",command=self._end )
        leave_button.grid(row=2,column=0,sticky='')


        self.element_help_and_tip=Label(F4,HELP_LABEL_STYLE, text=_("Seléctionnez une balise pour avoir de l'aide"), wrap=350,anchor='nw')
        self.element_help_and_tip.pack(side='left',fill='y')
        self.more_help=Button(F4, text=_("Plus d'aide"),command=self.see_more_help_and_details,anchor='w')
        self.more_help.pack(side='bottom')
        self.attribute_help_and_tip=Label(F4,HELP_LABEL_STYLE, text=_("Seléctionnez un attribut pour avoir de l'aide"), wrap=350,anchor='nw')
        self.attribute_help_and_tip.pack(side='right',fill='y')

        #HyperW3C=Hyperlien(F4,"www.w3c.org",LABEL_STYLE,text="Site du World Wide Web Consortium",justify='left')
        #HyperW3C.pack(side='left',fill='y')


        
        ######----Menus-----######
        FILEMENU={}
        FILEMENU["name"]=_("Fichier")
        FILEMENU["command"]=[{'label':_("Nouveau"),'command':self.new_file},\
                             {'label':_("Enregistrer [Ctrl+S]"),'command':lambda: self._save_file_dialog()},\
                             {'label':_("Essayer ! [Ctrl+T]"),'command':lambda: self.save_file_to_test_control()}]
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

        self.translate_html_level_tk_var=IntVar(value=self.model.all_option_saved_in_file["translate_html_level"])
        self.indent_size_tk_var=IntVar(value=self.model.all_option_saved_in_file["indent_size"])
        OPTIONMENU={}
        OPTIONMENU["name"]=_("Options")
        OPTIONMENU["command"]=[]
        OPTIONMENU["radiobutton"]=[{'label':_("Remplacer tout caractère spécial"),\
                                    'command':self.set_translation,'value':1,"variable":self.translate_html_level_tk_var},\
                                   {'label':_("Remplacer aucun caractère spécial"),\
                                    'command':self.set_translation,'value':0,"variable":self.translate_html_level_tk_var},\
                                   {'label':_("Indenter avec 2 espaces"),\
                                    'command':self.set_indent_size,'value':2,"variable":self.indent_size_tk_var},\
                                   {'label':_("Indenter avec 3 espaces"),\
                                    'command':self.set_indent_size,'value':3,"variable":self.indent_size_tk_var},\
                                   {'label':_("Indenter avec 4 espaces"),\
                                    'command':self.set_indent_size,'value':4,"variable":self.indent_size_tk_var}]
        #([{'label':_("Compact"),'command':self.change_mapping,'value':True,"variable":self.small_layout},
                                    #{'label':_("Etendu"),'command':self.change_mapping,'value':False,"variable":self.small_layout}])
        HELPMENU={}
        HELPMENU["name"]="Aide"
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
        #F0.grid(row=0,column=0,columnspan=3,sticky='we')#Menus
        intern_root.grid(row=0,column=0,sticky='snew')
        intern_root.columnconfigure(0,weight=2)
        intern_root.rowconfigure(0,weight=2)

        self.group_app_tabs.grid(row=0,column=0,sticky='nswe')
        self.group_app_tabs.columnconfigure(0,weight=3)
        self.group_app_tabs.rowconfigure(0,weight=3)

        #self.frame_of_frames_html.columnconfigure(0,weight=4)
        #self.frame_of_frames_html.rowconfigure(0,weight=4)

        F0.grid(row=0,column=0,sticky='nsw')
        
        F1Options.grid(row=0,column=1,sticky='nsw')
        F2.grid(row=0,column=2,sticky='nsw')
        F3.grid(row=0,column=3,sticky='nsw',rowspan=2)
        F4.grid(row=1,column=0,columnspan=3,sticky='nsew')#columnspan est la taille de l'objet

        
    def _start(self):
        self._prepare_new_session()
        print(("width: %d\nheight: %d") % (self.winfo_screenwidth(),self.winfo_screenheight()))
        self.mainloop()

    def _end(self):
        self.destroy()
        
    def see_more_help_and_details(self):
        help_window=Toplevel(self)
        Label(help_window,text="help... coming").pack()
        
    def change_size(self,event):
        #treeview is growing, even with control- fix it with something like that
        #self.elements_in_treeview['width']=25
        try:
            equivalent=event.keysym#when someone zooms with keyboard
        except AttributeError:
            equivalent=event#zoom with something else 
        if equivalent== '0':
            self.current_font['size']= -18
            self.elements_in_treeview['height']=25
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
        license_text.pack(side='right')
        license_text.insert('end',LICENSE)
        
        LICENSE_NOTICE=codecs.open("Documentation/notice_license.txt",'r','utf-8').read()
        License_notice_text=Text(license_window)
        License_notice_text.pack(side='left')
        License_notice_text.insert('end',LICENSE_NOTICE)
        
        if not already_accepted:
            license_window.grab_set()
            license_window.focus_set()
            license_window.focus_force()#force focus
            def accept(self,prepation):
                self.model.set_option("license_accepted_and_read",True)
                license_window.destroy()
                self._prepare_new_session()

            def refuse(self):
                self.model.set_option("license_accepted_and_read",False)
                self._end()
            
            license_window.protocol("WM_DELETE_WINDOW", lambda:refuse(self))
            
            accept_button=Button(license_window,text=_("Accepter"),command=lambda:accept(self,license_window))
            accept_button.pack(side='bottom')
            refuse_button=Button(license_window,text=_("Refuser"),command=lambda:refuse(self))
            refuse_button.pack(side='bottom')
        
    def _prepare_new_session(self):#view
        if not self.model.all_option_saved_in_file["license_accepted_and_read"]:
            self.view_license()
        else:
            
            self.Contexte=Toplevel(self,bd=1,bg=WINDOW_BACK_COLOR)
            self.Contexte.title(_("Commencer"))
            self.Contexte.geometry('700x600+200+200')
            self.Contexte.grab_set()
            self.Contexte.focus_set()
            self.Contexte.focus_force()#force focus
            
            
            frame_title=LabelFrame(self.Contexte, FRAME_STYLE,text=_("Titre du document"))
            self.title_tk_var=StringVar(value=self.model.all_option_saved_in_file["document_title"])
            Entry(frame_title,ENTRY_STYLE,textvariable=self.title_tk_var).pack()

            
            self.new_doc_radiobutton_var=IntVar(value=0)
            frame_where_to_start=LabelFrame(self.Contexte, FRAME_STYLE,text=_("Document"))
            new_doc_radiobutton=TTK.Radiobutton(frame_where_to_start, text=_("Commencer un nouveau document standard"),value=0,variable=self.new_doc_radiobutton_var)
            new_doc_radiobutton.pack(anchor="w")
            new_blank_doc_radiobutton=TTK.Radiobutton(frame_where_to_start,text=_("Commencer un nouveau document vierge"), value=-1,variable=self.new_doc_radiobutton_var)
            new_blank_doc_radiobutton.pack(anchor="w")
            edit_doc_radiobutton=TTK.Radiobutton(frame_where_to_start, text=_("Modifier un document existant"),value=1,variable=self.new_doc_radiobutton_var)
            edit_doc_radiobutton.pack(anchor="w")
            
            #change this barbar method to control encoding
            self._which_encoding_var=StringVar(value=self.model.current_text_html.get_encoding()+";"+self.model.current_text_html.get_w3c_encoding())
            frame_which_encoding=LabelFrame(self.Contexte, FRAME_STYLE,text=_("Encodage(Version test)"))
            for encotext,pyencodings,standardenco in ENCODINGS:
                encoding_radiobutton=TTK.Radiobutton(frame_which_encoding, text=encotext,value=pyencodings+";"+standardenco,variable=self._which_encoding_var)
                encoding_radiobutton.pack(anchor='w')

            frame_title.grid(row=0,column=0,sticky='w')
            frame_where_to_start.grid(row=1,column=0,sticky='nswe')
            frame_which_encoding.grid(row=1,column=1,sticky='nswe')

            ConfirmerContexte=TTK.Button(self.Contexte, text=_("Confirmer[Entrée]"), command=self._confirm_new_session)
            ConfirmerContexte.grid(row=2,column=0)

            self.Contexte.bind("<Return>",self._confirm_new_session)

        
    def _confirm_new_session(self,*event):#controller
        self.model.set_option("document_title",self.title_tk_var.get())
        new_encoding_py , new_w3c_encoding = (self._which_encoding_var.get().split(";"))
        
        self.model.current_text_html.set_encoding(new_encoding_py)
        self.model.current_text_html.set_w3c_encoding(new_w3c_encoding)
        
        self.model.start_mod=self.new_doc_radiobutton_var.get()
        self.model._start_new_session()
        if (self.model.element_still_not_closed_list):
            self.close_last_element['state']='normal'
        else:
            self.close_last_element['state']='disabled'
        self.Contexte.destroy()
        
    def _mark_as_modified(self):
        self.title(MAIN_TITLE_2)

    def _mark_as_not_modified(self):
        self.title(MAIN_TITLE)

    def tk_copy_text(self,text_to_copy):
        self.main_text_field.yview("moveto","1.0")
        self._mark_as_modified()
        self.main_text_field.delete('1.0', 'end'+'-1c')
        self.main_text_field.insert('end',text_to_copy)
        
    def set_translation(self):
        self.model.set_option("translate_html_level",self.translate_html_level_tk_var.get())

    def set_indent_size(self):
        self.model.set_option("indent_size",self.indent_size_tk_var.get())
        
    def add_attribute(self,event):
        """
{
    "name":{
        "alt(s)":alternative list,
        "default_value":"default value ...",
        "possible_values":possible values list,
        "version":"html version"
    },
    """
        selected_item_id=event.widget.selection()[0]
        attribute=(event.widget.item(selected_item_id,'value'))[0]
        attribute_details=ATTRIBUTES[attribute]
        attribute_local_details=LOCAL_ATTRIBUTES[attribute]
        if not attribute in self.attribute_area_form.get('1.0', 'end'+'-1c'):
            self.attribute_area_form.insert('end',"{}=\"{}\"\n".format(attribute,attribute_details["default_value"]))
            
        self.attribute_help_and_tip['text']=_("Aide pour l'attribut {} ({}) : \n{}\nValeur par défaut: {}").\
                                             format(attribute,attribute_local_details["translation"],attribute_local_details["description"],\
                                                    attribute_details["default_value"])
        
    def update_choice1(self,*event):
        selected_item_id=self.elements_in_treeview.selection()[0]
        if not self.elements_in_treeview.get_children(selected_item_id):#only parents have childs
            element_tag=(self.elements_in_treeview.item(selected_item_id,'value'))[0]

            self.content_area_form.delete('1.0', 'end'+'-1c')#Mettre en option
            self.attribute_area_form.delete('1.0', 'end'+'-1c')
            
            
            self.elements_in_treeview.heading("local name",text=_("Code: ")+element_tag)
            self.element_help_and_tip['text']=_("Aide pour")+((" <%s> (%s):\n%s") %\
                                                              (element_tag,LOCAL_ELEMENTS[element_tag]["translation"],\
                                                               LOCAL_ELEMENTS[element_tag]["description"]))
            
            _i=self.specific_attributes_treeview.get_children()
            for item in _i: self.specific_attributes_treeview.delete(item)#delete all items in specific_attributes_treeview before
            for couple in ELEMENTS:
                for ele in couple[1]:
                    if ele==element_tag:
                        self.current_element_void=couple[1][ele]["void"]
                        if self.current_element_void:
                            self.content_area_form['state']='disabled'
                        else:
                            self.content_area_form['state']='normal'
                        #todo add must attributes somewhere
                        for attribute in couple[1][ele]["specific_attributes"]:
                                self.specific_attributes_treeview.insert("",'end',text=attribute,value=attribute,tags="specific_attribute")
                        break


            self.confirm_add_button['command']=self.confirm_write
        
   
    def switch_writing_place(self,*event):
        self.model.current_text_html.text=self.main_text_field.get('1.0', 'end'+'-1c')
        if event:
            self.insertion_tk_var.set(True)
        if self.insertion_tk_var.get():
            line_before=self.main_text_field.get('insert'+'-1l', 'insert')
            #CTabulations=line_before.count(indent_var_changed)
            self.insertion_cursor.grid(row=2,column=0,sticky='nw')
            #self.insertion_cursor.set(CTabulations)
            
            
            before_cursor_text=self.main_text_field.get('1.0', 'insert')
            
            self.model.insertion=len(before_cursor_text)
            
        else:
            self.insertion_cursor.grid_forget()
            self.model.insertion=None
            
    def confirm_write(self):
        #self.elements_in_treeview,
        selected_item_id=self.elements_in_treeview.selection()[0]
        if not self.elements_in_treeview.get_children(selected_item_id):#only parents have childs
            element_tag=(self.elements_in_treeview.item(selected_item_id,'value'))[0]
            options_with_spaces=" "+self.attribute_area_form.get('1.0', 'end'+'-1c').replace("\n"," ")#On remplace les sauts de lignes par des espaces
                #if self.model.insertion is None:
            if self.current_element_void:
                self.model.open_close_void_element(element_tag,options_with_spaces)
            else:
                self.model.open_element1(element_tag, options_with_spaces)
                self.model.add_to_text1(self.content_area_form.get('1.0', 'end'+'-1c'))
                self.close_last_element['state']='active'###
                if self.autoclose_element_check_variable.get():
                    if not self.model.close_element1():
                        self.close_last_element['state']='disabled'#
                    """
                else:
                    #problem it closes the element added before and not the current
                    self.close_last_element['state']='active'
                    if self.autoclose_element_check_variable.get():
                        self.model.close_element1(self.model.insertion)
                        if self.model.instant_indenting_level[0]==0:
                            self.close_last_element['state']='disabled'
                    
                    self.model.add_to_text1(self.content_area_form.get('1.0', 'end'+'-1c'),insertion=self.model.insertion)
                    self.model.open_element1(((self.elements_in_treeview.item(item,'value'))[1]), options_with_spaces,self.model.insertion)
                    #todo here put the cursor at the end of what is just added and change insertion point the same way
                self.update_choice1()"""
        
                   
    def write_in_real_time(self,*event):#TODO
        try:
            self.main_text_field.delete("hi")
        except IndexError:
            pass
        
    def confirm_close_element(self):
        self.model.close_element1(self.model.insertion)
        if not(self.model.element_still_not_closed_list):
            self.close_last_element['state']='disabled'
        
    def new_file(self):
        if self.model.current_text_html.is_saved():
            self._prepare_new_session()
        else:
            Reponse=MessageBox.askyesnocancel(title=_("Attention"), message=_("Voulez vous sauvegarder avant de commencer un nouveau document ?"))#True False ou None 
            if Reponse:                                                      # Oui
                if self._save_file_dialog():
                    self._prepare_new_session()
            elif Reponse is None: pass                             # Annuler
            else :
                self._prepare_new_session()                       #Non
    
    def edit_file_dialog(self):
        file_path=FileDialog.askopenfilename(defaultextension=".html",filetypes=[("HyperText Mark-Up Language file", "*.html" ),])
        #to-do double check if the file exist here because it could have been deleted during the time the user chooses the file
        if file_path:
            self.model.edit_file(file_path)


    def _save_file_dialog(self,*event):
        NomDuFichier=FileDialog.asksaveasfilename(defaultextension=".html",filetypes=[("HyperText Mark-Up Language file", "*.html" ),],\
                                                  initialfile=self.model.all_option_saved_in_file["document_title"])
        
        if NomDuFichier != "":
            self.model._save_file(NomDuFichier)
            return True#Sauvegarde réussi !
        else:
            return False

    def save_file_to_test_control(self,*event):#Try with CTRL+T
        self.model.save_file_totest()

    def intercept_close(self): # intercept_close
        try:
            if not self.model.current_text_html.is_saved():
                Reponse=MessageBox.askyesnocancel(title=_("Attention"), message=_("Voulez vous sauvegarder avant de quitter ?"))#True False ou None 
                if Reponse:                                                      # Oui
                    if self._save_file_dialog():
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












class WebSpree(object):#Model
    
    def __init__(self):
        
        #meta
        self.encoding_py=DEFAULT_ENCODING_PY
        self.encoding_in_doc=DEFAULT_ENCODING_WEB

        #options
        default_values={\
                "translate_html_level": 1,\
                "indent_size":2,\
                "document_title":"Titre",\
                "license_accepted_and_read":False,\
                "language":"fr",\
                "html_version":5.0,\
                "footer_bonus":False}
        
        self.options_file_object=Options(imported_default_values=default_values)
        self.all_option_saved_in_file=self.options_file_object.read_file()
        
        #start
        self.start_mod=-2#0:standard, -1: blank, 1:open -2 nothing
        self.interface=InterfaceTk(self)
        self._start_new_session()
        self.interface._start()
        

    def set_option(self,option_name,value):
        self.options_file_object.add_option_to_file(option_name,value)
        self.all_option_saved_in_file[option_name]=value
        
    def _start_new_session(self):

        #editing
        self.current_text_html = Text_HTML(content="",saved=True,path="",encoding_py=DEFAULT_ENCODING_PY,\
                                                                  w3c_encoding=DEFAULT_ENCODING_WEB,version=5)
        self.element_still_not_closed_list=list()
        self.instant_indenting_level=list()
        self.instant_indenting_level.append(0)
        self.instant_indenting_level.append(0)
        self.insertion=None
        
        if self.start_mod==0:
            self.add_standard_beginning()
        elif self.start_mod==-1:
            self.add_to_text1("",0)
        elif self.start_mod==1:
            self.interface.edit_file_dialog()
            
    def _save_file(self,file_path):
        the_time=get_time()
        for BalisesNonFermees in range(len(self.element_still_not_closed_list)):
            self.close_element1()#On ferme toutes les balises encore ouvertes
        if self.all_option_saved_in_file["footer_bonus"]:
            optional_bonus=("<!-- Document produit avec WebSpree\n{}\n{} -->".format(the_time,"Fait par Cyril Walle\ncapocyril@hotmail.com"))
            self.add_to_text1(optional_bonus,0,None)
        
        if os.path.splitext(file_path)[1]!=".html":
            file_path=os.path.splitext(file_path)[0]+".html"
        #TODO Let user choose other extension if he/she really wants to have a forced extension
        
        self.current_text_html.set_save_path(file_path)
        self.current_text_html.save_in_file()
        
    def save_file_totest(self):#Try with CTRL+T
        self.current_text_html.test_file_with_browser()

    def edit_file(self,file_path):
        ContenuExistant=open(file_path,'r').read()
        self.add_to_text1(ContenuExistant,0)
        #todo
        #change the way it sniffs out the encoding
        #the code below won t work because variable names have changed
        """
        currentencoding=ContenuExistant[ContenuExistant.find("charset")+8::].split(" ")[0].strip().split("\"")[0]
        currentencoding2=ContenuExistant[ContenuExistant.find("charset")+9::].split(" ")[0].strip().split("\"")[0]
        if currentencoding!='PE' and currentencoding.strip()!="":
            ChoixEncodage.set(currentencoding+";"+currentencoding)
            print("Encoding detected: "+currentencoding)
        elif currentencoding2!='PE' and currentencoding2.strip()!="":
            ChoixEncodage.set(currentencoding2+";"+currentencoding2)
            print("Encoding detected: "+currentencoding2)
        else:
            print("Encoding not detected; set to: "+DEFAULTENCODING)
            ChoixEncodage.set(DEFAULTENCODING)
        """

    
            
    def add_standard_beginning(self,html_version=5.0):
        if html_version==5.0:
            self.add_to_text1("<!DOCTYPE html>",0,first=True)
            self.open_element1("html ","lang=\"{}\"".format(self.all_option_saved_in_file["language"]))
            self.open_element1("head")
            self.open_close_void_element("meta"," charset=\"{}\"".format(self.current_text_html.get_w3c_encoding()))
            self.open_close_void_element("link"," rel=\"stylesheet\" href=\"{}\"".format("coming_style.css"))
            self.open_element1("title")
            self.add_to_text1(self.all_option_saved_in_file["document_title"],0)
            self.close_element1()#title close
            self.close_element1()#head close
            self.open_element1("body")
        elif html_version==4.0:
            pass#complete here
        
    def add_indent_and_line(self, text,indent_level,translate_html_level,first):
        NVTexte=""
        if not first:
            NVTexte="\n"
        for level in range(indent_level):
            NVTexte=NVTexte+(self.all_option_saved_in_file["indent_size"] * " " )
        if translate_html_level==1:
            for chars in text:
                NVTexte=NVTexte+self.NormalVersHTML5(chars)
                if self.NormalVersHTML5(chars)=="<br />":#Ce if rend la prévisualisation plus lisible
                    NVTexte=NVTexte+"\n"
                    for INds in range(indent_level+1):
                        NVTexte=NVTexte+(self.all_option_saved_in_file["indent_size"] * " " )
        else:
            NVTexte=NVTexte+text
        return NVTexte

    def HTML5VersNormal(self,MotCleHTML5):
        #utilise le dictionnaire html5
        if MotCleHTML5[0]=='&':
            CarNormal=html5[MotCleHTML5[1::]]
        else:#Ce n'est pas un mot-cle
            CarNormal=MotCleHTML5
        return CarNormal

    def NormalVersHTML5(self,CarNormal):
        #utilise le dictionnaire html5reci
        try:
            CarHTML5='&'+html5reci[CarNormal]
            if CarHTML5[-1] != ';':
                CarHTML5=CarHTML5+';'
        except KeyError:
            CarHTML5=CarNormal#n'a pas besoin de changer !
        if CarHTML5=="&<br />;":
            CarHTML5="<br />"
        return CarHTML5

    def add_to_text1(self,text,translate_html_level="not given",insertion="not given",first=False):
        """add the text to our current_text_html
        and call the method to do it in the appropriate GUI too ( should be only visual but not change core variables)
        if translate_html is True the texte will be translated into HTML5 special syntax (example: é --> &eacute; )
        if insertion!=0 the text is insert ont the position value of insertion
        also make possible to write and visualize in real time but not here"""
        if translate_html_level == "not given":
            translate_html_level=self.all_option_saved_in_file["translate_html_level"]
        if insertion == "not given":
            insertion=self.insertion
        if ((insertion is None)                                             #no insertion => add to the end
            or (insertion>len(self.current_text_html))):        #insertion out of bound is the same
            insertion=len(self.current_text_html)        
        self.current_text_html.text=(self.current_text_html[0:insertion] +
                                            self.add_indent_and_line(text,self.instant_indenting_level[0],translate_html_level,first) +
                                            self.current_text_html[insertion:])
        
        self.interface.tk_copy_text(self.current_text_html.text)

    def open_close_void_element(self,BaliseNue,Options,insertion="not given"):
        if insertion == "not given":
            insertion=self.insertion
        Baliseopen_close_void_element="<"+BaliseNue+Options+"/>"
        self.add_to_text1(Baliseopen_close_void_element,0,insertion)

    def open_element1(self,BaliseNue,Options="",insertion="not given"):
        if insertion == "not given":
            insertion=self.insertion
        #if BaliseNue???void
        BaliseOuvrante="<"+BaliseNue+Options+">"
        BaliseFermante="</"+BaliseNue+">"
        self.add_to_text1(BaliseOuvrante,0,insertion)
        self.element_still_not_closed_list.append(BaliseFermante)
        self.instant_indenting_level[0]=self.instant_indenting_level[0]+1
        

    def close_element1(self,insertion="not given"):
        if insertion == "not given":
            insertion=self.insertion
        self.instant_indenting_level[0]=self.instant_indenting_level[0]-1
        BaliseFermee=self.element_still_not_closed_list.pop()
        self.add_to_text1(BaliseFermee,0,insertion)
        return len(self.element_still_not_closed_list)>0
        
if __name__=='__main__':
    WebSpreeInstance=WebSpree()
