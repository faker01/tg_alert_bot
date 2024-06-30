import configparser
from take_start_directory import start_directory

start_directory()
# -----settings import------
cfg = configparser.ConfigParser()
cfg.read("settings/settings.ini")
TOKEN = cfg["Main"]["TOKEN"]
# --------------------------

# --importing welcome text--
with open("settings/texts/hello.txt", 'r', encoding="UTF-8") as wt:
    welcome_text = wt.read()
# --------------------------

# ------admin import--------
def admin_import(db):
    admins = []
    for i in db.show_users():
        user = list(i)
        if 'admin' in user[2]:
            admins.append(int(user[0]))
    return admins
# --------------------------
