# import json

import json
from jsoncomment import JsonComment

# import jsoncomment
from aiogram import Bot, Dispatcher, executor, types

class processorMenu:
    def __init__(self, name):
        self.name = name
        parser = JsonComment(json)
        with open(name, 'r', encoding='utf-8') as f: #открыли файл с данными
            self.parsed_object = parser.load(f)
        return
    async def doMenu(self, message):
        await message.reply("Привет!\nЯ Эхо-бот\nОтправь мне любое сообщение, а я тебе обязательно отвечу.")
        
        return