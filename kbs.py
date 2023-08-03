from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from processorMenu import *

class kbs:
    def get_kb(menu, msg: types.Message) -> ReplyKeyboardMarkup:
        msgCmd = msg.text
        first = msgCmd[0]
        if first == '/':
            msgCmd = msgCmd[1:]
            pass
        menuReply, title = menu.getMenu(msgCmd, msg)
        return menuReply, title
            
        kb_clients = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('say 1')
        b2 = KeyboardButton('say 2', request_contact=True)
        b3 = KeyboardButton('say 3')
        kb_clients.add(b1).add(b2).add(b3)
        msgReply = menu.getAssisitans("base", "answer1", 1)
        return kb_clients, 'Test andy'