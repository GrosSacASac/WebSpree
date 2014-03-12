#!/usr/bin/python
#-*-coding:utf-8*

#GraphicalUserInterfaceTk.py
#Role: define the class GraphicalUserInterfaceTk used for WebSpree

#Walle Cyril
#20/03/2014

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

#import tkinter ...
try:#3.X
    import tkinter as tk
    import tkinter.ttk  as ttk
    import tkinter.filedialog as filedialog
    import tkinter.messagebox as messagebox
    import tkinter.font as tkfont
except ImportError:#2.X
    import Tkinter as tk
    import ttk as ttk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
    import tkFont as tkfont

import webbrowser


##DATA##
from file_extractor import*
##STYLES##
from tks_styles import*
##LOG##
#from log_writer import log_writer
##TOOLS##
from tk_tools import*
from tks_widgets_1 import DragDropFeedback,MainPlusHelp

def _(l_string):
    #print("local language: "+l_string)
    return l_string

class HTMLWindows(tk.Frame):
    """"""

    def __init__(self,parent,master_window,model):
        tk.Frame.__init__(self)
        self.model=model
        self.master_window=master_window

        #short term solution:
        self.bind_all('<Control-Shift-T>',self.save_file_to_test_control)
        self.bind_all('<Control-Shift-S>',self._save_file_dialog)
        self.bind_all('<Control-s>',self.model.save_html_file)
        self.bind_all('<Control-o>',self.edit_file_dialog)
        self.bind_all('<Control-n>',self.new_file)
        self.bind_all('<Control-w>',self.close_tab)
        #long term solution: bind the app and not this frame and then look which tab is selected to call the correct action 
        
        
        
        self.autoclose_element_check_variable=tk.BooleanVar(value=True)
        self.insertion_tk_var=tk.BooleanVar(value=False)

        #elements 
        frame_element_master=tk.Frame(self,FRAME_STYLE_2,bg=COLOURS_A[0])
        self.element_plus_help=MainPlusHelp(frame_element_master,_("Balises"),_("Aide"))
        self.elements_in_treeviews_lift = ttk.Scrollbar(self.element_plus_help.main_frame)
        self.elements_in_treeview=ttk.Treeview(self.element_plus_help.main_frame,selectmode='browse',\
                                            columns=("element","local"),height=21,cursor="hand2",\
                                             yscrollcommand=self.elements_in_treeviews_lift.set,padding=0,takefocus=True,\
                                             displaycolumns=(1,0),show='headings')#,show='tree'
        self.elements_in_treeview.column("#0",width=20,stretch=False)
        self.elements_in_treeview.heading("local",text=_("Traduction"))
        self.elements_in_treeview.column("local",minwidth=100)
        self.elements_in_treeview.heading("element",text=_("Code"))
        self.elements_in_treeview.bind('<<TreeviewSelect>>',self.update_element_selection)
        self.elements_in_treeview.bind('<Button-1>',self.drag_start,add='+')
        self.elements_in_treeview.bind("<B1-Motion>",self.drag_and_drop_visual, add='+')
        self.elements_in_treeview.bind('<ButtonRelease-1>',self.drop_end,add='+')
        self.elements_in_treeviews_lift.config(command=self.elements_in_treeview.yview)
        #_List of elements:
        i=0
        tags=["tag_1","tag_2"]
        self.elements_in_treeview.tag_configure("tag_1", background='#cccfff')
        self.elements_in_treeview.tag_configure("tag_2", background='#cfffcc')
        self.elements_in_treeview.tag_configure("tag_3", background='#ffccbc')
        for couple in ELEMENTS:
            function=self.elements_in_treeview.insert("",'end',values=("",couple[0]),tag=tags[i%2])
            i+=1
            for ele in couple[1]:
                self.elements_in_treeview.insert(function,'end', \
                                                 values=(ele,LOCAL_ELEMENTS[ele]["translation"]),tag="tag_3")

        self.elements_in_treeview.grid(row=0,column=0,columnspan=2,sticky='nsw')
        self.elements_in_treeviews_lift.grid(row=0,column=2,sticky='nsw')


        #attributes
        frame_attribute_master=tk.Frame(self,FRAME_STYLE_2,bg=COLOURS_A[1])#attributes
        self.attribute_plus_help=MainPlusHelp(frame_attribute_master,_("Attributs"),_("Aide"))    
        #_List of attributes:
        self.general_attributes_treeview=ttk.Treeview(self.attribute_plus_help.main_frame,selectmode='browse',\
                                        height=21,columns=("real","local"),displaycolumns=(1),show='headings')
        self.general_attributes_treeview.heading("local",text=_("Général"))
        self.general_attributes_treeview.grid(row=0,column=0,sticky='w')
        for general_attribute in GENERAL_ATTRIBUTES_LIST:
            self.general_attributes_treeview.insert("",'end',values=(general_attribute,LOCAL_ATTRIBUTES[general_attribute]["translation"]))
        self.general_attributes_treeview.bind('<<TreeviewSelect>>',self.update_attribute_selection,"")
        
        self.specific_attributes_treeview=ttk.Treeview(self.attribute_plus_help.main_frame,\
            selectmode='browse',height=21,columns=("real","local"),displaycolumns=(1),show='headings')
        self.specific_attributes_treeview.heading("local",text=_("Spécifique"))
        #self.specific_attributes_treeview.tag_configure("specific_attribute")not here later make tag ofr must and specifiq in different colours
        self.specific_attributes_treeview.grid(row=0,column=1,sticky='w')
        self.specific_attributes_treeview.bind('<<TreeviewSelect>>',self.update_attribute_selection,"")


        #Help
        self.complete_help_element=ttk.Label(self.element_plus_help.help_frame, text=_(""),wrap=400)
        self.complete_help_element.grid(row=0,column=0,sticky='nswe')
        self.complete_help_attribute=ttk.Label(self.attribute_plus_help.help_frame, text=_(""),wrap=400)
        self.complete_help_attribute.grid(row=0,column=0,sticky='nswe')
        #HyperW3C=Hyperlien(master,"www.w3c.org",LABEL_STYLE,text="Site du World Wide Web Consortium",justify='left')
        #HyperW3C.pack(side='left',fill='y')

        
        #user input
        frame_2_user_input=tk.Frame(self, FRAME_STYLE_2,bg=COLOURS_A[2])#Buttons et saisies
        help_label_for_content=ttk.Label(frame_2_user_input, text=_("Ecrivez le contenu"))
        help_label_for_content.grid(row=0,column=0,sticky='nw')
        help_label_for_attribute=ttk.Label(frame_2_user_input, text=_("Placez les attributs"))
        help_label_for_attribute.grid(row=0,column=1,sticky='nw')

        self.content_area_form=Text(frame_2_user_input,ENTRY_STYLE,width=42,height=10)
        self.content_area_form.grid(row=1,column=0,sticky='nw')
        self.content_area_form.bind('<Button-3>',create_context_menu)
        self.attribute_area_form=Text(frame_2_user_input,ENTRY_STYLE,width=40,height=10)
        self.attribute_area_form.grid(row=1,column=1,sticky='nw')
        self.attribute_area_form.bind('<Button-3>',create_context_menu)
        #self.content_area_form.bind('<KeyRelease>',write_in_real_time)

        self.confirm_add_button=ttk.Button(frame_2_user_input, text=_("Confirmer"),command=self.confirm_write)
        self.confirm_add_button.grid(row=2,column=0,sticky='nw')

        self.var_for_auto_close_checkbutton=tk.BooleanVar(value=True)
        self.auto_close_checkbutton=ttk.Checkbutton(frame_2_user_input, text=_("Auto Fermeture"),variable=self.var_for_auto_close_checkbutton)
        self.auto_close_checkbutton.grid(row=2,column=1,sticky='nw')
        

        #HTML tabs
        frame_3_html_box=tk.Frame(self, FRAME_STYLE_2,bg=COLOURS_A[3])
        self.html_text_tabs=ttk.Notebook(frame_3_html_box)
        self.html_text_tabs.grid(row=0,column=0,sticky='nsw')
        self.html_text_tabs.bind('<<NotebookTabChanged>>',self.change_tab)#xxx#
        

        frame_3_html_box_1=tk.LabelFrame(frame_3_html_box, text="Outils", relief='ridge', borderwidth=1,bg=WINDOW_BACK_COLOR)#
        RadioFin=ttk.Radiobutton(frame_3_html_box_1, text=_("Ecrire à la fin"),variable=self.insertion_tk_var, value=False, command=self.switch_writing_place )
        RadioFin.grid(row=0,column=0,sticky='nw')
        RadioIns=ttk.Radiobutton(frame_3_html_box_1, text=_("Insèrer au curseur"),variable=self.insertion_tk_var, value=True,command=self.switch_writing_place )
        RadioIns.grid(row=1,column=0,sticky='nw')

        
        frame_3_html_box_1.grid(row=1,column=0,sticky='e')
        if self.model.get_option("developper_interface"):
            leave_button=ttk.Button(frame_3_html_box, text="Quitter",command=self.master_window._end )
            leave_button.grid(row=2,column=0,sticky='')

        self.master_window._treeviews=self.master_window._treeviews+[self.elements_in_treeview,self.general_attributes_treeview,self.specific_attributes_treeview]
        #keep this do work around a ttk bug: growing treeviews
        
        #self.columnconfigure(0,weight=1)
        #self.rowconfigure(0,weight=1)
        
        frame_element_master.grid(row=0,column=0,sticky='nsw')
        frame_attribute_master.grid(row=0,column=1,sticky='nsw')
        frame_2_user_input.grid(row=1,column=0,columnspan=2,sticky='nsw')
        frame_3_html_box.grid(row=0,column=2,sticky='nsw',rowspan=2)
        self.grid(sticky='nswe')
        #self.grid_columnconfigure(0,weight=0)
        
    def _prepare_new_session(self):#view
        self.Contexte=tk.Toplevel(self,bd=1,bg=WINDOW_BACK_COLOR)
        self.Contexte.title(_("Commencer"))
        self.Contexte.geometry('700x600+200+200')
        self.Contexte.grab_set()
        self.Contexte.focus_set()
        self.Contexte.focus_force()#force focus
        
        frame_title=tk.LabelFrame(self.Contexte, FRAME_STYLE,text=_("Titre du document"))
        self.title_tk_var=tk.StringVar(value=self.model.get_option("last_html_document_title"))
        tk.Entry(frame_title,ENTRY_STYLE,textvariable=self.title_tk_var).pack()

        
        self.new_doc_radiobutton_var=tk.IntVar(value=0)
        frame_where_to_start=tk.LabelFrame(self.Contexte, FRAME_STYLE,text=_("Document"))
        new_doc_radiobutton=ttk.Radiobutton(frame_where_to_start, text=_("Commencer un nouveau document standard"),value=0,variable=self.new_doc_radiobutton_var)
        new_doc_radiobutton.pack(anchor="w")
        new_blank_doc_radiobutton=ttk.Radiobutton(frame_where_to_start,text=_("Commencer un nouveau document vierge"), value=-1,variable=self.new_doc_radiobutton_var)
        new_blank_doc_radiobutton.pack(anchor="w")
        edit_doc_radiobutton=ttk.Radiobutton(frame_where_to_start, text=_("Modifier un document existant"),value=1,variable=self.new_doc_radiobutton_var)
        edit_doc_radiobutton.pack(anchor="w")
        
        #to do change this barbar method to control encoding properlyindex=self.model.selected_tab
        self._which_encoding_var=tk.StringVar(value="utf-8;utf-8")
        #self._which_encoding_var=StringVar(value=self.model.current_text_html.get_encoding()+";"+self.model.current_text_html.get_w3c_encoding())
        frame_which_encoding=tk.LabelFrame(self.Contexte, FRAME_STYLE,text=_("Encodage(beta)"))
        for encotext,pyencodings,standardenco in ENCODINGS:
            encoding_radiobutton=ttk.Radiobutton(frame_which_encoding, text=encotext,value=pyencodings+";"+standardenco,variable=self._which_encoding_var)
            encoding_radiobutton.pack(anchor='w')

        self.indent_style_tk_var=tk.StringVar(value=self.model.get_option("indent_style"))
        self.indent_size_tk_var_2=tk.IntVar(value=self.model.get_option("indent_size"))
        frame_indentation=tk.LabelFrame(self.Contexte, FRAME_STYLE,text=_("Indentation"))
        indent_style_radiobutton=ttk.Radiobutton(frame_indentation, text=_("Espaces"),value=" ",variable=self.indent_style_tk_var)
        indent_style_radiobutton.pack(anchor='w')
        indent_style_radiobutton2=ttk.Radiobutton(frame_indentation, text=_("Tabulations"),value="\t",variable=self.indent_style_tk_var)
        indent_style_radiobutton2.pack(anchor='w')
        for i in range(1,9):
            indent_size_radiobutton=ttk.Radiobutton(frame_indentation, text=str(i),value=i,variable=self.indent_size_tk_var_2)
            indent_size_radiobutton.pack(anchor='w')

        frame_submit=tk.LabelFrame(self.Contexte, FRAME_STYLE,text=_("Valider"))
        accept_and_begin=ttk.Button(frame_submit, text=_("Confirmer[Entrée]"), command=self._confirm_new_session)
        accept_and_begin.grid(row=0,column=0)
        cancel=ttk.Button(frame_submit, text=_("Annuler[Escape]"), command=self.Contexte.destroy)
        cancel.grid(row=1,column=0)

        
        frame_title.grid(row=0,column=0,sticky='w')
        frame_where_to_start.grid(row=1,column=0,sticky='nswe')
        frame_which_encoding.grid(row=1,column=1,sticky='nswe')
        frame_indentation.grid(row=2,column=0,sticky='nswe')
        frame_submit.grid(row=2,column=1,sticky='nswe')

        self.Contexte.bind('<Escape>',lambda e:self.Contexte.destroy())
        self.Contexte.bind('<Return>',self._confirm_new_session)

        
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
        tab_index=self.model.selected_tab
        current_object=self.model.tabs_html[tab_index]
        current_close_last=self.text_fields[tab_index][1]
        
        new_encoding_py , new_w3c_encoding = (self._which_encoding_var.get().split(";"))
        current_object.set_encoding(new_encoding_py)
        current_object.set_w3c_encoding(new_w3c_encoding)
        #this should be passe via start new session method-------
        
        if current_object.element_still_not_closed_list:
            current_close_last['state']='normal'
        else:
            current_close_last['state']='disabled'
        self.Contexte.destroy()
        
    def new_html_tab(self,tab_index,title):
        html_text_tab=tk.Frame(self.html_text_tabs)
        main_scrollbar = ttk.Scrollbar(html_text_tab)
        self.text_fields.append([Text(html_text_tab,yscrollcommand=main_scrollbar.set,state='normal',height=35,undo=True),\
                                             ttk.Button(html_text_tab, text=_("Fermer la dernière\nbalise ouverte"), command=self.confirm_close_element)])

        #tab_index=self.model.selected_tab
        #self.text_fields[tab_index][0]  Text
        #self.text_fields[tab_index][1]  close_last_element_button

        
        main_scrollbar.config(command=self.text_fields[tab_index][0].yview)
        self.text_fields[tab_index][0].grid(row=0,column=0,sticky='nsw')
        main_scrollbar.grid(row=0,column=1,sticky='ns')
        self.text_fields[tab_index][0].bind('<KeyRelease>', self.so_you_decided_to_write_html_directly)
        self.text_fields[tab_index][0].bind('<Button-3>',create_context_menu)#it doesn t change the real object !!!
        self.text_fields[tab_index][0].bind('<ButtonRelease-1>',self.switch_writing_place)
        self.text_fields[tab_index][1].grid(row=1,column=0,sticky='nsw')
        self.text_fields[tab_index][1]['state']='disabled'
        #Indicateur = InformationBubble(parent=main_text_field,texte=_("Vous pouvez éditer ici directement si vous ça vous chante"))
        self.html_text_tabs.add(html_text_tab,text=title)
        self.html_text_tabs.select(tab_index)

    def change_tab(self,*event):#mysteriously non functional
        self.html_text_tabs.update_idletasks()
        self.model.selected_tab=self.html_text_tabs.index(self.html_text_tabs.select())
        
    def close_tab(self,*event):
        def kill_tab(self,tab_index):
            self.model.existing_tabs-=1
            del self.model.tabs_html[tab_index]
            del self.text_fields[tab_index]
            self.html_text_tabs.forget(tab_index)
            if self.model.existing_tabs>0:
                self.html_text_tabs.select(0)
                self.model.selected_tab=0
            else:
#here is the way to let open at least 1 tab instead of closing the app
                self.model.start_mod=2
                self.model._start_new_session()#open with a different name than last name used
        
        tab_index=self.model.selected_tab
        current_object=self.model.tabs_html[tab_index]
        if event[0]=="for_save":
            if not current_object.is_saved():
                answer=messagebox.askyesnocancel(title=_("Attention"), message=_("Voulez vous sauvegarder avant de fermer cet onglet ?"))#True False ou None 
                if answer:                                                      # Yes
                    if not self.model.save_html_file():
                        return "cancel"
                elif answer==None:                                      # Cancel or X pressed
                    return "cancel"
            return "no_cancel"
        elif event[0]=="already_saved":
            kill_tab(self,tab_index,)
        else:#manual tab_closing
            try:
                if not current_object.is_saved():
                    answer=messagebox.askyesnocancel(title=_("Attention"), message=_("Voulez vous sauvegarder avant de fermer cet onglet ?"))#True False ou None 
                    if answer:                                                      # Yes
                        if self.model.save_html_file():
                            kill_tab(self,tab_index)
                    elif answer==None: pass                                  # Cancel or X pressed
                    else :
                        kill_tab(self,tab_index)                             # Non
                else:
                    kill_tab(self,tab_index)
            except Exception:#caused when the windows creation process was interrupted because the
                #current_text_html.is_saved() attribute is created after the windows
                #solution: just le the user close the windows since nothing can be lost
                kill_tab(self,tab_index)
                                
    def update_attribute_selection(self,event):
        selected_item_id=event.widget.selection()[0]
        attribute=(event.widget.item(selected_item_id,'value'))[0]
        attribute_details=ATTRIBUTES[attribute]
        attribute_local_details=LOCAL_ATTRIBUTES[attribute]
        if not attribute in self.attribute_area_form.get('1.0', 'end'+'-1c'):
            self.attribute_area_form.insert('end',"{}=\"{}\"\n".format(attribute,attribute_details["default_value"]))

        minimum="{}\n{}\n{}".format(attribute_local_details["description"],attribute_local_details["role"],\
                                                           attribute_local_details["common usage"]).strip()
        complete_help=(_("{} ({})\n{}\nAlternatives: {}\nValeur par défaut: {}\nValeur possibles: {}\nVersion: {}")\
                                        .format(attribute,attribute_local_details["translation"],\
                                                    minimum,", ".join(attribute_details["alt(s)"]),\
                                                    attribute_details["default_value"],\
                                                    ", ".join(attribute_details["possible_values"]),\
                                                    attribute_details["version"],)).strip()
        self.attribute_plus_help.short_help['text']=minimum+"..."
        self.complete_help_attribute['text']=complete_help
        
    def update_element_selection(self,*event):
        index=self.model.selected_tab
        current_object=self.model.tabs_html[index]
        current_widget=self.text_fields[index][0]
        selected_item_id=self.elements_in_treeview.selection()[0]
        if self.elements_in_treeview.get_children(selected_item_id):#folder of element
            self.elements_in_treeview.see(self.elements_in_treeview.get_children(selected_item_id)[0])
        else:#element
            element_tag=(self.elements_in_treeview.item(selected_item_id,'value'))[0]
            current_object.last_selected_element=element_tag
            

            previous=self.content_area_form['state']
            self.content_area_form['state']='normal'
            self.content_area_form.delete('1.0', 'end'+'-1c')#Mettre en option
            self.content_area_form['state']=previous
            self.attribute_area_form.delete('1.0', 'end'+'-1c')
            self.elements_in_treeview.heading("element",text=_("Code: ")+element_tag)
            
            
            
            _i=self.specific_attributes_treeview.get_children()
            for item in _i:
                self.specific_attributes_treeview.delete(item)#delete all items in specific_attributes_treeview before
            for couple in ELEMENTS:
                for ele in couple[1]:
                    if ele==element_tag:
                        current_object.last_selected_element_is_void=couple[1][ele]["void"]
                        minimum="{}\n{}\n{}".format(LOCAL_ELEMENTS[element_tag]["description"],LOCAL_ELEMENTS[element_tag]["role"],\
                                                           LOCAL_ELEMENTS[element_tag]["common usage"]).strip()
                        complete_help_element=\
                            _("<{}> ({})\n{}\nAlternatives: {}\nAttributs obligatoires: {}\nAttributs spécifiques: {}\nDois avoir comme parent: {}\nVersion: {}\nElement vide: {}")\
                            .format(element_tag,LOCAL_ELEMENTS[element_tag]["translation"],\
                                        minimum,", ".join(couple[1][ele]["alt(s)"]),\
                                        ", ".join(couple[1][ele]["must_attributes"]),
                                        ", ".join(couple[1][ele]["specific_attributes"]),\
                                        couple[1][ele]["parent"],couple[1][ele]["version"],str(couple[1][ele]["void"])).strip()
                        
                        self.element_plus_help.short_help['text']=minimum+"..."
                        self.complete_help_element['text']=complete_help_element
                        
                        self.content_area_form['state']='normal'
                        if current_object.last_selected_element_is_void:
                            self.content_area_form.insert('end',_("Les éléments vides n'ont pas de contenu"))
                            self.content_area_form['state']='disabled'
                        #todo add must attributes somewhere
                        for attribute in couple[1][ele]["specific_attributes"]:
                                self.specific_attributes_treeview.insert("",'end',values=(attribute,LOCAL_ATTRIBUTES[attribute]["translation"]))#,tags="specific_attribute")
                                
                        break


                
    def confirm_write(self):
        #tab_index=self.model.selected_tab
        #self.text_fields[tab_index][0]  Text
        #self.text_fields[tab_index][1]  close_last_element_button
        tab_index=self.model.selected_tab
        current_object=self.model.tabs_html[tab_index]
        current_text_field=self.text_fields[tab_index][0]
        current_close_last=self.text_fields[tab_index][1]
        
        element_tag=current_object.last_selected_element
        attributes_with_spaces=self.attribute_area_form.get('1.0', 'end'+'-1c').strip()
        if attributes_with_spaces!="":
            attributes_with_spaces=" "+attributes_with_spaces.replace("\n"," ")
        
        if current_object.last_selected_element_is_void:
            text_to_add=current_object.add_indent_and_line(current_object.open_close_void_element(element_tag,attributes_with_spaces))
        else:#if not void
            text_to_add=current_object.add_indent_and_line(current_object.open_element(element_tag, attributes_with_spaces))
            text_to_add+=current_object.add_indent_and_line(self.content_area_form.get('1.0', 'end'+'-1c'))
            if self.var_for_auto_close_checkbutton.get():
                text_to_add+=current_object.add_indent_and_line(current_object.close_element())
        current_object.add_to_text(text_to_add)
        self.tk_copy_text(current_object)

        
        if not current_object.element_still_not_closed_list:
            current_close_last['state']='disabled'
        else:
            current_close_last['state']='active'###
    #todo here put the cursor at the end of what is just added

    
            
    def so_you_decided_to_write_html_directly(self,event):
        tab_index=self.model.selected_tab
        current_object=self.model.tabs_html[tab_index]
        current_text_field=self.text_fields[tab_index][0]
        self.switch_writing_place()
        if current_object.text!=current_text_field.get('1.0', 'end'+'-1c'):
            current_object.text=current_text_field.get('1.0', 'end'+'-1c')
            
    def switch_writing_place(self,*event):#todo redesign this old thing
        tab_index=self.model.selected_tab
        current_object=self.model.tabs_html[tab_index]
        current_text_field=self.text_fields[tab_index][0]
        if self.insertion_tk_var.get():
            #line_before=current_text_field.get('insert'+'-1l', 'insert')
            #CTabulations=line_before.count(indent_var_changed)
            before_cursor_text=current_text_field.get('1.0', 'insert')
            current_object.insertion=len(before_cursor_text)
        else:
            current_object.insertion=None
        
                   
##    def write_in_real_time(self,*event):#TODO
##        try:
##            self.main_text_field.delete("hi")
##        except IndexError:
##            pass
        
    def confirm_close_element(self):
        tab_index=self.model.selected_tab
        current_object=self.model.tabs_html[tab_index]
        current_close_last=self.text_fields[tab_index][1]
        
        if current_object.element_still_not_closed_list:#there is something to close
            text_to_add=current_object.add_indent_and_line(current_object.close_element())
            current_object.add_to_text(text_to_add)
            self.tk_copy_text(current_object)
        else:
            pass
        if current_object.element_still_not_closed_list:#there is still something to close
            pass
        else:
            current_close_last['state']='disabled'
        
#Intern methods called by other or by changing an option --------------###############################
            
    def new_file(self,*event):
        self._prepare_new_session()
    
    def edit_file_dialog(self,*event):
        file_path=filedialog.askopenfilename(defaultextension=".html",initialdir=self.model.guess_dir(),\
                                             filetypes=[("HyperText Mark-Up Language file", "*.html" ), ("All","*.*")])
        #to-do double check if the file exist here because it could have been deleted during the time the user chooses the file
        if file_path:
            self.model.edit_file(file_path)


    def _save_file_dialog(self,*event):
        file_path=filedialog.asksaveasfilename(defaultextension=".html",initialdir=self.model.guess_dir(),\
                                                  filetypes=[("HyperText Mark-Up Language file", "*.html" ),\
                                                                   ("All","*.*")],\
                                                  initialfile=self.model.get_option("last_html_document_title"))
        
        if file_path:
            if self.model._save_html_file_as(file_path):
                #self._mark_as_not_modified()
                return True
        return False
    
    def save_file_to_test_control(self,*event):#Try with CTRL+Shift+T
        self.model.save_file_totest()
        
    

    
        
    def tk_copy_text(self,text_to_copy,new=False):
        index=self.model.selected_tab
        if  new:
            title=self.model.get_option("last_html_document_title")
            self.new_html_tab(index,title)

        
        current_widget=self.text_fields[index][0]
        #self._mark_as_modified()
        current_widget.delete('1.0', 'end'+'-1c')
        current_widget.insert('end',text_to_copy)
        current_widget.yview("moveto","1.0")
        
    def set_translation(self):
        self.model.set_option("translate_html_level",self.translate_html_level_tk_var.get())

    def set_indent_size(self):
        if self.indent_size_tk_var.get()== -1:
            self.model.set_option("indent_size",1)
            self.model.set_option("indent_style","\t")
        else:
            self.model.set_option("indent_size",self.indent_size_tk_var.get())
            self.model.set_option("indent_style"," ")
        
    

    
        

#Mostly visual and not important --------------###############################
            

        
    def drag_start(self,event):
        self.drag_element=self.elements_in_treeview.set(self.elements_in_treeview.identify_row(event.y),column="element")
    def drag_and_drop_visual(self,event):
        if self.drag_element!="":
            try:
                self.info.reset_position(event.x,event.y)
            except AttributeError:
                self.info=DragDropFeedback(parent=None,text="<%s>" % self.drag_element, x=event.x, y=event.y)
                
##            self.drop_menu = Menu(event.widget, tearoff=0, takefocus=0)
##            self.drop_menu.add_command(label=self.drag_element)
##            self.drop_menu.tk_popup(event.x_root+42, event.y_root+10,entry="0")
        
    def drop_end(self,event):
        try:
            self.info.destroy()
            del self.info
        except AttributeError:
            pass
        tab_index=self.model.selected_tab
        current_object=self.model.tabs_html[tab_index]
        current_text_field=self.text_fields[tab_index][0]
        if self.drag_element!="" and self.winfo_containing(event.x_root,event.y_root) is current_text_field:            
            line_dot_char=current_text_field.index("@%s,%s" % (event.x, event.y))
            current_object.insertion=len("\n".join(current_object.text.split("\n")[0:int(line_dot_char.split(".")[0])]))
            self.confirm_write()
