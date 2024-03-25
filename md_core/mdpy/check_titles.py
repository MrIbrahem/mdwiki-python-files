#!/usr/bin/python3
"""
التحقق من المقالات التحويلات أو المحذوفة

python3 core8/pwb.py mdpy/check_titles -lang:ur

python3 core8/pwb.py mdpy/check_titles test

"""
#
# (C) Ibrahem Qasim, 2024
#
#

import sys
import tqdm
import time
# ---
from newapi import printe
from mdpy.bots import sql_for_mdwiki
from newapi.wiki_page import MainPage, NEW_API
from newapi.mdwiki_page import MainPage as md_MainPage
# api_new  = NEW_API('ar', family='wikipedia')
# infos  = Find_pages_exists_or_not(titles)


def get_langs_tabs():
    # ---
    que = 'select id, title, lang, target from pages where target != "";'
    # ---
    lang_to_get = ''
    for arg in sys.argv:
        arg, _, value = arg.partition(":")
        if arg == "-lang":
            lang_to_get = value
    # ---
    langs = {}
    # ---
    printe.output(que)
    # ---
    for tab in sql_for_mdwiki.mdwiki_sql(que, return_dict=True):
        lang = tab['lang']
        if not lang in langs:
            langs[lang] = []
        langs[lang].append(tab)
    # ---
    if lang_to_get in langs:
        langs = {lang_to_get: langs[lang_to_get]}
    # ---
    return langs


def get_new_target_log(lang, target):
    # ---
    done = []
    # ---
    to_check = target
    # ---
    api_new = NEW_API(lang, family='wikipedia')
    # ---
    printe.output(f'get_new_target_log() lang:{lang}, target:{target}')
    # ---
    n = 0
    # ---
    while to_check != '':
        # ---
        n += 1
        # ---
        printe.output(f'<<blue>> get_new_target_log({n}) lang:{lang}, target:{target}')
        # ---
        logs = api_new.get_logs(to_check)
        # ---
        new = ''
        # ---
        for log in logs:
            title = log.get("title", "")
            new = log.get("params", {}).get("target_title", "")
            # ---
            if new:
                break
        # ---
        if new:
            done.append(to_check)
            printe.output(f'> title:{to_check} moved to:{new}')
            to_check = new
        else:
            break
        # ---
        if to_check in done:
            printe.output(f'to_check:{to_check} in done')
            break
    # ---
    printe.output(f'get_new_target_log() lang:{lang}, target:{target}, new:{to_check}')
    # ---
    return to_check


def add_text(tab):
    # ---
    if not tab:
        return
    # ---
    date = time.strftime("%Y-%m-%d", time.gmtime())
    # ---
    wikitext = f'== {date} ==\n'
    wikitext += '{|\n|-\n! lang !! target !! new_target\n|-\n'
    # ---
    for x in tab:
        wikitext += f'|-\n| {x[0]} || [[:{x[0]}:{x[1]}]] || [[:{x[0]}:{x[2]}]]\n'
    # ---
    wikitext += '|}\n'
    # ---
    printe.output(wikitext)
    itle = 'User:Mr. Ibrahem/tofix'
    # ---
    page = md_MainPage(itle, 'www', family='mdwiki')
    # ---
    text = page.get_text()
    newtext = f"{wikitext}\n{text}"
    # ---
    page.save(newtext=newtext, summary="update", nocreate=0)


def start():
    # ---
    text = []
    # ---
    langs = get_langs_tabs()
    # ---
    for lang, tabs in langs.items():
        # ---
        printe.output(f'<<green>> lang:{lang}, has {len(tabs)} tabs')
        # ---
        titles = [x['target'] for x in tabs]
        # ---
        api_new = NEW_API(lang, family='wikipedia')
        pages = api_new.Find_pages_exists_or_not(titles, get_redirect=True)
        # ---
        missing = [x for x, v in pages.items() if not v]
        redirects = [x for x, v in pages.items() if v == 'redirect']
        # ---
        printe.output(f'lang:{lang}, missing:{len(missing)}, redirects:{len(redirects)}')
        # ---
        new_tabs = [tab for tab in tabs if tab['target'] in missing or tab['target'] in redirects]
        # ---
        printe.output(f'lang:{lang}, has {len(new_tabs)} new tabs')
        # ---
        for tab in tqdm.tqdm(new_tabs):
            iid, lang, target = tab["id"], tab["lang"], tab["target"]
            # ---
            new_target = ''
            # ---
            if target in missing and 'onlyredirect' not in sys.argv:
                printe.output(f'<<red>> page "{target}" not exists in {lang}')
                new_target = get_new_target_log(lang, target)
            elif target in redirects:
                page = MainPage(target, lang, family='wikipedia')
                new_target = page.get_redirect_target()
            # ---
            if new_target:
                page2 = MainPage(new_target, lang, family='wikipedia')
                # ---
                if page2.exists() and not page2.isRedirect():
                    printe.output(f'<<yellow>> set_target_where_id() new_target:{new_target}, old target:{target}')
                    sql_for_mdwiki.set_target_where_id(new_target, iid)
                    text.append([lang, target, new_target])
    # ---
    if text:
        add_text(text)


if __name__ == "__main__":
    if 'test' in sys.argv:
        # get_new_target_log("ar", "الحكَّة المهبلية")
        get_new_target_log("fr", "L'encéphalite à tiques")
    else:
        start()
