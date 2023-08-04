
import requests
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
    def findPlaceEquipmentByInvetoryId(inventory_number):
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

    # запрос на расположение устройства по shop_code (торговая точка)
    def findPlaceEquipmentByShopId(shop_code):
        # Поиск торговой точки
        URL = 'https://insitech.okdesk.ru/api/v1/maintenance_entities/?' + mainConst.OKDESK_TOKEN +  '&search_string=' + str(shop_code)
        res = requests.get(URL).json()
        if len(res) == 0:
            return None
        for shop in res:
            parameters = shop['parameters']
            for param in parameters:
                name = param['name'].lower()
                value = param['value'].lower()
                if 'objectPartnerCode'.lower() in name and value == shop_code.lower():
                    return shop
        return None

    # поиск пользователя
    def findUserByPhone(phone, company_id):
        #  проверка на наличие человека в базе
        sURLrequestUser = 'https://insitech.okdesk.ru/api/v1/contacts/?' + mainConst.OKDESK_TOKEN + '&phone=' + str(phone)
        res = requests.get(sURLrequestUser).json()
        if len(res) == 0:
            return None

        # $idUser = $decodeRequest['id'];
        # $company_id = $decodeRequest['company_id'];
        # //если он есть
        # $isUser = isset($idUser);
        # if ($isUser == false)
        #     return null;
        # return $idUser;


    # создание пользователя
    def postOkDeskCreateUser(data, phone, company_id, bot_data):
        return None
        # $company_id = null;
        # $idUser = self::findUserByPhone($phone, $company_id);
        # if ($idUser == null) {
        #     $sURLcreateUser = 'https://insitech.okdesk.ru/api/v1/contacts/?' . okDeskToken;
        #     //если нет то создаем
        #     $json = array(
        #         'contact' => array(
        #             'first_name' => $data['chat']['first_name'],
        #             'last_name' => $data['chat']['last_name'],
        #             'phone' => $phone
        #         )
        #     );

        #     //$dataOut = json_encode($json, JSON_UNESCAPED_UNICODE );
        #     $options = array(
        #         'http' => array(
        #             'method' => 'POST',
        #             'header' => "Content-Type: application/json; charset=utf-8\r\n",
        #             'content' => json_encode($json)
        #         )
        #     );
        #     $context = stream_context_create($options);
        #     $resultRequest = file_get_contents($sURLcreateUser, false, $context);

        #     $decodeRequest = json_decode($resultRequest, true);
        #     $idUser = $decodeRequest['id'];
        # }
        # return $idUser;

    # создание заявки
    def createRequest(inventory_number, messageRequest, typeRequst, bot_data, description, menuParam, usedNumbers):
        return None
        # получаем Объект обслуживания:
        # URL = 'https://insitech.okdesk.ru/api/v1/equipments/?' + mainConst.OKDESK_TOKEN + '&inventory_number=' . str(inventory_number)
        # res = requests.get(URL).json()
        # if len(res) == 0:
        #     return None
        
        # # поиск человека
        # $company_id = null;
        # $idUser = botUtils::postOkDeskCreateUser($data, $bot_data['phone'], $company_id, $bot_data);
        # $idUser = (string)$idUser;
        # //5 оформление заявки
        # $idRequest = botUtils::postOkDeskRequest($typeRequst, $messageRequest, $idUser, $dataRes, $description, $usedNumbers, $company_id, $data);
        # $idRequest = json_decode($idRequest, true);

        # $idRequestAddress = botUtils::getLoginLink() . '&redirect=/issues/' . $idRequest;
        # $msg = botMenu::translateTextById('Request', $menuParam) . " ";
        # self::saveRequest($bot_data, $idRequest);

        # $info = $msg . $idRequest;

        # if ($idRequest == null)
        #     return null;


        # botUtils::sendMessage($info, $data);
        # //
        # $adminList = botMenu::readAdmin('admin.json');
        # $msgAdmin = botMenu::translateTextById('RequestNew', $menuParam) . " " . $idRequest;
        # botProcRequest::sendMessageAllAdmin($msgAdmin, $adminList);
		# //
        # return $idRequest;
