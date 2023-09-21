import html
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from managerQR import managerQR
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
        if msgCmd == 'start':
            msgCmd = 'StartFirst'
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
                # titleTmp = menu.getAssisitans('base', 'answer1', userInfo.assistant)
                # await msg.answer(titleTmp)
                # userInfo.current_menu = msgNext
                # userInfo.save()
                # await msg.answer(title, reply_markup=menuReply)

                userInfo.current_menu = msgNext
                userInfo.save()
                await kbs.gotoMenu(msg, menu, 'StartFirst', userInfo)
            return
        # переход к следующему меню
        next_menu = kbs.findNextMenu(menu, msg.text, current_menu, msg, userInfo)
        if next_menu is not None:
            if 'next' in next_menu:
                msgNext = next_menu['next']
                if 'msg' in next_menu:
                    msgReply = menu.getAssisitans("base", next_menu['msg'], userInfo.assistant)
                    await msg.answer(msgReply)
                    
                menuReply, title, selMenu = menu.getMenu(msgNext, msg, userInfo)

                # режим сотрудников
                if current_menu == 'menuEmployer'.lower():
                    if 'id' in next_menu:
                        id = next_menu['id'].lower()
                        if id == 'addLekalo'.lower() or id == 'tempLekalo'.lower() or id == 'changeCut'.lower():
                            msgReply = menu.getAssisitans("base", 'answer30', userInfo.assistant)
                            # await msg.answer(msgReply)
                            await kbs.gotoMenu(msg, menu, 'menuWaitComment', userInfo, msgReply)
                            
                        if id == 'closePoint'.lower():
                            msgReply = menu.getAssisitans("base", 'answer29', userInfo.assistant)
                            await kbs.gotoMenu(msg, menu, 'menuWaitComment', userInfo, msgReply)
                            # await msg.answer(msgReply)
                        if id == 'openPoint'.lower():
                            msgReply = menu.getAssisitans("base", 'answer28', userInfo.assistant)
                            await kbs.gotoMenu(msg, menu, 'menuWaitComment', userInfo, msgReply)
                            # await msg.answer(msgReply)
                        return

                # режим мой магазин
                if current_menu == 'menuShop'.lower():
                    if 'id' in next_menu:
                        id = next_menu['id'].lower()
                        if id == 'requestTraining'.lower():
                            msgReply = menu.getAssisitans("base", 'answer13', userInfo.assistant)
                            await msg.answer(msgReply)
                        if id == 'requestDataBase'.lower():
                            msgReply = menu.getAssisitans("base", 'answer14', userInfo.assistant)
                            await msg.answer(msgReply)

                # создание списка заявок (если в этом режиме)
                RequestList = await kbs.createRequestList(menu, current_menu, msg, userInfo, msgNext)
                if RequestList is not None:
                    for request in RequestList:
                        kb = KeyboardButton(request)
                        menuReply.add(kb)
                    pass

                # создание заявки (если в этом режиме)
                Request = await kbs.createRequest(menu, current_menu, msg, userInfo, msgNext)
                
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
        else:
            await msg.answer(f"ОШИБКА: меню {msgCmd} не найдено")

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
                        exec(f"userInfo.{paramName} = userType.{value}")
                        paramName = value
                        userInfo.save()
                        return
                await msg.answer("Параметр не нрайден")
            else:
               await msg.answer("Небходим номер запроса")
        return
    def getMainUserInfo(msg: types.Message):
        userCurrent = userDB(True)
        userInfo, isNew = userCurrent.getUserInfo(msg)
        return userInfo, isNew
    

    async def doEquipmentByInvetoryId(menu, current_menu, msg: types.Message, userInfo, InvetoryId):
        res = okDesk.findPlaceEquipmentByInvetoryId(InvetoryId)
        if res is None:
            await msg.answer("Оборудование не найдено. Повторите!")
            return
        userInfo.okDeskInfo =  'hardNum=' + InvetoryId
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

    # отработка введенных данных
    async def getUserData(menu, current_menu, msg: types.Message, userInfo):
        # ввод номера плоттера
        if current_menu == "menuRequestDeviceId".lower():
            # res = okDesk.findEquipmentByInvetoryId(msg)
            res = okDesk.findPlaceEquipmentByInvetoryId(msg.text)
            if res is None:
                await msg.answer("Оборудование не найдено. Повторите!")
                return
            userInfo.okDeskInfo = 'hardNum=' + msg.text
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
            userInfo.okDeskInfo = 'shopId=' + msg.text
            userInfo.save()
            
            msgReplay = res['name'] + '\n' + res['address']
            await msg.answer(msgReplay)
            await kbs.get_kb_by_idmenu(menu, msg, 'menuShopPlaceId')
            return

        # проблема с поддержкой
        if current_menu == "menuProblemDo".lower():
            msgReply = menu.getAssisitans("base", "answer32", userInfo.assistant)
            await msg.answer(msgReply)
            await kbs.gotoMenu(msg, menu, 'StartFirst', userInfo)
            return
        # ожидание комментарев для сотрудников
        if current_menu == "menuWaitComment".lower():
            msgReply = menu.getAssisitans("base", "answer6", userInfo.assistant, "12345678")
            await msg.answer(msgReply)
            await kbs.gotoMenu(msg, menu, 'menuContinueRequest', userInfo, "Сотрудник Иван Иванович взял заявку в работу")
            return
        # ---------------------------------------------------------------------------------
        # создание завки
        # 1 Обратиться в поддержку
        if current_menu == "menuCreateRequestSupport".lower():
            userInfo.okDeskInfo = msg.text+'\n'
            userInfo.save()
            msgReply = menu.getAssisitans("base", "answer6", userInfo.assistant, "12345678")
            await msg.answer(msgReply)
            # test
            # await msg.answer("Сотрудник Иван Иванович взял заявку в работу")
            # await kbs.gotoMenu(msg, menu, 'menuContinueRequest', userInfo)
            # await kbs.gotoMenu(msg, menu, 'menuFinalizeRequest', userInfo)
            await kbs.gotoMenu(msg, menu, 'menuContinueRequest', userInfo, "Сотрудник Иван Иванович взял заявку в работу")

            # msgReply = menu.getAssisitans("base", "answer7", userInfo.assistant)
            # await msg.answer(msgReply)

            return
        # 2 запросить расходники
        if current_menu == "menuGetSupplies".lower():
            userInfo.okDeskInfo = msg.text+'\n'
            userInfo.save()
            msgReply = menu.getAssisitans("base", "answer12", userInfo.assistant)
            await msg.answer(msgReply)
            await kbs.gotoMenu(msg, menu, 'StartFirst', userInfo)
            
            return
        # 3 подтвердить доставку
        if current_menu == "menuConfirmDelivery".lower():
            msgReply = menu.getAssisitans("base", "answer24", userInfo.assistant)
            await msg.answer(msgReply)
            return
        # 4 редактирование заявки
        if current_menu == "menuEditRequests".lower():
            # msgReply = menu.getAssisitans("base", "answer24", userInfo.assistant)
            # await msg.answer(msgReply)
            return

        await msg.answer("Непонятно")
        return
    
    async def sendMediaData(menu, msg: types.Message):
        userInfo, isNew = kbs.getMainUserInfo(msg)
        current_menu = userInfo.current_menu.lower()
        # сохранение данных для передачи
        if current_menu == "menuConfirmDelivery".lower():
            await kbs.gotoMenu(msg, menu, 'menuCorrespondsToAct', userInfo)
            return True
        # проверка qr кода плоттера для анализа его адреса
        if current_menu == "SelectPlotterByQRMenu".lower():
            InvetoryId = await managerQR.getQr(msg, userInfo)
            if InvetoryId is None:
                await msg.answer("Не QR код. Повторите ввод")
            else:
                await kbs.doEquipmentByInvetoryId(menu, current_menu, msg, userInfo, InvetoryId)
            return True
        # передача фотографий в режиме (рез по QR коду)
        if current_menu == "menuRequestQR".lower():
            msgReply = menu.getAssisitans("base", "answer23", userInfo.assistant)
            await kbs.gotoMenu(msg, menu, 'StartFirstPure', userInfo, msgReply)
            return True
        # передача фотографий в режиме (запрос на гарантию)
        if current_menu == "menuRequestGaranty".lower():
            msgReply = menu.getAssisitans("base", "answer16", userInfo.assistant)
            await kbs.gotoMenu(msg, menu, 'StartFirstPure', userInfo, msgReply)
            return True
        # передача фотографий в режиме (добавить лекало)
        if current_menu == "menuAddLekalo".lower():
            # if 'msg' in next_menu:
            # exec(f"userInfo.{counter} = 0")
            # exec(userInfo.counter = 0)
            if userInfo.counter < 0:
                userInfo.counter = 0
            if userInfo.counter == 0:
                msgReply = menu.getAssisitans("base", "answer10", userInfo.assistant)
                userInfo.counter += 1
                await msg.answer(msgReply)
                userInfo.save(False)
                return True
            if userInfo.counter == 1:
                userInfo.save()
                msgReply = menu.getAssisitans("base", "answer6", userInfo.assistant, "12345678")
                await kbs.gotoMenu(msg, menu, 'menuContinueRequest', userInfo, msgReply)
                return True
            return True

        return False
    # проверка на выбор пункта меню в зависимости от места в обработке
    async def testMenuYesNo(menu, msg: types.Message):
        userInfo, isNew = kbs.getMainUserInfo(msg)
        current_menu = userInfo.current_menu.lower()
        # подтверждение доставки
        if current_menu == "menuCorrespondsToAct".lower():
            if msg.text.lower() == "да":
                msgReply = menu.getAssisitans("base", "answer26", userInfo.assistant)
                await msg.answer(msgReply)
                await kbs.gotoMenu(msg, menu, 'StartFirst', userInfo)
                return True
            if msg.text.lower() == "нет":
                msgReply = menu.getAssisitans("base", "answer27", userInfo.assistant)
                await msg.answer(msgReply)
                await kbs.gotoMenu(msg, menu, 'StartFirst', userInfo)
                return True

        return False
    # создание меню с списком заявок
    async def createRequestList(menu, current_menu, msg: types.Message, userInfo, msgNext):
        if msgNext.lower()=='menuEditRequests'.lower():
            requsts = okDesk.getListReqwests(userInfo.okDeskUserId)
            return requsts
        return None
    # создание заявки
    async def createRequest(menu, current_menu, msg: types.Message, userInfo, msgNext):
        if msgNext.lower()=='menuCreateRequest'.lower():
            return True
        return False
    # переход на меню по имени
    async def gotoMenu(msg: types.Message, menu, menuName, userInfo, titleExt = None):
        msgNext = menuName
        menuReply, title, selMenu = menu.getMenu(msgNext, msg, userInfo)

        if menuReply is not None:
            userInfo.current_menu = msgNext
            userInfo.save()
            if titleExt is not None:
                title = titleExt
            await msg.answer(title, reply_markup=menuReply)
    