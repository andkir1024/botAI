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
from requests.auth import HTTPBasicAuth
import sched, time


print ("start test1")

import json  
url = 'http://api-machine.armorjack.ru/v4/ajm/settings/index'  
param_dict ={
    "list_update": "2022-09-05 12:30:03"
}
response = requests.post(url, data=json.dumps(param_dict), auth=HTTPBasicAuth('9942589e0caa7fc3e960ea75118745e6',""))
content = response.content
data = json.loads(content)
print (data)

# import json  
# def partnercheck (partner_id):
#     url = 'https://api-machine3.armorjack.ru/v4/ajm/check/index' 
#     param_dict = {
#         "partner_id": 8,
#         "shop": "000",
#         "list_update": "2022-03-02 10:30:03"    
#     }
#     response = requests.post(url, data=json.dumps(param_dict), auth=HTTPBasicAuth('9942589e0caa7fc3e960ea75118745e6',""))
#     content = response.content
#     data = json.loads(content)
#     return data
# partner_ids=[8]
# for partner_id in partner_ids:
#      print (f"партнер {partner_id}")
#      response= partnercheck (partner_id)
#      print (response)


# print ("start test")

# import json  
# url = 'https://api-machine3.armorjack.ru/v4/ajm/check/index'  
# param_dict = {
#     "partner_id": 8,
#     "shop": "L142",
#     "list_update": "2022-03-02 10:30:03"
#     # "local": {
#     #     "time": "2023-07-09 23:04:50"
#     # }
# }
# response = requests.post(url, data=json.dumps(param_dict), auth=HTTPBasicAuth('9942589e0caa7fc3e960ea75118745e6', ''))
# content = response.content
# data = json.loads(content)
# # s = json.dumps(content, indent=4, sort_keys=True)
# print (data)

# s = sched.scheduler(time.time, time.sleep)

# def f():
#     s.enter(5, 1, f)  # Перезапуск через 5 секунд
#     print(time.time())      
#     response = requests.post(url, data=json.dumps(param_dict), auth=HTTPBasicAuth('9942589e0caa7fc3e960ea75118745e6', ''))
#     print (response.content)
# f()
# s.run()
