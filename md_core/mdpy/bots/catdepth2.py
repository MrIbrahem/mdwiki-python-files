#!/usr/bin/env python
"""

python3 core8/pwb.py mdpy/bots/catdepth2

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import sys
import json
import traceback

import time
import os
from datetime import datetime

# ---
from mdpy.bots import mdwiki_api
from mdpy.bots import sql_for_mdwiki
from mdpy.bots.check_title import valid_title  # valid_title(title)

# ---
Day_History = datetime.now().strftime("%Y-%m-%d")
# ---
from pathlib import Path

Dir = str(Path(__file__).parents[0])
# print(f'Dir : {Dir}')
# ---
dir2 = Dir.replace('\\', '/')
dir2 = dir2.split('/mdwiki/')[0] + '/mdwiki'
# ---
# sql_for_mdwiki.mdwiki_sql(query, update = False)
# mdtitle_to_qid = sql_for_mdwiki.get_all_qids()
# sql_for_mdwiki.add_titles_to_qids(tab, add_empty_qid=False)
# ---
all_pages = []


def Get_cat(enlink, print_url=False):
    # ---
    # إيجاد categorymembers والتصانيف الفرعية لتصنيف
    # ---
    # print(' Get_cat for %s' % (enlink) )
    # ---
    if not enlink.startswith('Category:'):
        enlink = f'Category:{enlink}'
    # ---
    params = {
        "action": "query",
        "format": "json",
        "utf8": 1,
        "generator": "categorymembers",
        "gcmtitle": enlink,
        "gcmprop": "title",
        "gcmlimit": "max",
        "redirects": 1,
        "gcmtype": "page|subcat",
    }
    # ---
    # print('<<lightblue>> API_CALLS %d  for %s' % (API_CALLS[1],enlink) )
    # ----
    continue_p = ''
    continue_v = 'x'
    # ---
    table = {}
    # ----
    while continue_v != '':
        # ---
        if continue_v != 'x':
            params[continue_p] = continue_v
        # ---
        continue_v = ''
        # ---
        api = mdwiki_api.post_s(params)
        # ---
        if not api:
            break
        # ---
        continue_d = api.get("continue", {})
        for p, v in continue_d.items():
            if p == 'continue':
                continue
            continue_v = v
            continue_p = p
        # ----
        pages = api.get("query", {}).get("pages", {})
        # ----
        for category in pages:
            # ---
            caca = category
            # ---
            if isinstance(pages, dict):
                caca = pages[category]
            # ---
            cate_title = caca["title"]
            tablese = {'title': caca['title']}
            # ---
            if "ns" in caca:
                tablese['ns'] = caca['ns']
                # print("<<lightblue>> ns: %s" %  caca['ns'])
            # ---
            if 'templates' in caca:
                tablese['templates'] = [x['title'] for x in caca['templates']]
            # ---
            if 'langlinks' in caca:
                tablese['langlinks'] = {fo['lang']: fo['*'] for fo in caca['langlinks']}
            # ---
            table[cate_title] = tablese
            # ---
    # ---
    return table


def subcatquery(title, depth=0, ns="all", limit=0, test=False):
    # ---
    # إيجاد categorymembers والتصانيف الفرعية لتصنيف
    # ---
    # print('<<lightyellow>> catdepth.py sub cat query for %s:%s,depth:%d,ns:%s.' % ('',title,depth,ns) )
    # ---
    start = time.time()
    final = time.time()
    # ---
    if not title.strip().startswith('Category:'):
        title = f'Category:{title.strip()}'
    # ---
    tablemember = Get_cat(title, print_url=True)
    # ---
    # result_table = { x : da for x, da in tablemember.items() if valid_title(x) }
    result_table = {x: da for x, da in tablemember.items() if int(da["ns"]) == 0}
    # ---
    # for x in tablemember: if valid_title(x) :  result_table[x] = tablemember[x]
    # ---
    cat_done = []
    # ---
    new_list = [v['title'] for x, v in tablemember.items() if int(v["ns"]) == 14]
    # ---
    if not isinstance(depth, int) and depth.isdigit():
        depth = int(depth)
    # ---
    if 'newlist' in sys.argv:
        print(f'lenof main cat:{len(result_table)}')
    # ---
    depth_done = 0
    # ---
    while depth > depth_done:  # and ( limit > 0 and len(result_table) < limit ):
        depth_done += 1
        new_tab2 = []
        # ---
        for cat in new_list:
            if cat not in cat_done:
                cat_done.append(cat)
                # ---
                table2 = Get_cat(cat)
                # ---
                for x, tabla in table2.items():
                    # ---
                    if int(tabla["ns"]) == 14 or tabla["title"].startswith('Category:'):
                        new_tab2.append(x)
                    # ---
                    if ns in [0, '0']:
                        if int(tabla["ns"]) == 0:
                            result_table[x] = tabla
                    else:
                        result_table[x] = tabla
        # ---
        new_list = new_tab2
    # ---
    final = time.time()
    # ---
    # if "printresult" in sys.argv: print(result_table)
    # ---
    if 'newlist' in sys.argv:
        delta = int(final - start)
        print(f'<<lightblue>>catdepth.py: find {len(result_table)} pages(ns:{str(ns)}) in {title}, depth:{depth}, subcat:{len(cat_done)} in {delta} seconds')
        if cat_done:
            print(f"subcats:{', '.join(cat_done)}")
    return list(result_table.keys())


def subcatquery2(cat, depth=0, ns="all", limit=0, test=False):
    filename = f'{dir2}/public_html/Translation_Dashboard/cats_cash/{cat}.json'
    # ---
    if cat == 'RTT':
        depth = 2
    # ---
    if not os.path.isfile(filename):
        # ---
        try:
            with open(filename, "w", encoding='utf8') as uu:
                json.dump({}, uu)
        except Exception as e:
            print('Traceback (most recent call last):')
            print(f'<<lightred>> {__file__} Exception:{str(e)}')
            print('CRITICAL:')
            # ---
    # ---
    try:
        with open(filename, "r", encoding="utf-8") as file:
            textn = file.read()
    except Exception:
        print('Traceback (most recent call last):')
        print(traceback.format_exc())
        print('CRITICAL:')
        textn = ''
    Table = json.loads(textn) if textn != '' else {}
    # ---
    if str(Table.get('Day_History', '')) != str(Day_History) or 'newlist' in sys.argv or len(Table['list']) < 1500:
        # ---
        if 'print' in sys.argv:
            print('get new catmembers')
        # ---
        Listo = subcatquery(cat, depth=depth, ns=ns, limit=limit, test=test)
        Table = {}
        # ---
        Table['list'] = [x for x in Listo if valid_title(x)]
        # ---
        Table['Day_History'] = Day_History
        # ---
        with open(filename, "w", encoding='utf8') as aa:
            json.dump(Table, aa)
        # ---
    # ---
    if 'print' in sys.argv:
        print(f"len of list:{len(Table['list'])}")
    # ---
    return Table


def get_RTT():
    # ---
    Listo = subcatquery('RTT', depth='3', ns='0')
    # ---
    # Listo = Listo['list']
    # ---
    for x in Listo[:]:
        if x.startswith('Category:'):
            Listo.remove(x)
    # ---
    return Listo


def make_cash_to_cats(return_all_pages=False):
    # ---
    cats = sql_for_mdwiki.get_db_categories()
    # ---
    for cat, depth in cats.items():
        ca = subcatquery2(cat, depth=depth, ns='all')
        # ---
        print(f"len of pages in {cat}, depth:{depth}, : %d" % len(ca['list']))
        # ---
        for x in ca['list']:
            if x not in all_pages:
                all_pages.append(x)
    # ---
    if return_all_pages:
        return all_pages


if __name__ == '__main__':
    make_cash_to_cats()
