import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.admin_panel import admin_buttons
from loader import dp, usersdb


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username

    user = usersdb.select_user(id=id)
    if user is None:
        try:
            usersdb.add_user(id=id, name=name, username=username)
            print("Зарегистрировано")
        except sqlite3.IntegrityError as err:
            print(err)
    else:
        print(user[2])
        print('Такая запис уже имеется')
    text = f"Привет, {message.from_user.full_name}! Выбери что ты хочешь сделать из кнопок ниже 👇"
    await message.answer(text=text, reply_markup=admin_buttons)
