#!/usr/bin/python
#-*-coding:utf-8*

#HTMLFrame.py
#Role: Define the HTML specific tools in tkinter

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
from tks_widgets_1 import *

def _(l_string):
    return l_string
wrap=420
class HTMLFrame(tk.Frame):
    """HTML  frame."""

    def __init__(self, parent, master_window, model, adapted_height):
        tk.Frame.__init__(self, parent)
        self.model = model
        self.master_window = master_window
        
        self.last_selected_element = "p"
        self.last_selected_element_is_void = False
        #self.master_window == model.graphical_user_interface_   (same object) use notation 1

        self.autoclose_element_check_variable = tk.BooleanVar(value=True)

        #elements 
        frame_element_master = tk.Frame(self, FRAME_STYLE_2, bg=COLOURS_A[0])
        self.element_plus_help = MainPlusHelp(frame_element_master, _("Balises"), _("Aide"))
        self.elements_in_treeviews_lift = ttk.Scrollbar(self.element_plus_help.main_frame)
        self.elements_in_treeview = ttk.Treeview(self.element_plus_help.main_frame,
            selectmode='browse', columns=("element", "local"), height=adapted_height,
            cursor="hand2", yscrollcommand=self.elements_in_treeviews_lift.set,
            padding=0, takefocus=True, displaycolumns=(1, 0), show='headings')#,show='tree'.
        
        
        self.element_plus_help.next_ = next_gen(self.elements_in_treeview)
        self.element_plus_help.previous = prev_gen(self.elements_in_treeview)
        self.elements_in_treeview.column("#0", width=20, stretch=False)
        self.elements_in_treeview.heading("local", text=_("Traduction"))
        self.elements_in_treeview.column("local", minwidth=100)
        self.elements_in_treeview.heading("element", text=_("Code"))
        self.elements_in_treeview.bind('<<TreeviewSelect>>', self.update_element_selection)
        self.elements_in_treeview.bind('<Button-1>', self.drag_start, add='+')
        self.elements_in_treeview.bind("<B1-Motion>", self.drag_and_drop_visual,  add='+')
        self.elements_in_treeview.bind('<ButtonRelease-1>', self.drop_end, add='+')
        self.elements_in_treeviews_lift.config(command=self.elements_in_treeview.yview)
        #_List of elements:
        i = 0
        tags = ["tag_1","tag_2"]
        self.elements_in_treeview.tag_configure("tag_1", background='#cccfff')
        self.elements_in_treeview.tag_configure("tag_2", background='#cfffcc')
        self.elements_in_treeview.tag_configure("tag_3", background='#ffccbc')
        categories_treeview_part = {}
        for element in ELEMENTS:
            category_name = ELEMENTS[element]["category"]
            if category_name not in categories_treeview_part:
                categories_treeview_part[category_name] = self.elements_in_treeview.insert("",'end',
                    values=("",category_name),tag=tags[i%2])
                i+=1
            self.elements_in_treeview.insert(categories_treeview_part[category_name],'end',
                values=(element,LOCAL_ELEMENTS[element]["translation"]),tag="tag_3")

        self.elements_in_treeview.grid(row=0,column=0,columnspan=2,sticky='nsw')
        self.elements_in_treeviews_lift.grid(row=0,column=2,sticky='nsw')


        #attributes
        frame_attribute_master = tk.Frame(self,FRAME_STYLE_2,bg=COLOURS_A[1])#attributes
        self.attribute_plus_help = MainPlusHelp(frame_attribute_master,_("Attributs"),_("Aide"))
        #_List of attributes:
        self.general_attributes_treeview = ttk.Treeview(self.attribute_plus_help.main_frame,selectmode='browse',\
                                        height=adapted_height,columns=("real","local"),displaycolumns=(1),show='headings')
        
        self.attribute_plus_help.next_ = next_gen(self.general_attributes_treeview)
        self.attribute_plus_help.previous = prev_gen(self.general_attributes_treeview)
        self.general_attributes_treeview.heading("local",text=_("Général"))
        self.general_attributes_treeview.grid(row=0,column=0,sticky='w')
        for general_attribute in GENERAL_ATTRIBUTES_LIST:
            self.general_attributes_treeview.insert("",'end',values=(general_attribute,LOCAL_ATTRIBUTES[general_attribute]["translation"]))
        self.general_attributes_treeview.bind('<<TreeviewSelect>>',self.update_attribute_selection,"")
        
        self.specific_attributes_treeview = ttk.Treeview(self.attribute_plus_help.main_frame,
            selectmode='browse',height=adapted_height,columns=("real","local"),displaycolumns=(1),show='headings')
        self.specific_attributes_treeview.heading("local",text=_("Spécifique"))
        #self.specific_attributes_treeview.tag_configure("specific_attribute")not here later make tag ofr must and specifiq in different colours
        self.specific_attributes_treeview.grid(row=0,column=1,sticky='w')
        self.specific_attributes_treeview.bind('<<TreeviewSelect>>',self.update_attribute_selection,"")

        
        #Help element
        frame_element_help_labels = ttk.Frame(self.element_plus_help.help_frame)
        frame_element_help_labels.for_data_type = "html_element"
        frame_element_help_labels.grid(row=0,column=0,columnspan=3)
        str_list_help = ["element", "alt(s)", "must_attributes", "version",
            "parent", "specific_attributes", "void"]
        str_list_help_local = ["translation", "description", "role", "common usage"]
        self.help_element, self.help_element_local = {}, {}
        i = 0
        #wraplength=wrap)
        for string in str_list_help:
            self.help_element[string] = LabelString(frame_element_help_labels,
                string=string, text=_(u""), wraplength=wrap)
            self.help_element[string].grid(row=i,column=0,sticky='nswe')
            self.help_element[string].bind('<Button-3>',local_menu_print)
            i += 1
        for string in str_list_help_local:
            self.help_element_local[string] = LabelString(frame_element_help_labels,
                string=string, text=_(u""), wraplength=wrap)
            self.help_element_local[string].grid(row=i,column=0,sticky='nswe')
            self.help_element_local[string].bind('<Button-3>',local_menu_print)
            i += 1
        #Help attribute this is  a copy from here to #Help element
        frame_attribute_help_labels = ttk.Frame(self.attribute_plus_help.help_frame)
        frame_attribute_help_labels.for_data_type = "html_attribute" #see tks_widgets_1
        frame_attribute_help_labels.grid(row=0,column=0,columnspan=3)
        str_list_help = ["attribute", "alt(s)", "default_value", "version", "possible_values"]
        str_list_help_local = ["translation", "description", "role", "common usage"]
        self.help_attributes, self.help_attributes_local = {}, {}
        i = 0
        for string in str_list_help:
            self.help_attributes[string] = LabelString(frame_attribute_help_labels,
                                                       string=string, text=_(u""),
                                                       wraplength=wrap)
            self.help_attributes[string].grid(row=i,column=0,sticky='nswe')
            self.help_attributes[string].bind('<Button-3>',local_menu_print)
            i += 1
        for string in str_list_help_local:
            self.help_attributes_local[string] = LabelString(frame_attribute_help_labels,string=string, text=_(u""))
            self.help_attributes_local[string].grid(row=i,column=0,sticky='nswe')
            self.help_attributes_local[string].bind('<Button-3>',local_menu_print)
            i += 1
            
                
        #user input
        frame_2_user_input = tk.Frame(self, FRAME_STYLE_2,bg=COLOURS_A[2])
        help_label_for_content = ttk.Label(frame_2_user_input,text=_("Ecrivez le contenu"))
        help_label_for_content.grid(row=0,column=0,sticky='nw')
        help_label_for_attribute = ttk.Label(frame_2_user_input, text=_("Placez les attributs"))
        help_label_for_attribute.grid(row=0,column=1,sticky='nw')

        height_c = int(float(adapted_height)/4.0)
        self.content_area_form = tk.Text(frame_2_user_input,ENTRY_STYLE,width=42,height = height_c)
        self.content_area_form.grid(row=1,column=0,sticky='nw')
        self.content_area_form.bind('<Button-3>',create_context_menu)
        self.attribute_area_form = tk.Text(frame_2_user_input,ENTRY_STYLE,width=40,height = height_c)
        self.attribute_area_form.grid(row=1,column=1,sticky='nw')
        self.attribute_area_form.bind('<Button-3>',create_context_menu)
        #self.content_area_form.bind('<KeyRelease>',write_in_real_time)

        self.confirm_add_button = ttk.Button(frame_2_user_input, text=_("Confirmer"),command=self.confirm_write)
        self.confirm_add_button.grid(row=2,column=0,sticky='nw')

        self.var_for_auto_close_checkbutton = tk.BooleanVar(value=True)
        self.auto_close_checkbutton = ttk.Checkbutton(frame_2_user_input, text=_("Fermer la balise"),variable=self.var_for_auto_close_checkbutton)
        self.auto_close_checkbutton.grid(row=2,column=1,sticky='nw')
        

        #HTML tabs
        

        self.master_window._treeviews = self.master_window._treeviews+[self.elements_in_treeview,self.general_attributes_treeview,self.specific_attributes_treeview]
        #keep this do work around a ttk bug: growing treeviews
        
        #self.columnconfigure(0,weight=1)
        #self.rowconfigure(0,weight=1)
        
        frame_element_master.grid(row=0,column=0,sticky='nsw')
        frame_attribute_master.grid(row=0,column=1,sticky='nsw')
        frame_2_user_input.grid(row=1,column=0,columnspan=2,sticky='nsw')
        
    def update_attribute_selection(self,event):
        selected_item_id = event.widget.selection()[0]
        attribute = (event.widget.item(selected_item_id,'value'))[0]
        attribute_details = ATTRIBUTES[attribute]
        attribute_local_details = LOCAL_ATTRIBUTES[attribute]
        if not attribute in self.attribute_area_form.get('1.0','end-1c'):
            self.attribute_area_form.insert('end',"{}=\"{}\"\n".format(attribute,attribute_details["default_value"]))

        minimum = "{}\n{}\n{}".format(attribute_local_details["description"],
            attribute_local_details["role"],
            attribute_local_details["common usage"]).strip()
        
        self.attribute_plus_help.short_help['text'] = minimum
        self.help_attributes["attribute"]['text'] = attribute
        self.help_attributes["alt(s)"]['text'] = user_stringify(attribute_details["alt(s)"])
        self.help_attributes["default_value"]['text'] = user_stringify(attribute_details["default_value"])
        self.help_attributes["version"]['text'] = user_stringify(attribute_details["version"])
        self.help_attributes["possible_values"]['text'] = user_stringify(attribute_details["possible_values"])
        
        self.help_attributes_local["translation"]['text'] = attribute_local_details["translation"]
        self.help_attributes_local["description"]['text'] = attribute_local_details["description"]
        self.help_attributes_local["common usage"]['text'] = attribute_local_details["common usage"]
        self.help_attributes_local["role"]['text'] = attribute_local_details["role"]
        
    def update_element_selection(self,*event):
        tree = self.elements_in_treeview
        index = self.model.selected_tab
        current_object = self.model.tabs_html[index]
        selected_item_id = tree.selection()[0]
        if tree.get_children(selected_item_id):#folder of element
            tree.item(selected_item_id, open=not(tree.item(selected_item_id, "open")))
            return
        
        #else element
        element_tag = (tree.item(selected_item_id,'value'))[0]
        if element_tag == self.last_selected_element:
            return
        self.last_selected_element = element_tag
        self.content_area_form.delete('1.0','end-1c')#this should be optional
        self.attribute_area_form.delete('1.0','end-1c')
        tree.heading("element",text = _(u"Code: {}").format(element_tag))
        
        
        #delete all items in specific_attributes_treeview before displaying the new
        displayed_specific_attributes = self.specific_attributes_treeview.get_children()
        for item in displayed_specific_attributes:
            self.specific_attributes_treeview.delete(item)
        
        html_element = ELEMENTS[element_tag]
        self.last_selected_element_is_void = html_element["void"]
        minimum = u"{}\n{}\n{}".format(LOCAL_ELEMENTS[element_tag]["description"],LOCAL_ELEMENTS[element_tag]["role"],\
                                           LOCAL_ELEMENTS[element_tag]["common usage"]).strip()
        self.element_plus_help.short_help['text'] = minimum

        #only alt(s) is somehow formated to be seen
        self.help_element["element"]['text'] =  element_tag
        self.help_element["alt(s)"]['text']  =  user_stringify(html_element["alt(s)"])
        self.help_element["must_attributes"]['text'] = user_stringify(html_element["must_attributes"])
        self.help_element["specific_attributes"]['text'] = user_stringify(html_element["specific_attributes"])
        self.help_element["parent"]['text']  =  user_stringify(html_element["parent"])
        self.help_element["version"]['text'] =  user_stringify(html_element["version"])
        self.help_element["void"]['text'] = user_stringify(html_element["void"])
        
        self.help_element_local["translation"]['text'] = LOCAL_ELEMENTS[element_tag]["translation"] 
        self.help_element_local["description"]['text'] = LOCAL_ELEMENTS[element_tag]["description"]
        self.help_element_local["role"]['text'] =        LOCAL_ELEMENTS[element_tag]["role"]
        self.help_element_local["common usage"]['text'] = LOCAL_ELEMENTS[element_tag]["common usage"]
        
        self.content_area_form['state'] = 'normal'
        if self.last_selected_element_is_void:
            self.content_area_form.insert('end',_("Les éléments vides n'ont pas de contenu"))
            self.content_area_form['state'] = 'disabled'
        #todo add must attributes somewhere
        for attribute in html_element["specific_attributes"]:
            try:
                self.specific_attributes_treeview.insert("",'end',values = (attribute,LOCAL_ATTRIBUTES[attribute]["translation"]))#,tags="specific_attribute")
            except KeyError:
                pass #the key is not found in the data (that the user can change)


                
    def confirm_write(self):
        """Adds to the text the selected code from the gui.

Ignores identation !"""
        #self.text_fields[tab_index][0]  Text
        #self.text_fields[tab_index][1]  close_last_element_button

        element_tag = self.last_selected_element
        attributes_with_spaces = self.attribute_area_form.get('1.0', 'end-1c').strip()
        
        html_fragment = self.model.return_fragment("html")
        current_close_last = self.master_window.text_fields[self.model.selected_tab][1]
        
        enteredText = self.content_area_form.get('1.0','end-1c')

        translate_html_level = self.model.get_option("translate_html_level")
        # all 10 , minimum 1 , nothing 0

        
        if translate_html_level > 0:
            translated = html_fragment.escapeHTML(enteredText, translate_html_level)
        else:
            translated = enteredText

        
        if attributes_with_spaces != "":
            attributes_with_spaces = " "+attributes_with_spaces.replace("\n"," ")
        
        if self.last_selected_element_is_void:
            text_to_add = html_fragment.open_close_void_element(element_tag,attributes_with_spaces)
        else:
            text_to_add = html_fragment.open_element(element_tag, attributes_with_spaces) + translated
            if self.var_for_auto_close_checkbutton.get():
                text_to_add += html_fragment.close_element(element_tag)
        cursor_position = self.master_window.get_cursor_position()
        html_fragment.insert(text_to_add, cursor_position)
        #do same on textfield
        self.master_window.tk_insert_text(text_to_add, cursor_position)
    #todo here put the cursor at the end of what is just added

        
#Intern methods called by other or by changing an option --------------###############################
        
    def set_translation(self):
        self.model.set_option("translate_html_level",self.translate_html_level_tk_var.get())

    
        
    

#Mostly visual and not important --------------###############################
            

        
    def drag_start(self,event):
        self.drag_element = self.elements_in_treeview.set(self.elements_in_treeview.identify_row(event.y),column="element")
    def drag_and_drop_visual(self,event):
        if self.drag_element != "":
            try:
                self.info.reset_position(event.x_root,event.y_root)
            except AttributeError:
                self.info = DragDropFeedback(parent=None,text="<{}>".format(self.drag_element), x=event.x_root, y=event.y_root)
                

        
    def drop_end(self,event):
        try:
            self.info.destroy()
            del self.info
            tab_index = self.model.selected_tab
            current_object = self.model.tabs_html[tab_index]
            current_text_field = self.master_window.text_fields[tab_index][0]
            if self.drag_element != "" and self.winfo_containing(event.x_root,event.y_root) is current_text_field:            
                line_dot_char = current_text_field.index("@%s,%s" % (event.x, event.y))
                line = int(line_dot_char.split(".")[0])
                current_object.insertion = len("\n".join(
                    current_object.text.split("\n")[0:line]
                ))
                self.confirm_write()
        except AttributeError:
            pass

