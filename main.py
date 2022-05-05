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
    p["lvl"] = 0
    p["wpn"] = 'Fist'
    p["suit"] = 'None'
    p["act"] = None
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
        i = i.split()
        data[str(i[0])] = {}
        data[str(i[0])]["name"] = i[1]
        data[str(i[0])]["hp"] = i[2]
        data[str(i[0])]["rad"] = i[3]
        data[str(i[0])]["pwr"] = i[4]
        data[str(i[0])]["money"] = i[5]
        data[str(i[0])]["lvl"] = i[6]
        data[str(i[0])]["wpn"] = i[7]
        data[str(i[0])]["suit"] = i[8]
        data[str(i[0])]["act"] = i[9]
        data[str(i[0])]["act_time"] = i[10]
        data[str(i[0])]["loc"] = i[11]
    return data


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
        [get_but('Отправиться в вылазку', 'positive'), get_but('Отправиться в другой лагерь', 'positive')],
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


def savebd():
    with open("files\data.txt", "w") as file:
        for i in data:
            p = str(i) + " " + str(data[i]["name"]) + " " + str(data[i]["hp"]) + " " + str(data[i]["rad"]) + " " \
                + str(data[i]["pwr"]) + " " + str(data[i]["money"]) + " " + str(data[i]["lvl"]) + " " + \
                str(data[i]["wpn"]) + " " + str(data[i]["suit"]) + " " + str(data[i]["act"]) + " " +\
                str(data[i]["act_time"]) + " " + str(data[i]["loc"])
            file.write(p + '\n')


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
                vk_session.method('messages.send', {'user_id': id,
                                                    'message': 'Вот доступные вылазки:\n1. Охота на мутантов'
                                                               '\n2. Рейд на лагерь бандитов'
                                                               '\n3. Охота на артефакты',
                                                    'random_id': 0, 'keyboard': main_keyboard})
            elif message == '1' or message == '2' or message == '3':
                vk_session.method('messages.send', {'user_id': id, 'message': 'Ну чтож, в путь!',
                                                    'random_id': 0, 'keyboard': explore_keyboard})
                end_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
                data[str(id)]['act_time'] = end_time
                data[str(id)]['act'] = 'Explore'
            elif message == 'состояние вылазки' and data[str(id)]['act'] == 'Explore':
                if data[str(id)]["act_time"] > datetime.datetime.now():
                    send_message(id, f'Осталось {data[str(id)]["act_time"] - datetime.datetime.now()} времени', None)
                else:
                    send_message(id, 'Вылазка завершена', None)
                    data[str(id)]['money'] = data[str(id)]['money'] + 1350
            elif message == 'вернуться в лагерь' and data[str(id)]['act'] == 'Explore':
                vk_session.method('messages.send', {'user_id': id, 'message': 'Вылазка отменена',
                                                    'random_id': 0, 'keyboard': main_keyboard})
                data[str(id)]['act'] = None
            elif message == 'Отправиться в другой лагерь':
                pass
            # часть кода отвечающая за торговлю
            elif message == 'торговец' and data[str(id)]['act'] is None:
                data[str(id)]['act'] = 'Trade'
                if data[str(id)]["loc"] == 'Cordon':
                    msg = 'Войдя в подвал и открыв железную дверь вы видете торговца.\n- Ну, здарова.'
                vk_session.method('messages.send', {'user_id': id,
                                                    'message': msg,
                                                    'random_id': 0, 'keyboard': trade_keyboard})
            elif message == 'оружие' and data[str(id)]['act'] == 'Trade':
                send_message(id, 'Вот такие стволы в ассортименте:\n1. ПМ - 280 руб.\n2. Обрез - 400 руб.\n'
                                 '3. Гадюка - 1100 руб.\n4. АКС-74/2У - 3000 руб.\n5. СВД - 16000 руб.\n'
                                 '6. РПГ-7у - 26000 руб.', None)
            elif message == 'бронежилеты' and data[str(id)]['act'] == 'Trade':
                send_message(id, "Вот такие жилеты в ассортименте:\n1. Кожаная куртка - 1000 руб.\n2. Заря - 5000 руб."
                                 "\n3. Берилл-5М - 12500 руб.\n4. ССП-99 'Эколог' - 24000 руб.\n5. СЕВА - 30000 руб.\n"
                                 "6. Экзоскелет - 60000 руб.", None)
            elif message == 'расходники' and data[str(id)]['act'] == 'Trade':
                send_message(id, 'Вот такие предметы в ассортименте:\n 1. Консерва - 200 руб.\n2. Антирад - 600 руб.\n'
                                 '3. Энергетик - 150 руб.\n4. Водка - 200 руб.\n5. Аптечка - 300 руб.\n'
                                 '6. Аптечка армейская - 650 руб.\n7.Аптечка научная - 1000 руб.', None)
            elif message == 'уйти' and data[str(id)]['act'] == 'Trade':
                data[str(id)]["act"] = None
                vk_session.method('messages.send', {'user_id': id,
                                                    'message': 'Вы отошли от торговца',
                                                    'random_id': 0, 'keyboard': main_keyboard})
            # часть кода отвечающая за костёр
            elif message == 'костёр' and data[str(id)]['act'] is None:
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
                data[str(id)]["act"] = None
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
                                  {"peer_id": id,
                                   "message": msg,
                                   "random_id": 0})
            elif message == 'спать':
                vk_session.method("messages.send",
                                  {"peer_id": id,
                                   "message": 'Вы легли спать',
                                   "random_id": 0,
                                   "keyboard": sleep_keyboard})
            elif message == 'обучение':
                msg = 'Всё легко и просто:\n1. Ходите в вылазки и получайте деньги пока ноги держут\n' \
                      '2. Следите за заражением радиацией, чем больше заражение, тем меньше максимальное HP\n' \
                      '3. Если HP упадёт до 0, то ничего с персонажем не будет, правда мародёры не прочь поживиться' \
                      ' вашим хабаром\n4. Бегать по заданиям бесконечно вы не сможете, поэтому вам надо восстановить' \
                      ' силы у костра или поспать\n5. Не советую бежать до центра Зоны в одной кожаной курточке, ' \
                      'обзаведись хорошей защитой перед продвижением в глубь Зоны\n6. В вылазку лучше брать маслят ' \
                      'так 200, а то и 300. Ведь никогда не угадаешь что может произойти.'
                send_message(id, msg, None)
            elif message == 'профиль':
                msg = "Привет, " + str(data[str(id)]["name"]) + "\n"
                msg = msg + str(data[str(id)]["hp"]) + " HP\n"
                msg = msg + str(data[str(id)]["rad"]) + " радиации\n"
                msg = msg + str(data[str(id)]["money"]) + " .руб"
                msg = msg + "\n" + str(data[str(id)]["pwr"]) + " из 10 энергии"
                # msg = msg + "\n" + str(data[str(id)]["lvl"]) + " уровня"
                msg = msg + "\n-----------------"
                if data[str(id)]["loc"] == 'Cordon':
                    msg = msg + "\nВы на локации Кордон"
                if data[str(id)]["wpn"] == 'Fist':
                    msg = msg + "\nОружие: Кулаки"
                if data[str(id)]["suit"] == 'None':
                    msg = msg + "\nБроня: Отсутствует"
                vk_session.method("messages.send", {"user_id": id, "message": msg, "random_id": 0})
            elif message == 'speedwagon':
                data[str(id)]["money"] = int(data[str(id)]["money"]) + 1000
            else:
                send_message(id, 'Неизвестная или неправильная команда', None)
