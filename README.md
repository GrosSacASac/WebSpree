WebSpree
========

Learn Web-related technologies

##How to join and contribute ?
  Look for interesting missions in To_do.html in the Documentation folder

##How to run the sofware ?
  Download the entire repository.
  
  Make sure you have Python on your machine
  
  Run WebSpree.py or WebSpree_beta.py
  
  ???
  
  Profit !!!
  
##Updates
  You can see the complete patch notes in the Documentation in Patch_Notes.html
  
#More
  You want to know more ? Read this:

##Functional Specifications
functional_spec.txt
Last Update of this document:
22/02/2014

Goals:
WebSpree is meant to be an app to help beginners with Web related technologies.
Part of the project is to encourage good habits and teach the importance of standards.
It should also give clues to explore further than the app.
HTML and CSS are the first technologies implemented.
JavaScript later


Non-goals:
WebSpree should not be a WHYSIWYG (What you see is what you get). It should not replace a traditional text editor application.


Features summary:
Standalone app to learn HTML CSS and JavScript
Help and tips for every element and attribute.
Link between elements and attributes.
Easy and fast access to each of those.
Basic text editor.
some guides to create webpages step by step with advices.
links in the guides to real websites to illustrate the guides.
Possibility to launch document directly in a browser.
Correction tool.


so much more in mind but I can t write everything now
...
##Tune into my project
tune_in_my_project.txt
Last Update of this document:
22/02/2014

Main language for code:
Python 3 in English

Main environment:
Windows xp and later

Portability:
UniX and MacX should be able to display the app correctly.
the main code should also work with Python 2.76+ but this may change. When I write this, Python 2 is still used a lot but it may change in the future.

write idiomatic code!(pythonic):
https://www.jeffknupp.com/writing-idiomatic-python-ebook/
good
if a:
bad
if a==True:


naming:
check the file in conventions to learn more

docstrings:
everything you can !(See file in Conventions for details.)

indent:
use 4 spaces ! Tip: If you are used to press TAB to indent then go into your text editor settings and enable the "automatically replace TAB by 4 spaces" There should be an option like that(if not throw away your text editor).

Newline:
\r\n or \n but who cares ? I think this can be interesting to reduce a little bit the the size of the project.

GUI:
tkinter

Format to organize data in files:
-JSON(For now it s still a custom format I created but I m working on it.)

File encoding:
UTF-8(without BOM), no exception, period. Have a look at
http://www.utf8everywhere.org/

Documentation format:
raw txt for text
HTML for anything that requires more than just text or that should serve the end-user
jpg for images
mp3, flac for sound
mp4 ,[insert other open format for videos here] for videos
try to not use other formats, HTML is very easy and with the app it s easier. If you can't then you should make a folder with text files and images and later do html with it.

What should I do:
Check the To_do.html file in Documentation.

Builds:
We need an easy freezing tool : freeze("WebSpree.py") --> WebSpree.exe

Distributed Version control:
GitHub !

Bug-tracking:
coming

Test driven developpement:
coming
