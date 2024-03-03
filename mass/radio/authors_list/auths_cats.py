'''

python3 core8/pwb.py mass/radio/authors_list/auths_cats

tfj run authscats --mem 1Gi --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/radio/authors_list/auths_cats"

'''
import re
import sys
import json
import os
from pathlib import Path
from multiprocessing import Pool
from newapi import printe
from newapi.ncc_page import CatDepth
from newapi.ncc_page import MainPage as ncc_MainPage

# ---
main_dir = Path(__file__).parent.parent
# ---
with open(main_dir / 'authors_list' / 'authors_to_cases.json', 'r', encoding='utf-8') as f:
    authors_to_cases = json.load(f)
# ---
print(f"Length of authors_to_cases: {len(authors_to_cases)}")
# ---
def cases_cats():
    members = CatDepth('Category:Radiopaedia images by case', sitecode='www', family="nccommons", depth=0, ns="14")
    reg = r'^Category:Radiopaedia case (\d+) (.*?)$'
    # ---
    id2cat = {}
    # ---
    for cat in members:
        match = re.match(reg, cat)
        if match:
            case_id = match.group(1)
            case_title = match.group(2)
            # ---
            id2cat[case_id] = cat
    # ---
    print(f'lenth of members: {len(members)} ')
    print(f'lenth of id2cat: {len(id2cat)} ')
  
    return id2cat

def create_cat(cat, text):
    page = ncc_MainPage(cat, 'www', family='nccommons')

    if page.exists():
        pa_text = page.get_text()
        if pa_text == text:
            print("no different")
            return
        page.save(newtext=text, summary='create')
    else:
        page.Create(text=text, summary='create')

def add(da=[], title="", cat=""):
    if da:
        title, cat = da[0], da[1]
    # ---
    page = ncc_MainPage(title, 'www', family='nccommons')

    if not page.exists():
        return
    
    text = page.get_text()
    # ---
    if text.find(cat) != -1:
        printe.output(f"cat {title} already has it.")
        return
    # ---
    newtext = text
    newtext += f"\n[[{cat}]]"
    # ---
    page.save(newtext=newtext, summary=f'Bot: added [[:{cat}]]')

def mu(tab):
    pool = Pool(processes=3)
    pool.map(add, tab)
    pool.close()
    pool.terminate()

def add_cat(pages, cat):
    if "multi" in sys.argv:
        tab = [[x, cat] for x in pages]
        mu(tab)
    else:
        for title in pages:
            add(title=title, cat=cat)

def one_auth(auth, cat_list):
    printe.output(f"Author: {auth}, {len(cat_list)=}")
    # ---
    cat  = f"Category:Radiopaedia cases by {auth}"
    text = f"[[Category:Radiopaedia cases by author|{auth}]]"
    # ---
    create_cat(cat, text)
    # ---
    done = CatDepth(cat, sitecode='www', family="nccommons", depth=0, ns="14")
    # ---
    new_cat_list = [ x for x in cat_list if x not in done]
    # ---
    printe.output(f"{len(done)=}, {len(new_cat_list)=}")
    # ---
    add_cat(new_cat_list, cat)

def start():
    # ---
    cats = cases_cats()
    # ---
    for numb, (x, x_cases) in enumerate(authors_to_cases.items(), start=1):
        # ---
        printe.output(f"{x=}, cases: {len(x_cases)=}")
        # ---
        cat_list = [cats[c] for c in x_cases if c in cats]
        cat_no_list = [c for c in x_cases if c not in cats]
        # ---
        printe.output(f"<<red>> {len(cat_no_list)=}")
        # ---
        one_auth(x, cat_list)
        # ---
        if "break" in sys.argv and numb % 10 == 0:
            break
    
if __name__ == '__main__':
    start()
