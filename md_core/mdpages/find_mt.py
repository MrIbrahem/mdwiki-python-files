#!/usr/bin/env python
"""

Usage:

python3 core8/pwb.py mdpages/find_mt

"""

#

from mdpages.qids_others import sql_qids_others
from mdpy import printe
from mdpy.bots import sql_for_mdwiki
from mdpy.bots.check_title import valid_title

# ---

# ---

qids_others = sql_qids_others.get_others_qids()

qids = sql_for_mdwiki.get_all_qids()

# ---

to_work = [
    title for title, q in qids.items() if q == "" and valid_title(title)
]

printe.output(f"<<green>> to_work list: {len(to_work)}")

# ---

new_qids = {x: qids_others[x] for x in to_work if x in qids_others}

printe.output(f"<<green>> new_qids list: {len(new_qids)}")

# ---


def doo():
    # ---

    if len(to_work) == 0:
        printe.output('<<green>> to_work list is empty. return "".')

        return

    # ---

    if len(new_qids) == 0:
        printe.output('<<green>> new_qids list is empty. return "".')

        return

    # ---

    sql_for_mdwiki.add_titles_to_qids(new_qids)


if __name__ == "__main__":
    doo()
