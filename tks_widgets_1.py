#! /usr/bin/python
#-*-coding:utf-8*

#Label_Plus
#InformationBubble avec failles
#HyperLink
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
        
        more_help_button=ttk.Button(self.main_frame, text=_("Plus d'aide"))
        more_help_button.grid(row=2,column=0,sticky='nswe',columnspan=3)
        more_help_button.bind('<ButtonRelease-1>', self.switch_help)
        
        leave_help=ttk.Button(self.help_frame, text=_("Quitter l'aide"))
        leave_help.grid(row=1,column=0,sticky='nswe')        
        leave_help.bind('<ButtonRelease-1>', self.switch_help)
        self.grid(sticky='nswe')
        
    def switch_help(self,event):
        def toogle_index(i):#0 becomes 1 and 1 becomes 0
            return int(not i)
        w=event.widget
        current_tab=w.nametowidget(w.winfo_parent())
        not_current_tab_as_index=toogle_index(self.index(current_tab))
        self.select(not_current_tab_as_index)
        #redirect to the correct help tab

class HyperLink():
    def __init__(self,parent,URL="",*TkPaquet,**TkDic):
        if 'text' in (TkDic):
            pass
        else:
            TkDic['text']=URL
        self.URL=URL
        self.lab=tk.Label(parent,TkDic,fg='blue')
        Police = tkfont.Font(self.lab, self.lab.cget('font'))# On prend la police
        Police['underline'] = True# On la rend soulignée
        self.lab['font'] = Police           # On la reaffecte
        
        self.lab.bind('<ButtonRelease-1>',self.OuvrirLien)#La souris clique droit
        self.lab['cursor']='center_ptr'#Curseur flèche
    def OuvrirLien(self,event):
        print(event.x_root,event.y_root)
        if self.lab.winfo_containing(event.x_root,event.y_root) is self.lab:
            webbrowser.open_new_tab(self.URL)
    def pack(self):
        self.lab.pack()
    
    



class InformationBubble(tk.Toplevel):
    def __init__(self,parent=None,texte="", DecalageX=20, DecalageY=0):
        tk.Toplevel.__init__(self,parent,bd=1,bg='black')
        self.parent=parent
        self.withdraw()#L'objet  se fait effacer
        self.overrideredirect(1)#L'objet n as pas le contour d'une fenetre
        self.transient()#Effet sur le focus
        InfoTexte=tk.Label(self,text=texte,justify='left',bg='light yellow')
        InfoTexte.pack()
        #InfoTexte.update_idletasks()
        
        self.LargeurObjet = InfoTexte.winfo_width()#On adapte la taille de l'InformationBubble à son contenu(texte); largeur
        self.HauteurObjet = InfoTexte.winfo_height()#hauteur

        self.DecalageX=DecalageX
        self.DecalageY=DecalageY
        self.parent.bind('<Enter>',self.Afficher)#La souris entre
        self.parent.bind('<Button-1>',self.Effacer)#La souris clique droit
        self.parent.bind('<Button-2>',self.Effacer)
        self.parent.bind('<Button-3>',self.Effacer)
        self.parent.bind('<Button-4>',self.Effacer)
        self.parent.bind('<Leave>',self.Effacer)#La souris sort
        self.parent.bind('<Motion>',self.Mouver)#La souris bouge
    
    def Reajustement(self,event):
        #localisation du widget parent+localisation de la souris +10
        PosX=self.parent.winfo_rootx()+event.x+self.DecalageX#On suit la souris
        PosY=self.parent.winfo_rooty()+event.y+self.DecalageY
        if PosX + self.LargeurObjet > self.winfo_screenwidth():#Si on dépasse l'écran ...
            PosX = PosX-self.winfo_width()-self.LargeurObjet
        if PosY + self.HauteurObjet > self.winfo_screenheight():
            PosY = PosY-self.winfo_height()-self.HauteurObjet
        return PosX,PosY
 
    def Afficher(self,event):
        self.update_idletasks()
        PosX,PosY=self.Reajustement(event)
        self.geometry("+"+str(PosX)+"+"+str(PosY))
        self.deiconify()#L'objet  se fait dessiner
        self.update_idletasks()
 
    def Mouver(self,event):
        PosX,PosY=self.Reajustement(event)
        self.geometry("+"+str(PosX)+"+"+str(PosY))
        self.update_idletasks()
 
    def Effacer(self,event):
        self.withdraw()#L'objet  se fait effacer
        
class DragDropFeedback(tk.Toplevel):
    def __init__(self,parent=None,text="no text given", x=0, y=0):
        tk.Toplevel.__init__(self,parent,bd=0,bg='#333300')
        self.reset_position(x,y)
        tk.Label(self,text=text).pack()
        self.overrideredirect(1)#L'objet n as pas le contour d'une fenetre
    def reset_position(self,x,y):
        self.geometry('200x20+%d+%d' % (135+x,240+y))
        
 
if __name__ == '__main__':#essay
    root=tk.Tk()
    F1=tk.LabelFrame(root, FRAME_STYLE,text="Infobulles")
    F2=tk.LabelFrame(root, FRAME_STYLE,text="LabelFrame_2")
    F3=tk.LabelFrame(root, FRAME_STYLE,text="testzqts")
    F4=tk.LabelFrame(root, FRAME_STYLE,text="main and help")

    H=HyperLink(F1,URL="www.python.org",text="Lien Avec Texte particulier",font='50');H.pack()
    H2=HyperLink(F1,URL="www.wikipedia.org",font='10');H2.pack()
    AideLien = InformationBubble(parent=H2.lab,texte="Lien sans texte particulier",DecalageX=0, DecalageY=-50)


    YOLO=tk.Label(F1,text="YOLO",font='10');YOLO.pack()
    azr=TRY(F3)
    help_and=MainPlusHelp(F4,"data","help about data")
    main_c=tk.Label(help_and.main_frame,text="Main content This can be anything",font='10');main_c.grid(row=0,column=0)
    help_c=tk.Label(help_and.help_frame,text="help_details This can be anything",font='10');help_c.grid(row=0,column=0)
    test2 = InformationBubble(parent=YOLO,texte="You Only Live Online",DecalageX=-15, DecalageY=35)

    A=tk.Listbox(F2,LISTBOX_STYLE);A.pack()
    A.insert('end', 'element 1');A.insert('end', 'element 2')


    F1.pack(side='left')
    F2.pack(side='right')
    F3.pack(side='right')
    F4.pack(side='right')
    root.mainloop()
    
    az2r=TRY()
