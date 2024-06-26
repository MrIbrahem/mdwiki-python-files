#!/usr/bin/env python
#   himo
"""
python3 core8/pwb.py mdpages/cashwd

"""

#
# (C) Ibrahem Qasim, 2022
#
#
import json
import os
import traceback
from datetime import datetime
import pywikibot
from pathlib import Path
# ---
from mdpy import printe
from mdpy.bots import sql_for_mdwiki
from mdpy.bots import en_to_md  # en_to_md.mdtitle_to_qid #en_to_md.enwiki_to_mdwiki # en_to_md.mdwiki_to_enwiki
from mdpy.bots import mdwiki_api
from mdpy.bots import wikidataapi
from mdpy.bots.check_title import valid_title  # valid_title(title)
# ---
Dir = str(Path(__file__).parents[0])
# print(f'Dir : {Dir}')
# ---
dir2 = Dir.replace('\\', '/')
dir2 = dir2.split('/mdwiki/')[0] + '/mdwiki'
# ---
Day_History = datetime.now().strftime("%Y-%m-%d")
# ---
Dashboard_path = f'{dir2}/public_html/Translation_Dashboard'
# ---
redirects_qids = {}
mis_qids = []
# ---
main_table_sites = {}
# ---
missing = {'all': 0, 'date': Day_History, 'langs': {}}
# ---
skip_codes = ["commons", "species", "ary", "arz", "meta"]
# ---
change_codes = {
    "nb": "no",
    "bat_smg": "bat-smg",
    "be_x_old": "be-tarask",
    "be-x-old": "be-tarask",
    "cbk_zam": "cbk-zam",
    "fiu_vro": "fiu-vro",
    "map_bms": "map-bms",
    "nds_nl": "nds-nl",
    "roa_rup": "roa-rup",
    "zh_classical": "zh-classical",
    "zh_min_nan": "zh-min-nan",
    "zh_yue": "zh-yue",
}


def get_qids_sitelinks(qidslist):
    """
    Retrieves sitelinks for a list of Wikidata QIDs.

    Args:
        qidslist (dict): A dictionary containing QIDs as keys and mdwiki titles as values.

    Returns:
        dict, dict: Two dictionaries representing the sitelinks for each QID, one using mdtitle as keys and the other using sitelinks as keys.

    Raises:
        No explicit exceptions are raised.

    Details:
        This function retrieves sitelinks from Wikidata for a list of QIDs. It processes the QIDs in batches of 100 and organizes the results into two dictionaries, one using mdtitle as keys and the other using sitelinks as keys.
    """
    # ---
    qs_list = list(qidslist.keys())
    # ---
    params_wd = {
        "action": "wbgetentities",
        "format": "json",
        # "ids": ,
        "redirects": "yes",
        "props": "sitelinks",
        "utf8": 1,
    }
    # ---
    #  {"heads": ["arwiki"], "qids": {"Q1": {"mdtitle": "test", "sitelinks": {"arwiki": "test"}}}}
    table_d = {"heads": [], "qids": {}}
    table_l = {"heads": [], "qids": {}}
    # ---
    heads = []
    # ---
    numb = 0
    # ---
    all_entities = {}
    # ---
    for i in range(0, len(qs_list), 100):
        # ---
        qids = qs_list[i: i + 100]
        # ---
        params_wd["ids"] = '|'.join(qids)
        # ---
        printe.output(f'<<lightgreen>> done:{len(all_entities)} from {len(qidslist)}, get sitelinks for {len(qids)} qids.')
        # ---
        json1 = wikidataapi.post(params_wd, apiurl='https://www.wikidata.org/w/api.php')
        # ---
        if json1:
            # ---
            entities = json1.get("entities", {})
            # ---
            all_entities = {**all_entities, **entities}
        # ---
        for _qid_1, kk in all_entities.items():
            # ---
            numb += 1
            if "missing" in kk:
                # ---
                mis_qids.append(kk.get("id"))
                # ---
                continue
            # ---
            redirects = kk.get("redirects", {})
            if redirects:  # "redirects": {"from": "Q113489270","to": "Q22792051"}
                redirects_qids[redirects.get("from")] = redirects.get("to")
            # ---
            qid = kk.get("id", '')
            # ---
            if qid != '' and qid not in table_d["qids"]:
                table_d["qids"][qid] = {"mdtitle": '', "sitelinks": {}}
                table_l["qids"][qid] = {"mdtitle": '', "sitelinks": []}
            # ---
            mdwiki_title = qidslist.get(qid, '')
            if mdwiki_title != '':
                table_d["qids"][qid]["mdtitle"] = mdwiki_title
                table_l["qids"][qid]["mdtitle"] = mdwiki_title
            # ---
            sitelinks = {}
            # ---
            # "abwiki": {"site": "abwiki","title": "Обама, Барак","badges": []}
            # ---
            for _, tab in kk.get("sitelinks", {}).items():
                # ---
                title = tab.get("title", '')
                site = tab.get("site", '')
                # ---
                if site in skip_codes or site[:-4] in skip_codes:
                    continue
                # ---
                if title == '' or not site.endswith("wiki"):
                    continue
                # ---
                site = site[:-4]
                # ---
                site = change_codes.get(site) or site
                # ---
                if site not in heads:
                    heads.append(site)
                # ---
                if site not in main_table_sites:
                    main_table_sites[site] = []
                # ---
                # add mdwiki title to cash_exists/wiki.json table
                # ---
                if mdwiki_title != '' and mdwiki_title not in main_table_sites[site]:
                    main_table_sites[site].append(mdwiki_title)
                # ---
                sitelinks[site] = title
            # ---
            table_d["qids"][qid]["sitelinks"] = sitelinks
            table_l["qids"][qid]["sitelinks"] = list(sitelinks.keys())
            # ---
    # ---
    table_d["heads"] = heads
    table_l["heads"] = heads
    # ---
    return table_d, table_l


def cash_wd():
    # ---
    printe.output('<<lightgreen>> cash_wd')
    # ---
    titles = []
    # ---
    cac = sql_for_mdwiki.get_db_categories()
    # ---
    for cat, dep in cac.items():
        # ---
        mdwiki_pages = mdwiki_api.subcatquery(cat, depth=dep, ns='0')
        # ---
        titles.extend([dd for dd in mdwiki_pages if valid_title(dd) and dd not in titles])
    # ---
    printe.output(f'<<lightgreen>> len of mdwiki_api.subcatquery:RTT:{len(titles)}.')
    # ---
    qids_list = {}
    # ---
    missing['all'] = len(titles)
    # ---
    for x in titles:
        # ---
        qid = en_to_md.mdtitle_to_qid.get(x, '')
        # ---
        if qid != '':
            qids_list[qid] = x
    # ---
    lists, _table_l = get_qids_sitelinks(qids_list)
    # ---
    with open(f'{Dashboard_path}/Tables/sitelinks.json', "w", encoding="utf-8") as aa:
        json.dump(lists, aa)
    # ---
    # json.dump( table_l, open( Dashboard_path + '/Tables/sitelinks_list.json' , "w", encoding="utf-8"), ensure_ascii=False, indent=2 )
    # ---
    # table_to_log = { "redirects": redirects_qids, "missing": mis_qids }
    # ---
    # json.dump( table_to_log, open( Dashboard_path + '/Tables/qid_redirects_missing.json' , "w", encoding="utf-8") )
    # ---
    for site, miss_list in main_table_sites.items():
        # printe.output('<<lightblue>> main_table_sites:%s, len:%d.' % (site, len(miss_list)) )
        # ---
        # remove duplicates
        miss_list = list(set(miss_list))
        # ---
        leeen = len(titles) - len(miss_list)
        missing['langs'][site] = {'missing': leeen, 'exists': len(miss_list)}
        # ---
        json_file = f'{Dashboard_path}/cash_exists/{site}.json'
        # ---
        if not os.path.exists(json_file):
            printe.output(f'.... <<lightred>> file:"{site}.json not exists ....')
        # ---
        # dump miss_list to json_file
        try:
            with open(json_file, "w", encoding="utf-8") as aa:
                json.dump(miss_list, aa, ensure_ascii=False, indent=2)
            printe.output(f'<<lightgreenn>>dump to cash_exists/{site}.json done..')
        except Exception:
            pywikibot.output('Traceback (most recent call last):')
            pywikibot.output(traceback.format_exc())
            pywikibot.output('CRITICAL:')
            continue
    # ---
        """
    Retrieves Wikidata QIDs for a list of mdwiki titles, obtains sitelinks for each QID, and saves the results in JSON files.

    Returns:
        None
    """
    # email_address = "ibrahem.al-radaei@outlook.com"
    # send aleart email to email_address
    # ---
    noqids = sorted([x for x in titles if x not in en_to_md.mdtitle_to_qid])
    # ---
    with open(f'{Dashboard_path}/Tables/noqids.json', "w", encoding="utf-8") as dd:
        json.dump(noqids, dd)
    # ---
    # redirects_qids
    # mis_qids
    # ---
    for old_q, new_q in redirects_qids.items():
        printe.output(f'<<lightblue>> redirects_qids:{old_q.ljust(15)} -> {new_q}.')
    # ---
    for qd in mis_qids:
        printe.output(f'<<lightblue>> missing_qids:{qd}.')
    # ---
    printe.output(f' len of redirects_qids:  {len(redirects_qids.keys())}')
    printe.output(f' len of missing_qids:    {len(mis_qids)}')
    # ---
    with open(f'{Dashboard_path}/Tables/missing.json', "w", encoding="utf-8") as xx:
        json.dump(missing, xx)
    printe.output(' log to missing.json true.... ')
    printe.output(f"{missing['all']=}")


if __name__ == '__main__':
    cash_wd()
