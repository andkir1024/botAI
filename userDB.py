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
    data : str
    def __init__(self):
        self.id = 1335723885
        self.phone = '89218866929'
        self.first_name = 'Андрей'
        self.last_name = 'Кирилов'
        self.mode = -1
        self.right = userRight.admin
        self.assistant = userAssistant.assistant0
        self.data = ""

    def __init__(self, message : types.Message):
        from_user = message.from_user
        self.id = from_user.id
        self.phone = None
        self.first_name = from_user.first_name
        self.last_name = from_user.last_name
        self.mode = -1
        self.right = userRight.user
        self.assistant = userAssistant.assistant0
        self.data = ""

    def save(self):
        s = json.dumps(self.__dict__)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        fileUser = dir_path + mainConst.DIR_USER + str(self.id) + '.json'
        with open(fileUser, "w") as text_file:
            text_file.write(str(s) + '\n')
        return

    def load(self):
        s = json.dumps(self.__dict__)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        fileUser = dir_path + mainConst.DIR_USER + str(self.id) + '.json'
        exists = os.path.exists(fileUser)
        if exists:
            f = open(fileUser)
            data = json.load(f)
            self.__dict__ = data
            return
        return
        
class userDB:
    def __init__(self, isModel):
        self.isModel = isModel
        return
    def getUserInfo(self, message : types.Message):
        if mainConst.DB_TEST:
            return self.getTestUserInfo(message)
        return None
    def getTestUserInfo(self, message : types.Message):
        id = message.from_id
        dir_path = os.path.dirname(os.path.realpath(__file__))
        fileUser = dir_path + mainConst.DIR_USER + str(id) + '.json'
        exists = os.path.exists(fileUser)
        if exists:
            usr =  user(message)
            usr.load()
            pass
        else:
            # новый пользователь (сохранить, создать)
            usr =  user(message)
            usr.save()
            return usr
            pass
        # if id == 1335723885:
            # return user()
        return None    
