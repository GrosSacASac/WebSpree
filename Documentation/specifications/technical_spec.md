technical_spec.md
Last Update of this document:
2014-07-14

##Tutorials to create web pages with verification

a tutorial is a set of html documents in the tuto/tut_folder_name/ folder where index.html is the beginning/home of the tutorial. For a tutorial (folder) to be valid
it must contain index.html and a valid tuto.json file. 
In tuto.json you find a collection {} with:


* "name" string Name of tutorial (display in WebSpree)
* "authors" list strings Authors. can be empty
* "languages" list strings language use the same letters as for the HTML attribute lang="".
* "dates" list strings of important dates in the creation process of the tutorial e.g. when created, updated, published
* "level" int between 1-10 to indicate the difficulty (1 for absolute beginners and 10 for experienced webmasters
* "steps" list strings of all steps in the tutorial. A step should be a html file with exercices
* "reward" int reward
* "showlink" boolean show link to next even if false


There may also be a verification.json file there. A verification is a dic. Each dic correspond to 1 file
* "afterthis" the next html file
* "this" the current html file
* "show_solution" boolean,show or not show solution link if fail, if true there must be a file solution file "solution_%s" % (this)
* "verification" list of special regular expression. A special regular expression is defined as**:
    * [["t","x"], ["tag1","tag2","tagn"]] t means tag. This will look at least x times for the tags, must be closed of course
    
    * [["a","attribute_name","attribute_value"], ["tag1","tag2","tagn"]] a means attribute Will look x times for attribute name with the value value in any tags if not specified or in written tags 
    * [["r"], ["text"]] will search in raw mode (without parsing html)
    * [["r","o"], ["text"]] search in raw mode without compiling as regular expression
    * [["d","o","tag"], ["text"]] d for data will look if expression  matches  in tags. d  uses regular expressions and d + o without regular expression this will only look if expression is directly in tag !

    example:
    "verification":[
            [["t","1"],["html","body","p"]],
            [["a","src","fig1.jpg"], ["img"]],
            [["d","p"],["bonjour"]],
            [["r","o"],["<!DOCTYPE html>"]],
            [["r","o"],["<red>"]]
        ],
    


----------

How does it work ? 

class FileDocument

    is 1 file and on screen 1 tab
    the instance holds all file related information

    has 0 or more 
    
        class HTMLFragment
            insert, append(str or HTMLFragment)
            __str__
            parse all
        class CSSFragment
        class JSFragment
    
    +parse from rawdata
    +add raw(is parsed)
    +insert raw
    +save...