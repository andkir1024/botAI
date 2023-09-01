from processorQR import *
from aiogram import types
from kbs import *
import time


class managerQR:

    async def testPhoto(message: types.Message):
        userCurrent = userDB(True)
        userInfo, isNew = userCurrent.getUserInfo(message)
        if isNew == False and userInfo.current_menu == 'SelectPlotterByQRMenu':
            photo = message.photo[-1]
            # photoD = photo.download()
            # destination_file = bot.download_file(file_path, destination)
            timeStart = time.time()
            await message.photo[-1].download('tempData/test.jpg')
            resultQR = decodeImage('tempData/test.jpg', 0)
            if userInfo.infoMode == infoShow.QR:
                timeDelta = time.time() - timeStart
                await message.answer(f"Информация по QR запросу {timeDelta:0.2f} сек")
                for result in resultQR:
                    await message.answer(result)

            return True
        return False
