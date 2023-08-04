
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
        if len(res) == 0:
            return None
        
        maintenance_entity_id = res['maintenance_entity_id']

        URLmaintenance = 'https://insitech.okdesk.ru/api/v1/maintenance_entities/' + str(maintenance_entity_id) + '?' + mainConst.OKDESK_TOKEN
        resMaintenance = requests.get(URLmaintenance).json()
        if len(resMaintenance) == 0:
            return None
        return resMaintenance

    # запрос на расположение устройства по InvetoryId (торговая точка)
    def createShopByInvetoryId(inventory_number):
        # Поиск торговой точки
        URL = 'https://insitech.okdesk.ru/api/v1/maintenance_entities/?' + mainConst.OKDESK_TOKEN +  '&search_string=' + str(inventory_number)
        res = requests.get(URL).json()
        if len(res) == 0:
            return None
        return None

        # $result = botUtils::getOkDesk($sURL);
        # $dataRes = json_decode($result, true);
        # $all = count($dataRes);
        # $addressResult = array();
        # for ($i = 0; $i < $all; $i++) {
        #     //Получение списка обьектов обслуживания
        #     $maintenance_entity_id = $dataRes[$i]['id'];
        #     if ($maintenance_entity_id != null) {
        #         $sURLmaintenance = 'https://insitech.okdesk.ru/api/v1/maintenance_entities/' . $maintenance_entity_id . '?' . okDeskToken;
        #         $resultsMaintenance = botUtils::getOkDesk($sURLmaintenance);
        #         $dataResMaintenance = json_decode($resultsMaintenance, true);
        #         $address = $dataResMaintenance['address'];
        #         array_push($addressResult, $dataResMaintenance);

        #     }
        # }
        # if (count($addressResult) > 0) {
        #     //sendMessage($info, $data);
        #     return $addressResult;
        # }
        # return null;

