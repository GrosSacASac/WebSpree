"""A custom parser for HTML and XHTML."""

from html_parser import*
class HTMLParser2(HTMLParser):
    def __init__(self, strict=False):
        HTMLParser.__init__(self, strict)
        self.start_list=[]
        self.end_list=[]
    

    # Overridable -- finish processing of start+end tag: <tag.../>
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    # Overridable -- handle start tag
    def handle_starttag(self, tag, attrs):
        self.start_list.append(tag)
        pass

    # Overridable -- handle end tag
    def handle_endtag(self, tag):
        self.end_list.append(tag)
        pass

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
        pass

    # Overridable -- handle comment
    def handle_comment(self, data):
        pass

    # Overridable -- handle declaration
    def handle_decl(self, decl):
        print(decl)
        pass

    # Overridable -- handle processing instruction
    def handle_pi(self, data):
        #print(data)
        pass


if __name__=='__main__':
    ml=r"""
<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="utf-8"/>
        <link rel="stylesheet" href="style.css"/>
        <title>index exos C</title>
    </head>
    <body>

<nav>
    <h1>
    Navigation
    </h1>
<a href="index.html">index.html</a>
<ol>
<li>
    TD1
<ol>
<li>
<a href="1.html">
    ex1
</a>
</li>
<li>
<a href="2.html">
    ex2
</a>
</li>
<li>
<a href="3.html">
    ex3
</a>
</li>
<li>
<a href="4.html">
    ex4
</a>
</li>
</ol>
</li>
<li>
    TD2<ol>
<li><a href="td2/nombre_parfait_td23.c" target="_blank">nombre_parfait_td23.c</a></li>
<li><a href="td2/pi_td25.c" target="_blank">pi_td25.c</a></li>
<li><a href="td2/pi_td25b.c" target="_blank">pi_td25b.c</a></li>
<li><a href="td2/premiers_td24.c" target="_blank">premiers_td24.c</a></li>
<li><a href="td2/puissance_td22.c" target="_blank">puissance_td22.c</a></li>
<li><a href="td2/puissance_td22b.c" target="_blank">puissance_td22b.c</a></li>
    </ol>
</li>
<li>
    TD3<ol>
    <li><a href="td3/liste_nombre_premiers.txt" target="_blank">liste_nombre_premiers.txt</a></li>
<li><a href="td3/re_ins_supp_td31.c" target="_blank">re_ins_supp_td31.c</a></li>
<li><a href="td3/re_ins_supp_td31b.c" target="_blank">re_ins_supp_td31b.c</a></li>
<li><a href="td3/re_ins_supp_td31cnontriee.c" target="_blank">re_ins_supp_td31cnontriee.c</a></li>
<li><a href="td3/re_ins_supp_td31ctriee.c" target="_blank">re_ins_supp_td31ctriee.c</a></li>
<li><a href="td3/re_ins_supp_td31d.c" target="_blank">re_ins_supp_td31d.c</a></li>
<li><a href="td3/td32a.c" target="_blank">td32a.c</a></li>
<li><a href="td3/td32b.c" target="_blank">td32b.c</a></li>
<li><a href="td3/td32c.c" target="_blank">td32c.c</a></li>
<li><a href="td3/td33.c" target="_blank">td33.c</a></li>
<li><a href="td3/td33b.c" target="_blank">td33b.c</a></li>
<li><a href="td3/td34.c" target="_blank">td34.c</a></li>
<li><a href="td3/td35.c" target="_blank">td35.c</a></li>
<li><a href="td3/td36.c" target="_blank">td36.c</a></li>
<li><a href="td3/td37.c" target="_blank">td37.c</a></li>
</li></ol>
<li>
    TD4
</li>
</ol>
</nav>


<main>
<article>
<h1>
    Exercices en C
</h1>
<p>
    Bonjour, ici je déposerai les exercices en C. Pour l'instant je n'ai pas encore tout terminé mais je mettrai le site à jour en temps voulu. Certains exercices ne sont pas términé, ce sera alors précisé. Si vous avez résolu différement un exo, vous pouvez me l'envoyer et je le publierai aussi.
</p>
</article>
<article>
<h1>
    Prochain devoir
</h1>
<p>
    Pour le prochain devoir il faut savoir manipuler des tableaux. Donc le mieux est de savoir faire tous les exos jusqu
au td3 inclus
</p>
</article>
</main>



<footer>
    <p>Ce site statique est hébergé gratuitement sur
<a target="_blank" href="https://www.bitballoon.com/">bitballoon</a>.Si vous avez des idées pour le CSS, alors envoyez.
</footer>
    </body>
</html>
"""
    p = HTMLParser2()
    p.feed(ml)
    p.close()
    print(p.start_list)
    print(p.end_list)
    print(p.start_list.sort()==p.end_list.sort())#True if every closed thing is the same as opened
