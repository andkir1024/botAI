# import json

import json
from jsoncomment import JsonComment

# import jsoncomment
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
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
        # await message.reply(str(message.chat.id), reply_markup=kb.greet_kb)
        # await message.reply("Привет!\nЯ Эхо-бот\nОтправь мне любое сообщение, а я тебе обязательно отвечу.")
        await self.createMenu(1000, message)
        
        return
    
    async def createMenu(self, menuId, message):
        button_hi = KeyboardButton('Привет! 👋')

        greet_kb = ReplyKeyboardMarkup()
        greet_kb.add(button_hi)

        # kb = [
        #     [
        #         types.KeyboardButton(text="Сможешь повторить это?"),
        #         types.KeyboardButton(text="А это?")
        #     ],
        # ]
        # keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
 
        # await message.reply("Привет!\nЯ Эхобот от Skillbox!\nОтправь мне любое сообщение, а я тебе обязательно отвечу.", reply_markup=keyboard)        
        
        # button1 = InlineKeyboardButton(text="button1", callback_data="In_First_button")
        # button2 = InlineKeyboardButton(text="button2", callback_data="In_Second_button")
        # keyboard_inline = InlineKeyboardMarkup().add(button1, button2)
        # await message.reply("hi! how are you", reply_markup=keyboard_inline)
        
        return greet_kb
    
    def getAssisitans(self, typeBotTest, answerTest, assistance):
        typeBotTest = typeBotTest.lower()
        answerTest = answerTest.lower()
        assistants = self.parsed_object['assistant']
        for ass in assistants:
            if typeBotTest == ass['typeBot'].lower():
                answers = ass['answers']
                for answer in answers:
                    if answerTest == answer['id'].lower():
                        text = answer['text']
                        lenText = len(text)
                        if assistance < lenText:
                            return text[str(assistance)]
                        return text['0']
        return None
    def testMsg(self, typeBot, msg, assistant):
        if "answer" in msg:
            titleTmp = self.getAssisitans(typeBot, msg, assistant)
            if titleTmp is not None:
                return titleTmp
            return msg
        return msg
    
    def getMenu(self, msgCmd):
        try:
            msgCmd = msgCmd.lower()
            menus = self.parsed_object['menus']
            for menu in menus:
                if menu['id11'].lower() == msgCmd:
                    menuCmd = menu['menu']
                    typeBot = menu['typeBot']
                    title = self.testMsg(typeBot, menu['title'], 0)
                    kb_clients = ReplyKeyboardMarkup(resize_keyboard=True)
                    for menuItem in menuCmd:
                        place = 'place' in menuItem
                        name = self.testMsg(typeBot, menuItem['name'], 0)
                        kb = KeyboardButton(name)
                        if place == False:
                            kb_clients.add(kb)
                        else:
                            if menuItem['place'] == '0':
                                kb_clients.add(kb)
                            else:
                                kb_clients.insert(kb)

                    return kb_clients , title

        except Exception as e:
            return None, None
            
        return None, None
    