#!/usr/bin/python
#-*-coding:utf-8*

#name.py
#Role:overwrite insteresting methods

#Walle Cyril
#13/03/2014

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

from html_parser import*
class HTMLParser2(HTMLParser):
    def __init__(self, strict=False):
        HTMLParser.__init__(self, strict)
        self.start_list=[]
        self.end_list=[]
        self.content_list=[]
        self.key_attribute_list=[]
        self.value_attribute_list=[]
        
    

    # Overridable -- finish processing of start+end tag: <tag.../>
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    # Overridable -- handle start tag
    def handle_starttag(self, tag, attrs):
        
        #if attrs:
            #attrs.insert(0,tag)
        if attrs:
            i1=len(self.key_attribute_list)
            i2=len(self.value_attribute_list)
            self.key_attribute_list.append([])
            self.value_attribute_list.append([])
            for attr in attrs:
                self.key_attribute_list[i1].append(attr[0])
                self.value_attribute_list[i2].append(attr[1])
        else:
            self.key_attribute_list.append(None)
            self.value_attribute_list.append(None)
        
        self.start_list.append(tag)
        

    # Overridable -- handle end tag
    def handle_endtag(self, tag):
        self.end_list.append(tag)

    # Overridable -- handle character reference
    def handle_charref(self, name):
        pass

    # Overridable -- handle entity reference
    def handle_entityref(self, name):
        pass

    # Overridable -- handle data
    def handle_data(self, data):
        #print(data.strip(),end="")
        #print(type(data))
        stripped_data=data.strip()
        if stripped_data:
            self.content_list.append(stripped_data)
        else:
           pass#self.content_list.append("") 

    # Overridable -- handle comment
    def handle_comment(self, data):
        pass

    # Overridable -- handle declaration
    def handle_decl(self, decl):
        #print(decl)
        pass

    # Overridable -- handle processing instruction
    def handle_pi(self, data):
        #print(data)
        pass


if __name__=='__main__':
    a=r"""
<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="utf-8"/>
        <title>index exos C</title>
    </head>
    <body hey>
<p>bonjour<fail/>
<footer>
    <p>Ce site statique est hébergé gratuitement sur
<a j target="_blank" href="https://www.bitballoon.com/">bitballoon</a>.Si vous avez des idées pour le CSS, alors envoyez.
</footer>
    </body>
</html>
"""
    p = HTMLParser2()
    p.feed(a)
    p.close()
    
##    print(p.start_list)
##    p.start_list.sort()
##    print(p.start_list)
##    print(p.end_list)
##    p.end_list.reverse()
##    print("reversed end :",p.end_list)
##    p.end_list.sort()
##    print(p.end_list)
##    print("correctly open_closed: ",p.start_list==p.end_list)#True if every closed thing is the same as opened
##    print(p.attribute_list)
