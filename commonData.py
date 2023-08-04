from aiogram import types
import enum

class mainConst():
    API_TOKEN = '6232440369:AAG-bS18nYh-cXVUWrMKham3mP6OTjTaw4k'    
    DB_TEST = True
    OKDESK_TOKEN = 'api_token=ae71c1f696464efe94383d6acf37fa031b1848fb'
    DIR_DATA = '/data/'
    DIR_USER = '/users/'
    DIR_RESOURCE = '/resource/'
    
class userRight(str,enum.Enum):
    undifined = 'undifined'
    admin = 'admin'
    worker = 'worker'
    user = 'user'

class userAssistant(str, enum.Enum):
    undifined = 'undifined'
    assistant0 = 'assistant0'
    assistant1 = 'assistant1'
    assistant2 = 'assistant2'

# class user:
#     id : int
#     phone : str
#     first_name : str
#     last_name : str
#     mode : int
#     right : userRight
#     assistant : userAssistant
#     def __init__(self):
#         self.id = 1335723885
#         self.phone = '89218866929'
#         self.first_name = 'Андрей'
#         self.last_name = 'Кирилов'
#         self.mode = -1
#         self.right = userRight.admin
#         self.assistant = userAssistant.assistant0