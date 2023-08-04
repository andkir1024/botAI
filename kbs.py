from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from okDeskUtils import okDesk
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

    def findNextMenu(menu, findMsg, current_menu):
        allMenu = menu.parsed_object['menus']
        for mm in allMenu:
            id = mm['id']
            if id.lower() == current_menu.lower():
                for itemMenu in mm['menu']:
                    if itemMenu['name'].lower() == findMsg.lower():
                        return itemMenu
        return  None
    async def get_next_kb(menu, msg: types.Message) -> ReplyKeyboardMarkup:
        userCurrent = userDB(True)
        userInfo, isNew = userCurrent.getUserInfo(msg)
        
        current_menu = userInfo.current_menu.lower()
        # next_menu = kbs.findNextMenu(menu, msg.text, current_menu)
        # выбор ассистента
        if current_menu == 'Registry'.lower():
            lenName = len(msg.text)
            if lenName == 14:
                userInfo.assistant = userAssistant.assistant0
            elif lenName == 4:
                userInfo.assistant = userAssistant.assistant1
            else:
                userInfo.assistant = userAssistant.assistant2
                
            # await msg.answer('2222')
            msgCmd = 'start'
            menuReply, title = menu.getMenu(msgCmd, msg)

            if menuReply is not None:
                titleTmp = menu.getAssisitans('base', 'answer1', userInfo.assistant)
                await msg.answer(titleTmp)
                userInfo.current_menu = msgCmd
                userInfo.save()
                await msg.answer(title, reply_markup=menuReply)
            return
        # переход к следующему меню
        next_menu = kbs.findNextMenu(menu, msg.text, current_menu)
        if next_menu is not None:
            msgCmd = next_menu['next']
            menuReply, title = menu.getMenu(msgCmd, msg)

            if menuReply is not None:
                userInfo.current_menu = msgCmd
                userInfo.save()
                await msg.answer(title, reply_markup=menuReply)
            else:
                if title is not None:
                    await msg.answer('ОШИБКА: '+title)
            return
        # отрабатываем ввод данных
        else:
            await kbs.getUserData(menu, current_menu, msg)
            pass

    async def get_kb_by_idmenu(menu, msg: types.Message, msgCmd) -> ReplyKeyboardMarkup:
        userCurrent = userDB(True)
        userInfo, isNew = userCurrent.getUserInfo(msg)
        
        menuReply, title = menu.getMenu(msgCmd, msg)

        if menuReply is not None:
            userInfo.current_menu = msgCmd
            userInfo.save()
            await msg.answer(title, reply_markup=menuReply)
        return

    async def getUserData(menu, current_menu, msg: types.Message):
        # ввод номера плоттера
        if current_menu == "menuRequestDeviceId".lower():
            # res = okDesk.findEquipmentByInvetoryId(msg)
            res = okDesk.createEquipmentByInvetoryId(msg.text)
            msgReplay = res['name'] + '\n' + res['address']
            await msg.answer(msgReplay)
            await kbs.get_kb_by_idmenu(menu, msg, 'menuPlaceId')
        return