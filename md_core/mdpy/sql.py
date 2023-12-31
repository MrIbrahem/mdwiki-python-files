#!/usr/bin/python3
"""
بوت قواعد البيانات

python3 core8/pwb.py mdpy/sql justsql break
python3 core8/pwb.py mdpy/sql justsql
python3 core8/pwb.py mdpy/sql

"""

#
# (C) Ibrahem Qasim, 2022
#
#
import re
import os
import sys
import time as tttime
from pymysql.converters import escape_string
# ---
from mdpy.bots import add_to_wd
from mdpy.bots import py_tools
from mdpy import printe
from mdpy.bots import wiki_sql
from mdpy.bots import sql_for_mdwiki
from mdpy.others.fixcat import cat_for_pages
# ---
from mdpy.sql_bots.add_to_mdwiki import add_to_mdwiki_sql
# ---
Lang_usr_mdtitle = {}
targets_done = {}
Langs_to_title_and_user = {}
to_update_lang_user_mdtitle = {}
# ---
skip_langs = ['zh-yue', 'ceb']
# ---
New_Table_by_lang = {}
# ---
Skip_titles = {
    'Mr. Ibrahem': {
        'targets': [
            'جامعة نورث كارولاينا',
            'جامعة ولاية كارولينا الشمالية إيه آند تي',
            'نيشان راجاميترابورن',
        ],
        'mdtitles': [],
    },
    'Avicenno': {
        'targets': ['ألم فرجي', 'لقاح المكورة السحائية', 'استئصال اللوزتين'],
        'mdtitles': [],
    },
    'Subas Chandra Rout': {
        'targets': [],
        'mdtitles': [
            "Wilms' tumor",
            "Sheehan's syndrome",
            "Membranous nephropathy",
        ],
    },
}
# ---
Skip_titles_global = ['جامعة نورث كارولاينا', 'جامعة ولاية كارولينا الشمالية إيه آند تي', 'نيشان راجاميترابورن', 'موميتازون']
# ---
tit_user_lang = {}
printsql = {1: False}
# ---
query_main_old = '''
    select DISTINCT p.page_title, c.comment_text , a.actor_name , r.rev_timestamp
    from change_tag t
    INNER JOIN change_tag_def ctd on ctd.ctd_id = t.ct_tag_id
    INNER JOIN revision r on r.rev_id = t.ct_rev_id
    INNER JOIN actor a ON r.rev_actor = a.actor_id
    inner join comment c on c.comment_id = r.rev_comment_id
    INNER JOIN page p on r.rev_page=p.page_id
    where ctd.ctd_name in ("contenttranslation", "contenttranslation-v2") #id = 3 # id = 120
    and r.rev_parent_id = 0
    #AND a.actor_name in ('Mr. Ibrahem')
    AND r.rev_timestamp > 20210101000000
    #and comment_text like "%[[:en:Special:Redirect/revision/%|User:Mr. Ibrahem/%]]%"
    and comment_text like "%User:Mr. Ibrahem/%"
    and p.page_namespace = 0
    #limit 10
'''
# ---
query_main = '''
    select DISTINCT p.page_title as title,
    SUBSTRING_INDEX(SUBSTRING_INDEX(c.comment_text, 'Ibrahem/', -1), ']]', 1) as comment_text,
    a.actor_name, r.rev_timestamp, p.page_namespace, r.rev_parent_id
    from change_tag t
    INNER JOIN change_tag_def ctd on ctd.ctd_id = t.ct_tag_id
    INNER JOIN revision r on r.rev_id = t.ct_rev_id
    INNER JOIN actor a ON r.rev_actor = a.actor_id
    inner join comment c on c.comment_id = r.rev_comment_id
    INNER JOIN page p on r.rev_page=p.page_id
    where ctd.ctd_name in ("contenttranslation", "contenttranslation-v2") #id = 3 # id = 120
    #and r.rev_parent_id = 0
    AND r.rev_timestamp > 20210101000000
    and comment_text like "%User:Mr. Ibrahem/%"
    #and p.page_namespace = 0
    group by p.page_title, a.actor_name, c.comment_text
'''

def dodo_sql():
    # ---
    lang_o = ''
    # ---
    for arg in sys.argv:
        arg, _, value = arg.partition(':')
        if arg in ['lang', '-lang']:
            lang_o = value
            Langs_to_title_and_user[value] = {}
        # ---
        if arg == 'printsql':
            printsql[1] = True
    # ---
    que = 'select title, user, lang, target from pages '
    # ---
    if lang_o != '':
        que += f' where lang = "{lang_o}"'
    # ---
    que += ' ;'
    # ---
    printe.output(que)
    # ---
    sq = sql_for_mdwiki.mdwiki_sql(que, return_dict=True)
    # ---
    len_no_target = 0
    len_done_target = 0
    # ---
    for tab in sq:
        mdtitle = tab['title']
        user = tab['user']
        target = tab['target']
        lang = tab['lang'].lower()
        # ---
        if lang_o != '' and lang != lang_o.strip():
            continue
        # ---
        tul = mdtitle + user + lang
        tit_user_lang[tul] = target
        # ---
        if lang not in Lang_usr_mdtitle:
            Lang_usr_mdtitle[lang] = {}
        if user not in Lang_usr_mdtitle[lang]:
            Lang_usr_mdtitle[lang][user] = []
        # ---
        Lang_usr_mdtitle[lang][user].append(mdtitle)
        # ---
        if lang not in Langs_to_title_and_user:
            Langs_to_title_and_user[lang] = {}
        if lang not in to_update_lang_user_mdtitle:
            to_update_lang_user_mdtitle[lang] = {}
        # ---
        if user not in to_update_lang_user_mdtitle[lang]:
            to_update_lang_user_mdtitle[lang][user] = []
        # ---
        if target == "":
            len_no_target += 1
            # ---
            Langs_to_title_and_user[lang][mdtitle] = user
            # ---
            to_update_lang_user_mdtitle[lang][user].append(mdtitle)
            # ---
        else:
            # ---
            if lang not in targets_done:
                targets_done[lang] = {}
            # ---
            target = target.replace("_", " ")
            target2 = py_tools.ec_de_code(target, 'encode')
            # ---
            lineout = 'done. <<lightgreen>> target:%s for mdtit:%s, user:%s'
            laloly = lineout % (target.ljust(40), mdtitle.ljust(30), user)
            # ---
            # printe.output(laloly)
            # ---
            len_done_target += 1
            # ---
            # targets_done[lang][mdtitle] = { "user" : user , "target" : target }
            # targets_done[lang][mdtitle] = { "user" : user , "target" : target }
            # targets_done[lang][py_tools.ec_de_code(target , 'encode')] = { "user" : user , "target" : target }
            # ---
            targets_done[lang][target] = {"user": user, "target": target}
            targets_done[lang][target2] = {"user": user, "target": target}
    # ---
    printe.output(f'<<lightyellow>> find {len_done_target} with target, and {len_no_target} without in mdwiki database. ')
    # ---
    if 'print' in sys.argv:
        printe.output(Langs_to_title_and_user)
    # ---
    tttime.sleep(3)


def start(result, lange):
    printe.output(f'sql.py len(result) = "{len( result )}"')
    # ---
    # texddt = '\n'
    # ---
    for lis in result:
        # ---
        # printe.output( lis )
        # ---
        target        = lis['title']
        co_text       = lis['comment_text']
        user          = lis['actor_name']
        pupdate       = lis['rev_timestamp']
        namespace     = lis['page_namespace']
        rev_parent_id = lis['rev_parent_id']
        # ---
        # target        = py_tools.Decode_bytes(lis[0])
        # co_text       = py_tools.Decode_bytes(lis[1])
        # user          = py_tools.Decode_bytes(lis[2])
        # pupdate       = py_tools.Decode_bytes(lis[3])
        # namespace     = py_tools.Decode_bytes(lis[4])
        # rev_parent_id = py_tools.Decode_bytes(lis[5])
        # ---
        namespace = str(namespace)
        pupdate = pupdate[:8]
        pupdate = re.sub(r'^(\d\d\d\d)(\d\d)(\d\d)$', r'\g<1>-\g<2>-\g<3>', pupdate)
        # ---
        md_title = co_text.replace("_", " ").strip()
        md_title = re.sub("/full$", "", co_text)
        # ---
        target = target.replace("_", " ")
        # ---
        user = user.replace("_", " ")
        # ---
        if target in Skip_titles_global:
            continue
        if target in Skip_titles.get(user, {}).get('targets', []):
            continue
        # ---
        if md_title in Skip_titles.get(user, {}).get('mdtitles', []):
            continue
        # ---
        Taba2 = {"mdtitle": md_title, "target": target, "user": user, "lang": lange, "pupdate": pupdate, "namespace": namespace}
        # ---
        laloly = f'<<lightyellow>> target:{lange}:{target.ljust(40)}, ns:{namespace.ljust(3)} for mdtit:<<lightyellow>>{md_title.ljust(30)}, user:<<lightyellow>>{user}'
        # ---
        tgd = targets_done.get(lange, {})
        # ---
        target2 = py_tools.ec_de_code(target, 'encode')
        # ---
        tul = md_title + user + lange
        tul_target = tit_user_lang.get(tul, '')
        # ---
        cattest = cat_for_pages.get(md_title, '')
        # ---
        if namespace != '0':
            if 'ns' in sys.argv and tul_target == '' and cattest:
                printe.output(laloly)
            continue
        # ---
        # للتأكد من الصفحات غير المنشورة
        if target2 not in tgd and target not in tgd:
            # ---
            if tul_target == '':
                New_Table_by_lang[lange][md_title] = Taba2
                printe.output(laloly)
            elif tul_target == target:
                printe.output(f'target already in, {target}')
            else:
                printe.output(f'puplished target: {tul_target} != target to add: {target}')


def main():
    # ---
    dodo_sql()
    # ---
    numb_lang = 0
    lnn = len(Langs_to_title_and_user.keys())
    # ---
    # for lange,lal in Langs_to_title_and_user.items():
    for lange in Langs_to_title_and_user:
        # ---
        New_Table_by_lang[lange] = {}
        # ---
        numb_lang += 1
        # ---
        printe.output(' \\/\\/\\/\\/\\/ ')
        printe.output('mdwiki/mdpy/sql.py: %d Lang from %s : "%s"' % (numb_lang, lnn, lange))
        # ---
        result = {}
        # ---
        qua = query_main
        # ---
        if lange == 'ar':
            qua += """
                and p.page_title not in (
                    'جامعة_نورث_كارولاينا',
                    'جامعة_ولاية_كارولينا_الشمالية_إيه_آند_تي',
                    'نيشان_راجاميترابورن'
                )
            """
        # ---
        qua += '\n;'
        # ---
        if lange in skip_langs:
            printe.output(f'skip lang:{lange}')
            continue
        # ---
        if 'printquery' in sys.argv:
            print(qua)
        # ---
        # result = wiki_sql.Make_sql_many_rows(qua, wiki=str(lange))
        result = wiki_sql.sql_new(qua, str(lange))
        # ---
        if result != {}:
            start(result, lange)
        # ---
        add_to_wd.add_tab_to_wd({lange: New_Table_by_lang[lange]})
        # ---
        add_to_mdwiki_sql({lange: New_Table_by_lang[lange]}, to_update_lang_user_mdtitle)


if __name__ == '__main__':
    main()
