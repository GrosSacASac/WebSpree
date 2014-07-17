functional_spec.md
Last Update of this document:
2014-07-13

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
* App to learn HTML CSS and JavScript
* Help and tips for every element and attribute
* Link between elements and attributes
* Create your own tutorials with custom verification
* Macros
* Launch document directly in a browser
* Preview CSS with templates
* Validation tool
* Works off-line - No connection required

Details
========

##Text editor
Write,save,open,new tabs.


##Help and tips for every element and attribute
###HTML
After a click on an element or attribute help is shown.


##Tutorials to create web pages with verification

A tutorial is a set of documents to let the user discover new worlds and build something on his own fast.
To implement a tutorial you need to create a folder with html pages in it. index.html is a must and is considered as the starting point. The user can start a tutorial by clicking on a menu and select the tutorial. By doing that the web browser will display index.html of that tutorial

At index.html you can find an introduction,author,level and more and a link to start. Tutorials can also have a verification. Verification allows the tutorial author to ensure the user tries/writes/experiments while reading the tutorial. After the user finishes a step of the tutorial, the document can be checked. With success a link to the next step can be displayed. With no success the errors are displayed 

After succeeding a complete tutorial the tutorial is shown in green or some other visual corresponding to "success"


so much more in mind but I can t write everything now

##Macros
A macro is a short-cut for doing multiple commands at once. It is useful to win in productivity.

###Build Site

Often you need to have some parts of your site to be the same for obvious reasons such as consistency, identity and user experience. These parts are traditionally the top and the bottom of your site.
You can copy manually these parts on every html document but the problem is that you'll then need to re-open all of those documents whenever you want to change these parts.
The solution of this kind of problem is to separate the development and the production branch. The development branch is where you do all the changes and the production branch is the final product. In the development branch there are no copies, every file is completely unique and when you create the production files you copy all the common parts to their respective final destination.
You can automate this task with simple powerful algorithms accessible in WebSpree


`
    __Development branch__ 
    
    /images
    /js
        /source
            main.js
        /library
    /css
        screen.css
        print.css
    header.html
        <header><h1>Welcome to my site !</h1></header>
    footer.html
    
    index.html
        <<header.html>>
        <main><p>I built this site with consistency using clever macros</p></main>
        <<footer.html>>
    docs.html
    about.html
    ...
    
   produces --> __Production branch__ 

    /images
    /js
        /source
            main.js
        /library
    /css
        screen.css
        print.css
    
    index.html (with header and footer included)
        <header><h1>Welcome to my site !</h1></header>
        <main><p>I built this site with consistency using clever macros</p></main>
        <footer>footer content arrives here</footer>
    docs.html (with header and footer included)
    about.html (with header and footer included)
    ...

That way you can change the header once, build the site and have all pages the new header included for production. As you can see this solution scales very well as your site grows.