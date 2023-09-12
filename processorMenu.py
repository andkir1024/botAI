
import traceback
import json
from jsoncomment import JsonComment
import os
# import jsoncomment
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from userDB import *

class processorMenu:
    def __init__(self):
        parser = JsonComment(json)
        with open("." + mainConst.DIR_RESOURCE + "config_ru.jsonc", 'r', encoding='utf-8') as f: #открыли файл с данными
            self.parsed_object = parser.load(f)

        with open("." + mainConst.DIR_RESOURCE + "config_employer_ru.jsonc", 'r', encoding='utf-8') as f: #открыли файл с данными
            self.parsed_employer = parser.load(f)

        with open("." + mainConst.DIR_RESOURCE + "answer_ru.jsonc", 'r', encoding='utf-8') as f: #открыли файл с данными
            self.parsed_answer = parser.load(f)
            
        # self.user = userDB(True)
        # user.getUserInfo(1000)
        return
    # async def doMenu(self, message):
    #     users = userDB(True)
    #     user = users.getUserInfo(message.chat.id)
    #     await message.reply(str(message.chat.id))
    #     await self.createMenu(1000, message)
        
    #     return
    
    async def createMenu(self, menuId, message):
        button_hi = KeyboardButton('Привет! 👋')

        greet_kb = ReplyKeyboardMarkup()
        greet_kb.add(button_hi)
        
        return greet_kb
    
    def getAssisitans(self, typeBotTest, answerTest, assistance):
        typeBotTest = typeBotTest.lower()
        answerTest = answerTest.lower()
        assistance = str(assistance) 
        assistance = assistance.replace('userAssistant.assistant', '')
        assistance = assistance.replace('assistant', '')
        if assistance.isdigit == False:
            return None
        assistance = int(assistance)
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
    
    def getMenu(self, msgCmd, msgMain: types.Message, userInfo):
        try:
            msgCmd = msgCmd.lower()
            menus = self.parsed_object['menus']
            assistant = userInfo.assistant
            for menu in menus:
                if menu['id'].lower() == msgCmd:
                    menuCmd = menu['menu']
                    typeBot = 'base'
                    if 'typeBot' in menu:
                        typeBot = menu['typeBot']
                    title = self.testMsg(typeBot, menu['title'], assistant)
                    kb_clients = ReplyKeyboardMarkup(resize_keyboard=True)
                    for menuItem in menuCmd:
                        place = 'place' in menuItem
                        name = self.testMsg(typeBot, menuItem['name'], assistant)
                        kb = KeyboardButton(name)
                        if place == False:
                            kb_clients.add(kb)
                        else:
                            if menuItem['place'] == '0':
                                kb_clients.add(kb)
                            else:
                                kb_clients.insert(kb)

                    return kb_clients , title, menu

        except Exception as e:
            err = "Error {0}".format(traceback.format_exc())
            return None, err, None
            
        return None, None, None
    def writeMsg(self, msg):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + mainConst.DIR_DATA + "messages.txt", "a") as text_file:
            text_file.write(str(msg) + '\n')

        return None            