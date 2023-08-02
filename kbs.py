from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class kb:
    def get_kb(menu) -> ReplyKeyboardMarkup:
        kb_clients = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('say 1')
        b2 = KeyboardButton('say 2', request_contact=True)
        b3 = KeyboardButton('say 3')
        kb_clients.add(b1).add(b2).add(b3)
        return kb_clients