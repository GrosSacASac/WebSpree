technical_spec.md
Last Update of this document:
18/03/2014

##Tutorials to create web pages with verification

a tutorial is a set of html documents in the tuto/*name you want*/ folder where index.html is the beginning/home of the tutorial. it s also an element in tuto/tuto.json file.

Each element is a dic(key+value)
* "name" stringName of tutorial (display in WebSpree)
* "folder" string Folder path to open the folder './tuto/' is normalized and excluded.this should be a unique and static value
* "authors" list strings Authors. this can be empty
* "languages" list strings language use the same letters as for the HTML attribute lang="en".
* "dates" list of TODECIDE
* "level" int between 1-10 to indicate the difficulty (1 for absolute beginners  and 10 for webmasters(vague definition)
* more ?

each html file can have a verification. A verification is a dic.Each dic correspond to 1 file
* "afterthis" the next html file
* "this" the current html file
* "show_solution" boolean,show or not show solution link if fail, if true there must be a file solution file "solution%s_" % (this)
* "verification" list of special regular expression. A special regular expression is defined as**:
    * "{t:x}tag1,tag2,...,tagn" t means tag. This will look x times for the tags
    * "{tc:x}tag1,tag2,...,tagn" tc means tag closed. Same as above but will also look if that tag is closed
    * "{a:attribute_name:x}tag1,tag2,...,tagn:value or None" a means attribute Will look x times for attribute name with the value value in any tags or in tags if tags is there.you must put ":" for no value
    * "{r}" will search in raw mode (without parsing html)
    * "{ro}" search in raw mode without compiling as regular expression
    * "{do:tag:x}expression" d for data will look if expression  matches x times in tags.just d uses regular expressions and do without regular expression
    * No prefix will be searched as data as non regular expression
    
* "showlink" boolean show link to next even if false



