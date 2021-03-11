from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📢Рассылка")
        ]
    ],
    resize_keyboard=True
)
