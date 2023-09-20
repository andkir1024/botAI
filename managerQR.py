from processorQR import *
from aiogram import types
from kbs import *
from commonData import *
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
                resultQR =  await managerQR.decodePhoto(message, photo_name, userInfo)
                result = managerQR.isPlotterQRplotter(resultQR, userInfo.current_menu)
                return result
        return None

    async def testPhoto(message: types.Message):
        userCurrent = userDB(True)
        userInfo, isNew = userCurrent.getUserInfo(message)
        if isNew == False and userInfo.current_menu == 'SelectPlotterByQRMenu':
            photo = message.photo[-1]
            photo_id = photo.file_unique_id
            photo_name = f'tempData/{photo_id}.jpg'     

            await photo.download(photo_name)
            # raw = await photo.download()
            resultQR =  await managerQR.decodePhoto(message, photo_name, userInfo)
            result = managerQR.isPlotterQRplotter(resultQR, userInfo.current_menu)
            return result

        return None

    async def getQr(message: types.Message, userInfo):
        photo = message.photo[-1]
        photo_id = photo.file_unique_id
        photo_name = f'tempData/{photo_id}.jpg'     

        await photo.download(photo_name)
        # raw = await photo.download()
        resultQR =  await managerQR.decodePhoto(message, photo_name, userInfo)
        result = managerQR.isPlotterQRplotter(resultQR, userInfo.current_menu)
        return result

    async def decodePhoto(message: types.Message, photo_name, userInfo):
        timeStart = time.time()
        resultQR = decodeImage(photo_name, decodeQRMode.onlyQR)
        os.remove(photo_name)
        if userInfo.infoMode == infoShow.QR:
            timeDelta = time.time() - timeStart
            await message.answer(f"Информация по QR запросу {timeDelta:0.2f} сек")
            for result in resultQR:
                await message.answer(result)

        return resultQR

    def isPlotterQRplotter(qrvalue, cmd):
        if len(qrvalue) == 1:
            paramsResult = qrvalue[0].split("\n")
            if len(paramsResult) >= 4:
                hardware = paramsResult[0]
                hardwareAll = hardware.split("=")
                if len(hardwareAll) == 2:
                    return hardwareAll[1]
        return None
