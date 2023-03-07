import requests
import re
# import time
#
# cur_time = time.time()


# 887919045


def PriceNow(symbol):
    link = f"https://api.binance.com/api/v3/ticker/price?symbol=" + symbol  # получаем данные
    responce = requests.get(link).text
    PriceNow = re.sub(r'[^0-9.]+', r'', responce)

    return PriceNow


def Ticker_24h(symbol):
    link = f"https://api.binance.com/api/v1/ticker/24hr?symbol=" + symbol  # получаем данные
    responce = requests.get(link).text  # превращаем в текст
    responce = responce.split(',')  # разбиваем на список по запятым
    responce = responce[3]  # оставляем только то что нам нужно
    Ticker_24h = re.sub(r'[^0-9.]+', r'', responce)

    return Ticker_24h


def PriceChangePercent(symbol):
    link = f"https://api.binance.com/api/v1/ticker/24hr?symbol=" + symbol  # получаем данные
    responce = requests.get(link).text  # превращаем в текст
    responce = responce.split(',')  # разбиваем на список по запятым
    responce = responce[2]  # оставляем только то что нам нужно
    PriceChangePercent = re.sub(r'[^0-9.-]+', r'', responce)

    return PriceChangePercent


def LowPrice(symbol):
    link = f"https://api.binance.com/api/v1/ticker/24hr?symbol=" + symbol  # получаем данные
    responce = requests.get(link).text  # превращаем в текст
    responce = responce.split(',')  # разбиваем на список по запятым
    responce = responce[13]  # оставляем только то что нам нужно
    LowPrice = re.sub(r'[^0-9.-]+', r'', responce)

    return LowPrice


def HightPrice(symbol):
    link = f"https://api.binance.com/api/v1/ticker/24hr?symbol=" + symbol  # получаем данные
    responce = requests.get(link).text  # превращаем в текст
    responce = responce.split(',')  # разбиваем на список по запятым
    responce = responce[13]  # оставляем только то что нам нужно
    HightPrice = re.sub(r'[^0-9.-]+', r'', responce)

    return HightPrice


def notification(symbol):
    def MakeMessage(symbol):
        s = len(symbol)
        coin = symbol[:s - 4]
        Message = f'[coin: [-{coin}-]]\n[Изменение за 24ч: {PriceChangePercent(symbol)}%]\n[Цена в данный момент:' \
                  f' {PriceNow(symbol)}$]\n[Средняя цена 1-й монеты за последние 24ч: {Ticker_24h(symbol)}$] '
        return Message

    bot_token = '5270460126:AAFqNoaIwTW_cRVRP068CeEjMHElNfs41s0'  # bot_token
    file = open('chat.txt', 'r')
    chatID = file.read()  # chatID

    def telegram_bot_sendtext(bot_token, chatID, message):
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chatID}&parse_mode=Markdown&text={message}"
        response = requests.get(url)
        return response.json()

    telegram_bot_sendtext(bot_token, chatID, MakeMessage(symbol))


def notificationLOW(symbol):
    def MakeMessage(symbol):
        s = len(symbol)
        coin = symbol[:s - 4]
        Message = f'[ПАДЕНИЕ К МИНИМУМУ! - [-{coin}-]]\n[Цена в данный момент:' \
                  f' {PriceNow(symbol)}$]\n[Средняя цена 1-й монеты за последние 24ч: {Ticker_24h(symbol)}$] '
        return Message

    bot_token = '5270460126:AAFqNoaIwTW_cRVRP068CeEjMHElNfs41s0'  # bot_token
    file = open('chat.txt', 'r')
    chatID = file.read()  # chatID

    def telegram_bot_sendtext(bot_token, chatID, message):
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chatID}&parse_mode=Markdown&text={message}"
        response = requests.get(url)
        return response.json()

    telegram_bot_sendtext(bot_token, chatID, MakeMessage(symbol))


def notificationHIGHT(symbol):
    def MakeMessage(symbol):
        s = len(symbol)
        coin = symbol[:s - 4]
        Message = f'[ПРИБЛИЖЕНИЕ К МАКСИМУМУ! - [-{coin}-]]\n[Цена в данный момент:' \
                  f' {PriceNow(symbol)}$]\n[Средняя цена 1-й монеты за последние 24ч: {Ticker_24h(symbol)}$] '
        return Message

    bot_token = '5270460126:AAFqNoaIwTW_cRVRP068CeEjMHElNfs41s0'  # bot_token
    file = open('chat.txt', 'r')
    chatID = file.read()  # chatID

    def telegram_bot_sendtext(bot_token, chatID, message):
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chatID}&parse_mode=Markdown&text={message}"
        response = requests.get(url)
        return response.json()

    telegram_bot_sendtext(bot_token, chatID, MakeMessage(symbol))


file = open('symbols.txt', 'r')
symbol = file.read()
symbol = symbol.split('\n')
x = len(symbol)
file.close()

# объевляем массив
temp = [0] * x
for i in range(x):
    temp[i] = [0] * 5

x1 = 0
while True:

    if x1 <= x:

        PN = float(PriceNow(symbol[x1]))
        T24 = float(Ticker_24h(symbol[x1]))
        PCP = float(PriceChangePercent(symbol[x1]))
        LP = float(LowPrice(symbol[x1]))
        HP = float(HightPrice(symbol[x1]))
        PNL = PN - (PN / 100) * 1.5
        PNH = PN + (PN / 100) * 1.5

        if temp[x1][0] == 0:
            if LP >= PNL:
                notificationLOW(symbol[x1])
                temp[x1][0] = 1
        elif PN > LP + (LP / 100) * 3:
            temp[x1][0] = 0
            ###
        if temp[x1][1] == 0:
            if PCP <= -10:
                notification(symbol[x1])
                temp[x1][1] = 1
        elif PCP >= -9:
            temp[x1][1] = 0
            ###
        if temp[x1][3] == 0:
            if PCP >= 10:
                notification(symbol[x1])
                temp[x1][3] = 1
        elif PCP + 1 <= 10:
            temp[x1][3] = 0
            ###
        if temp[x1][4] == 0:
            if HP <= PNH:
                notificationHIGHT(symbol[x1])
                temp[x1][4] = 1
        elif HP > PN + (PN / 100) * 3:
            temp[x1][4] = 0

    if x1 < x:
        x1 += 1
        if x1 == x:
            x1 = 0
    # print(time.time() - cur_time)
