

# статус паралельных линий
import enum

class mainConst():
    DB_TEST = True
class TypeСutout(enum.Enum):
    undifined = 0
    UType0 = 1
    UType1 = 2
    UType2 = 3
    UType3 = 4

class user:
    id : int
    phone : str
    first_name : str
    last_name : str
    mode : int
    def __init__(self):
        id = 1335723885
        phone = '89218866929'
        first_name = 'Андрей'
        last_name = 'Кирилов'
        mode = -1