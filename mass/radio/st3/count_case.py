'''
from mass.radio.st3.One_Case_New import OneCase
'''
import sys
import os
from pathlib import Path
import json
from mass.radio.studies import get_images_stacks, get_images
# ---
from mass.radio.jsons_files import jsons, dumps_jsons, ids_to_urls, urls_to_ids
# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, ids=0, all_ids=0, urls_to_get_info=0)
# ---
api_new  = NEW_API('www', family='nccommons')
api_new.Login_to_wiki()
# ---
main_dir = Path(__file__).parent.parent
# --

class OneCase:
    def __init__(self, caseId, studies_ids):
        self.caseId = caseId
        self.studies_ids = studies_ids
        self.images_count = 0

    def get_studies(self):
        for study in self.studies_ids:
            st_file = os.path.join(str(main_dir), 'studies', f'{study}.json')
            # ---
            images = {}
            # ---
            if os.path.exists(st_file):
                try:
                    with open(st_file, 'r', encoding='utf-8') as f:
                        images = json.loads(f.read())
                except Exception as e:
                    print(f'{study} : error')
            # ---
            images = [ image for image in images if image ]
            # ---
            if not images:
                images = get_images_stacks(self.caseId)
            # ---
            if not images:
                images = get_images(f'https://radiopaedia.org/cases/{self.caseId}/studies/{study}')
            # ---
            print(f'{study} : len(images) = {len(images)}')
            self.images_count += len(images)
    
    def start(self):
        self.get_studies()
        print(f'Images count: {self.images_count}')

    def images(self):
        return self.images_count
