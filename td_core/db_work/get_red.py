#!/usr/bin/python3
#   himo
"""
اصلاح التحويلات في قواعد البيانات

python3 core8/pwb.py db_work/get_red

"""
#
# (C) Ibrahem Qasim, 2022
#
#
import os
from datetime import datetime

# ---
from newapi import printe
from mdapi_sql import sql_for_mdwiki
from apis import mdwiki_api

mdwiki_to_qid = sql_for_mdwiki.get_all_qids()

def get_table():
    table = {}
    # ---
    titles = list(mdwiki_to_qid.keys())
    # ---
    done = 0
    # ---
    len_grup = 100
    # ---
    for i in range(0, len(titles), len_grup):
        group = titles[i: i + len_grup]
        # ---
        done += len(group)
        # ---
        asa = mdwiki_api.get_redirect(group)
        # ---
        print(f'work on {len_grup} pagees, done: {done}/{len(titles)}.')
        # ---
        table = {**table, **asa}
    # ---
    print(f'len of table {len(table)} ')
    # ---
    return table
def get_pages():
    # ---
    table = get_table()
    # ---
    tat = ''
    # ---
    rep = 0
    remo = 0
    # ---
    to_add = {}
    to_del = []
    # ---
    for old_title, new_title in table.items():
        ll = f'"old_title: {old_title}" to: "{new_title}",\n'
        # ---
        # replace_titles(old_title, new_title)
        # ---
        new_title_qid = mdwiki_to_qid.get(new_title, False)
        old_title_qid = mdwiki_to_qid.get(old_title, False)
        # ---
        if old_title_qid:
            if not new_title_qid:
                # استبدال
                rep += 1
                # ---
                printe.output(f'<<yellow>>{ll.strip()}')
                # ---
                sql_for_mdwiki.set_title_where_qid(new_title, old_title_qid)
                # ---
                to_del.append(old_title)
                to_add[new_title] = old_title_qid
                # ---
                tat += ll
                # ---
            elif new_title_qid == old_title_qid:
                remo += 1
                to_del.append(old_title)
    # ---
    printe.output('===================')
    if tat != '':
        printe.output('<<red>> redirects: ')
        printe.output(tat)
        printe.output('===================')
    # ---
    printe.output(f'replace {rep} pages. ')
    printe.output(f'remove {remo} pages. ')
    # ---
    if to_del:
        printe.output(f'delete {len(to_del)} pages. ')
        printe.output(to_del)
    # ---
    if to_add:
        printe.output(f'add {len(to_add)} pages. ')
        printe.output(to_add)
        sql_for_mdwiki.add_titles_to_qids(to_add)

if __name__ == '__main__':
    get_pages()
