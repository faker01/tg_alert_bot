

class Users_list:
    def __init__(self, db):
        self.db = db

    def make_page(self, page):
        users_on_page = []
        for user_index in range(page * 6, len(self.db)):
            users_on_page.append(self.db[user_index])

