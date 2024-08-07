# import os
from prior.p4 import work_in_links

# ---
from pathlib import Path

Dir = str(Path(__file__).parents[0])
# print(f'Dir : {Dir}')
# ---
project_json = f'{Dir}/json/'


def start_test(links=[]):
    # ---
    if links == []:
        links = ["Syncope (medicine)"]
    # start work in all links
    # ---
    # links.sort()
    # ---
    main_File = f"{project_json}test.json"
    main_File_en = f"{project_json}en_test.json"
    # ---
    # python3 core8/pwb.py prior/p4 test
    # ---
    work_in_links(links, main_File, main_File_en, Log=False)
    # ---
    # log_all(main_File)
    # log_allen(main_File_en)
    # ---
    return all#, allen


# ---
