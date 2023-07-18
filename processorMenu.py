from aiogram import Bot, Dispatcher, executor, types

class processorMenu:
    def __init__(self, name):
        self.name = name
        return
    async def doMenu(self, message):
        await message.reply("Привет!\nЯ Эхо-бот\nОтправь мне любое сообщение, а я тебе обязательно отвечу.")
        
        return