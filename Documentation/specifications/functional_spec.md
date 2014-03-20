functional_spec.md
Last Update of this document:
18/03/2014

Goals:
======
WebSpree is meant to be an app to help beginners with Web related technologies.
Part of the project is to encourage good habits and teach the importance of standards.
It should also give clues to explore further than the app.
By "Web related technologies", I mean HTML and CSS and JavaScript later.


Non-goals:
===========
WebSpree should not be a WHYSIWYG (What you see is what you get). It should not replace a complete text editor application.


Features summary:
=================
* Text editor
* Standalone app to learn HTML CSS and JavScript
* Help and tips for every element and attribute
* Link between elements and attributes
* Tutorials to create web pages with verification
* Possibility to integrate your own tutorials in the app and distribute them
* Some Macros
* Possibility to launch document directly in a browser
* Possibility to preview CSS with templates
* Correction tool. Links to w3c validator

Details
========

##Text editor
Write,save,open,new,tabs.


##Help and tips for every element and attribute
###HTML
After a click on an element or attribute help is shown.


##Tutorials to create webpages with verification

A tutorial is a document to let the user discover new worlds and build something on his own fast.
To implement a tutorial you need to create a folder with html pages in it. index.html is a must and is considered as the starting point. The user can start a tutorial by clicking on a menu and select the tutorial. By doing that the web browser will display index.html of that tutorial

At index.html you can find an introduction,author,level and more and a link to start. Tutorials can also have a verification. Verification allows the tutorial author to ensure the user tries/writes/experiments while reading the tutorial. After the user finishes a step of the tutorial, the document can be checked. With success a link to the next step is displayed. With no success the errors are displayed 

After succeeding a complete tutorial the tutorial is shown in green or some other visual corresponding to "success"
The tutorial support is html so it can include any text,images videos and games.



so much more in mind but I can t write everything now

 