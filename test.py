# import asyncio
# import time


# async def fun1(x):
#     print(x**2)
#     await asyncio.sleep(3)
#     print('fun1 завершена')


# async def fun2(x):
#     print(x**0.5)
#     await asyncio.sleep(3)
#     print('fun2 завершена')


# async def main():
#     task1 = asyncio.create_task(fun1(4))
#     task2 = asyncio.create_task(fun2(4))

#     await task1
#     await task2


# print(type(fun1))

# print(type(fun1(4)))

import requests
from requests.auth import AuthBase


# class TokenAuth(AuthBase):
#     """Implements a custom authentication scheme."""
 
#     def __init__(self, token):
#         self.token = token
 
#     def __call__(self, r):
#         """Attach an API token to a custom auth header."""
#         r.headers['X-TokenAuth'] = f'{self.token}'  # Python 3.6+
#         return r
 
 
# qq0 =requests.get('https://api-machine3.armorjack.ru//v4/ajm/check/index', auth=TokenAuth('OTk0MjU4OWUwY2FhN2ZjM2U5NjBlYTc1MTE4NzQ1ZTY6'))
# qq1 =requests.get('http://api-machine.armorjack.ru/v4/ajm/base/index', auth=TokenAuth('9942589e0caa7fc3e960ea75118745e6'))
# qq1 =requests.get('http://api-machine3.armorjack.ru/v4/ajm/clock/index', auth=TokenAuth('9942589e0caa7fc3e960ea75118745e6'))

# session = requests.Session()
# session.auth = ('9942589e0caa7fc3e960ea75118745e6', '')

# auth = session.post('http://api-machine3.armorjack.ru/v4/ajm/clock/index')
# response = session.get('http://' + hostname + '/rest/applications')

from requests.auth import HTTPBasicAuth
res = requests.post("http://api-machine.armorjack.ru/v4/ajm/clock/index", auth=HTTPBasicAuth("9942589e0caa7fc3e960ea75118745e6", ""))

print ("start test")

import json  
url = 'https://api-machine3.armorjack.ru//v4/ajm/check/index'  
param_dict = {
    # "partner_id": 8,
    # "shop": "L142",
    # "list_update": "2022-03-02 10:30:03"
    "local": {
        "time": "2023-07-09 23:04:50"
    }
}
response = requests.post(url, data=json.dumps(param_dict))
print (response)


import sched, time

s = sched.scheduler(time.time, time.sleep)

def f():
    s.enter(5, 1, f)  # Перезапуск через 5 секунд
    print(time.time())      
    response = requests.post(url, data=json.dumps(param_dict))
    print (response)
f()
s.run()
