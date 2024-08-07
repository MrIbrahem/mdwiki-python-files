"""
# ---
from newupdater import user_account_new
username = user_account_new.my_username
password = user_account_new.mdwiki_pass
user_agent = user_account_new.user_agent

# ---
"""

import os
import configparser

# ---
from pathlib import Path

Dir = str(Path(__file__).parents[0])
# print(f'Dir : {Dir}')
# ---
Dir = str(Path(__file__).parents[0])
dir2 = Dir.replace("\\", "/").split("/pybot/")[0]
# ---
config = configparser.ConfigParser()
config.read(f"{dir2}/confs/user.ini")

my_username = config["DEFAULT"].get("my_username", "")

mdwiki_pass = config["DEFAULT"].get("mdwiki_pass", "")

user_agent = config["DEFAULT"].get("user_agent", "")
