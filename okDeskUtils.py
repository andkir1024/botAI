
import requests
# from requests import async
from commonData import mainConst

class okDesk:
    # поиск оборудования по InvetoryId
    def findEquipmentByInvetoryId(inventory_number):
        URL = 'https://insitech.okdesk.ru/api/v1/equipments/?' + mainConst.OKDESK_TOKEN + '&inventory_number=' + str(inventory_number)
        res = requests.get(URL)
        return

    # поиск точки обслуживания по maintenance_entity_id
    def findMaintenanceEntitiesByInvetoryId(maintenance_entity_id):
        URL = 'https://insitech.okdesk.ru/api/v1/maintenance_entities/' + str(maintenance_entity_id) + '?' + mainConst.OKDESK_TOKEN
        res = requests.get(URL)
        return
