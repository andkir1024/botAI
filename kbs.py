from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from processorMenu import *

class kbs:
    def get_kb(menu, msg: types.Message, userInfo, isNew) -> ReplyKeyboardMarkup:
        msgCmd = msg.text
        first = msgCmd[0]
        if first == '/':
            msgCmd = msgCmd[1:]
        if isNew:
            msgCmd = 'Registry'
        menuReply, title = menu.getMenu(msgCmd, msg)
        return menuReply, title, msgCmd
            
        kb_clients = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('say 1')
        b2 = KeyboardButton('say 2', request_contact=True)
        b3 = KeyboardButton('say 3')
        kb_clients.add(b1).add(b2).add(b3)
        msgReply = menu.getAssisitans("base", "answer1", 1)
        return kb_clients, 'Test andy'
    
    async def get_next_kb(menu, msg: types.Message, userInfo, isNew) -> ReplyKeyboardMarkup:
        current_menu = userInfo.current_menu.lower()
        # выбор ассистента
        if current_menu == 'Registry'.lower():
            lenName = len(msg.text)
            if lenName == 14:
                userInfo.assistant = userAssistant.assistant0
            elif lenName == 4:
                userInfo.assistant = userAssistant.assistant1
            else:
                userInfo.assistant = userAssistant.assistant2
                
            await msg.answer('2222')
            msgCmd = 'start'
            menuReply, title = menu.getMenu(msgCmd, msg)
            return menuReply, title, msgCmd
        return None, None, None
