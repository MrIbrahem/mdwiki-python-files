#!/usr/bin/python3
"""

from wprefs.wpref_text import fix_page
# fix_page(text, title)

"""
import re
import wikitextparser as wtp
from wprefs.helps import print_s
from wprefs.bots import txtlib2


def expend_new(main_temp):
    parsed = wtp.parse(main_temp)
    for template in parsed.templates:
        # ---
        if not template:
            continue
        # ---
        str_ = template.string
        if str_.strip() != main_temp.strip():
            continue
        # ---
        template_name = str(template.normal_name()).strip()
        template.name = f"{template_name}\n"
        # ---
        for arg in template.arguments:
            param = arg.name.rstrip()
            value = arg.value.rstrip()
            # ---
            if len(param.strip()) == 1:
                continue
            # ---
            newparam = param.ljust(17)
            # ---
            arg.name = newparam
            arg.value = f"{value}\n"
        # ---
        new_temp = template.string
        break
    # ---
    return new_temp


def Expend_Infobox(text, title, section_0):
    """Expand the infobox in the provided text.

    This function processes the input text to expand an infobox based on the
    specified title. It identifies sections within the text and modifies
    them accordingly. If the section is empty, it attempts to extract
    relevant information from the text. The function also handles template
    extraction and ensures that the infobox is formatted correctly.

    Args:
        text (str): The input text containing the infobox to be expanded.
        title (str): The title of the infobox to be processed.
        section_0 (str): An optional section of text that may contain relevant information.

    Returns:
        str: The modified text with the expanded infobox.
    """

    # ---
    newtext = text
    # ---
    if not section_0:
        if newtext.find('==') != -1:
            section_0 = newtext.split('==')[0]
        else:
            tagg = f"'''{title}'''1"
            if newtext.find(tagg) != -1:
                section_0 = newtext.split(tagg)[0]
            else:
                section_0 = newtext
                print_s('section_0 = newtext')
    # ---
    try:
        title2 = re.escape(title)
    except Exception as e:
        title2 = title
    # ---
    newtext = re.sub(r"\}\s*(\'\'\'%s\'\'\')" % title2, r"}\n\n\g<1>", newtext)
    section_0 = re.sub(r"\}\s*(\'\'\'%s\'\'\')" % title2, r"}\n\n\g<1>", section_0)
    # ---
    tempse_by_u = {}
    tempse = {}
    # ---
    ingr = txtlib2.extract_templates_and_params(section_0)
    u = 0
    for temp in ingr:
        u += 1
        name, namestrip, params, template = temp['name'], temp['namestrip'], temp['params'], temp['item']
        if len(params) > 4 and section_0.find(f'>{template}') == -1:
            tempse_by_u[u] = temp
            # ---
            tempse[u] = len(template)
            # ---
            print_s(namestrip)
    # ---
    main_temp = {}
    # ---
    if len(tempse_by_u) == 1:
        for _x, v in tempse_by_u.items():
            main_temp = v
    else:
        PP = [[y1, u1] for u1, y1 in tempse.items()]
        PP.sort(reverse=True)
        # ---
        for y2, u2 in PP:
            print_s(f'len: {y2}, u2: {u2}')
            main_temp = tempse_by_u[u2]
            break
    # ---
    # work in main_temp:
    if main_temp != {}:
        main_temp_text = main_temp.get('item', '')
        params = main_temp.get('params', [])
        # ---
        new_temp = expend_new(main_temp_text)
        # ---
        if new_temp != main_temp_text:
            newtext = newtext.replace(main_temp_text, new_temp)
            newtext = newtext.replace(f"{new_temp}'''", f"{new_temp}\n'''")
    # ---
    return newtext
