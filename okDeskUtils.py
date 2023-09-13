
import json
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
    def getListReqwests(idUser):
        statusAdd = '&status_not[]=closed&status_not[]=Allow_auto';
		
        # URLrequest = 'https://insitech.okdesk.ru/api/v1/issues/count?' + mainConst.OKDESK_TOKEN +  '&contact_ids[]=' + idUser + statusAdd
        URLrequest = 'https://insitech.okdesk.ru/api/v1/issues/count?' + mainConst.OKDESK_TOKEN +  '&contact_ids[]=' + str(idUser)
        res = requests.get(URLrequest).json()
        if 'errors' in res:
            return None
        if len(res) == 0:
            return None
        resOut = res[-5:]
        resOut = resOut[::-1]
        msgs = []
        for requestiD in resOut:
            URLrequest = 'https://insitech.okdesk.ru/api/v1/issues/' + str(requestiD) + '?' + mainConst.OKDESK_TOKEN
            res = requests.get(URLrequest).json()
            msg = f"id={requestiD} : {res['title']} : {res['created_at']}"
            msgs.append(msg)
        return msgs

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
    def findUserByPhone(phone):
        #  проверка на наличие человека в базе
        sURLrequestUser = 'https://insitech.okdesk.ru/api/v1/contacts/?' + mainConst.OKDESK_TOKEN + '&phone=' + str(phone)
        res = requests.get(sURLrequestUser).json()
        if len(res) == 0:
            return None

        if 'id' in res:
            return res['id']
        return None

    def getUserByPhone(userInfo):
        phone = userInfo.phone
        idUser = okDesk.findUserByPhone(phone)
        return idUser

    # создание пользователя
    def postOkDeskCreateUser(userInfo):
        phone = userInfo.phone
        idUser = okDesk.findUserByPhone(phone)
        if idUser is None:
            # если нет то создаем
            sURLcreateUser = 'https://insitech.okdesk.ru/api/v1/contacts/?' + mainConst.OKDESK_TOKEN
            # $json = array(
            #     'contact' => array(
            #         'first_name' => $data['chat']['first_name'],
            #         'last_name' => $data['chat']['last_name'],
            #         'phone' => $phone
            #     )
            # );

            # //$dataOut = json_encode($json, JSON_UNESCAPED_UNICODE );
            # $options = array(
            #     'http' => array(
            #         'method' => 'POST',
            #         'header' => "Content-Type: application/json; charset=utf-8\r\n",
            #         'content' => json_encode($json)
            #     )
            # );
            # $context = stream_context_create($options);
            # $resultRequest = file_get_contents($sURLcreateUser, false, $context);

            # $decodeRequest = json_decode($resultRequest, true);
            # $idUser = $decodeRequest['id'];
        return idUser

    # создание заявки
    # def createRequest(inventory_number, messageRequest, typeRequst, bot_data, description, menuParam, usedNumbers):
    def createRequest(inventory_number, userInfo, typeRequest):
        # return None
        # получаем Объект обслуживания:
        URL = 'https://insitech.okdesk.ru/api/v1/equipments/?' + mainConst.OKDESK_TOKEN + '&inventory_number=' + str(inventory_number)
        resEqupment = requests.get(URL).json()
        if len(resEqupment) == 0:
            return None
        
        # поиск человека
        idUser = okDesk.postOkDeskCreateUser(userInfo)
        if idUser is None:
            return None

        # оформление заявки
        idRequest =okDesk.postOkDeskRequest(idUser, resEqupment, 'title', typeRequest, 'description')
        # idRequest =okDesk.postOkDeskRequest($typeRequst, $messageRequest, $idUser, $dataRes, $description, $usedNumbers, $company_id, $data)
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

    def testCluster(cluster):
        if cluster is None:
            return None
        pieces = cluster.split()
        if len(pieces) != 2:
            return None
        if pieces[1] == '2':
            return 'normal'
        if pieces[1] == '3':
            return 'high'
        if pieces[1] == '4':
            return 'highest'
        return 'low'

    def addCompanyToContact(userId, company_id):
        # редактирование контакта
        sURLeditUser = 'https://insitech.okdesk.ru/api/v1/contacts/' + str(userId) + '?' + mainConst.OKDESK_TOKEN
        # send_data = [
        #     'company_id' => company_id,
        #     # 'email' => 'aa1@mail.ru',

        # ]
        # options = array(
        #     'http' => array(
        #         'method' => 'PATCH',
        #         'header' => "Content-Type: application/json; charset=utf-8\r\n",
        #         'content' => json_encode(send_data)
        #     )
        # );
        # context = stream_context_create(options)
        # resultRequest = file_get_contents(sURLeditUser, false, context)
    
    def postOkDeskRequest(idUser, resEqupment, title, typeRequest, description):
        maintenance_entity_id = resEqupment['maintenance_entity_id']
        equipment_id = resEqupment['id']
        URLmaintenance = 'https://insitech.okdesk.ru/api/v1/maintenance_entities/' + str(maintenance_entity_id) + '?' + mainConst.OKDESK_TOKEN
        resultsMaintenance = requests.get(URLmaintenance).json()
        if len(resultsMaintenance) == 0:
            return None
        cluster = resultsMaintenance['parameters'][3]['value']
        clusterId = okDesk.testCluster(cluster)
        if maintenance_entity_id is None:
            if 'company_id' in resultsMaintenance:
                okDesk.addCompanyToContact(idUser, resultsMaintenance['company_id'])
                maintenance_entity_id = resEqupment['maintenance_entity_id']

        URLrequest = 'https://insitech.okdesk.ru/api/v1/issues/?' + mainConst.OKDESK_TOKEN
        typeUser = "contact"
        request = {
            'issue': {
                'title': str(title),
                "type": str(typeRequest),
                "description": str(description),
                "contact_id": str(idUser),
                "maintenance_entity_id": str(maintenance_entity_id),
                "priority": str(clusterId),
                "equipment_ids": [
                    str(equipment_id),
                ],
                "author": {
                    "id": str(idUser),
                    "type": str(typeUser),
                },
            },
        }
        
        json_string = json.dumps(request)
        res = requests.post(URLrequest, json=request)
        # res = requests.post(URLrequest, data=json_string)
        # zzz= json.dumps(res.json(), sort_keys=True, indent=4)
        # res = requests.post(URLrequest, data=request)

        return None 
        # $maintenance_entity_id = $dataRes['maintenance_entity_id'];
        # $equipment_id = null;
        # $equipment_id = $dataRes['id'];
        # if ($usedNumbers == false) {
        #     $maintenance_entity_id = null;
        #     $equipment_id = null;
        # }
        # if ($company_id == null)
        #     $maintenance_entity_id = null;
        # $sURLmaintenance = 'https://insitech.okdesk.ru/api/v1/maintenance_entities/' . $dataRes['maintenance_entity_id'] . '?' . okDeskToken;
        # $resultsMaintenance = self::getOkDesk($sURLmaintenance);
        # $dataResMaintenance = json_decode($resultsMaintenance, true);
        # $cluster = $dataResMaintenance['parameters'][3]['value'];
        # $clusterId = self::testCluster($cluster);

#         if ($maintenance_entity_id == null) {
#             if ($dataResMaintenance['company_id'] != null) {
#                 self::addCompanyToContact($userId, $dataResMaintenance['company_id']);
#                 $maintenance_entity_id = $dataRes['maintenance_entity_id'];
#             }
#         }
#         $sURLrequest = 'https://insitech.okdesk.ru/api/v1/issues/?' . okDeskToken;
#         $adminList = botMenu::readAdmin('admin.json');
#         $adminParam = botMenu::paramAdmin($data, $adminList);
#         $user_id = $adminParam['user_id'];
#         $type = 'contact';
#         $id = $userId;
#         if ($user_id != null) {
#             $type = 'employee';
#             $id = $user_id;
#         }
#         $json = array(
#             'issue' => array(
#                 'title' => $title,
#                 'type' => $typeRequest,
#                 'description' => $description,
#                 'contact_id' => $userId,
#                 'maintenance_entity_id' => $maintenance_entity_id,
#                 'priority' => $clusterId,
#                 'equipment_ids' => array(
#                     $equipment_id,
#                 ),
#                 'author' => array(
#                     'id' => (string)$id,
# //				'type' => 'contact',
#                     'type' => $type,
#                 )
#             )
#         );

#         $options = array(
#             'http' => array(
#                 'method' => 'POST',
#                 'header' => "Content-Type: application/json; charset=utf-8\r\n",
#                 'content' => json_encode($json)
#             )
#         );
#         $context = stream_context_create($options);
#         $resultRequest = file_get_contents($sURLrequest, false, $context);

#         $decodeRequest = json_decode($resultRequest, true);
#         $idRequest = $decodeRequest['id'];
#         if ($maintenance_entity_id == null) {
#             # получение информации о обекто обслуживания
#             self::postOkDeskAddComment($userId, 'Это новый контакт.' . "\n" . $dataResMaintenance['name'] . "\n" . ' Необходима привязка', $idRequest);
#             self::addCompanyToContact($userId, $dataResMaintenance['company_id']);
#         }
#         return $idRequest;
