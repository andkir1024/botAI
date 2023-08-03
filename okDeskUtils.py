
import requests
from commonData import mainConst


class okDesk:
    # поиск оборудования по InvetoryId
    def findEquipmentByInvetoryId(inventory_number):
        # Поиск оборудования
        URL = 'https://insitech.okdesk.ru/api/v1/equipments/?' + mainConst.OKDESK_TOKEN + '&inventory_number=' + str(inventory_number)
        res = requests.get(URL)
        # res = requests.post(URL, data={'st3': 'jim hopper'})
        # res = requests.post('https://httpbin.org/post', data={'st3': 'jim hopper'})
        # print(res.text)
        return

        # $result = botUtils::getOkDesk($sURL);
		# return $dataRes;
