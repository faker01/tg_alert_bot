import os

def start_directory():
    path = os.getcwd()
    path = path.split("\\")
    path = path[:path.index("tg_alert_bot") + 1]
    path = "\\".join(path)
    os.chdir(path)