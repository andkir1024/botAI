import sys
import cv2
import time
import pytesseract
from PIL import Image
from fuzzywuzzy import fuzz
from pyzbar import pyzbar

from commonData import decodeQRMode

def prepareImagheForTextDecode(img, alpha, beta, scale, clahe, contrast):
    if scale == True:
        scale_percent = 200  # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # clahe = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(8, 8))
    # clahe = cv2.createCLAHE(clipLimit=1.3, tileGridSize=(4, 4))

    if clahe == True:
        clahe = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(16, 16))
        gray = clahe.apply(gray)

    # alpha = 1.8
    # beta = 10
    if contrast == True:
        gray = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
    return gray


def createQRcode(sTest):
    if sTest == "":
        return ""
    paramsResult = sTest.split()
    if len(paramsResult) == 2:
        paramsTime = paramsResult[1].split(".")
        if len(paramsTime) != 3:
            return ""
        strTime = paramsTime[2] + paramsTime[1] + paramsTime[0]
        sOut = "t=" + strTime + "T0000&s=0000.00&fn=" + paramsResult[0] + "&i=0000&fp=000000006&n=0"
        # t=20220422T1652&s=8582.00&fn=9960440301915601&i=2046&fp=100861626&n=1
        return sOut
    return ""

def createQRcodeFromPhone(sTest, bar):
    # text_file = open("Output.txt", "w")
    # text_file.write(textRusUpd)
    # text_file.close()

    sbar = bar.decode("utf-8")
    sResult = findPlaceDate(sTest, "дата")
    # text_file.write(sTest)
    # text_file.write(sResult)
    if sResult == "":
        return ""
    paramsResult = sResult.split(".")
    if len(paramsResult) == 3:
        strTime = paramsResult[2] + paramsResult[1] + paramsResult[0]
        sOut = "t=" + strTime + "T0000&s=0000.00&fn=" + paramsResult[0] + "&i=0000&fp=" + sbar +  "&n=0"
        # sOut = "t=" + strTime + "T0000&s=0000.00&fn=" + paramsResult[0] + "&i=0000&fp=000000006&n=0"
        # t=20220422T1652&s=8582.00&fn=9960440301915601&i=2046&fp=100861626&n=1
        return sOut
    return ""

def findPlaceDate(sTest, key):
    # text_file = open("Output.txt", "w")
    for strIndex in range(len(sTest)):
        strT = sTest[strIndex]
        coff = fuzz.partial_token_sort_ratio(strT, key)

        # text_file.write(strT + "\n")

        if coff > 80:
            sResult = sTest[strIndex ]
            paramsResult = sResult.split(":")
            if len(paramsResult) >= 2:
                paramsTime = paramsResult[1].split()
                if len(paramsTime) >= 1:
                    return paramsTime[0]

    return ""

def findPlaceText(sTest, key):
    for strIndex in range(len(sTest)):
        str = sTest[strIndex]
        coff = fuzz.partial_token_sort_ratio(str, key)
        # coff = fuzz.partial_token_set_ratio(str, key)
        if coff > 80:
            sResult = sTest[strIndex + 1]
            paramsResult = sResult.split()
            if len(paramsResult) > 3:
                if len(paramsResult[1]) < 3:
                    return paramsResult[0] + " " + paramsResult[2]
                return paramsResult[0] + " " + paramsResult[1]
    return ""


def findEyeText(sTest, key):
    for strIndex in range(len(sTest)):
        str = sTest[strIndex]
        coff = fuzz.partial_token_sort_ratio(str, key)
        # coff = fuzz.partial_token_set_ratio(str, key)
        if coff > 80:
            sResult = sTest[strIndex]
            return sResult
    return ""


def findEye(sTest):
    for strIndex in range(len(sTest)):
        str = sTest[strIndex]
        coff0 = fuzz.partial_token_sort_ratio(str, "эль")
        coff1 = fuzz.partial_token_sort_ratio(str, "эпь")
        if coff0 > 80 or coff1 > 80:
            sResult = findEyeText(sTest, "товарный")
            paramsResult = sResult.split()
            if len(paramsResult) > 5:
                return paramsResult[3] + " " + paramsResult[5]
    return ""


def extractFromText(sTest, rusKey, nameFile):
    # находим слово документ
    sEye = findEye(sTest)
    if sEye != "":
        return sEye
    else:
        sResult = findPlaceText(sTest, "документ")
        return sResult
    return ""

    # sBase = sTest
    # coffStart0 = fuzz.partial_token_sort_ratio(sBase, "Итого")
    # coffStart1 = fuzz.partial_token_set_ratio(sBase, "Итого")
    # coffStart2 = fuzz.partial_token_set_ratio(sBase, "итого")
    #
    # coff2 = fuzz.partial_token_sort_ratio(sBase, "документ")
    # coff3 = fuzz.partial_token_sort_ratio(sBase, "Товарный чек")
    #
    # coff0 = fuzz.token_set_ratio(sBase, "документ")
    # coff1 = fuzz.token_set_ratio(sBase, "Товарный чек №")
    # coff14 = fuzz.token_set_ratio(sBase, "товарный чек")
    # coff15 = fuzz.token_sort_ratio(sBase, "Товарный чек №")
    #
    # coff4 = fuzz.ratio(sBase, "Товарный чек №")
    # coff5 = fuzz.partial_ratio(sBase, "Товарный чек №")
    # coff6 = fuzz.ratio(sBase, "Товарный чек №")
    # coff7 = fuzz.token_set_ratio(sBase, "Товарный чек №")
    # coff8 = fuzz.token_sort_ratio(sBase, "Товарный чек №")
    #
    # coff9 = fuzz.WRatio(sBase, "Товарный чек №")
    # coff10 = fuzz.WRatio(sBase, "документ")
    # coff11 = fuzz.WRatio(sBase, "Товарный чек")
    # coff12 = fuzz.WRatio(sBase, "товарный чек ")
    # if coff2 > 90:
    #     return "ggg"
    # if coff1 >70 and coff2 < 60:
    #     return "ggg"
    # return "ttt"


def calkFuzz(sTest, sTemplate):
    if len(sTest) < 5:
        return 0
    # z2 = fuzz.token_sort_ratio(sTest, sTemplate)
    # z4 = fuzz.WRatio(sTest, sTemplate)

    a4 = fuzz.partial_ratio(sTest, sTemplate)
    return a4


def testText(rusKey, strokeRus, maxWord1):
    findedCmd = rusKey.find("_ ")
    if (findedCmd == 0):
        rusKey = rusKey[2:]
        strokeKey = rusKey.split(" ")
        maxWordKey = []
        for numberKey in range(len(strokeKey)):
            maxWordTemp = 0;
            testKey = strokeKey[numberKey]
            for number in range(len(strokeRus)):
                testStr = strokeRus[number]
                a1 = calkFuzz(testStr.lower(), testKey.lower())
                if a1 > maxWordTemp:
                    maxWordTemp = a1
            maxWordKey.append(maxWordTemp)

        maxWord = 40;
        for numberMax in range(len(maxWordKey)):
            maxKey = maxWordKey[numberMax]
            if maxKey > maxWord:
                maxWord = maxKey
            if maxKey < maxWord1:
                maxWord = maxWord1
                break
        maxWord1 = maxWord
        return maxWord1
    else:
        for number in range(len(strokeRus)):
            testStr = strokeRus[number]
            a1 = calkFuzz(testStr.lower(), rusKey.lower())
            if a1 > maxWord1:
                maxWord1 = a1
        return maxWord1
    return 0


def decodeImage(nameImage, modeS=-1):
    result = []
    mode = int(modeS)
    rusKey = ''
    rusKeyApp0 = ''
    engKey = ''
    # mtc
    if mode == decodeQRMode.MTC:
        rusKey = 'РусскаяТелефоннаяк'
        engKey = 'ArmorJack'
    # вымпелком
    if mode == decodeQRMode.Vimpel:
        rusKey = 'Вымпелком услуга аппаратная пленка'
    # mvideo
    if mode == decodeQRMode.MVideo:
        rusKey = '_ МВМ накл плёнки'
        rusKeyApp0 = '_ МВМ ИНСИТЕХ'
        # rusKeyApp0 = 'МВМ услуги изготовлению наклейке пленки'
    if mode == decodeQRMode.MegaFon:
        rusKey = 'Мегафон'
        engKey = 'ArmorJack'
    if mode == decodeQRMode.Paper:
        rusKey = 'Изготовление+наклейка'

    timeStart = time.time()
    img = Image.open(nameImage)

    # обнаружить и декодировать
    imgZ2 = cv2.imread(nameImage)

    # detector = cv2.QRCodeDetector()
    # data, bbox, straight_qrcode = detector.detectAndDecode(imgZ2)
    qrcode_detector = cv2.wechat_qrcode_WeChatQRCode(
        "model/detect.prototxt",
        "model/detect.caffemodel",
        "model/sr.prototxt",
        "model/sr.caffemodel",
    )
    # imgZ2 = cv2.rotate(imgZ2, cv2.ROTATE_90_CLOCKWISE)
    # imgZ2 = cv2.rotate(imgZ2, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # grayExt = cv2.threshold(grayExt, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # grayExt = cv2.medianBlur(grayExt, 3)
    decoded_objects = qrcode_detector.detectAndDecode(imgZ2)

    # result = qrcode_detector.detectAndDecode(imgZ2)
    # res, points = detector.detectAndDecode(imgZ2)
    # res = detector.detectAndDecode(imgZ2)

    messageQR = 'не декодирован';
    # decoded_objects1 = decode(img)
    # lenObject = len(decoded_objects1)
    lenObject = len(decoded_objects[0])
    if lenObject == 0:
        grayExt = cv2.cvtColor(imgZ2, cv2.COLOR_BGR2GRAY)
        # grayExt = cv2.threshold(grayExt, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # clahe = cv2.createCLAHE(clipLimit=1.2, tileGridSize=(8, 8))
        clahe = cv2.createCLAHE(clipLimit=1.2, tileGridSize=(8, 8))
        equalized = clahe.apply(grayExt)
        decoded_objects = qrcode_detector.detectAndDecode(equalized)
    lenObject = len(decoded_objects[0])

    # --------------------------------------------------------------------------
    # если lenObject == 0 значит QR код не найден и возможно  это некассовый чек
    if lenObject == 0:
        barcodes = pyzbar.decode(imgZ2)
        if len(barcodes) != 0:
            # gray = prepareImagheForTextDecode(imgZ2, 1.2, 0, False, False, False)
            # grayUpd = prepareImagheForTextDecode(imgZ2, 1.2, 0, True, True, True)
            grayUpd = prepareImagheForTextDecode(imgZ2, -1.1, 80, True, True, True)
            # gray = prepareImagheForTextDecode(imgZ2, 1.8, 10, first, first, first)
            # cv2.imwrite("F:/photos/checksPhones0/zz.png", gray)
            # cv2.imwrite("zzUpd.png", grayUpd)

            # textRus = pytesseract.image_to_string(gray, lang="rus")
            textRusUpd = pytesseract.image_to_string(grayUpd, lang="rus", config='--psm 6')
            # ocr_result = pytesseract.image_to_string(gray, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
            # ocr_result = pytesseract.image_to_string(gray, lang='eng', config="-c tessedit_char_whitelist=0123456789")
            # strokeRus = textRus.split("\n")
            # checkInfo = createQRcodeFromPhone(strokeRus)

            strokeRusUpd = textRusUpd.split("\n")
            checkInfo = createQRcodeFromPhone(strokeRusUpd, barcodes[0][0])

            # text_file = open("Output.txt", "w")
            # text_file.write(textRusUpd)
            # text_file.close()

            # videoCheck = 50
            # videoCheck = testText(".видео", strokeRus, videoCheck)
            maxWordCheck = 50
            # if videoCheck > 70:
            maxWordCheck = testText("Изгот.+наклейка", strokeRusUpd, maxWordCheck)

            if checkInfo == "":
               checkInfo = messageQR
            result.append(checkInfo)
            result.append(f"text {maxWordCheck}")
            print(result[0])
            print(result[1])
            return result

        first = True
        # gray = prepareImagheForTextDecode(imgZ2, 1.8, 10, False,False,False)
        # gray = prepareImagheForTextDecode(imgZ2, 1.8, 10, True,True,True)
        checkInfo = ""
        for i in range(2):
            gray = prepareImagheForTextDecode(imgZ2, 1.8, 10, first, first, first)

            textRus = pytesseract.image_to_string(gray, lang="rus", config='--psm 4')
            strokeRus = textRus.split("\n")
            checkInfo = extractFromText(strokeRus, rusKey, nameImage)
            checkInfo = createQRcode(checkInfo)

            textRusUpd = pytesseract.image_to_string(gray, lang="rus",config='--psm 6')
            strokeRusUpd = textRusUpd.split("\n")
            checkInfoUpd = extractFromText(strokeRusUpd, rusKey, nameImage)
            checkInfoUpd = createQRcode(checkInfoUpd)
            if checkInfo == "":
                checkInfo = checkInfoUpd
                
            maxWordCheck = 77
            maxWordCheck = testText("Изготовление+наклейка", strokeRus, maxWordCheck)

            if checkInfo != "":
                break
            else:
                first = False if first==True else True

        if checkInfo == "":
            checkInfo = messageQR
        result.append(checkInfo)
        result.append(f"text {maxWordCheck}")
        print(result[0])
        print(result[1])
        return result

    if lenObject != 0:
        # qrcode = decoded_objects1[0].data.decode("utf-8")
        qrcode = decoded_objects[0][0]
        if lenObject == 2:
            qrcode0 = decoded_objects[0][0]
            qrcode1 = decoded_objects[0][1]
            if "t=" in qrcode0:
                qrcode = qrcode0
            if "t=" in qrcode1:
                qrcode = qrcode1
        if mode >= 0:
            substring = "t="
            if substring in qrcode:
                messageQR = qrcode
        else:
            messageQR = qrcode

    result.append(messageQR)

    gray = cv2.cvtColor(imgZ2, cv2.COLOR_BGR2GRAY)
    if rusKey != "":
        textRus = pytesseract.image_to_string(gray, lang="rus")
        strokeRus = textRus.split("\n")

    if engKey != "":
        textEng = pytesseract.image_to_string(gray, lang="eng")
        strokeEng = textEng.split("\n")

    maxWord1 = 40
    if rusKey != "":
        maxWord1_0 = testText(rusKey, strokeRus, maxWord1)
        maxWord1_1 = testText(rusKeyApp0, strokeRus, maxWord1)
        maxWord1 = max(maxWord1_0, maxWord1_1)

    maxWord0 = 40
    if engKey != "":
        for number in range(len(strokeEng)):
            testStr = strokeEng[number]
            a0 = calkFuzz(testStr, engKey)
            if a0 > maxWord0:
                maxWord0 = a0

    if mode == 0:
        result.append(f"text {min(maxWord0, maxWord1)}")
    if mode == 1:
        result.append(f"text {maxWord1}")
    if mode == 2:
        result.append(f"text {maxWord1}")
    if mode == 3:
        result.append(f"text {min(maxWord0, maxWord1)}")
    if mode == 4:
        result.append(f"text {maxWord1}")

    timeEnd = time.time()
    for res in result:
        print(res)
    return result


if __name__ == "__main__":
    nameImg = sys.argv[1]
    extractText = sys.argv[2]
    decodeImage(nameImg, extractText)
    # decodeImage('ok.jpg', -2)
    # decodeImage('ok1.jpg', 0)

