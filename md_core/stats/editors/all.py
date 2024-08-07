'''

python3 core8/pwb.py stats/all ask

'''
import json
import re
import os
import sys
from pathlib import Path

# ---
from newapi import printe
from newapi.mdwiki_page import MainPage as md_MainPage
from stats.editors import validate_ip

# ---
Dir = Path(__file__).parent
editors_dir = Dir / 'editors'
# ---
skip_sites = ['enwiki', 'wikidatawiki', 'commonswiki', 'specieswiki']


def filter_editors(editors, site):
    # ---
    for x in editors.copy().keys():
        if validate_ip(x):
            del editors[x]
    # ---
    return editors


def work_all(editors):
    # ---
    editors = filter_editors(editors, 'all')
    # ---
    if not editors:
        printe.output('<<red>> no editors')
        return
    # ---
    title = f"WikiProjectMed:WikiProject_Medicine/Stats/Top_medical_editors_2023/all"
    # ---
    text = '{{:WPM:WikiProject Medicine/Total medical articles}}\n'
    text += '{{Top medical editors 2023 by lang}}\n'
    # ---
    text += 'Numbers of 2023.\n'
    # ---
    text += '''{| class="sortable wikitable"\n!#\n!User\n!Count\n'''
    text += '''!Wiki\n'''
    # ---
    for i, (user, ta) in enumerate(editors.items(), start=1):
        # ---
        count = ta['all']
        # ---
        # print(ta['sites'])
        # ---
        # ta['sites'] = {'es': 71, 'fr': 22, 'ja': 15, 'ru': 21}
        # wiki = the most popular wiki
        wiki = max(ta['sites'], key=ta['sites'].get)
        # ---
        user = user.replace('_', ' ')
        # ---
        text += f'|-\n' f'!{i}\n' f'|[[:w:{wiki}:user:{user}|{user}]]\n' f'|{count:,}\n' f'|{wiki}\n'
        # ---
        if i == 1000:
            break
        # ---
    # ---
    text += '\n|}'
    # ---
    page = md_MainPage(title, 'www', family='mdwiki')
    p_text = page.get_text()
    # ---
    if p_text != text:
        page.save(newtext=text, summary='update', nocreate=0, minor='')
    else:
        printe.output('<<green>> no changes')
    # ---
    return editors


def start():
    # ---
    # read json files in editors_dir
    files = os.listdir(editors_dir)
    # ---
    all_editors = {}
    # ---
    for numb, file in enumerate(files, start=1):
        # ---
        printe.output(f'<<green>> n: {numb} file: {file}:')
        # ---
        site = file[:-5]
        # ---
        if f'{site}wiki' in skip_sites:
            continue
        # ---
        with open(editors_dir / f'{site}.json', "r", encoding="utf-8") as f:
            editors = json.load(f)
        # ---
        for user, count in editors.items():
            if user not in all_editors:
                all_editors[user] = {'all': 0, 'sites': {}}
            all_editors[user]['sites'][site] = count
            all_editors[user]['all'] += count
        # ---
    # ---
    all_editors = dict(sorted(all_editors.items(), key=lambda x: x[1]['all'], reverse=True))
    # ---
    work_all(all_editors)


if __name__ == "__main__":
    start()
