import datetime
import random
import json
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token="f185453c27991cca4fbe371bd01f7d8c8239fd880b01e883de98a9b683df59772bdbdb00c632e75764e3f")
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

joke_list = []
joke = open("files\jokes.txt", 'r', encoding="utf-8")
for line in joke:
    joke_list.append(str(line))

legend_list = []
legend = open("files\legends.txt", 'r', encoding="utf-8")
for line in legend:
    legend_list.append(str(line))

songs = ["audio-212274851_456239018", 'audio-212274851_456239019', 'audio-212274851_456239020']


def construct(id):
    p = {}
    p["name"] = id
    p["hp"] = 100
    p["rad"] = 0
    p["pwr"] = 10
    p["money"] = 0
    p["wpn"] = 'Fist'
    p["suit"] = 'None'
    p["ammo"] = 0
    p["act"] = 'None'
    p["act_time"] = 0
    p["loc"] = 'Cordon'
    data[str(id)] = p


def top():
    lst = []
    for i in data:
        lst.append((data[i]["name"], int(data[i]["money"])))
    lst = sorted(lst, key=lambda x: x[1], reverse=True)
    lst = lst[:10]
    return lst


def send_message(id, text, attachment):
    vk_session.method('messages.send', {'user_id': id, 'message': text, "attachment": attachment, 'random_id': 0})


def loadbd():
    file = open("files\data.txt", "r+", encoding='utf-8')
    datas = file.read()
    datas = datas.splitlines()
    file.close()
    data = {}
    for i in datas:
        i = i.split('#')
        data[str(i[0])] = {}
        data[str(i[0])]["name"] = i[1]
        data[str(i[0])]["hp"] = i[2]
        data[str(i[0])]["rad"] = i[3]
        data[str(i[0])]["pwr"] = i[4]
        data[str(i[0])]["money"] = i[5]
        data[str(i[0])]["wpn"] = i[6]
        data[str(i[0])]["suit"] = i[7]
        data[str(i[0])]["ammo"] = i[8]
        data[str(i[0])]["act"] = i[9]
        data[str(i[0])]["act_time"] = i[10]
        data[str(i[0])]["loc"] = i[11]
    return data


def savebd():
    with open("files\data.txt", "w", encoding='utf-8') as file:
        for i in data:
            p = str(i) + "#" + str(data[i]["name"]) + "#" + str(data[i]["hp"]) + "#" + str(data[i]["rad"]) + "#" \
                + str(data[i]["pwr"]) + "#" + str(data[i]["money"]) + "#" + \
                str(data[i]["wpn"]) + "#" + str(data[i]["suit"]) + "#" + str(data[i]["ammo"]) + "#" + \
                str(data[i]["act"]) + "#" + str(data[i]["act_time"]) + "#" + str(data[i]["loc"])
            file.write(p + '\n')


def get_but(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


trade_keyboard = {
    "one_time": False,
    "buttons": [
        [get_but('Оружие', 'positive'), get_but('Расходники', 'positive'), get_but('Бронежилеты', 'positive')],
        [get_but('Уйти', 'positive')]
    ]
}
trade_keyboard = json.dumps(trade_keyboard, ensure_ascii=False).encode('utf-8')
trade_keyboard = str(trade_keyboard.decode('utf-8'))

bar_keyboard = {
    "one_time": False,
    "buttons": [
        [get_but('Оружие', 'positive'), get_but('Расходники', 'positive'), get_but('Бронежилеты', 'positive')],
        [get_but('Казино', 'primary')],
        [get_but('Уйти', 'positive')]
    ]
}
bar_keyboard = json.dumps(bar_keyboard, ensure_ascii=False).encode('utf-8')
bar_keyboard = str(bar_keyboard.decode('utf-8'))

back_keyboard = {
    "one_time": False,
    "buttons": [
        [get_but('Вернуться', 'negative')]
    ]
}
back_keyboard = json.dumps(back_keyboard, ensure_ascii=False).encode('utf-8')
back_keyboard = str(back_keyboard.decode('utf-8'))

explore_keyboard = {
    "one_time": False,
    "buttons": [
        [get_but('Состояние вылазки', 'positive')],
        # [get_but('Свернуть с проверенного маршурута', 'negative')],
        [get_but('Вернуться в лагерь', 'positive')]
    ]
}
explore_keyboard = json.dumps(explore_keyboard, ensure_ascii=False).encode('utf-8')
explore_keyboard = str(explore_keyboard.decode('utf-8'))

sleep_keyboard = {
    "one_time": False,
    "buttons": [
        [get_but('Проснуться', 'primary')],
    ]
}
sleep_keyboard = json.dumps(sleep_keyboard, ensure_ascii=False).encode('utf-8')
sleep_keyboard = str(sleep_keyboard.decode('utf-8'))

main_keyboard = {
    "one_time": False,
    "buttons": [
        [get_but('Отправиться в вылазку', 'negative'), get_but('Отправиться в другой лагерь', 'negative')],
        [get_but('Торговец', 'positive'), get_but('Костёр', 'positive')],
        [get_but('Профиль', 'positive'), get_but('Лидеры', 'positive')],
        [get_but("Спать", 'primary')],
        [get_but("Обучение", 'primary')]
    ]
}
main_keyboard = json.dumps(main_keyboard, ensure_ascii=False).encode('utf-8')
main_keyboard = str(main_keyboard.decode('utf-8'))

campfire_keyboard = {
    "one_time": False,
    "buttons": [
        [get_but('Продолжать слушать', 'primary')],
        [get_but('Уйти', 'secondary')]
    ]
}
campfire_keyboard = json.dumps(campfire_keyboard, ensure_ascii=False).encode('utf-8')
campfire_keyboard = str(campfire_keyboard.decode('utf-8'))

data = loadbd()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            message = event.text.lower()
            message_split = event.text.split()
            id = event.user_id
            # проверка авторизации
            n = 0
            for i in data:
                if str(id) == i:
                    n = 1
            if n == 0:
                construct(id)
            # читаем сообщения
            if message == 'начать':
                vk_session.method('messages.send', {'user_id': id, 'message': 'Советуем ознакомиться с обучением',
                                                    'random_id': 0, 'keyboard': main_keyboard})
            # часть кода отвечающая за вылазки
            elif message == 'отправиться в вылазку':
                if int(data[str(id)]['pwr']) <= 0:
                    vk_session.method('messages.send', {'user_id': id,
                                                        'message': '"Не могу... Глаза слипаются"\nНеобходимо'
                                                                   ' пополнить энергию',
                                                        'random_id': 0, 'keyboard': main_keyboard})
                else:
                    if int(data[str(id)]['ammo']) < 60:
                        send_message(id, "'Мда, маслят будет маловато'\nСлишком ало боеприпасов, бонус от оружия не"
                                         " учитывается", None)
                    vk_session.method('messages.send', {'user_id': id,
                                                        'message': 'Вот доступные вылазки:\n1. Охота на мутантов'
                                                                   '\n2. Рейд на лагерь бандитов'
                                                                   '\n3. Охота на артефакты',
                                                        'random_id': 0, 'keyboard': back_keyboard})
                    data[str(id)]['act'] = 'Explore_chose'
            elif message == 'вернуться' and data[str(id)]['act'] == 'Explore_chose':
                vk_session.method('messages.send', {'user_id': id, 'message': 'Отмена вылазки',
                                                    'random_id': 0, 'keyboard': main_keyboard})
            elif (message == '1' or message == '2' or message == '3') and data[str(id)]['act'] == 'Explore_chose':
                if message == '1':
                    data[str(id)]['rad'] = int(data[str(id)]['rad']) + random.randint(0, 10)
                    data[str(id)]['hp'] = (int(data[str(id)]['hp']) - int(data[str(id)]['rad'])) - random.randint(0, 70)
                elif message == '2':
                    data[str(id)]['rad'] = int(data[str(id)]['rad']) + random.randint(0, 10)
                    data[str(id)]['hp'] = (int(data[str(id)]['hp']) - int(data[str(id)]['rad'])) - random.randint(0, 60)
                elif message == '3':
                    data[str(id)]['rad'] = int(data[str(id)]['rad']) + random.randint(0, 30)
                    data[str(id)]['hp'] = (int(data[str(id)]['hp']) - int(data[str(id)]['rad'])) - random.randint(0, 30)
                vk_session.method('messages.send', {'user_id': id, 'message': 'Ну чтож, в путь!',
                                                    'random_id': 0, 'keyboard': explore_keyboard})
                end_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
                data[str(id)]['act_time'] = end_time
                data[str(id)]['act'] = 'Explore'
            elif message == 'состояние вылазки' and data[str(id)]['act'] == 'Explore':
                if data[str(id)]["act_time"] > datetime.datetime.now():
                    send_message(id, f'Осталось {data[str(id)]["act_time"] - datetime.datetime.now()} времени', None)
                else:
                    if int(data[str(id)]["hp"]) < 1:
                        vk_session.method('messages.send', {'user_id': id, 'message': 'Вы потеряли сознание во время'
                                                                                      ' вылазки. \nВас вернули в лагерь'
                                                                                      ' но марадёры забрали 40% от '
                                                                                      'ваших денег',
                                                            'random_id': 0, 'keyboard': main_keyboard})
                        data[str(id)]['money'] = int(data[str(id)]['money']) * 0.30
                        data[str(id)]['hp'] = 1
                    else:
                        vk_session.method('messages.send', {'user_id': id, 'message': 'Вылазка завершена',
                                                            'random_id': 0, 'keyboard': main_keyboard})

                        data[str(id)]['money'] = int(data[str(id)]['money']) + 1350
                    data[str(id)]['pwr'] = int(data[str(id)]['pwr']) - 2
                    data[str(id)]['act_time'] = 0
                    data[str(id)]['act'] = 'None'
                    savebd()
            elif message == 'вернуться в лагерь' and data[str(id)]['act'] == 'Explore':
                vk_session.method('messages.send', {'user_id': id, 'message': 'Вылазка отменена',
                                                    'random_id': 0, 'keyboard': main_keyboard})
                data[str(id)]['act'] = 'None'
            elif message == 'отправиться в другой лагерь':
                vk_session.method('messages.send',
                                  {'user_id': id, 'message': 'Тропы в другие лагеря ещё не исследованы',
                                   'random_id': 0, 'keyboard': main_keyboard})
            # часть кода отвечающая за торговлю
            elif message == 'торговец' and data[str(id)]['act'] == 'None':
                data[str(id)]['act'] = 'Trade'
                if data[str(id)]["loc"] == 'Cordon':
                    msg = 'Войдя в подвал и открыв железную дверь вы видете торговца.\n- Ну, здарова.'
                vk_session.method('messages.send', {'user_id': id,
                                                    'message': msg,
                                                    'random_id': 0, 'keyboard': trade_keyboard})
            elif message == 'оружие' and data[str(id)]['act'] == 'Trade':
                vk_session.method('messages.send', {'user_id': id, 'message': 'Вот такие стволы в ассортименте:'
                                                                              '\n1. ПМ - 280 руб.\n2. Обрез - 400 руб.'
                                                                              '\n3. Гадюка - 1100 руб.\n4. АКС-74/2У - '
                                                                              '3000 руб.\n5. СВД - 16000 руб.',
                                                    'random_id': 0, 'keyboard': back_keyboard})
                data[str(id)]['act'] = 'Trade_wpn'
            elif message == '1' and data[str(id)]['act'] == 'Trade_wpn':
                if data[str(id)]['money'] < 280:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 280
                    data[str(id)]['wpn'] = 'ПМ'
                    send_message(id, 'Поздравляем с покупкой ПМ', None)
                    savebd()
            elif message == '2' and data[str(id)]['act'] == 'Trade_wpn':
                if data[str(id)]['money'] < 400:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 400
                    data[str(id)]['wpn'] = 'Обрез'
                    send_message(id, 'Поздравляем с покупкой обреза', None)
                    savebd()
            elif message == '3' and data[str(id)]['act'] == 'Trade_wpn':
                if data[str(id)]['money'] < 1100:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 1100
                    data[str(id)]['wpn'] = 'Гадюка'
                    send_message(id, 'Поздравляем с покупкой Гадюки', None)
                    savebd()
            elif message == '4' and data[str(id)]['act'] == 'Trade_wpn':
                if data[str(id)]['money'] < 3000:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 3000
                    data[str(id)]['wpn'] = 'АКС-74/2У'
                    send_message(id, 'Поздравляем с покупкой АКС-74/2У', None)
                    savebd()
            elif message == '5' and data[str(id)]['act'] == 'Trade_wpn':
                if data[str(id)]['money'] < 16000:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 16000
                    data[str(id)]['wpn'] = 'СВД'
                    send_message(id, 'Поздравляем с покупкой СВД', None)
                    savebd()
            elif message == 'бронежилеты' and data[str(id)]['act'] == 'Trade':
                vk_session.method('messages.send', {'user_id': id, 'message': "Вот такие жилеты в ассортименте:\n"
                                                                              "1. Кожаная куртка - 1000 руб.\n2. Заря -"
                                                                              " 5000 руб. \n3. Берилл-5М - 12500 руб."
                                                                              "\n4. ССП-99 'Эколог' - 24000 руб.\n5. "
                                                                              "СЕВА - 30000 руб.\n6. Экзоскелет - 60000"
                                                                              " руб.",
                                                    'random_id': 0, 'keyboard': back_keyboard})
                data[str(id)]['act'] = 'Trade_suit'
            elif message == '1' and data[str(id)]['act'] == 'Trade_suit':
                if data[str(id)]['money'] < 1000:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 1000
                    data[str(id)]['suit'] = 'Кожаная куртка'
                    send_message(id, 'Поздравляем с покупкой кожаной куртки', None)
                    savebd()
            elif message == '2' and data[str(id)]['act'] == 'Trade_suit':
                if data[str(id)]['money'] < 5000:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 5000
                    data[str(id)]['suit'] = 'Заря'
                    send_message(id, 'Поздравляем с покупкой Зари', None)
                    savebd()
            elif message == '3' and data[str(id)]['act'] == 'Trade_suit':
                if data[str(id)]['money'] < 12500:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 12500
                    data[str(id)]['suit'] = 'Берилл-5М'
                    send_message(id, 'Поздравляем с покупкой Берилла-5М', None)
                    savebd()
            elif message == '4' and data[str(id)]['act'] == 'Trade_suit':
                if data[str(id)]['money'] < 24000:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 24000
                    data[str(id)]['suit'] = "ССП-99 'Эколог'"
                    send_message(id, 'Поздравляем с покупкой ССП-99 "Эколог"', None)
                    savebd()
            elif message == '5' and data[str(id)]['act'] == 'Trade_suit':
                if data[str(id)]['money'] < 30000:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 30000
                    data[str(id)]['suit'] = 'СЕВА'
                    send_message(id, 'Поздравляем с покупкой СЕВЫ', None)
                    savebd()
            elif message == '6' and data[str(id)]['act'] == 'Trade_suit':
                if data[str(id)]['money'] < 60000:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 60000
                    data[str(id)]['suit'] = 'Экзоскелет'
                    send_message(id, 'Поздравляем с покупкой экзоскелета', None)
                    savebd()
            elif message == 'расходники' and data[str(id)]['act'] == 'Trade':
                vk_session.method('messages.send', {'user_id': id, 'message': "Вот такие предметы в ассортименте:\n"
                                                                              '1. Консерва - 200 руб.\n2. Антирад - 600'
                                                                              ' руб.\n3. Энергетик - 150 руб.\n4. '
                                                                              'Водка - 200 руб.\n5. Аптечка - 300 руб.'
                                                                              '\n6. Аптечка армейская - 650 руб.\n'
                                                                              '7. Аптечка научная - 1000 руб. \n8. '
                                                                              'Боеприпасы(x60) - 700 руб.',
                                                    'random_id': 0, 'keyboard': back_keyboard})
                data[str(id)]['act'] = 'Trade_misc'
            elif message == '1' and data[str(id)]['act'] == 'Trade_misc':
                if data[str(id)]['money'] < 200:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 200
                    if data[str(id)]['hp'] > 80:
                        pass
                    send_message(id, 'Вы купили и использовали консерву', None)
                    savebd()
            elif message == '2' and data[str(id)]['act'] == 'Trade_misc':
                if data[str(id)]['money'] < 600:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 600
                    if data[str(id)]['rad'] < 70:
                        data[str(id)]['rad'] = 0
                    else:
                        if int(data[str(id)]['rad']) > 70:
                            data[str(id)]['rad'] = int(data[str(id)]['rad']) - 70
                        else:
                            data[str(id)]['rad'] = 0
                    send_message(id, 'Вы купили и использовали антирад', None)
                    savebd()
            elif message == '3' and data[str(id)]['act'] == 'Trade_misc':
                if data[str(id)]['money'] < 150:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    send_message(id, 'Вы купили и использовали энергетик', None)
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 150
                    if data[str(id)]['pwr'] < 10:
                        data[str(id)]['pwr'] = int(data[str(id)]['pwr']) + 1
                    savebd()
            elif message == '4' and data[str(id)]['act'] == 'Trade_misc':
                if data[str(id)]['money'] < 200:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 200
                    send_message(id, 'Вы купили и использовали водку', None)
                    if int(data[str(id)]['rad']) > 30:
                        data[str(id)]['rad'] = int(data[str(id)]['rad']) - 30
                    else:
                        data[str(id)]['rad'] = 0
                    data[str(id)]['pwr'] = int(data[str(id)]['pwr']) - 1
                    savebd()
            elif message == '5' and data[str(id)]['act'] == 'Trade_misc':
                if data[str(id)]['money'] < 300:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 300
                    send_message(id, 'Вы купили и использовали аптечку', None)
                    if 100 - int(data[str(id)]['rad']) < int(data[str(id)]['hp']) + 30:
                        data[str(id)]['hp'] = 100 - int(data[str(id)]['rad'])
                    else:
                        data[str(id)]['hp'] = int(data[str(id)]['hp']) + 30
                    savebd()
            elif message == '6' and data[str(id)]['act'] == 'Trade_misc':
                if data[str(id)]['money'] < 650:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 650
                    send_message(id, 'Вы купили и использовали армейскую аптечку', None)
                    if 100 - int(data[str(id)]['rad']) < int(data[str(id)]['hp']) + 75:
                        data[str(id)]['hp'] = 100 - int(data[str(id)]['rad'])
                    else:
                        data[str(id)]['hp'] = int(data[str(id)]['hp']) + 75
                    if int(data[str(id)]['rad']) < 10:
                        data[str(id)]['rad'] = 0
                    else:
                        data[str(id)]['rad'] = int(data[str(id)]['rad']) - 10
                    savebd()
            elif message == '7' and data[str(id)]['act'] == 'Trade_misc':
                if data[str(id)]['money'] < 1000:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 1000
                    data[str(id)]['hp'] = 100
                    data[str(id)]['rad'] = 0
                    send_message(id, 'Вы купили и использовали аптечку научную', None)
                    savebd()
            elif message == '8' and data[str(id)]['act'] == 'Trade_misc':
                if data[str(id)]['money'] < 700:
                    send_message(id, 'Недостаточно денег', None)
                else:
                    data[str(id)]['money'] = int(data[str(id)]['money']) - 700
                    data[str(id)]['ammo'] = int(data[str(id)]['ammo']) + 60
                    send_message(id, 'Вы купили боеприпасы(x60)', None)
                    savebd()
            elif message == 'вернуться' and (data[str(id)]['act'] == 'Trade_wpn' or data[str(id)]['act']
                                             == 'Trade_suit' or data[str(id)]['act'] == 'Trade_misc'):
                vk_session.method('messages.send', {'user_id': id, 'message': "'Что интересует?'", 'random_id': 0,
                                                    'keyboard': trade_keyboard})
                data[str(id)]["act"] = 'Trade'
            elif message == 'уйти' and data[str(id)]['act'] == 'Trade':
                data[str(id)]["act"] = 'None'
                vk_session.method('messages.send', {'user_id': id,
                                                    'message': 'Вы ушли от торговца',
                                                    'random_id': 0, 'keyboard': main_keyboard})
            # часть кода отвечающая за костёр
            elif message == 'костёр' and data[str(id)]['act'] == 'None':
                data[str(id)]["act"] = "campf"
                campfire_act = random.randint(1, 3)
                if campfire_act == 1:
                    vk_session.method('messages.send', {'user_id': id,
                                                        'message': f'У костра сидит несколько '
                                                                   f'сталкеров и внимательно слушают другого:\n'
                                                                   f'{random.choice(joke_list)}',
                                                        'random_id': 0, 'keyboard': campfire_keyboard})
                elif campfire_act == 2:
                    vk_session.method('messages.send', {'user_id': id,
                                                        'message': f'У костра сидит несколько '
                                                                   f'сталкеров и внимательно слушают другого:\n'
                                                                   f'{random.choice(legend_list)}',
                                                        'random_id': 0, 'keyboard': campfire_keyboard})
                else:
                    vk_session.method('messages.send', {'user_id': id,
                                                        'message': f'У костра сидит несколько '
                                                                   f'сталкеров и внимательно слушают гитариста',
                                                        'random_id': 0, "attachment": random.choice(songs),
                                                        'keyboard': campfire_keyboard})
            elif message == 'продолжать слушать' and data[str(id)]["act"] == "campf":
                campfire_act = random.randint(1, 3)
                if campfire_act == 1:
                    vk_session.method('messages.send', {'user_id': id,
                                                        'message': f'{random.choice(joke_list)}',
                                                        'random_id': 0, 'keyboard': campfire_keyboard})
                elif campfire_act == 2:
                    send_message(id, f'{random.choice(legend_list)}', None)
                else:
                    send_message(id, f'Какой-то виртуоз исполняет на гитаре:\n', attachment=random.choice(songs))
            elif message == "уйти" and data[str(id)]["act"] == "campf":
                data[str(id)]["act"] = 'None'
                vk_session.method('messages.send', {'user_id': id, 'message': 'Вы отошли от костра',
                                                    'random_id': 0, 'keyboard': main_keyboard})
            # взаимодействие с контекстом(?)
            elif message_split[0].lower() == "ник":
                if len(message_split) == 1:
                    send_message(id, 'Неправильный формат ника', None)
                else:
                    data[str(id)]["name"] = message_split[1]
                    vk_session.method('messages.send', {'user_id': id, 'message': 'Ваш ник изменён', 'random_id': 0})
                    savebd()
            elif message == 'лидеры':
                msg = f'Топ Игроков\n №   Ник   Деньги\n'
                num1 = 1
                for i in top():
                    msg += f'№{num1} {i[0]}  {i[1]} .руб\n'
                    num1 += 1
                vk_session.method("messages.send",
                                  {"user_id": id,
                                   "message": msg,
                                   "random_id": 0})
            # часть кода ответственная за сон
            elif message == 'спать' and data[str(id)]["act"] == 'None':
                vk_session.method("messages.send",
                                  {"user_id": id,
                                   "message": 'Вы легли спать',
                                   "random_id": 0,
                                   "keyboard": sleep_keyboard})
                data[str(id)]["act"] = 'Sleep'
                data[str(id)]["act_time"] = datetime.datetime.now()
            elif message == 'проснуться' and data[str(id)]["act"] == 'Sleep':
                vk_session.method("messages.send", {"user_id": id,
                                                    "message": f'Вы проспали '
                                                               f'{datetime.datetime.now() - data[str(id)]["act_time"]}'
                                                               f' и восстановили '
                                                               f'{(datetime.datetime.now() - data[str(id)]["act_time"]).seconds // 1200} энергии',
                                                    "random_id": 0,
                                                    "keyboard": main_keyboard})
                if int(data[str(id)]["pwr"]) + (
                        (datetime.datetime.now() - data[str(id)]["act_time"]).seconds // 1200) > 10:
                    data[str(id)]["pwr"] = 10
                else:
                    data[str(id)]["pwr"] = int(data[str(id)]["pwr"]) + (
                                (datetime.datetime.now() - data[str(id)]["act_time"]).seconds // 1200)
                data[str(id)]["act"] = 'None'
                savebd()
            elif message == 'обучение':
                msg = 'Всё легко и просто:\n1. Ходите в вылазки и получайте деньги пока ноги держут\n' \
                      '2. Следите за заражением радиацией, чем больше заражение, тем меньше максимальное HP и больше' \
                      ' урона вы получаете за вылазку\n3. Если HP упадёт до 0, то ничего с персонажем не будет, правда' \
                      ' мародёры не прочь поживиться вашим хабаром\n4. Бегать по заданиям бесконечно вы не сможете,' \
                      ' поэтому вам надо восстановить силы у костра или поспать\n5. Не советую бежать до центра Зоны' \
                      ' в одной кожаной курточке, обзаведись хорошей защитой перед продвижением в глубь Зоны'
                send_message(id, msg, None)
            elif message == 'помощь':
                vk_session.method("messages.send", {"user_id": id, "message": 'Ник [желаемый ник]',
                                                    "random_id": 0, "keyboard": sleep_keyboard})
            elif message == 'профиль':
                msg = "Привет, " + str(data[str(id)]["name"]) + "\n"
                msg = msg + str(data[str(id)]["hp"]) + " HP\n"
                msg = msg + str(data[str(id)]["rad"]) + " радиации\n"
                msg = msg + str(data[str(id)]["money"]) + " руб."
                msg = msg + "\n" + str(data[str(id)]["pwr"]) + " из 10 энергии"
                msg = msg + "\n------------------"
                if data[str(id)]["loc"] == 'Cordon':
                    msg = msg + "\nВы на локации Кордон"
                # отображение оружия в профиле
                if data[str(id)]["wpn"] == 'Fist':
                    msg = msg + "\nОружие: Кулаки"
                elif data[str(id)]["wpn"] == 'ПМ':
                    msg = msg + "\nОружие: Пистолет Макарова"
                elif data[str(id)]["wpn"] == 'Обрез':
                    msg = msg + "\nОружие: Обрез"
                elif data[str(id)]["wpn"] == 'Гадюка':
                    msg = msg + "\nОружие: Гадюка"
                elif data[str(id)]["wpn"] == 'АКС-74/2У':
                    msg = msg + "\nОружие: АКС-74/2У"
                elif data[str(id)]["wpn"] == 'СВД':
                    msg = msg + "\nОружие: СВД"
                # отображение брони в профиле
                if data[str(id)]["suit"] == 'None':
                    msg = msg + "\nБроня: Отсутствует"
                elif data[str(id)]["suit"] == 'Кожаная куртка':
                    msg = msg + "\nБроня: Кожаная куртка"
                elif data[str(id)]["suit"] == 'Заря':
                    msg = msg + "\nБроня: Комбинезон Заря"
                elif data[str(id)]["suit"] == 'Берилл-5М':
                    msg = msg + "\nБроня: Берилл-5М"
                elif data[str(id)]["suit"] == "ССП-99 'Эколог'":
                    msg = msg + "\nБроня: ССП-99 'Эколог'"
                elif data[str(id)]["suit"] == "СЕВА":
                    msg = msg + "\nБроня: СЕВА"
                elif data[str(id)]["suit"] == "Экзоскелет":
                    msg = msg + "\nБроня: Экзоскелет"
                vk_session.method("messages.send", {"user_id": id, "message": msg, "random_id": 0})
            # промокод
            elif message == 'speedwagon':
                data[str(id)]["money"] = int(data[str(id)]["money"]) + 1000
            else:
                send_message(id, 'Неизвестная или неправильная команда', None)

