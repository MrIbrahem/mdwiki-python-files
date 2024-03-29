"""

python3 core8/pwb.py mass/radio/get_studies test

"""
import os
from pathlib import Path
from bs4 import BeautifulSoup
import re
import requests
import json
from newapi import printe

# ---
from mass.radio.jsons_files import jsons, urls_to_ids

# dumps_jsons(infos=0, urls=0, cases_in_ids=0, cases_dup=0, authors=0, to_work=0, all_ids=0, urls_to_get_info=0)
# ---
main_dir = Path(__file__).parent
# ---
studies_dir = "/data/project/mdwiki/studies"
# ---
if not os.path.exists(studies_dir):
    printe.output(f"<<red>> studies_dir {studies_dir} not found")
    studies_dir = main_dir / "studies"


def get_images(url):
    print(f"url: {url}")

    response = requests.get(url, timeout=10)
    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
        studies = []

        return "", studies

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    # <a class="view-fullscreen-link" href="/cases/97085/studies/117071?lang=us">
    scripts = soup.find_all("script")

    image_info = []

    for script in scripts:
        text = script.text.strip()
        if text.find("stackedImages") != -1:
            match = re.search(r"var stackedImages = (.*?);", text)
            print("stackedImages:")
            if match:
                data = json.loads(match.group(1))
                for entry in data:
                    modality = entry.get("modality")
                    # { "id": 21152341, "fullscreen_filename": "https://prod-images-static.radiopaedia.org/images/21152341/f802b27c53bf577c1ab269b3ef526a_big_gallery.jpeg", "public_filename": "https://prod-images-static.radiopaedia.org/images/21152341/f802b27c53bf577c1ab269b3ef526a.png", "plane_projection": "Sagittal", "aux_modality": "T1", "position": 10, "content_type": "image/png", "width": 512, "height": 512, "show_feature": false, "show_pin": false, "show_case_key_image": false, "show_stack_key_image": false, "download_image_url": "/images/21152341/download?layout=false", "crop_pending": false }
                    images = entry.get("images")
                    for image in images:
                        if not image.get("modality", "") and modality:
                            image["modality"] = modality
                        image_info.append(image)

    print(f"len image_info: {len(image_info)}")

    return image_info


def get_images_stacks(study_id):
    new_url = f"https://radiopaedia.org/studies/{study_id}/stacks"
    print(f"study_id: {study_id}, new_url: {new_url}")
    # ---
    response = requests.get(new_url, timeout=10)

    image_info = []

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
        return image_info

    text = response.text
    if not text.startswith("[") and not text.endswith("]"):
        print(f"Failed to retrieve content from the URL. Status Code: {response.status_code}")
        return image_info

    json_data = json.loads(text)
    for entry in json_data:
        modality = entry.get("modality")
        # { "id": 21152341, "fullscreen_filename": "https://prod-images-static.radiopaedia.org/images/21152341/f802b27c53bf577c1ab269b3ef526a_big_gallery.jpeg", "public_filename": "https://prod-images-static.radiopaedia.org/images/21152341/f802b27c53bf577c1ab269b3ef526a.png", "plane_projection": "Sagittal", "aux_modality": "T1", "position": 10, "content_type": "image/png", "width": 512, "height": 512, "show_feature": false, "show_pin": false, "show_case_key_image": false, "show_stack_key_image": false, "download_image_url": "/images/21152341/download?layout=false", "crop_pending": false }
        images = entry.get("images")
        for image in images:
            if not image.get("modality", "") and modality:
                image["modality"] = modality
            image_info.append(image)

    print(f"len image_info: {len(image_info)}")

    return image_info


def main():
    n = 0
    # ---
    # ids_to_work = jsons.all_ids
    ids_to_work = {}
    # ---
    no_id = 0
    # ---
    for url in jsons.urls:
        # ---
        caseid = urls_to_ids.get(url, "")
        # ---
        if caseid and jsons.cases_in_ids.get(caseid):
            continue
        # ---
        no_id += 1 if not caseid else 0
        # ---
        tab = {
            "url": url,
            "studies": []
        }
        if caseid and jsons.all_ids.get(caseid):
            tab.update(jsons.all_ids[caseid])
        # ---
        ids_to_work[url] = tab
    # ---
    print(f"len ids_to_work: {len(ids_to_work)}, no_id: {no_id}")
    # ---
    for _, tab in ids_to_work.items():
        for study in tab["studies"]:
            n += 1
            print(f"n: {n}/ f {len(ids_to_work)}")
            # study id
            st_id = study.split("/")[-1]
            st_file = studies_dir / f"{st_id}.json"
            # ---
            if not os.path.exists(st_file):
                # ---
                ux = get_images_stacks(st_id)
                # ---
                if not ux:
                    ux = get_images(study)
                # ---
                with open(st_file, "w", encoding="utf-8") as f:
                    json.dump(ux, f, ensure_ascii=False, indent=4)
                # ---


if __name__ == "__main__":
    main()
