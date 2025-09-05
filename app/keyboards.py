from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Чат')]
],
resize_keyboard=True,
input_field_placeholder='Выберите пункт меню')


cansel = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отмена')]
],
resize_keyboard=True,
)
