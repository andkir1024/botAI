import json
from commonData import *
from aiogram import types
import os.path

class user:
    id : int
    phone : str
    first_name : str
    last_name : str
    mode : int
    right : userRight
    assistant : userAssistant
    current_menu : str
    okDeskInfo : str
    okDeskUserId : int
    data : str
    userType : str
    counter : int
    # информация выводимая ботом для конкретного пользователя
    infoMode : int
    def __init__(self):
        self.id = 1335723885
        self.phone = '89218866929'
        self.first_name = 'Андрей'
        self.last_name = 'Кирилов'
        self.mode = -1
        self.right = userRight.admin
        self.assistant = userAssistant.assistant0
        self.current_menu = ""
        self.okDeskInfo = ""
        self.data = ""
        self.infoMode = infoShow.undifined
        self.userType = userType.client
        self.okDeskUserId = -1
        self.counter = -1

    def __init__(self, message : types.Message):
        from_user = message.from_user
        self.id = from_user.id
        self.phone = None
        self.first_name = from_user.first_name
        self.last_name = from_user.last_name
        self.mode = -1
        self.right = userRight.user
        self.assistant = userAssistant.assistant0
        self.current_menu = ""
        self.okDeskInfo = ""
        self.data = ""
        self.infoMode = infoShow.undifined
        self.userType = userType.client
        self.okDeskUserId = -1
        self.counter = -1
        
    def save(self, clearCounter = True):
        if clearCounter:
            self.counter = -1

        s = json.dumps(self.__dict__)
        fileUser = user.getFileName(self.id)
        with open(fileUser, "w") as text_file:
            text_file.write(str(s))
        return

    def load(self):
        fileUser = user.getFileName(self.id)
        exists = os.path.exists(fileUser)
        if exists:
            f = open(fileUser)
            try:
                data = json.load(f)
                self.__dict__ = data
            except:
                pass
            try:
                aa = self.counter
            except:
                exec("self.counter=-1")
            return
        return

    def getFileName(id):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        fileUser = dir_path + mainConst.DIR_USER + str(id) + '.json'
        return fileUser
        
        
class userDB:
    def __init__(self, isModel):
        self.isModel = isModel
        return
    def getUserInfo(self, message : types.Message):
        if mainConst.DB_TEST:
            return self.getTestUserInfo(message)
        return None, None
    def getTestUserInfo(self, message : types.Message):
        id = message.from_id
        fileUser = user.getFileName(id)
        exists = os.path.exists(fileUser)
        if exists:
            usr =  user(message)
            usr.load()
            return usr, False
        # новый пользователь (сохранить, создать)
        usr =  user(message)
        usr.save()
        return usr, True
