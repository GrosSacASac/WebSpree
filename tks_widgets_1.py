#! /usr/bin/python
#-*-coding:utf-8*

#tks_widgets_1.py
#Role: Define custom tools for tkinter

#Walle Cyril
#11/05/2014

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

#DragDropFeedback
#MainPlusHelp
#, next_gen, prev_gen
#InformationBubble
#HyperLink
#and more
import webbrowser

try:#3.X
    import tkinter as tk
    import tkinter.ttk  as ttk
    import tkinter.font as tkfont
except ImportError:#2.X
    import Tkinter as tk
    import ttk as ttk
    import tkFont as tkfont


from tks_styles import*
def _(l_string):
    #print("local language: "+l_string)
    return l_string

class MainPlusHelp(ttk.Notebook):
    def __init__(self,parent,title_content,title_help):
        ttk.Notebook.__init__(self,parent)
        self.parent = parent

        self.main_frame=tk.Frame(self,FRAME_STYLE_2)
        self.help_frame=tk.Frame(self,FRAME_STYLE_2)
        self.add(self.main_frame,text=title_content,sticky='swen')
        self.add(self.help_frame,text=title_help,sticky='swen')

        self.short_help=tk.Label(self.main_frame,HELP_LABEL_STYLE, text=_("Cliquer sur un objet pour avoir de l'aide..."), wrap=400,anchor='nw',fg='#2220dd')
        self.short_help.grid(row=1,column=0,columnspan=2,sticky='nsw')
        self.short_help.bind('<ButtonRelease-1>', self.switch_help)
        self.short_help['cursor']="hand2"
        
        more_help_button=ttk.Button(self.main_frame, text=_("Plus d'aide"))
        more_help_button.grid(row=2,column=0,sticky='nswe',columnspan=3)
        more_help_button.bind('<ButtonRelease-1>', self.switch_help)

        help_frame_bottom=tk.Frame(self.help_frame)#,FRAME_STYLE_2)
        help_frame_bottom.grid(row=1,column=0)
        self.previous_help=ttk.Button(help_frame_bottom, text=_("Précédent"),command=self.previous)
        self.previous_help.grid(row=1,column=0,sticky='nswe')
        self.next_help=ttk.Button(help_frame_bottom, text=_("Suivant"),command=self.next_)
        self.next_help.grid(row=1,column=2,sticky='nswe')
        leave_help=ttk.Button(help_frame_bottom, text=_("Quitter l'aide"))
        leave_help.grid(row=1,column=1,sticky='nswe')        
        leave_help.bind('<ButtonRelease-1>', self.switch_help)
        self.grid(sticky='nswe')
        
    def switch_help(self,event):
        def toogle_index(i):#0 becomes 1 and 1 becomes 0
            return int(not i)
        w=event.widget
        current_tab=w.nametowidget(w.winfo_parent())
        try:
            not_current_tab_as_index=toogle_index(self.index(current_tab))
        except tk.TclError:
            not_current_tab_as_index=toogle_index(self.index(current_tab.nametowidget(current_tab.winfo_parent())))
        self.select(not_current_tab_as_index)
        #redirect to the correct help tab
        
    #overwrite those
    def next_(self):
        pass
    def previous(self):
        pass

    #when those are overwritten the next and previous button will be updated to call the right function
    @property
    def next_(self,):
        pass
    
    @next_.setter
    def next_(self,function):
        self.next_help['command']=function
        
    @property
    def previous(self,):
        pass
    
    @previous.setter
    def previous(self,function):
        self.previous_help['command']=function

#external methods for main plus help with a treeview inside
def next_gen(t):
    def next_():
        if t.selection()=="":
            t.selection_set(t.get_children()[0])
        if t.get_children(t.selection()[0]):#if folder of element
            next_item=(t.get_children(t.selection()[0])[0])# we take the first child
        else:
            next_item=t.next(t.selection()[0])
            if next_item=="":#if it was the last
                #we take the parent's next,who is also a parent and then take the first child of it
                next_item=t.next(t.parent(t.selection()[0]))
                if next_item=="":#we re at the very end
                    next_item=(t.get_children(next_item)[0])
                try:#polyvalence
                    next_item=(t.get_children(next_item)[0])
                except IndexError:
                    pass
        t.selection_set(next_item)
        t.see(next_item)
        #elf.update_element_selection() # is called when selection changes
    return next_

def prev_gen(t):
    def prev_():
        if t.selection()=="":
            t.selection_set(t.get_children()[0])
        if t.get_children(t.selection()[0]):#if folder of element
            prev_item=(t.get_children(t.prev(t.selection()[0]))[-1])# we take the last child of prev
        else:
            prev_item=t.prev(t.selection()[0])
            if prev_item=="":#if it was the first
                prev_item=t.prev(t.parent(t.selection()[0]))
                if prev_item=="":
                    prev_item=(t.get_children(prev_item)[-1])
                try:#polyvalence
                    prev_item=(t.get_children(prev_item)[-1])
                except IndexError:
                    pass
        t.selection_set(prev_item)
        t.see(prev_item)
        #elf.update_element_selection() # is called when selection changes
    return prev_
        
class HyperLink(tk.Label):
    def __init__(self,parent,URL,text):
        tk.Label.__init__(self,parent,text=text)
        if not (URL=="" and text==""):
            self.URL=URL

            #underline font and blue it
            font=tkfont.Font(self, self.cget('font'))
            font['underline'] = True
            self['font']=font
            self['fg']="blue"

            #change cursor
            self['cursor']="hand2"
            self.bind('<ButtonRelease-1>',self.open_link)
        
    def open_link(self,event):
        #if the pointer is still on the link when click released
        if self.winfo_containing(event.x_root,event.y_root) is self:
            webbrowser.open_new_tab(self.URL)
        
class DragDropFeedback(tk.Toplevel):
    def __init__(self,parent=None,text="no text given", x=0, y=0):
        tk.Toplevel.__init__(self,parent,bd=0,bg='#333300')
        self.reset_position(x,y)
        tk.Label(self,text=text,anchor='center').pack(side='top')
        self.overrideredirect(1)#L'objet n as pas le contour d'une fenetre
    def reset_position(self,x,y):
        self.geometry('200x25+%d+%d' % (0+x,0+y))
def cut(event):
    event.widget.event_generate('<Control-x>')
    event.widget.event_generate('<KeyRelease>')
def copy(event):
    event.widget.event_generate('<Control-c>')
    event.widget.event_generate('<KeyRelease>')
def paste(event):
    event.widget.event_generate('<Control-v>')
    event.widget.event_generate('<KeyRelease>')

class handler(object):
    def __init__(self,function,*event):
        self.function=function
        self.event=event
    def __call__(self, *args):
        return self.function(*self.event +args)
        
def create_context_menu(event):
    """Opens a context menu with right click."""
    tools=[(_("Couper"), handler(cut,event)),
           (_("Copier"), handler(copy,event)),
           (_("Coller"), handler(paste,event))]

    context_menu = tk.Menu(event.widget, tearoff=0, takefocus=0)
    for (text, action) in tools:
        context_menu.add_command(label=text, command=action)
    context_menu.tk_popup(event.x_root+42, event.y_root+10,entry="0")
    event.widget.focus()


class InformationBubble(tk.Toplevel):#broken do not use
    def __init__(self,parent=None,texte="", DecalageX=20, DecalageY=0):
        #I deleted this becuase it was full of bugs and impolite
        pass
        
if __name__ == '__main__':#essay
    root=tk.Tk()
    F1=tk.LabelFrame(root, FRAME_STYLE,text="links")
    F2=tk.LabelFrame(root, FRAME_STYLE,text="LabelFrame_2")
    F3=tk.LabelFrame(root, FRAME_STYLE,text="test")
    F4=tk.LabelFrame(root, FRAME_STYLE,text="main and help")

    H=HyperLink(F1,URL="www.python.org",text="PYTHON");H.grid()
    H2=HyperLink(F1,URL="www.wikipedia.org",text="wikipedia !!!");H2.grid()
    #AideLien = InformationBubble(parent=H2,texte="Lien sans texte particulier",DecalageX=0, DecalageY=-50)


    YOLO=tk.Label(F1,text="YOLO",font='10');YOLO.grid()
    azr=MainPlusHelp(F3,"content","helplabel")
    help_and=MainPlusHelp(F4,"data","help about data")
    main_c=tk.Label(help_and.main_frame,text="Main content This can be anything",font='10');main_c.grid(row=0,column=0)
    help_c=tk.Label(help_and.help_frame,text="help_details This can be anything",font='10');help_c.grid(row=0,column=0)
    #test2 = InformationBubble(parent=YOLO,texte="You Only Live Online",DecalageX=-15, DecalageY=35)

    A=tk.Listbox(F2,LISTBOX_STYLE);A.grid()
    A.insert('end', 'element 1');A.insert('end', 'element 2')
    
    search_bar=tk.Text(F1,state='normal',height=5)
    search_bar.grid()

    results=tk.Listbox(search_bar,state='normal',height=1)
    results.insert('end',"result1")
    results.insert('end',"result2")
    results.insert('end',"result3")
    search_bar.window_create("1.1", window=results)

    F1.grid(row=0,column=0)
    F2.grid(row=0,column=1)
    F3.grid(row=0,column=2)
    F4.grid(row=0,column=3)
    root.mainloop()
    
