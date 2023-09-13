import html
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from okDeskUtils import okDesk
from processorMenu import *
from aiogram.types import InputFile

class kbs:
    def get_kb_phone(menu, msg: types.Message) -> ReplyKeyboardMarkup:
        kb_clients = ReplyKeyboardMarkup(resize_keyboard=True)
        b2 = KeyboardButton('Зарегистрироваться', request_contact=True)
        kb_clients.add(b2)
        return kb_clients, 'Для начала работы нам нужно зарегистрироваться', 'menuPhone'

    def get_kb(menu, msg: types.Message, userInfo, isNew) -> ReplyKeyboardMarkup:
        msgCmd = msg.text
        first = msgCmd[0]
        if first == '/':
            msgCmd = msgCmd[1:]
        if isNew:
            msgCmd = 'Registry'
        menuReply, title, selMenu = menu.getMenu(msgCmd, msg, userInfo)
        return menuReply, title, msgCmd
            
        kb_clients = ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = KeyboardButton('say 1')
        b2 = KeyboardButton('say 2', request_contact=True)
        b3 = KeyboardButton('say 3')
        kb_clients.add(b1).add(b2).add(b3)
        msgReply = menu.getAssisitans("base", "answer1", 1)
        return kb_clients, 'Test andy'

    def findNextMenu(menu, findMsg, current_menu, msg: types.Message, userInfo):
        # allMenu = menu.parsed_object['menus']
        allMenu = menu.getMenuReal(msg, userInfo)
        for mm in allMenu:
            id = mm['id']
            if id.lower() == current_menu.lower():
                for itemMenu in mm['menu']:
                    if itemMenu['name'].lower() == findMsg.lower():
                        return itemMenu
        return  None

    async def get_next_kb(menu, msg: types.Message, bot) -> ReplyKeyboardMarkup:
        # userCurrent = userDB(True)
        # userInfo, isNew = userCurrent.getUserInfo(msg)
        userInfo, isNew = kbs.getMainUserInfo(msg)
        
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
                
            # await msg.answer('2222')
            msgNext = 'start'
            menuReply, title, selMenu = menu.getMenu(msgNext, msg, userInfo)

            if menuReply is not None:
                titleTmp = menu.getAssisitans('base', 'answer1', userInfo.assistant)
                await msg.answer(titleTmp)
                userInfo.current_menu = msgNext
                userInfo.save()
                await msg.answer(title, reply_markup=menuReply)
            return
        # переход к следующему меню
        next_menu = kbs.findNextMenu(menu, msg.text, current_menu, msg, userInfo)
        if next_menu is not None:
            msgNext = next_menu['next']
            await kbs.createRequest(menu, current_menu, msg, userInfo, msgNext)
            
            menuReply, title, selMenu = menu.getMenu(msgNext, msg, userInfo)
            await kbs.showAppParameters(selMenu, msg, bot)

            if menuReply is not None:
                userInfo.current_menu = msgNext
                userInfo.save()
                await msg.answer(title, reply_markup=menuReply)
            else:
                if title is not None:
                    await msg.answer('ОШИБКА: '+title)
            return
        # отрабатываем ввод данных
        else:
            await kbs.getUserData(menu, current_menu, msg, userInfo)
        
    async def showAppParameters(selMenu, msg: types.Message, bot):
        if selMenu is not None:
            video = None
            dir_path = os.path.dirname(os.path.realpath(__file__))
            if 'video' in selMenu:
                video = selMenu['video']
                fileVideo = dir_path + mainConst.DIR_RESOURCE + video
                await bot.send_video(msg.chat.id, open(fileVideo, 'rb'))
            if 'photo' in selMenu:
                photo = selMenu['photo']
                filePhoto = dir_path + mainConst.DIR_RESOURCE + photo
                photo = InputFile(filePhoto)
                await bot.send_photo(msg.chat.id, photo = photo)
                # await bot.send_photo(msg.chat.id, open(filePhoto, 'rb'))
            if 'url' in selMenu:
                url = selMenu['url']
                await msg.reply(f"URL: {url}\n")                
                # await msg.reply(f"URL: {html.quote(url)}\n")                
        return

    async def get_kb_by_idmenu(menu, msg: types.Message, msgCmd) -> ReplyKeyboardMarkup:
        # userCurrent = userDB(True)
        # userInfo, isNew = userCurrent.getUserInfo(msg)
        
        userInfo, isNew = kbs.getMainUserInfo(msg)
        menuReply, title, selMenu = menu.getMenu(msgCmd, msg, userInfo)

        if menuReply is not None:
            userInfo.current_menu = msgCmd
            userInfo.save()
            await msg.answer(title, reply_markup=menuReply)
        return

    async def setInfoMode(msg: types.Message):
        # userCurrent = userDB(True)
        # userInfo, isNew = userCurrent.getUserInfo(msg)
        userInfo, isNew = kbs.getMainUserInfo(msg)
        if isNew == False:
            pieces = msg.text.split()
            if len(pieces)==2:
                mode = pieces[1]
                if mode.isdigit():
                    userInfo.infoMode = int(mode)
                    userInfo.save()
            else:
               await msg.answer("Небходим номер запроса")
        return

    async def setParam(msg: types.Message):
        # userCurrent = userDB(True)
        # userInfo, isNew = userCurrent.getUserInfo(msg)
        userInfo, isNew = kbs.getMainUserInfo(msg)
        if isNew == False:
            pieces = msg.text.split()
            if len(pieces)==3:
                all_variables = dir(userInfo)
                paramName = pieces[1]
                for param in all_variables:
                    if param == paramName:
                        value = pieces[2]
                        await msg.answer(f"Параметр {paramName} изменен на {value}")
                        exec(f"userInfo.{paramName} = {value}")
                        paramName = value
                        # userInfo.save()
                        return
                await msg.answer("Параметр не нрайден")
            else:
               await msg.answer("Небходим номер запроса")
        return
    def getMainUserInfo(msg: types.Message):
        userCurrent = userDB(True)
        userInfo, isNew = userCurrent.getUserInfo(msg)
        return userInfo, isNew
    

    # отработка введенных данных
    async def getUserData(menu, current_menu, msg: types.Message, userInfo):
        # ввод номера плоттера
        if current_menu == "menuRequestDeviceId".lower():
            # res = okDesk.findEquipmentByInvetoryId(msg)
            res = okDesk.findPlaceEquipmentByInvetoryId(msg.text)
            if res is None:
                await msg.answer("Оборудование не найдено. Повторите!")
                return
            userInfo.okDeskInfo = msg.text
            userInfo.save()
            
            msgReplay = res['name'] + '\n' + res['address']
            userInfo, isNew = kbs.getMainUserInfo(msg)
            await msg.answer(msgReplay)
            if userInfo.userType == 'employer':
                await kbs.get_kb_by_idmenu(menu, msg, 'menuPlaceIdemployerMain')
            elif userInfo.userType == 'client':
                await kbs.get_kb_by_idmenu(menu, msg, 'menuPlaceIdclientMain')
            elif userInfo.userType == 'clientAntiFrod':
                await kbs.get_kb_by_idmenu(menu, msg, 'menuPlaceIdclientAntiFrodMain')
            elif userInfo.userType == 'clientIntegration':
                await kbs.get_kb_by_idmenu(menu, msg, 'menuPlaceIdclientIntegrationMain')
            else:
                await kbs.get_kb_by_idmenu(menu, msg, 'menuPlaceIdBad')
            return
                

        # ввод торговой точки
        if current_menu == "menuEditPointId".lower():
            # res = okDesk.findEquipmentByInvetoryId(msg)
            res = okDesk.findPlaceEquipmentByShopId(msg.text)
            if res is None:
                await msg.answer("Точка не найдена. Повторите!")
                return
            userInfo.okDeskInfo = msg.text
            userInfo.save()
            
            msgReplay = res['name'] + '\n' + res['address']
            await msg.answer(msgReplay)
            await kbs.get_kb_by_idmenu(menu, msg, 'menuShopPlaceId')
            return

        # ---------------------------------------------------------------------------------
        # создание завки
        # Обратиться в поддержку
        if current_menu == "menuCreateRequestSupport".lower():
            userInfo.okDeskInfo = msg.text+'\n'
            userInfo.save()
            msgReply = menu.getAssisitans("base", "answer6", userInfo.assistant, "12345678")
            await msg.answer(msgReply)
            return

        await msg.answer("Непоняно")
        return
    
    # создание заявки
    async def createRequest(menu, current_menu, msg: types.Message, userInfo, msgNext):
        if msgNext.lower()=='menuCreateRequest'.lower():
            return
        return