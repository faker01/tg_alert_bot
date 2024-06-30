from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, ReplyKeyboardBuilder, KeyboardButton
import asyncio
import sys
import configparser
import logging
from settings.categories import categories
from methods.db_operations import DataBase
from methods.keyboards import *
from methods.reformate_for_output import reformat, calendar, create_info

# -----settings import------
cfg = configparser.ConfigParser()
cfg.read("settings/settings.ini")
# --------------------------

# --importing welcome text--
with open("texts/hello.txt", 'r', encoding="UTF-8") as wt:
    welcome_text = wt.read()
# --------------------------

# -----global variables-----
filtered_users = []
user_data = {}
user_count = {}
action = {}
events = {}
# --------------------------

# -database initialization--
db = DataBase()
if input("Очистить базу данных пользователей?(Yes/No)").lower().strip() == "yes":
    db.clear_user_db()
if input("Очистить базу данных мероприятий?(Yes/No)").lower().strip() == "yes":
    db.clear_events_db()
print(db.show_users())
print(db.create_list_of_users())
print(db.create_list_of_events())
# --------------------------

# ------admin import--------
admins = []
for i in db.show_users():
    user = list(i)
    if 'admin' in user[2]:
        admins.append(int(user[0]))
# --------------------------

# -------start logger-------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
                    )
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
# --------------------------

# --------bot start---------
bot = Bot(token=cfg["Main"]["TOKEN"], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
# --------------------------

# -------category keyboard--------
category_keyboard = InlineKeyboardBuilder()
for i in categories:
    cd = "event_category__" + i
    category_keyboard.add(InlineKeyboardButton(text=i, callback_data=cd))
# --------------------------------


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    global user_data, user_count
    if not db.find_user(message.from_user.id):
        await message.answer(text=welcome_text)

        await message.answer("Давай начнём с регистрации. Нам же надо знать какие ты хочешь получать оповещения)")
        user_data[message.from_user.id] = [False] * len(categories)

        user_count[message.from_user.id] = 0
        await message.answer(text=f'Вам нравиться {categories[0]}?',
                             reply_markup=quiz_keyboard.as_markup())
    else:
        await message.answer(text="Давно тебя не было в уличных гонках. Лови меню! Покопайся во всех моих закаулках",
                             reply_markup=menu_keyboard.as_markup())


@dp.callback_query(F.data.startswith("quiz"))
async def quiz_keyboard_callback(callback: CallbackQuery) -> None:
    global user_data, user_count
    answer = callback.data.split("_")[1]
    user = callback.from_user.id
    if answer == "Yes":
        u = user_data.get(user)
        u[user_count[user]] = True
        user_data[user] = u
    user_count[user] += 1
    if user_count[user] < len(categories):
        await callback.message.edit_text(f"Ответ принят")
        await callback.message.answer(text=f'Вам нравиться {categories[user_count[user]]}?',
                                      reply_markup=quiz_keyboard.as_markup())
    else:
        await callback.message.edit_text(f"Ответ принят")
        u = user_data.get(user)
        db.add_user(str(user), "".join([str(i) for i in range(len(categories)) if u[i]]))
        await callback.message.answer(text='Успешная регистрация', reply_markup=menu_keyboard.as_markup())


@dp.callback_query(F.data.startswith("menu"))
async def menu_keyboard_callback(callback: CallbackQuery) -> None:
    answer = callback.data.split("_")[1]
    print(answer)
    if answer == "info":
        for k in db.show_events():
            print(k)
            await callback.message.answer(text=create_info(list(k)))
    elif answer == "calendar":
        await callback.message.answer(calendar(db.show_events()))


@dp.message(Command('admin'), F.from_user.id.in_(admins))
async def admin_panel(message: Message) -> None:
    print(db.find_user(message.from_user.id)[0])
    if "main admin" in db.find_user(message.from_user.id)[0]:
        await message.answer(text='Добро пожаловать величайший.', reply_markup=main_admin_menu_keyboard.as_markup())
    else:
        await message.answer(text='Вы вошли в панель администратора.', reply_markup=admin_menu_keyboard.as_markup())


@dp.callback_query(F.data.startswith("main_admin"))
async def main_admin_callback(callback: CallbackQuery) -> None:
    answer = callback.data.split("__")[1]
    if answer == "add_admin":
        action[callback.from_user.id] = "add_admin"
        await callback.message.answer(text="Введите id пользователя в формате: /id ...")
    elif answer == "delete_admin":
        action[callback.from_user.id] = "delete_admin"
        await callback.message.answer(text="Введите id пользователя в формате: /id ...")
    elif answer == "find_user":
        action[callback.from_user.id] = "find_user"
        await callback.message.answer(text="Введите id пользователя в формате: /id ...")
    elif answer == "show_users":
        ans = db.show_users()
        if type(ans) != str:
            out = ""
            for user_pf in ans:
                user_pf = [str(k) for k in list(user_pf)]
                out += f"Пользователь с id {user_pf[0]} имеет интерес в {user_pf[1]}, статус: {user_pf[2]}\n"
            await callback.message.answer(text=out)
        else:
            await callback.message.answer(text=ans)


@dp.callback_query(F.data.startswith("admin"))
async def admin_callback(callback: CallbackQuery) -> None:
    answer = callback.data.split('__')[1]
    if answer == 'add_event':
        events[callback.from_user.id] = ["", "", "", "", "", ""]
        action[callback.from_user.id] = "add_event"
        await callback.message.answer(text="Введите название мероприятия в формате /event_name ...")
    elif answer == "delete_event":
        action[callback.from_user.id] = "delete_event"
        await callback.message.answer(text="Введите id мероприятия в формате: /id ...")
    elif answer == "find_events":
        action[callback.from_user.id] = "find_event"
        await callback.message.answer(text="выберите критерий", reply_markup=find_event_keyboard.as_markup())
    elif answer == "show_events":
        await callback.message.answer(text=reformat(db.show_events()))


# --------add event---------
@dp.message(F.text, Command('event_name'))
async def name_of_event(message: Message):
    answer = message.text[12::]
    if action[message.from_user.id] == "add_event":
        events[message.from_user.id] = [answer, "", "", ""]
        await message.answer(text="Выберите категорию:", reply_markup=category_keyboard.as_markup())
    elif action[message.from_user.id] == "find_event":
        print(db.find_event_by_name(answer))
        await message.answer(text=reformat(db.find_event_by_name(answer)))
        action[message.from_user.id] = ""


@dp.callback_query(F.data.startswith("event_category"))
async def category_callback(callback: CallbackQuery) -> None:
    answer = callback.data.split('__')[1]
    if action[callback.from_user.id] == "add_event":
        u = events.get(callback.from_user.id)
        u[1] = answer
        events[callback.from_user.id] = u
        await callback.message.answer(text="Введите дату в формате /event_date дд.мм.гггг")
    elif action[callback.from_user.id] == "find_event":
        await callback.message.answer(text=reformat(db.find_event_by_category(answer)))
        action[callback.from_user.id] = ""


@dp.message(F.text, Command("event_date"))
async def date_of_event(message: Message):
    answer = message.text.split(' ')[1]
    if action[message.from_user.id] == "add_event":
        u = events.get(message.from_user.id)
        u[2] = answer
        events[message.from_user.id] = u
        await message.answer(text="Напишите краткое описание в формате /event_description ...")
    elif action[message.from_user.id] == "find_event":
        await message.answer(text=reformat(db.find_event_by_date(answer)))
        action[message.from_user.id] = ""


@dp.message(F.text, Command("event_description"))
async def description_of_event(message: Message):
    answer = message.text[19::]
    u = events.get(message.from_user.id)
    u[3] = answer
    del events[message.from_user.id]
    res = db.add_event(u[0], u[1], u[2], u[3])
    if res:
        await message.answer(text=f"Мероприятие {u[0]} с категорией {u[1]} пройдёт {u[2]}. Краткое описание:\n{u[3]}\nУспешно добавлено.")
    else:
        await message.answer(text=res)
    action[message.from_user.id] = ""
# --------------------------------


@dp.callback_query(F.data.startswith("find_event"))
async def find_event_callback(callback: CallbackQuery) -> None:
    answer = callback.data.split('__')[1]
    if answer == "name":
        await callback.message.answer(text="Введите название мероприятия в формате /event_name ...")
    elif answer == "category":
        await callback.message.answer(text="Выберите категорию", reply_markup=category_keyboard.as_markup())
    elif answer == "date":
        await callback.message.answer(text="Введите дату в формате /event_date дд.мм.гггг")


@dp.message(F.text, Command('id'))
async def take_id(message: Message):
    if action[message.from_user.id] == "add_admin":
        ans = db.add_admin(message.text[4::])
        if ans == True:
            await message.answer(text="Пользователь успешно стал администратором.")
        else:
            await message.answer(text=ans)
        action[message.from_user.id] = ""
    elif action[message.from_user.id] == "delete_admin":
        ans = db.delete_admin(message.text[4::])
        if ans == True:
            await message.answer(text="Пользователь больше не является администратором")
        else:
            await message.answer(text=ans)
        action[message.from_user.id] = ""
    elif action[message.from_user.id] == "find_user":
        ans = db.find_user(message.text[4::])
        if type(ans) != str:
            ans = [str(k) for k in list(ans[0])]
            await message.answer(text=f"Пользователь с id {ans[0]} имеет интерес в {ans[1]}, статус: {ans[2]}")
        else:
            await message.answer(text=ans)
        action[message.from_user.id] = ""
    elif action[message.from_user.id] == "delete_event":
        ans = db.delete_event(message.text[4::])
        if ans == True:
            await message.answer(text="Мероприятие успешно удалено")
        else:
            await message.answer(text=ans)
        action[message.from_user.id] = ""



@dp.message(F.text)
async def echo(message: Message):
    user_id = message.from_user.id
    if user_id in events.keys():
        del events[user_id]
    if user_id in action.keys():
        action[user_id] = ""


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
