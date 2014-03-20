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
import codecs
import os

##DATA##
from tutorial import detect_existing_tutorials,start_tutorial
#from file_extractor import*
##STYLES##
from tks_styles import*
##LOG##
from log_writer import log_writer
##Window##
from HTMLWindows import HTMLWindows


def _(l_string):
    #print("local language: "+l_string)
    return l_string
class GraphicalUserInterfaceTk(tk.Tk):
    """tkinter interface for WebSpree.

"""

#methods that changes something important --------------###############################
    
    def __init__(self,model):
        tk.Tk.__init__(self)
        self.model=model
        self.title(MAIN_TITLE)
        #self.attributes('-fullscreen', 1)#, '-topmost', 1)fullscreen #doesnt exist everywhere
        #self.geometry('1700x600+0+0')#static size is bad, it doesn t adapt
        self.configure(bd=1,bg=WINDOW_BACK_COLOR)
        #self.iconbitmap(LOGO1_PATH)#problems here, icon should be insert when freezing the app not here
        self.bind('<Control-plus>',self.change_size)
        self.bind('<Control-minus>',self.change_size)
        self.bind('<Control-0>',self.change_size)
        self.bind('<Control-Shift-A>',self.save_all)
        
        #image is ready for tkinter
        self.HTML5_PHOTO_ICO = tk.PhotoImage(file=os.path.normpath("images/icos/HTML5_Badge_32.gif"))
        self.CSS3_PHOTO_ICO = tk.PhotoImage(file=os.path.normpath("images/icos/CSS3_Badge_32.gif"))
        self.JS_PHOTO_ICO = tk.PhotoImage(file=os.path.normpath("images/icos/js32.gif"))
        #self.plus_image = tk.PhotoImage(file=os.path.normpath("images/widgets/plus_1.gif"))
        intern_root=tk.Frame(self)#this is almost the root
        self.group_app_tabs=ttk.Notebook(intern_root)#this contains every tab,html,css,...
        self.group_app_tabs.enable_traversal()
        self.current_font=tkfont.Font(family='helvetica', size=-15)
        mystyle=ttk.Style()
        mystyle.configure('.',font=self.current_font)

        #keep this do work around a ttk bug: growing treeviews
        self._treeviews=[]
        self.html_window=HTMLWindows(self.group_app_tabs,self,model)#html frame
        self.frame_of_frames_css=tk.Frame(self.group_app_tabs)#css frame
        self.frame_of_frames_js=tk.Frame(self.group_app_tabs)#js frame
        
        self.group_app_tabs.add(self.html_window,text="HTML",image=\
                                self.HTML5_PHOTO_ICO,compound='left',underline=0)
        self.group_app_tabs.add(self.frame_of_frames_css,text="CSS",image=\
                                self.CSS3_PHOTO_ICO,compound='left',underline=0)
        self.group_app_tabs.add(self.frame_of_frames_js,text="JavaScript",image=\
                                self.JS_PHOTO_ICO,compound='left',underline=0)
        tk.Label(self.frame_of_frames_js,text='coming VERY soon . really.').pack()
        tk.Label(self.frame_of_frames_css,text='coming soon ...').pack()
        
        

        self.protocol("WM_DELETE_WINDOW", self.intercept_close)
        ######----Menus-----######
        FILEMENU={}
        FILEMENU["name"]=_("Fichier")
        FILEMENU["command"]=[{'label':_("Nouveau [Ctrl+N]"),'command':self.html_window.new_file},\
                             {'label':_("Ouvrir [Ctrl+O]"),'command':self.html_window.edit_file_dialog},\
                             {'label':_("Enregistrer [Ctrl+S]"),'command':lambda: self.html_window.model.save_html_file()},\
                             {'label':_("Enregistrer sous[Ctrl+Shift+S]"),'command':lambda: self.html_window._save_file_dialog()},\
                             {'label':_("Enregistrer tout [Ctrl+Shift+A]"),'command':lambda: self.save_all("forced_arg")},\
                             {'label':_("Essayer ! [Ctrl+Shift+T]"),'command':lambda: self.html_window.save_file_to_test_control()},\
                             {'label':_("Fermer Onglet [Ctrl+W]"),'command':lambda: self.html_window.close_tab(("easy"))},\
                             {'label':_("Quitter"),'command':lambda: self.intercept_close()}]
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

        self.html_window.translate_html_level_tk_var=tk.IntVar(value=self.model.get_option("translate_html_level"))
        if self.model.get_option("indent_style")=="\t":
            self.html_window.indent_size_tk_var=tk.IntVar(value=-1)
        else:
            self.html_window.indent_size_tk_var=tk.IntVar(value=self.model.get_option("indent_size"))
        OPTIONMENU={}
        OPTIONMENU["name"]=_("Options")
        OPTIONMENU["command"]=[]
        OPTIONMENU["radiobutton"]=[{'label':_("Remplacer tout caractère spécial"),\
                                    'command':self.html_window.set_translation,'value':10,"variable":self.html_window.translate_html_level_tk_var},\
                                   {'label':_("Remplacer le minimum"),\
                                    'command':self.html_window.set_translation,'value':1,"variable":self.html_window.translate_html_level_tk_var},\
                                   {'label':_("Remplacer aucun caractère spécial"),\
                                    'command':self.html_window.set_translation,'value':0,"variable":self.html_window.translate_html_level_tk_var},\
                                   {'label':_("Indenter avec 2 espaces"),\
                                    'command':self.html_window.set_indent_size,'value':2,"variable":self.html_window.indent_size_tk_var},\
                                   {'label':_("Indenter avec 3 espaces"),\
                                    'command':self.html_window.set_indent_size,'value':3,"variable":self.html_window.indent_size_tk_var},\
                                   {'label':_("Indenter avec 4 espaces"),\
                                    'command':self.html_window.set_indent_size,'value':4,"variable":self.html_window.indent_size_tk_var},\
                                   {'label':_("Indenter avec 8 espaces"),\
                                    'command':self.html_window.set_indent_size,'value':8,"variable":self.html_window.indent_size_tk_var},\
                                   {'label':_("Indenter avec des tabulations"),\
                                    'command':self.html_window.set_indent_size,'value':-1,"variable":self.html_window.indent_size_tk_var}]
        #([{'label':_("Compact"),'command':self.change_mapping,'value':True,"variable":self.small_layout},
                                    #{'label':_("Etendu"),'command':self.change_mapping,'value':False,"variable":self.small_layout}])
        TUTORIALMENU={}
        TUTORIALMENU["name"]=_("Tutoriel")
        TUTORIALMENU["command"]=[]
        tutorial_finished=self.model.get_option("tutorial_finished")
        for name,folder in detect_existing_tutorials():
            c="#e5e5e5"#near white
            expl=""
            if folder in tutorial_finished:
                c="#46a717"#green
                expl=_(" (tutoriel terminé)")
            TUTORIALMENU["command"].append({'label':name+expl,"bg":c,'command':lambda: start_tutorial(folder,self)})
        
        TUTORIALMENU["radiobutton"]=[]
        
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
        ALL_MENUS=[FILEMENU,EDITMENU,VIEWMENU, OPTIONMENU, TUTORIALMENU,HELPMENU]
        top=self.winfo_toplevel()#for macs menu to render as users are used to
        self.Menus_tk=tk.Menu(top)
        top['menu']=self.Menus_tk
        sub_menu_list=[]
        #All_MENU_ITEM_OPTION={'activebackground':"blue"}
        
        #This loop creates the menus described just before. from dicts to menus of menus
        for index,submenu in enumerate(ALL_MENUS):
            sub_menu_list.append(tk.Menu(self.Menus_tk,tearoff=0))#,tearoff=0 disables the popopable menu item with the dottet bar
            self.Menus_tk.add_cascade(label=submenu["name"], menu=sub_menu_list[index],underline=0)
            for command_ in submenu["command"]:
                c="white"
                if 'bg' in command_:
                    c=command_['bg']
                sub_menu_list[len(sub_menu_list)-1].add_command(label=command_["label"], command=command_["command"],background=c,activebackground="blue")
            for radiobutton_ in submenu["radiobutton"]:
                sub_menu_list[len(sub_menu_list)-1].add_radiobutton(label=radiobutton_["label"], command=radiobutton_["command"],\
                                                                    variable=radiobutton_["variable"],value=radiobutton_["value"],activebackground="blue")


    
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.group_app_tabs.grid()
        intern_root.grid(row=0,column=0,sticky='snew')
        intern_root.columnconfigure(0,weight=2)
        intern_root.rowconfigure(0,weight=2)
        
    def _start(self):
        if not self.model.get_option("license_accepted_and_read"):
            self.view_license(already_accepted=False)
        log_writer("width",self.winfo_screenwidth())
        log_writer("height",self.winfo_screenheight())
        self.mainloop()
        
    def _end(self):
        self.destroy()

    def save_all(self,*event):
        m="for_save"
        if event:#called directly
            m="for_save_no_warning"
        #change this with css
        for tab_not_closed_index in range(len(self.model.tabs_html)-1,-1,-1):#we save all tabs or cancel
            self.html_window.html_text_tabs.select(tab_not_closed_index)
            self.model.selected_tab=tab_not_closed_index
            close_all=self.html_window.close_tab((m))
            if close_all=="cancel":
                return close_all
        return "no_cancel"
    
    def intercept_close(self):
        #change this with css
        if self.save_all() != "cancel":
            path_list=[]
            for tab_not_closed_index in range(len(self.model.tabs_html)-1,-1,-1):#we close all tabs and save the location for the next time
                if self.model.tabs_html[tab_not_closed_index].get_save_path():
                    path_list.insert(0,self.model.tabs_html[tab_not_closed_index].get_save_path())
                self.html_window.html_text_tabs.select(tab_not_closed_index)
                self.model.selected_tab=tab_not_closed_index
                self.html_window.close_tab(("already_saved"))
            self.model.set_option("previous_files_opened",path_list)
            self._end()
    
    def view_license(self,already_accepted=False):
        license_window=tk.Toplevel(self,bd=1,bg=WINDOW_BACK_COLOR)
        license_window.title("LICENSE")
        LICENSE=codecs.open("LICENSE.txt",'r','utf-8').read()
        license_text=tk.Text(license_window)
        license_text.grid(column=0,row=0)
        license_text.insert('end',LICENSE)
        
        LICENSE_NOTICE=codecs.open(os.path.normpath("Documentation/notice_license.txt"),'r','utf-8').read()
        License_notice_text=tk.Text(license_window)
        License_notice_text.grid(column=1,row=0)
        License_notice_text.insert('end',LICENSE_NOTICE)
        license_window.lift(self)
        
        if not already_accepted:
            license_window.grab_set()
            license_window.focus_set()
            license_window.focus_force()#force focus
            def accept(self):
                self.model.set_option("license_accepted_and_read",True)
                license_window.destroy()
                self.html_window._prepare_new_session()

            def refuse(self):
                self.model.set_option("license_accepted_and_read",False)
                self._end()
            
            license_window.protocol("WM_DELETE_WINDOW", lambda:refuse(self))
            
            accept_button=tk.Button(license_window,text=_("Accepter"),command=lambda:accept(self))
            accept_button.grid(column=0,row=1)
            refuse_button=tk.Button(license_window,text=_("Refuser"),command=lambda:refuse(self))
            refuse_button.grid(column=0,row=2)
            
    def change_size(self,event):
        #treeview is growing, even with control- fix it with something like that
        #self.elements_in_treeview['width']=25
        try:
            equivalent=event.keysym#when someone zooms with keyboard
        except AttributeError:
            equivalent=event#zoom with something else (menu old-style)

        for treeview in self._treeviews:
            treeview.column("local",width=200)
        if equivalent== '0':
            self.current_font['size']= -15
        elif equivalent == 'plus':
            if self.current_font['size'] > -60:
                self.current_font['size'] -= 1
        elif equivalent == 'minus':
            if self.current_font['size'] < -7:
                self.current_font['size'] += 1
    def lock_tutorial(self):
        #TODO when a tutorial starts, lock all tutorial.
        #to unlock you have to say yes to a cancelyes dialog
        #this fun is already linked correctly
        pass
