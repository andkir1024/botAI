from aiogram import types
from kbs import *

class testBotUtils:
    
    async def testManager(msg: types.Message):
        userCurrent = userDB(True)
        userInfo, isNew = userCurrent.getUserInfo(msg)
        if isNew == False:
            pieces = msg.text.split()
            if len(pieces)==2:
                mode = pieces[1]
                if mode == '0':
                    await testBotUtils.testCreateRequest(userInfo, msg)
                if mode == '1':
                    await testBotUtils.testQR(userInfo, msg)
                return
            else:
               await msg.answer("Небходим номер запроса")

    # поиск оборудования по InvetoryId
    async def testCreateRequest(userInfo,msg: types.Message):
        # userCurrent = userDB(True)
        # userInfo, isNew = userCurrent.getUserInfo(msg)
        # okDesk.findUserByPhone("+79218866929")
        # okDesk.findUserByPhone("9218866929")
        # okDesk.createRequest("5956", userInfo, 'Application_for_rez_Guarantee_auto')
        await msg.answer("Тестировиние OKDesk")

    # тестирование QR кодов
    async def testQR(userInfo,msg: types.Message):
        await msg.answer("Тестировиние QR")



