#!/usr/bin/python3
"""

page views bot

python3 core8/pwb.py mdpy/enwiki_views

"""

import json
#
# (C) Ibrahem Qasim, 2022
#
#
import sys
import traceback
# ---
from pathlib import Path

import pywikibot
from mdpy import printe
# ---
from mdpy.bots import rest_v1_views
from mdpy.bots.en_to_md import enwiki_to_mdwiki, mdwiki_to_enwiki

Dir = str(Path(__file__).parents[0])
# ---
dir2 = Dir.replace("\\", "/")
dir2 = dir2.split("/mdwiki/")[0] + "/mdwiki"
# ---


def get_RTT():
    RTT = []
    # ---
    filename = Path(
        dir2) / "public_html/Translation_Dashboard/cats_cash/RTT.json"
    # ---
    try:
        with open(filename, encoding="utf-8") as file:
            textn = file.read()
    except Exception:
        pywikibot.output("Traceback (most recent call last):")
        pywikibot.output(traceback.format_exc())
        pywikibot.output("CRITICAL:")
        textn = ""
    Table = json.loads(textn) if textn != "" else {}
    # ---
    RTT = Table["list"]
    # ---
    printe.output(f"len of RTT: {len(RTT)}")
    # ---
    return RTT


def get_RTT2():
    # ---
    RTT = []
    # ---
    sitelinks_file = (
        Path(dir2) / "public_html/Translation_Dashboard/Tables/sitelinks.json")
    # ---
    print(f"get sitelinks from {sitelinks_file}")
    # ---
    sitelinks_all = {}
    # ---
    with open(sitelinks_file, encoding="utf-8") as file:
        sitelinks_all = json.load(file)
    # ---
    diff = 0
    # ---
    qids = sitelinks_all.get("qids", {})
    # ---
    for _qid, tab in qids.items():
        mdtitle = tab["mdtitle"]
        en = tab.get("sitelinks", {}).get("en", "")
        if mdtitle != "" and en != "":
            RTT.append(mdtitle)
            if mdtitle != en:
                diff += 1
        else:
            printe.output(f'mdtitle:{mdtitle} or en:{en} == ""')
    # ---
    printe.output(
        f"len of RTT:{len(RTT)}, len of qids:{len(qids.keys())}, diff:{diff}")
    # ---
    return RTT


def main():
    # ---
    RTT = get_RTT()
    # ---
    en_keys = [mdwiki_to_enwiki.get(cc, cc) for cc in RTT]
    # ---
    en_keys.append("Cisatracurium")
    # ---
    print(f"start get_views_with_rest_v1: lenth: {len(en_keys)}")
    # ---
    enviews = rest_v1_views.get_views_last_30_days("en", en_keys)
    # ---
    printe.output(f"len of enviews: {len(enviews.keys())}")
    # ---
    no_views = 0
    # ---
    enwiki_pageviews = (
        Path(dir2) /
        "public_html/Translation_Dashboard/Tables/enwiki_pageviews.json")
    # ---
    old_views = {}
    # ---
    with open(enwiki_pageviews, encoding="utf-8-sig") as file:
        old_views = json.load(file)
    # ---
    n_views = dict(old_views.items())
    # ---
    for k, view in enviews.items():
        if view == 0:
            no_views += 1
            continue
        # ---
        if enwiki_to_mdwiki.get(k):
            k = enwiki_to_mdwiki.get(k)
        # ---
        n_views[k] = view
    # ---
    printe.output(
        f"no_views:{no_views},\t len of n_views: {len(n_views.keys())}")
    # ---
    if "nodump" not in sys.argv:
        with open(enwiki_pageviews, "w", encoding="utf-8") as outfile:
            json.dump(n_views, outfile, sort_keys=True, indent=4)
    # ---
    # add_to_mdwiki_sql(numbers , lange)
    # ---


if __name__ == "__main__":
    main()
