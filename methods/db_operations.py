from sqlite4 import SQLite4


class DataBase:
    def __init__(self) -> object:
        try:
            # self.database = SQLite4("db/data.db")
            self.database = SQLite4("methods/db/data.db")
            self.database.connect()
        except Exception:
            print('Failed to connect to the database.')

    # work with user table
    def create_list_of_users(self):
        try:
            self.database.create_table("users", ["id", "interests", "status"])
            if not self.database.select("users", condition='status = "main admin"'):
                var = input("Введите id главного администратора:")  # мой id 759000524
                self.database.insert("users", {"id": var, "interests": "", "status": "main admin"})
            return "User table done successfully."
        except Exception:
            return 'Failed to create user table.'

    def check_admin_rights(self, user_id):
        try:
            if self.database.select("users", ["status"], condition=f'id = "{user_id}"'):
                return True
            else:
                return False
        except Exception:
            return "Failed to find admin with this id."

    def add_user(self, user_id, user_interests):
        try:
            self.database.insert("users", {"id": user_id, "interests": user_interests, "status": "user"})
            return True
        except Exception:
            return 'Failed to add user. Check data!'

    def change_interests(self, user_id, user_interests):
        try:
            self.database.update("users", {"interests": user_interests}, condition=f'id = "{user_id}"')
            return True
        except Exception:
            return 'Failed to update status. Check registration!'

    def add_admin(self, user_id):
        try:
            self.database.update("users", {"status": "admin"}, condition=f'id = "{user_id}"')
            return True
        except Exception:
            return 'Failed to update status. Check registration!'

    def delete_admin(self, user_id):
        try:
            self.database.update("users", {"status": "user"}, condition=f'id = "{user_id}"')
            return True
        except Exception:
            return 'Failed to update status. Check registration!'

    def find_user(self, user_id):
        try:
            return self.database.select("users", condition=f'id == "{user_id}"')
        except Exception:
            return 'Failed to show table. Check database!'

    def show_users(self):
        try:
            return self.database.select("users")
        except Exception:
            return 'Failed to show table. Check database!'

    def clear_user_db(self):
        try:
            self.database.delete("users", "1 == 1")
            return True
        except Exception:
            return 'Failed to clear table. Check database!'

    # work with event table
    def create_list_of_events(self):
        try:
            self.database.create_table("events", ["id", "category", "name", "date", "short_description"])
            return "Event table done successfully."
        except Exception:
            return 'Failed to create event table.'

    def add_event(self, event_name, event_category, event_date, event_short_description):
        try:
            event_id = len(self.show_events())
            self.database.insert("events", {"id": event_id, "category": event_category, "name": event_name,
                                            "date": event_date, "short_description": event_short_description})
            return True
        except Exception:
            return "Failed to add event. Check data!"

    def delete_event(self, event_id):
        try:
            print(event_id)
            self.database.delete("events", condition=f'id=={event_id}')
            return True
        except Exception:
            return 'Failed to delete event. Check database!'

    def update_event_info(self, event_id, upd_cat, txt):
        try:
            self.database.update("events", {f"{upd_cat}": f"{txt}"}, condition=f'id = "{event_id}"')
            return True
        except Exception:
            return 'Failed to delete event. Check database!'

    def find_event_by_category(self, event_category):
        try:
            return self.database.select("events", condition=f'category == "{event_category}"')
        except Exception:
            return 'Failed to find event. Check your data!'

    def find_event_by_name(self, event_name):
        try:
            return self.database.select("events", condition=f'name == "{event_name}"')
        except Exception:
            return 'Failed to find event. Check your data!'

    def find_event_by_date(self, event_date):
        try:
            return self.database.select("events", condition=f'date == "{event_date}"')
        except Exception:
            return 'Failed to find event. Check your data!'

    def show_events(self):
        try:
            return self.database.select("events")
        except Exception:
            return 'Failed to show table. Check database!'

    def clear_events_db(self):
        try:
            self.database.delete("events", "1 == 1")
            return True
        except Exception:
            return 'Failed to clear table. Check database!'