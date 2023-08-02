

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

class userTheme(enum.Enum):
    undifined = 0
    theme0 = 1
    theme1 = 2
    theme2 = 3

class user:
    id : int
    phone : str
    first_name : str
    last_name : str
    mode : int
    right : userRight
    theme : userTheme
    def __init__(self):
        self.id = 1335723885
        self.phone = '89218866929'
        self.first_name = 'Андрей'
        self.last_name = 'Кирилов'
        self.mode = -1
        self.right = userRight.admin
        self.theme = userTheme.theme0