#!/usr/bin/python3
"""
بوت فرعي من
after_translate/sql.py

# ---
from after_translate.bots import add_to_wd
# add_to_wd.add_tab_to_wd(New_Table_by_lang)
# ---

"""

import re

# ---
from pymysql.converters import escape_string
from newapi import printe
from mdapi_sql import sql_for_mdwiki
from mdpy.bots import en_to_md
from mdpy import orred

# ---
from apis import wiki_api
from apis import mdwiki_api
from apis import wikidataapi

# ---
wddone_table = """CREATE TABLE wddone (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    mdtitle VARCHAR(120) NOT NULL,
    target VARCHAR(120) NOT NULL,
    lang VARCHAR(30) NOT NULL,
    user VARCHAR(120) NOT NULL
    )"""
# ---
que_wddone = """
select mdtitle,target,lang,user
from wddone
;
"""
# ---
sq_dd = sql_for_mdwiki.select_md_sql(que_wddone, return_dict=True)
# ---
wddone_by_u_t = []
wddone_by_u_l_mdt = []
# ---
for tab in sq_dd:
    mdtitle = tab["mdtitle"]
    target = tab["target"]
    lang = tab["lang"]
    user = tab["user"]
    # ---
    wddone_by_u_t.append((user, target))
    wddone_by_u_l_mdt.append((user, lang, mdtitle))


def work_with_2_qids(oldq, new_q):
    # ---
    printe.output("=============================")
    printe.output(f"start:work_with_2_qids: oldq:{oldq}, new_q:{new_q}")
    # ---
    fas = wikidataapi.Get_sitelinks_From_Qid(oldq)
    # {'sitelinks': {'enwiki': 'User:Mr. Ibrahem/Baricitinib', 'orwiki': 'ବାରିସିଟିନିବ'}, 'q': 'Q112331510'}
    # ---
    false_sitelinks = fas.get("sitelinks", {})
    # ---
    len_sites = len(false_sitelinks)
    # ---
    printe.output(f"<<blue>> len_sites {len_sites}")
    # ---
    printe.output(false_sitelinks)
    # ---
    en = false_sitelinks.get("enwiki", "")
    # ---
    if en.startswith("User:Mr. Ibrahem"):
        printe.output(f"<<blue>> remove sitelink {en}")
        remove = wikidataapi.post({"action": "wbsetsitelink", "id": oldq, "linksite": "enwiki"}, token=True)
        if "success" in remove:
            len_sites -= 1
            printe.output("<<green>> **remove sitelink true.")
        else:
            printe.output("<<red>> **remove sitelink false.")
            printe.output(remove)
        # ---
        remove2 = wikidataapi.post({"action": "wbsetlabel", "id": oldq, "language": "en", "value": ""}, token=True)
        if "success" in remove2:
            len_sites -= 1
            printe.output("<<green>> **remove2 label true.")
        else:
            printe.output("<<red>> **remove2 label false.")
            printe.output(remove2)
    # ---
    if len_sites in [1, 0]:
        printe.output("<<blue>> merge qids")
        return wikidataapi.WD_Merge(oldq, new_q)
    # ---
    return False


def add_wd(qid, enlink, lang, target):
    """Add a site link to a Wikidata item.

    This function adds a site link to a specified Wikidata item based on the
    provided parameters. It constructs the necessary API request to link the
    given target to either an existing item identified by `qid` or a new
    item identified by `enlink`. The function handles both cases and checks
    for potential conflicts with existing site links.

    Args:
        qid (str): The unique identifier for the Wikidata item (QID).
        enlink (str): The English link to the item if `qid` is not provided.
        lang (str): The language code for the site link (e.g., 'ar' for Arabic).
        target (str): The title of the site link to be added.

    Returns:
        bool: True if the site link was successfully added, False otherwise.
    """

    print("add_wd:")
    params = {
        "action": "wbsetsitelink",
        "linktitle": target,
        "linksite": f"{lang}wiki",
        "format": "json",
        "utf8": 1,
    }
    # ---
    if qid != "":
        params["id"] = qid
    else:
        params["title"] = enlink
        params["site"] = "enwiki"
    # ---
    ss = wikidataapi.post(params, token=True)
    # ---
    printe.output(str(ss))
    # ---
    if ss and "success" in ss:
        return True
    # ---
    # ss = {'error': {'code': 'failed-save', 'info': 'The save has failed.', 'messages': [{'name': 'wikibase-api-failed-save', 'parameters': [], 'html': {'*': 'لم ينجح الحفظ.'}}, {'name': 'wikibase-validator-sitelink-conflict', 'parameters': ['[https://ar.wikipedia.org/wiki/%D8%A5%D9%8A%D9%81%D8%A7%D9%83%D8%A7%D9%81%D8%AA%D9%88%D8%B1 arwiki:إيفاكافتور]', '[[Q113952553|Q113952553]]'], 'html': {'*': 'الوصلة <a class="external text" href="https://ar.wikipedia.org/wiki/%D8%A5%D9%8A%D9%81%D8%A7%D9%83%D8%A7%D9%81%D8%AA%D9%88%D8%B1">arwiki:إيفاكافتور</a> مستخدمة للعنصر <a href="/wiki/Q113952553" title="Q113952553">Q113952553</a>. يمكنك إزالتها من <a href="/wiki/Q113952553" title="Q113952553">Q113952553</a> إن لم تكن مناسبة هناك أو أن تدمج العنصرين إذا كانا عن نفس الموضوع تماماً.'}}], '*': 'See https://www.wikidata.org/w/api.php for API usage. Subscribe to the mediawiki-api-announce mailing list at &lt;https://lists.wikimedia.org/postorius/lists/mediawiki-api-announce.lists.wikimedia.org/&gt; for notice of API deprecations and breaking changes.'}, 'servedby': 'mw1402'}
    # ---
    if not isinstance(ss, dict):
        return False
    # ---
    # error = ss.get('error', {}).get('code', {})
    # ---
    if "wikibase-validator-sitelink-conflict" in str(ss):
        qii = re.match(r".*\"\>(Q\d+)\<\/a.*", str(ss))
        if qii:
            qid2 = qii.group(1)
            # ---
            if not qid:
                qids_from_wiki = wiki_api.Get_page_qid("en", enlink)
                # ---
                for _, tab in qids_from_wiki.items():
                    qid = tab.get("q", "")
                    break
            return work_with_2_qids(qid2, qid)
    # ---
    return False


def Add_to_wikidata(mdtitle, lang, target, user):
    # ---
    qid = en_to_md.mdtitle_to_qid.get(mdtitle, "")
    enlink = en_to_md.mdwiki_to_enwiki.get(mdtitle, mdtitle)
    # ---
    ss = add_wd(qid, enlink, lang, target)
    # ---
    if ss is True:
        # ---
        mdtit = escape_string(mdtitle)
        tar = escape_string(target)
        user = escape_string(user)
        # ---
        done_qua = f"""
            INSERT INTO wddone (mdtitle, target, lang, user)
            SELECT '{mdtit}', '{tar}', '{lang}', '{user}'
            WHERE NOT EXISTS (SELECT 1 FROM wddone
                WHERE mdtitle = '{mdtit}'
                AND target = '{tar}'
                AND lang = '{lang}'
                AND user = '{user}'
            )"""
        # ---
        printe.output("**************")
        printe.output(done_qua)
        printe.output("**************")
        sql_for_mdwiki.mdwiki_sql(done_qua, update=True)
    # ---
    tat = mdwiki_api.GetPageText(mdtitle)
    # ---
    lalas = f"[[{lang}:"
    # ---
    line = f"[[{lang}:{target}]]"
    if tat != "" and tat.find(line) == -1 and tat.find(lalas) == -1:
        mdwiki_api.Add_To_Bottom(f"\n{line}", f"add link to {line}", mdtitle)
    # ---
    if lang == "or":
        orred.create_redirect(target, mdtitle)


def add_tab_to_wd(table):
    # ---
    for _, tab in table.items():
        # ---
        number = 0
        # ---
        for tt in tab:
            tabe = tab[tt]  # {"mdtitle": md_title.replace("'" , "\'") , "target": target, "user":user.replace("'" , "\'"),"lang":lange}
            # ---
            mdtitle = tabe["mdtitle"]
            lang = tabe["lang"]
            target = tabe["target"]
            user = tabe["user"]
            ns = tabe["namespace"]
            # ---
            if str(ns) != "0":
                continue
            # ---
            if (user, target) in wddone_by_u_t:
                continue
            # ---
            if (user, lang, mdtitle) in wddone_by_u_l_mdt:
                continue
            # ---
            number += 1
            # ---
            printe.output("=========================")
            printe.output(f"<<green>>p {number}/{len(tab)}: mdtitle:{mdtitle},lang:{lang},target:{target}")
            # ---
            Add_to_wikidata(mdtitle, lang, target, user)


# ---
