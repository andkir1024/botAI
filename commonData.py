

# статус паралельных линий
import enum

class mainConst():
    API_TOKEN = '6232440369:AAG-bS18nYh-cXVUWrMKham3mP6OTjTaw4k'    
    DB_TEST = True
class userRight(enum.Enum):
    undifined = 0
    admin = 1
    worker = 2
    user = 3

class userAssistant(enum.Enum):
    undifined = 0
    assistant0 = 1
    assistant1 = 2
    assistant2 = 3

class user:
    id : int
    phone : str
    first_name : str
    last_name : str
    mode : int
    right : userRight
    assistant : userAssistant
    def __init__(self):
        self.id = 1335723885
        self.phone = '89218866929'
        self.first_name = 'Андрей'
        self.last_name = 'Кирилов'
        self.mode = -1
        self.right = userRight.admin
        self.assistant = userAssistant.assistant0