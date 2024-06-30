from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, ReplyKeyboardBuilder, KeyboardButton

# ------admin keyboard create-----
admin_menu_keyboard = InlineKeyboardBuilder()
keyboard_button_add_event = InlineKeyboardButton(text="Добавить мероприятие", callback_data="admin__add_event")
keyboard_button_delete_event = InlineKeyboardButton(text="Удалить мероприятие", callback_data="admin__delete_event")
keyboard_button_find_events = InlineKeyboardButton(text="найти мероприятия", callback_data="admin__find_events")
keyboard_button_show_events = InlineKeyboardButton(text="Показать мероприятия", callback_data="admin__show_events")
admin_menu_keyboard.add(keyboard_button_add_event, keyboard_button_delete_event,
                        keyboard_button_find_events, keyboard_button_show_events)
# --------------------------------

# ---main admin keyboard create---
main_admin_menu_keyboard = InlineKeyboardBuilder()
main_admin_keyboard_button_add_admin = InlineKeyboardButton(text="Добавить администратора",
                                                      callback_data="main_admin__add_admin")
main_admin_keyboard_button_delete_admin = InlineKeyboardButton(text="Удалить администратора",
                                                         callback_data="main_admin__delete_admin")
main_admin_keyboard_button_find_user = InlineKeyboardButton(text="Найти пользователя",
                                                      callback_data="main_admin__find_user")
main_admin_keyboard_button_show_users = InlineKeyboardButton(text="Показать пользователей",
                                                       callback_data="main_admin__show_users")
main_admin_menu_keyboard.add(keyboard_button_add_event, keyboard_button_delete_event,
                             keyboard_button_find_events, keyboard_button_show_events,
                             main_admin_keyboard_button_add_admin, main_admin_keyboard_button_delete_admin,
                             main_admin_keyboard_button_find_user, main_admin_keyboard_button_show_users)
# --------------------------------

# ------quiz keyboard create------
quiz_keyboard = InlineKeyboardBuilder()
keyboard_button_yes = InlineKeyboardButton(text="Да", callback_data="quiz_Yes")
keyboard_button_no = InlineKeyboardButton(text="Нет", callback_data="quiz_No")
quiz_keyboard.add(keyboard_button_yes)
quiz_keyboard.add(keyboard_button_no)
# --------------------------------

# ---------users keyboard---------
users_keyboard = InlineKeyboardBuilder()
keyboard_button_user_1 = InlineKeyboardButton(text="1", callback_data="user_1")
keyboard_button_user_2 = InlineKeyboardButton(text="2", callback_data="user_2")
keyboard_button_user_3 = InlineKeyboardButton(text="3", callback_data="user_3")
keyboard_button_user_4 = InlineKeyboardButton(text="4", callback_data="user_4")
keyboard_button_user_5 = InlineKeyboardButton(text="5", callback_data="user_5")
keyboard_button_user_6 = InlineKeyboardButton(text="6", callback_data="user_6")
keyboard_button_next_page = InlineKeyboardButton(text="next", callback_data="user_next")
keyboard_button_previous_page = InlineKeyboardButton(text="prev", callback_data="user_prev")
users_keyboard.add(keyboard_button_user_1, keyboard_button_user_2, keyboard_button_user_3,
                  keyboard_button_user_4, keyboard_button_user_5, keyboard_button_user_6,
                  keyboard_button_next_page, keyboard_button_previous_page)
# --------------------------------

# ---------menu keyboard----------
menu_keyboard = InlineKeyboardBuilder()
keyboard_button_info = InlineKeyboardButton(text="Информация о мероприятии", callback_data="menu_info")
keyboard_button_calendar = InlineKeyboardButton(text="Календарь", callback_data="menu_calendar")
menu_keyboard.add(keyboard_button_info)
menu_keyboard.add(keyboard_button_calendar)
# --------------------------------

# ------find event keyboard-------
find_event_keyboard = InlineKeyboardBuilder()
keyboard_button_name = InlineKeyboardButton(text="Название", callback_data="find_event__name")
keyboard_button_category = InlineKeyboardButton(text="Категория", callback_data="find_event__category")
keyboard_button_date = InlineKeyboardButton(text="Дата", callback_data="find_event__date")
find_event_keyboard.add(keyboard_button_name)
find_event_keyboard.add(keyboard_button_category)
find_event_keyboard.add(keyboard_button_date)
# --------------------------------
