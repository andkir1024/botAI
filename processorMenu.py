# import json

import json
from jsoncomment import JsonComment

# import jsoncomment
from aiogram import Bot, Dispatcher, executor, types
from userDB import *

class processorMenu:
    def __init__(self, name):
        self.name = name
        parser = JsonComment(json)
        with open(name, 'r', encoding='utf-8') as f: #открыли файл с данными
            self.parsed_object = parser.load(f)
            
        # user = userDB(True)
        # user.getUserInfo(1000)
        return
    async def doMenu(self, message):
        users = userDB(True)
        user = users.getUserInfo(message.chat.id)
        await message.reply(str(message.chat.id))
        await message.reply("Привет!\nЯ Эхо-бот\nОтправь мне любое сообщение, а я тебе обязательно отвечу.")
        
        return
    async def createMenu(self, menuId):
        return