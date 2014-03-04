#!/usr/bin/python
#-*-coding:utf-8*

#tk_tools.py
#Role: define the cut copy paste context_menu 

#Walle Cyril
#10/03/2014

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
    from tkinter import*
except ImportError:#2.X
    from Tkinter import*


def _(l_string):
    #print("local language: "+l_string)
    return l_string


def copy(event):
    event.widget.event_generate('<Control-c>')
    event.widget.event_generate('<KeyRelease>')
def cut(event):
    event.widget.event_generate('<Control-x>')
    event.widget.event_generate('<KeyRelease>')
def paste(event):
    event.widget.event_generate('<Control-v>')
    event.widget.event_generate('<KeyRelease>')

class handler():
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

    context_menu = Menu(event.widget, tearoff=0, takefocus=0)
    for (text, action) in tools:
        context_menu.add_command(label=text, command=action)
    context_menu.tk_popup(event.x_root+42, event.y_root+10,entry="0")
    event.widget.focus()

if __name__ == '__main__':
    root = Tk()
    m=Label(root,text="test right click")
    m.pack()
    e=Entry(root, width=100,fg="#406010")
    e.bind('<Button-3>',create_context_menu)
    e.pack()
    e.focus_set()
    root.mainloop()
