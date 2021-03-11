from aiogram.dispatcher.filters.state import StatesGroup, State


class RassilkaState(StatesGroup):
    type = State()
    send_check = State()

class AddButtonState(StatesGroup):
    text = State()
    btnadd = State()

class AddMediaFileState(StatesGroup):
    media = State()

