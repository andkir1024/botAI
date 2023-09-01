from processorQR import *
from aiogram import types
from kbs import *
import time
import os


class managerQR:

    async def testPhotoAsDocument(message: types.Message):
        userCurrent = userDB(True)
        userInfo, isNew = userCurrent.getUserInfo(message)
        if isNew == False and userInfo.current_menu == 'SelectPlotterByQRMenu':
            document = message.document
            if document.mime_base == 'image':
                photo_id = document.file_unique_id
                photo_name = f'tempData/{photo_id}.jpg'     
                await message.document.download(photo_name)
                return await managerQR.decodePhoto(message, photo_name, userInfo)
        return False

    async def testPhoto(message: types.Message):
        userCurrent = userDB(True)
        userInfo, isNew = userCurrent.getUserInfo(message)
        if isNew == False and userInfo.current_menu == 'SelectPlotterByQRMenu':
            photo = message.photo[-1]
            photo_id = photo.file_unique_id
            photo_name = f'tempData/{photo_id}.jpg'     

            await photo.download(photo_name)
            # raw = await photo.download()
            return await managerQR.decodePhoto(message, photo_name, userInfo)

        return False

    async def decodePhoto(message: types.Message, photo_name, userInfo):
        timeStart = time.time()
        resultQR = decodeImage(photo_name, decodeQRMode.onlyQR)
        os.remove(photo_name)
        if userInfo.infoMode == infoShow.QR:
            timeDelta = time.time() - timeStart
            await message.answer(f"Информация по QR запросу {timeDelta:0.2f} сек")
            for result in resultQR:
                await message.answer(result)
            return True

        return False
