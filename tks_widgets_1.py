#! /usr/bin/python
#-*-coding:utf-8*

#Label_Plus
#InformationBubble avec failles
#HyperLink
import webbrowser

try:#3.X
    from tkinter import*
    import tkinter.font as TKFONT
    import tkinter.ttk  as TTK
except ImportError:#2.X
    from Tkinter import*
    import tkFont as TKFONT
    import ttk  as TTK

from tks_styles import*



class HyperLink(Label):
    def __init__(self,parent,URL,*TkPaquet,**TkDic):
        try:
            TkDic.update(TkPaquet[0])
        except IndexError:
            pass
        if 'text' in (TkDic):
            TexteAffiche=TkDic['text']
        else:
            TexteAffiche=URL
        Label.__init__(self,parent,TkDic,text=TexteAffiche,fg='blue')

        Police = TKFONT.Font(self, self.cget('font'))# On prend la police
        Police['underline'] = True# On la rend soulignée
        self['font'] = Police           # On la reaffecte

        def OuvrirLien(event):
            webbrowser.open_new_tab(URL)
        self.bind('<Button-1>',OuvrirLien)#La souris clique droit
        self['cursor']='center_ptr'#Curseur flèche


def ModifierTheme(*Choix):
    for widgets in WidgetsList:
        widgets.ChangerCouleur(*Choix)
class Label_Plus(Label):
    """ Label dont on peut facilement modifier l'apparence (couleurs)
avec la fonction ModifierTheme
"""
    def __init__(self,parent=None,LISTWIDGET=["Obligatoire"],*TkPaquet,**TkDic):        
        try:
            TkDic.update(TkPaquet[0])
        except IndexError:
            pass
        Label.__init__(self,parent,TkDic, bg='white',fg='black')
        self.Style=0
        LISTWIDGET.append(self)
    def ChangerCouleur(self,Choix=-1):
        ChoixAuTotal=3
        def modifClassique(self):#0
            self['bg']='white'
            self['fg']='black'
            self.Style=0
        def modifSombre(self):#1
            self['bg']='black'
            self['fg']='white'
            self.Style=1
        def modifCustom(self):#2
            self['bg']='blue'
            self['fg']='yellow'
            self.Style=2
        if Choix==-1:
            Choix=(self.Style+1)%ChoixAuTotal
        if Choix==0:
            modifClassique(self)
        elif Choix==1:
            modifSombre(self)
        elif Choix==2:
            modifCustom(self)

class InformationBubble(Toplevel):
    def __init__(self,parent=None,texte="", DecalageX=20, DecalageY=0):
        Toplevel.__init__(self,parent,bd=1,bg='black')
        self.parent=parent
        self.withdraw()#L'objet  se fait effacer
        self.overrideredirect(1)#L'objet n as pas le contour d'une fenetre
        self.transient()#Effet sur le focus
        InfoTexte=Label(self,text=texte,justify='left',bg='light yellow')
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
    
    global Reajustement
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
        PosX,PosY=Reajustement(self,event)
        self.geometry("+"+str(PosX)+"+"+str(PosY))
        self.deiconify()#L'objet  se fait dessiner
        self.update_idletasks()
 
    def Mouver(self,event):
        PosX,PosY=Reajustement(self,event)
        self.geometry("+"+str(PosX)+"+"+str(PosY))
        self.update_idletasks()
 
    def Effacer(self,event):
        self.withdraw()#L'objet  se fait effacer
class DragDropFeedback(Toplevel):
    def __init__(self,parent=None,text="no text given", x=0, y=0):
        Toplevel.__init__(self,parent,bd=0,bg='#333300')
        self.reset_position(x,y)
        Label(self,text=text).pack()
        self.overrideredirect(1)#L'objet n as pas le contour d'une fenetre
    def reset_position(self,x,y):
        self.geometry('200x20+%d+%d' % (135+x,240+y))
        #self.transient()#Effet sur le focus
        
        #InfoTexte.update_idletasks()
        """
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
    
    global Reajustement
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
        PosX,PosY=Reajustement(self,event)
        self.geometry("+"+str(PosX)+"+"+str(PosY))
        self.deiconify()#L'objet  se fait dessiner
        self.update_idletasks()
 
    def Mouver(self,event):
        PosX,PosY=Reajustement(self,event)
        self.geometry("+"+str(PosX)+"+"+str(PosY))
        self.update_idletasks()
 
    def Effacer(self,event):
        self.withdraw()#L'objet  se fait effacer"""
 
if __name__ == '__main__':#essay
    f = TKFONT.Font(family='Arial', size="14")
    s = TTK.Style()
    WidgetsList=[]
    F1=LabelFrame(root, FRAME_STYLE,text="Infobulles")
    F2=LabelFrame(root, FRAME_STYLE,text="LabelFrame_2")

    H=HyperLink(F1,"www.python.org",text="Lien Avec Texte particulier",font='50');H.pack()
    H2=HyperLink(F1,"www.wikipedia.org",font='10');H2.pack()
    AideLien = InformationBubble(parent=H2,texte="Lien sans texte particulier",DecalageX=0, DecalageY=-50)

    You=Label_Plus(F1,WidgetsList,LABEL_STYLE,text="Texte youghourt",font='250');You.pack()
    YOLO=Label_Plus(F1,WidgetsList,text="YOLO",font='10');YOLO.pack()
    test1 = InformationBubble(parent=You,texte="Mmmm c'est bon")#Sans précision sur le décalage souris
    test2 = InformationBubble(parent=YOLO,texte="You Only Live Online",DecalageX=-15, DecalageY=35)

    A=Listbox(F2,LISTBOX_STYLE);A.pack()
    A.insert('end', 'element 1');A.insert('end', 'element 2')
    IndicateurBalise=Label_Plus(F2,WidgetsList,LABEL_STYLE,text="Label");IndicateurBalise.pack()

    B=Button(F2,text="Clair", command=lambda: ModifierTheme(0));B.pack()
    C=Button(F2,text="Sombre", command=lambda: ModifierTheme(1));C.pack()
    D=Button(F2,text="Changer", command=lambda: ModifierTheme());D.pack()

    F1.pack(side='left')
    F2.pack(side='right')
    root.mainloop()
