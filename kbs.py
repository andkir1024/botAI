from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_clients = ReplyKeyboardMarkup()
b1 = KeyboardButton('say 1')
b2 = KeyboardButton('say 2')
b3 = KeyboardButton('say 3')
kb_clients.add(b1).add(b2).add(b3)
