import os


def find_path(lst):
    for i in range(len(lst)):
        if "tg_alert_bot" in lst[i]:
            return i


def start_directory():
    path = os.getcwd()
    path = path.split("\\")
    path = path[:find_path(path) + 1]
    path = "\\".join(path)
    os.chdir(path)