#! /usr/bin/python
#-*-coding:utf-8*

#tks_widgets_1.py
#Role: Define custom tools for tkinter

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

#
import webbrowser
import time

try:#3.X
    import tkinter as tk
    import tkinter.ttk  as ttk
    import tkinter.font as tkfont
except ImportError:#2.X
    import Tkinter as tk
    import ttk as ttk
    import tkFont as tkfont


from tks_styles import *
from file_extractor import *
def _(l_string):
    return l_string

#TODO define other formats,
#set .for_data_type  = in the corresponding parent widget,
#bind the new format in the elifs here
HTML_ELEMENT_FORMAT = {
    "alt(s)":list,
    "must_attributes":list,
    "parent":list,
    "specific_attributes":list,
    "version":str,
    "void":bool,
    "common usage":str,
    "description":str,
    "role":str,
    "translation":str}

HTML_ATTRIBUTE_FORMAT = {
    "alt(s)":list,
    "default_value":str,
    "possible_values":list,
    "version":str,
    "common usage":str,
    "description":str,
    "role":str,
    "translation":str}
##CSS_SELECTOR_FORMAT = {
##    "define later":list}
##CSS_SELECTOR_FORMAT = {
##    "define later":list}
##CSS_SELECTOR_FORMAT = {
##    "define later":list}




def list_from_string(string):
    return list(filter(bool, map(str.strip, string.split(","))))

def bool_from_string(string):
    string_lower = string.lower()
    return "true" in string_lower or "yes" in string_lower

def list_of_strings_from_user_string(user_string):
    try:
        if user_string.startswith("[") or user_string.startswith("("):
            user_string = user_string[1::]
            if user_string.endswith("]") or user_string.endswith(")"):
                user_string = user_string[:-1]
        list_1 = list_from_string(user_string)
        
    except Exception:
        list_1 = list() # empty list
    finally:
        return list_1
    
def string_from_user_string(user_string):
    try:
        if user_string.startswith("\"") or user_string.startswith("'"):
            user_string = user_string[1::]
            if user_string.endswith("\"") or user_string.endswith("'"):
                user_string = user_string[:-1]
        string = user_string.strip()
        #look after 
    except Exception:
        string = str() # empty
    finally:
        return string
    
def bool_from_user_string(user_string):
    try:
        boolean = bool_from_string(user_string.strip())
    except Exception:
        boolean = False
    finally:
        return boolean
    
def int_from_user_string(user_string):
    try:
        integer = int(user_string.strip())
    except Exception:
        integer = 0
    finally:
        return integer
    
def float_from_user_string(user_string):
    try:
        float_1 = float(user_string.strip())
    except Exception:
        float_1 = 0.0
    finally:
        return float_1
    
DATA_FROM_USER_STRING_LINK = {
    list: list_of_strings_from_user_string,
    str: string_from_user_string,
    bool: bool_from_user_string,
    int: int_from_user_string,
    float: float_from_user_string}

def user_string_from_bool(bool_):
    if bool_:
        return u"True"
    return u"False"

def user_string_from_list_of_strings(list_of_strings):
    return u", ".join(list_of_strings)
    
def user_string_from_string(string):
    return string
    
def user_string_from_int(int_):
    return str(int_)
    
def user_string_from_float(float_):
    return str(float_)
    
USER_STRING_FROM_DATA_LINK = {
    list: user_string_from_list_of_strings,
    str: user_string_from_string,
    bool: user_string_from_bool,
    int: user_string_from_int,
    float: user_string_from_float}

def user_stringify(data):
    return USER_STRING_FROM_DATA_LINK[type(data)](data)

def f_only(function):
    def function_then_break(*event):
        function()
        return "break"#prevent default behavior
    return function_then_break

class memoized(object):
    """Decorator. Caches a function's return value each time it is called.

If called later with <0.25 second intervall, the cached value is returned instead."""
    def __init__(self, func):
        self.func = func
        self.last_call=0
        self.last_arg_0 = 0
    def __get__(self, instance, owner):
        if instance is None:
            return self
        d = self
        # use a lambda to produce a bound method
        mfactory = lambda self, *args: d(self, *args)
        mfactory.__name__ = self.func.__name__
        return mfactory.__get__(instance, owner)
    def __call__(self,instance, *args):
        now = time.time()
        interval= now - self.last_call
        self.last_call = now
        if interval < 0.25 and self.last_arg_0 == args[0]:
            return (self.a, self.b)
        else:
            self.last_arg_0=args[0]
            def closure(*args):
                return self.func(instance, *args)
            self.a, self.b = closure(*args)
            return (self.a, self.b)
    
class MainPlusHelp(ttk.Notebook):
    def __init__(self,parent,title_content,title_help):
        ttk.Notebook.__init__(self,parent)
        self.parent = parent

        self.main_frame=tk.Frame(self,FRAME_STYLE_2)
        self.help_frame=tk.Frame(self,FRAME_STYLE_2)
        self.add(self.main_frame,text=title_content,sticky='swen')
        self.add(self.help_frame,text=title_help,sticky='swen')

        self.short_help=tk.Label(self.main_frame,HELP_LABEL_STYLE,
            text=_("Cliquer sur un élément pour afficher l'aide"), wrap=400,
            anchor='nw',fg='#2220dd')
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
        def toogle_index(x):
            """0 becomes 1 and 1 becomes 0"""
            return -x + 1
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

class LabelString(ttk.Label):
    """Label, can store an additional string."""
    def __init__(self,parent,string,*args,**kw):
        ttk.Label.__init__(self,parent,*args,**kw)
        self.string = string

        
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
        return self.function(*self.event + args)


    
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
    

def bind_(widget, all_=False, modifier="", letter="", callback=None, add='',):
    """bind event and handler for both caps lock and without caps lock."""
    if modifier and letter:
        letter = "-" + letter
    if all_:
        widget.bind_all('<{}{}>'.format(modifier,letter.upper()), callback, add)
        widget.bind_all('<{}{}>'.format(modifier,letter.lower()), callback, add)
    else:
        widget.bind('<{}{}>'.format(modifier,letter.upper()), callback, add)
        widget.bind('<{}{}>'.format(modifier,letter.lower()), callback, add)


def soft_destruction(root,window):
    """destroy the windows when root gains focus, or esc, enter is hit."""
    def destroy(event):
        window.destroy()
    window.focus_set()
    window.bind('<Escape>',destroy)
    root.bind('<FocusIn>',destroy,add='+')
    window.bind('<Return>',destroy)

def warn_user(message):
    print(message)#use GUI
    
    
def receive_data_changes(data_type, keys, old_values, get_new_values):
    # data_key is the name of the thing the user wants to change
    # for data_type == "html_element" it is the name of the element
    
    if data_type == "html_element":
        format_rule = HTML_ELEMENT_FORMAT
        place = keys.index("element")
    elif data_type == "html_attribute" :
        format_rule = HTML_ATTRIBUTE_FORMAT
        place = keys.index("attribute")
##    elif data_type == "x" :
##        format_rule = HTML_ELEMENT_FORMAT
##    elif data_type == "y" :
##        format_rule = HTML_ELEMENT_FORMAT
##    elif data_type == "z" :
##        format_rule = HTML_ELEMENT_FORMAT
    new_values = get_new_values()
    data_key = old_values[place]
    del keys[place]
    del old_values[place]
    del new_values[place]
    clean_new_values = []
    i = 0
    
    for new_value in new_values:
        clean_new_values.append(DATA_FROM_USER_STRING_LINK[format_rule[keys[i]]](new_value))
        # certain values are meant to be false, this is not the correct way to solve it
##        if not clean_new_values[i]:
##            #perhaps throw error instead of sending
##            #false values so that you can use false values
##            #then replace if with except
##            warn_user("False,void or 0 value for {} we take the old value back".format(keys[i]))
##            if old_values[i]:
##                clean_new_values[i] = old_values[i]
        i += 1
    new_key_values = dict(zip(keys, clean_new_values))
    old_key_values = dict(zip(keys, old_values)) 
    
    
    save_data_changes(data_key, data_type, new_key_values)
    
def save_data_changes(data_key, data_type, new_key_values):
    if data_type == "html_element":
        data_holder = ELEMENTS
        data_holder_local = LOCAL_ELEMENTS
    elif data_type == "html_attribute":
        data_holder = ATTRIBUTES
        data_holder_local = LOCAL_ATTRIBUTES
    #elif data_type == "css selector" ...
    data_holder_in = data_holder[data_key]
    data_holder_local_in = data_holder_local[data_key]
    
    if copy_new_values(data_holder_in,new_key_values):#if anything has changed
        store_change_in_source(data_holder)
    if copy_new_values(data_holder_local_in,new_key_values):
        store_change_in_source(data_holder_local)
        
def general_editing_dialog(root, data_type, keys, old_values, focus_first=""):
    """Displays a form with default values ready to be edited."""
    edit_variable_dialog = tk.Toplevel(root)
    tk_string_holders = []
    i = 0
    for label,old_value in zip(keys,old_values):
        label_i = ttk.Label(edit_variable_dialog,text=label)
        label_i.grid(row=i,column=0)
        tk_string_holders.append(tk.StringVar(value=old_value))
        entry_i = ttk.Entry(edit_variable_dialog,textvariable=tk_string_holders[i])
        entry_i.grid(row=i,column=1)
        if focus_first == label:
            entry_i.select_range(0, tk.END)#Select All
            entry_i.focus()
        i += 1
    def get_new_values():#side effect destroys the dialog
        new_values = []
        widget_from_name = edit_variable_dialog.nametowidget
        i = 0
        for child_name in edit_variable_dialog.winfo_children():
            child = widget_from_name(child_name)
            if isinstance(child, ttk.Entry):
                new_values.append(tk_string_holders[i].get())
                i += 1
        edit_variable_dialog.destroy()
        return new_values
    confirm_button = ttk.Button(edit_variable_dialog,text=_(u"Confirmer"),
                                command=handler(receive_data_changes,
                                                data_type,keys,old_values,get_new_values))
    confirm_button.grid(row=i+1,column=0)
    cancel_button = ttk.Button(edit_variable_dialog,text=_(u"Annuler"),
                               command=edit_variable_dialog.destroy)
    cancel_button.grid(row=i+1,column=1)
    
def specific_editing_dialog_factory(event):
    """Returns a functions that print a editing dialog for the source."""
    w = event.widget # w = widget
    string = w.string
    parent_widget = w.nametowidget(w.winfo_parent())
    brothers = parent_widget.winfo_children()
    
    keys, old_values = [], []
    for brother in brothers:
        widget_brother = w.nametowidget(brother)
        if isinstance(widget_brother,LabelString):
            keys.append(widget_brother.string)
            old_values.append(widget_brother['text'])

    def specific_editing_dialog():
        general_editing_dialog(w, parent_widget.for_data_type, keys, old_values, w.string)
    return specific_editing_dialog

def local_menu_print(event):
    """Prints a context menu with usefull commands."""
    local_menu = tk.Menu(event.widget, tearoff=0, takefocus=0)
    local_menu.add_command(label=_(u"Modifier"), command=specific_editing_dialog_factory(event))
    #local_menu.add_command(label=_(u""), command=...)
    local_menu.tk_popup(event.x_root+42, event.y_root+10,entry="0")

#this could be in another more general module
#because it is not used specifcly for tkinter
def copy_new_values(dict1, dict2):
    """Updates dict1 with values of dict2 only if dict1 already has the keys.

It does never change the len(dict1).
dict1 will have the same values as dict2 for all keys in common.
dict2 is not changed. As dict1 is directly modified it is not returned again.
Return True if anything has changed, False otherwhise"""
    changed = False
    if dict1 == dict2:
        return changed
    #else :
    for key2 in dict2:
        if key2 in dict1 and dict1[key2] != dict2[key2]:
            dict1[key2] = dict2[key2]
            changed = True
    return changed

if __name__ == '__main__':
    import unittest
    
    class UserStringInputParseTestCase(unittest.TestCase):
        def test_list_of_strings_from_user_string(self):
            wanted = ["a", "and", "b"]
            self.assertEqual(list_of_strings_from_user_string("[a,and, b]"), wanted)
            self.assertEqual(list_of_strings_from_user_string("(  a, and,b  )"), wanted)
            self.assertEqual(list_of_strings_from_user_string("a,and,b"), wanted)
            
            wanted = []            
            self.assertEqual(list_of_strings_from_user_string(""), wanted)
            self.assertEqual(list_of_strings_from_user_string(" "), wanted)
            
        def test_string_from_user_string(self):
            wanted = "Hi"
            self.assertEqual(string_from_user_string("Hi\n"), wanted)
            self.assertEqual(string_from_user_string("\"Hi\""), wanted)

        def test_bool_from_user_string(self):
            self.assertFalse(bool_from_user_string("it s false!"))
            self.assertFalse(bool_from_user_string("I don t know"))
            self.assertTrue(bool_from_user_string("YES YES YES"))
            self.assertTrue(bool_from_user_string("it s TRue!"))
            self.assertTrue(bool_from_user_string("true"))
            
    
    root=tk.Tk()
    F1=tk.LabelFrame(root, FRAME_STYLE,text="links")
    F2=tk.LabelFrame(root, FRAME_STYLE,text="LabelFrame_2")
    F3=tk.LabelFrame(root, FRAME_STYLE,text="test")
    F4=tk.LabelFrame(root, FRAME_STYLE,text="main and help")

    H=HyperLink(F1,URL="www.python.org",text="PYTHON");H.grid()
    H2=HyperLink(F1,URL="www.wikipedia.org",text="wikipedia !!!");H2.grid()


    YOLO=tk.Label(F1,text="YOLO",font='10');YOLO.grid()
    azr=MainPlusHelp(F3,"content","helplabel")
    help_and=MainPlusHelp(F4,"data","help about data")
    main_c=tk.Label(help_and.main_frame,text="Main content This can be anything",font='10');main_c.grid(row=0,column=0)
    help_c=tk.Label(help_and.help_frame,text="help_details This can be anything",font='10');help_c.grid(row=0,column=0)

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
    
    unittest.main()
    
