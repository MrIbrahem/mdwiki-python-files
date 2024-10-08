#!/usr/bin/python3
"""

نسخ التاريخ من الإنجليزية إلى mdwiki

python3 core8/pwb.py mdpy/imp -page:Infertility

"""

#
# (C) Ibrahem Qasim, 2022
#
#
import sys
from newapi import printe
from mdpy.bots import py_tools
from newapi.mdwiki_page import MainPage, NEW_API

# ---
offset = {1: 0}
# ---
to_make = {}
# ---
for arg in sys.argv:
    arg, _, value = arg.partition(':')
    # ---
    if arg.lower() in ['offset', '-offset'] and value.isdigit():
        offset[1] = int(value)
# ---
# from export import * # export_en_history( title )
# ---
api_new = NEW_API('www', family='mdwiki')
# api_new.Login_to_wiki()
# pages   = api_new.Find_pages_exists_or_not(liste)
# pages   = api_new.Get_All_pages(start='', namespace="0", limit="max", apfilterredir='', limit_all=0)


def work(title, num, length, From=''):
    # ---
    printe.output(f'-------------------------------------------\n*<<yellow>> >{num}/{length} title:"{title}".')
    # ---
    if num < offset[1]:
        return ""
    # ---
    page = MainPage(title, 'www', family='mdwiki')
    exists = page.exists()
    if not exists:
        printe.output(f" page:{title} not exists in mdwiki.")
        return ""
    # ---
    # if page.isRedirect() :  return
    # target = page.get_redirect_target()
    # ---
    text = page.get_text()
    # ---
    ing = page.import_page(family="wikipedia")
    # ---
    if "test" in sys.argv:
        printe.output(ing)
    # ---
    done = ing.get("import", [{}])[0].get("revisions", 0)
    # ---
    printe.output(f"<<green>> imported {done} revisions")
    # ---
    if done > 0:
        # ---
        save_page = page.save(newtext=text, summary='', nocreate=1)
        # ---
        if save_page is not True:
            title2 = f'User:Mr._Ibrahem/{title}'
            # ---
            page2 = MainPage(title2, 'www', family='mdwiki')
            save = page2.save(newtext=text, summary='Returns the article text after importing the history', nocreate=0)


def main():
    printe.output('*<<red>> > main:')
    # ---
    # python3 imp.py -page:Crohn's_disease
    # python imp.py -newpages:1000
    # python imp.py -newpages:20000
    # ---
    page2 = ''
    From = '0'
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        # ---
        arg = arg.lower()
        # ---
        if arg == "-from":
            From = py_tools.ec_de_code(value, 'decode')
        # ---
        if arg in ["-page2", "page2"]:
            page2 = py_tools.ec_de_code(value, 'decode')
    # ---
    if page2 != '' and From != '':
        work(page2, 0, 1, From=From)
    # ---
    user = ''
    user_limit = '3000'
    # ---
    searchlist = {
        "drug": "insource:/https\\:\\/\\/druginfo\\.nlm\\.nih\\.gov\\/drugportal\\/name\\/lactulose/",
    }
    # ---
    limite = 'max'
    starts = ''
    # ---
    pages = []
    # ---
    namespaces = '0'
    newpages = ''
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        # ---
        arg = arg.lower()
        # ---
        if arg in ["-limit", "limit"]:
            limite = value
        # ---
        if arg in ["-userlimit", "userlimit"]:
            user_limit = value
        # ---
        if arg in ["-page", "page"]:
            pages.append(value)
        # ---
        if arg in ["-page2", "page2"]:
            value = py_tools.ec_de_code(value, 'decode')
            pages.append(value)
        # ---
        if arg in ['newpages', '-newpages']:
            newpages = value
        # ---
        # python imp.py -ns:0 -usercontribs:Edoderoobot
        # python imp.py -ns:0 -usercontribs:Ghuron
        if arg in ["-user", "-usercontribs"]:
            user = value
        # ---
        # python imp.py -start:!
        if arg in ['start', '-start']:
            starts = value
        # ---
        if arg == "-ns":
            namespaces = value
        # ---
        # python imp.py -file:mdwiki/list.txt
        # python3 imp.py -file:mdwiki/list.txt
        if arg == "-file":
            # ---
            # if value == 'redirectlist.txt' :
            # ---
            text2 = open(value, "r", 'utf8')
            text = text2.read()
            pages.extend(x.strip() for x in text.split("\n"))
        # ---
        # python imp.py -ns:0 search:drug
        if arg == 'search':
            if value in searchlist:
                value = searchlist[value]
            # ---
            ccc = api_new.Search(value=value, ns="0", srlimit="max")
            for x in ccc:
                pages.append(x)
            # ---
    # ---
    start_done = starts
    okay = True
    # ---
    if starts == 'all':
        while okay:
            # ---
            if starts == start_done:
                okay = False
            # ---
            # python imp.py -start:all
            #
            # ---
            lista = api_new.Get_All_pages(start='', namespace=namespaces, limit=limite)
            start_done = starts
            for num, page in enumerate(lista, start=1):
                work(page, num, len(lista))
                # ---
                starts = page
    # ---
    if starts != '':
        listen = api_new.Get_All_pages(start=starts, namespace=namespaces, limit=limite)
        for num, page in enumerate(listen, start=1):
            work(page, num, len(listen))
            # ---
    # ---
    lista = []
    # ---
    if newpages != "":
        lista = api_new.Get_Newpages(limit=newpages, namespace=namespaces)
    elif user != "":
        lista = api_new.UserContribs(user, limit=user_limit, namespace=namespaces, ucshow="new")
    elif pages != []:
        lista = pages
    # ---
    for num, page in enumerate(lista, start=1):
        work(page, num, len(lista))
    # ---
    if starts == 'all':
        while okay:
            # ---
            if starts == start_done:
                okay = False
            # ---
            # python imp.py -start:all
            #
            # ---
            lista = api_new.Get_All_pages(start='', namespace=namespaces, limit=limite)
            start_done = starts
            for num, page in enumerate(lista, start=1):
                work(page, num, len(lista))
                # ---
                starts = page
    elif starts != '':
        # while start_done != starts :
        while okay:
            # ---
            if starts == start_done:
                okay = False
            # ---
            # python3 imp.py -start:! -limit:3
            #
            # ---
            lista = api_new.Get_All_pages(start=starts, namespace=namespaces, limit=limite)
            start_done = starts
            for num, page in enumerate(lista, start=1):
                work(page, num, len(lista))
                # ---
                starts = page


if __name__ == "__main__":
    main()
