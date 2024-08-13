#!/usr/bin/python3
"""
python3 core8/pwb.py mdpy/sql_for_mdwiki

# ---
from mdapi_sql import sql_for_mdwiki
# sql_for_mdwiki. mdwiki_sql(query, return_dict=False, values=None)
# sql_for_mdwiki. get_all_qids()
# sql_for_mdwiki. set_title_where_qid(new_title, qid)
# sql_for_mdwiki. add_titles_to_qids(tab, add_empty_qid=False)
# sql_for_mdwiki. set_target_where_id(new_target, iid)
# sql_for_mdwiki. set_deleted_where_id(iid)

# pages = sql_for_mdwiki.get_all_pages()
# cats = sql_for_mdwiki.get_db_categories() # title:depth
# sql_for_mdwiki.get_all_pages_all_keys(lang=False)
# ---
"""
from newapi import printe
from mdapi_sql import sql_td_bot

# result = sql_td_bot.sql_connect_pymysql(query, return_dict=return_dict, values=values)


def mdwiki_sql(query, return_dict=False, values=None, **kwargs):
    # ---
    if not query:
        print("query == ''")
        return {}
    # ---
    # print('<<yellow>> newsql::')
    return sql_td_bot.sql_connect_pymysql(query, return_dict=return_dict, values=values)


def get_all_pages():
    return [ta["title"] for ta in mdwiki_sql("select DISTINCT title from pages;", return_dict=True)]


def get_all_pages_all_keys(lang=False, table="pages"):
    lang_line = ""
    # ---
    if lang:
        lang_line = f' where lang = "{lang}"'
    # ---
    if table not in ["pages", "pages_users"]:
        table = "pages"
    # ---
    qua = f"select DISTINCT * from {table} {lang_line};"
    return [ta for ta in mdwiki_sql(qua, return_dict=True)]


def get_db_categories():
    return {c["category"]: c["depth"] for c in mdwiki_sql("select category, depth from categories;", return_dict=True)}


# qids defs


def get_all_qids():
    # ---
    sq = mdwiki_sql("select DISTINCT title, qid from qids;", return_dict=True)
    return {ta["title"]: ta["qid"] for ta in sq}


def add_qid(title, qid):
    printe.output(f"<<yellow>> add_qid()  title:{title}, qid:{qid}")
    # ---
    qua = "INSERT INTO qids (title, qid) SELECT %s, %s;"
    # ---
    values = [title, qid]
    # ---
    return mdwiki_sql(qua, return_dict=True, values=values)


def set_qid_where_title(title, qid):
    printe.output(f"<<yellow>> set_qid_where_title()  title:{title}, qid:{qid}")
    # ---
    qua = "UPDATE qids set qid = %s where title = %s;"
    values = [qid, title]
    # ---
    return mdwiki_sql(qua, return_dict=True, values=values)


def delete_title_from_db(title):
    qua = "DELETE FROM qids where title = %s;"
    # ---
    printe.output(f"<<yellow>> delete_title_from_db() title:{title}")
    # ---
    return mdwiki_sql(qua, return_dict=True, values=[title])


def set_title_where_qid(new_title, qid):
    # ---
    printe.output(f"<<yellow>> set_title_where_qid() new_title:{new_title}, qid:{qid}")
    # ---
    qua = "UPDATE qids set title = %s where qid = %s;"
    values = [new_title, qid]
    # ---
    return mdwiki_sql(qua, return_dict=True, values=values)


def set_target_where_id(new_target, iid):
    # ---
    printe.output(f"<<yellow>> set_target_where_id() new_target:{new_target}, id:{iid}")
    # ---
    if new_target == "" or iid == "":
        return
    # ---
    query = "UPDATE pages set target = %s where id = %s;"
    values = [new_target, iid]
    # ---
    return mdwiki_sql(query, return_dict=True, values=values)


def set_deleted_where_id(iid):
    # ---
    printe.output(f"<<yellow>> set_deleted_where_id(), id:{iid}")
    # ---
    if iid == "":
        return
    # ---
    query = "UPDATE pages set deleted = 1 where id = %s;"
    # ---
    return mdwiki_sql(query, return_dict=True, values=[iid])


def add_titles_to_qids(tab0, add_empty_qid=False):
    # ---
    printe.output(f"<<green>> start add_titles_to_qids {add_empty_qid=}:")
    # ---
    if not tab0:
        printe.output("<<red>> add_titles_to_qids tab0 empty..")
        return
    # ---
    ids_in_db = get_all_qids()
    # ---
    # remove empty titles
    # remove empty qids if add_empty_qid == False
    tab = {t: q for t, q in tab0.items() if t.strip() and (q.strip() or add_empty_qid)}
    # ---
    printe.output(f"<<yellow>> len of tab: {len(tab)}, tab0: {len(tab0)}")
    # ---
    same = {x: qid for x, qid in tab.items() if qid == ids_in_db.get(x)}
    not_in = {x: qid for x, qid in tab.items() if x not in ids_in_db}
    # ---
    printe.output(f"<<yellow>> len of ids_in_db: {len(ids_in_db)}")
    printe.output(f"<<yellow>> len of same qids: {len(same)}")
    printe.output(f"<<yellow>> len of not_in: {len(not_in)}")
    # ---
    for title, new_qid in not_in.items():
        add_qid(title, new_qid)
    # ---
    rest_qids = {x: qid for x, qid in tab.items() if x not in same and x not in not_in}
    # ---
    printe.output(f"<<yellow>> len of rest_qids: {len(rest_qids)}.")
    # ---
    rest_qids = {x: qid for x, qid in rest_qids.items() if qid}
    # ---
    printe.output(f"<<yellow>> len of rest_qids: {len(rest_qids)} after remove empty qids..")
    # ---
    for title, new_qid in rest_qids.items():
        # ---
        if not ids_in_db.get(title):
            set_qid_where_title(title, new_qid)
    # ---
    has_diff_qid_in_db = {x: qid for x, qid in rest_qids.items() if ids_in_db.get(x)}
    # ---
    printe.output(f"<<yellow>> len of last_qids: {len(has_diff_qid_in_db)} after remove empty qids..")
    # ---
    for t, q in has_diff_qid_in_db.items():
        qid_in = ids_in_db.get(t)
        printe.output(f"<<yellow>>skip... set_qid_where_title({t=}) {qid_in=}, {q=}")