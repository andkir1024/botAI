
import requests
# from requests import async
from commonData import mainConst

class okDesk:
    # поиск оборудования по InvetoryId
    def findEquipmentByInvetoryId(inventory_number):
        URL = 'https://insitech.okdesk.ru/api/v1/equipments/?' + mainConst.OKDESK_TOKEN + '&inventory_number=' + str(inventory_number)
        res = requests.get(URL)
        return res

    # поиск точки обслуживания по maintenance_entity_id
    def findMaintenanceEntitiesByInvetoryId(maintenance_entity_id):
        URL = 'https://insitech.okdesk.ru/api/v1/maintenance_entities/' + str(maintenance_entity_id) + '?' + mainConst.OKDESK_TOKEN
        res = requests.get(URL)
        return res

    # запрос на расположение устройства по InvetoryId (номер плоттера)
    def createEquipmentByInvetoryId(inventory_number):
        # Поиск оборудования
        URL = 'https://insitech.okdesk.ru/api/v1/equipments/?' + mainConst.OKDESK_TOKEN + '&inventory_number=' + str(inventory_number)

        res = requests.get(URL).json()
        
        maintenance_entity_id = res['maintenance_entity_id']

        URLmaintenance = 'https://insitech.okdesk.ru/api/v1/maintenance_entities/' + str(maintenance_entity_id) + '?' + mainConst.OKDESK_TOKEN
        resMaintenance = requests.get(URLmaintenance).json()
        return resMaintenance

        # //Получение списка обьектов обслуживания
        # $maintenance_entity_id = $dataRes['maintenance_entity_id'];
        # //$sURLmaintenance = 'https://insitech.okdesk.ru/api/v1/maintenance_entities/list?'.okDeskToken;
        # $sURLmaintenance = 'https://insitech.okdesk.ru/api/v1/maintenance_entities/' . $maintenance_entity_id . '?' . okDeskToken;
        # $resultsMaintenance = botUtils::getOkDesk($sURLmaintenance);
        # $dataResMaintenance = json_decode($resultsMaintenance, true);
        # $address = $dataResMaintenance['address'];
        # $point = $dataResMaintenance['name'];
        # $addressResult = $dataResMaintenance;

        # //3 нахождение ддреса

        # $info = $dataResMaintenance['name'] . "\n" . 'По адресу: ' . $address;

        # if ($dataRes['maintenance_entity_id'] == null)
        #     return null;
        # botUtils::sendMessage($info, $data);
        # return $addressResult;
