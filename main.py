# 7155761835:AAGQrlBJL25xWVB0BuwxeKD5yDR58KJTrlo
import telebot
from telebot import types
import datetime
import csv
import io
import urllib.request
token = '7155761835:AAGQrlBJL25xWVB0BuwxeKD5yDR58KJTrlo'
bot = telebot.TeleBot(token)


url = 'https://docs.google.com/spreadsheets/d/1lmSfZIINVP3gnuDD1KppiGMlrJYpwLi0znT3Oh_Y9IQ/export?format=csv'

response = urllib.request.urlopen(url)
rows = []
with io.TextIOWrapper(response, encoding='utf-8') as f:
    reader = csv.reader(f)

    for row in reader:
        rows.append(row)


def getSubject(day, para, group):
    subject_type = ''
    subject_name = ''
    room = ''
    teacher = ''

    input_day_key = 0  # Позиция нужного дня в таблице
    input_para_key = 0  # Позиция нужной пары в таблице
    wday = {"ПОНЕДЕЛЬНИК": 0, "ВТОРНИК": 1, "СРЕДА": 2, "ЧЕТВЕРГ": 3, "ПЯТНИЦА": 4, "СУББОТА": 5}
    # Поиск позиции нужного дня в таблице
    for i in range(1, len(rows)):
        try:
            if wday[rows[i][0]] == day:
                input_day_key = i
        except KeyError:
            pass
    # Поиск позиции нужной пары в таблице, начиная с позиции нужного дня
    for i in range(input_day_key, len(rows)):
        buffer = rows[i][2]
        buffer = buffer.split('\n')
        if len(buffer) == 2:
            if buffer[0] == str(para):
                input_para_key = i
                break

    isLK = False
    groups = {3: 7, 4: 9}
    par_times = {1: '8:15 - 9:50', 2: '10:00 - 11:35', 3: '11:45 - 13:20', 4: '14:00 - 15:35', 5: '15:45 - 17:20'}

    group_ind = groups[group]
    subject = rows[input_para_key][group_ind]
    #print(subject)
    # print(subject)
    if subject == '':
        isLK = True
        subject3 = rows[input_para_key][groups[3]]
        if subject3 == '':
            subjectPI = rows[input_para_key][3]
            buffer = subjectPI.split('\n')
            subjectPI = buffer[0]
            if subjectPI == 'Физическая культура':
                return {'name': 'Физ.-ра', 'type': 'ПЗ', 'room': 'Карла Маркса, 31',
                        'teacher': 'Ксения-Ксения и Сергей-Сергей', 'time': par_times[para]}
            else:
                return {'name': 'форточка', 'type': '-', 'room': '-', 'teacher': '-', 'time': par_times[para]}
        else:
            subject = subject3

    buffer_list = subject.split('\n')
    print(buffer_list)
    buffer = buffer_list[0] # Название предмета
    teacher = buffer_list[1]
    # Разделение на тип предмета и имя предмета
    if buffer[-1:] == ' ':
        subject_type = buffer[-3:-1]
        if subject_type != "ЛК" and subject_type != "ПЗ":
            subject_type = 'undefined type\n'
            subject_name = buffer
        else:
            subject_name = buffer[:-5] + buffer[-1:]
    else:
        subject_type = buffer[-2:]
        if subject_type != "ЛК" and subject_type != "ПЗ":
            subject_type = 'undefined type\n'
            subject_name = buffer
        else:
            subject_name = buffer[:-4]
    if isLK and subject_type != 'ЛК':
        return {'name': 'форточка', 'type': '-', 'room': '-', 'teacher': '-', 'time': par_times[para]}
    if (subject_type != 'ЛК'):
        room = rows[input_para_key][group_ind + 1]
    else:
        room = rows[input_para_key][groups[4] + 1]

    return {'name': subject_name, 'type': subject_type, 'room': room, 'teacher': teacher, 'time': par_times[para]}

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    group_3 = types.KeyboardButton("/3")
    group_4 = types.KeyboardButton("/4")
    markup.add(group_3, group_4)
    bot.send_message(message.chat.id,
                     text="Укажи номер группы\n(сейчас доступны: 3, 4)".format(
                         message.from_user), reply_markup=markup)

"""def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    today = types.KeyboardButton("cегодня")
    monday = types.KeyboardButton("Понедельник")
    tuesday = types.KeyboardButton("Вторник")
    wendsday = types.KeyboardButton("Среда")
    thursdya = types.KeyboardButton("Четверг")
    friday = types.KeyboardButton("Пятница")
    saturday = types.KeyboardButton("Суббота")
    markup.add(today, monday, tuesday, wendsday, thursdya, friday, saturday)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я помогу с расписанием".format(
                         message.from_user), reply_markup=markup)"""
@bot.message_handler(commands=['3'])
def set_group_three(message):
    global set_group
    set_group = 3
    bot.send_message(message.chat.id, text="Группа изменена на " + str(set_group) + "!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    today = types.KeyboardButton("cегодня")
    monday = types.KeyboardButton("Понедельник")
    tuesday = types.KeyboardButton("Вторник")
    wendsday = types.KeyboardButton("Среда")
    thursdya = types.KeyboardButton("Четверг")
    friday = types.KeyboardButton("Пятница")
    saturday = types.KeyboardButton("Суббота")
    change_group = types.KeyboardButton("Сменить группу")
    markup.add(today, monday, tuesday, wendsday, thursdya, friday, saturday, change_group)
    bot.send_message(message.chat.id,
                     text="Выбери день".format(
                         message.from_user), reply_markup=markup)
@bot.message_handler(commands=['4'])
def set_group_four(message):
    global set_group
    set_group = 4
    bot.send_message(message.chat.id, text="Группа изменена на " + str(set_group) + "!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    today = types.KeyboardButton("cегодня")
    monday = types.KeyboardButton("Понедельник")
    tuesday = types.KeyboardButton("Вторник")
    wendsday = types.KeyboardButton("Среда")
    thursdya = types.KeyboardButton("Четверг")
    friday = types.KeyboardButton("Пятница")
    saturday = types.KeyboardButton("Суббота")
    change_group = types.KeyboardButton("Сменить группу")
    markup.add(today, monday, tuesday, wendsday, thursdya, friday, saturday, change_group)
    bot.send_message(message.chat.id,
                     text="Выбери день".format(
                         message.from_user), reply_markup=markup)
@bot.message_handler(content_types=['text'])
def func(message):
    global set_group
    if(message.text == "cегодня"):
        # Получение текущей даты и времени
        buffer = datetime.datetime.now()
        # Получение текущего дня недели (0 - Понедельник, 6 - Воскресенье)
        today_number = buffer.weekday()
    elif(message.text == "Понедельник"):
        today_number = 0
    elif(message.text == "Вторник"):
        today_number =1
    elif(message.text == "Среда"):
        today_number=2
    elif(message.text == "Четверг"):
        today_number=3
    elif(message.text=="Пятница"):
        today_number=4
    elif(message.text=="Суббота"):
        today_number=5
    elif(message.text=="Сменить группу"):
        start_message(message)
    else:
        bot.send_message(message.chat.id, text="Фигня какая-то")
        return
    days_of_week = {
        0: 'monday',
        1: 'tuesday',
        2: 'wednesday',
        3: 'thursday',
        4: 'friday',
        5: 'saturday',
        6: 'sunday' }
    if (today_number == 6):
        bot.send_message(message.chat.id, text="ВОСКРЕСЕНЬЕ БРАТАН, ЧИЛЛЬ!")
    else:
        amount_pars = 5
        if today_number == 0 or amount_pars == 5:
            amount_pars = 4
        bot.send_message(message.chat.id, text="Вот твоё расписание на "+str(message.text)+"!"+"\n(Номер группы: "+str(set_group)+")", parse_mode='HTML')
        output_message=""
        for i in range(amount_pars+1):
            i_subject = getSubject(today_number, i+1, set_group)
            name=i_subject['name']
            stype=''
            teacher=''
            time=''
            room=''
            if name!='форточка':
                name+="\n"
                stype = i_subject['type']
                if stype == "ПЗ":
                    stype = "Практосик\n"
                elif stype == "ЛК":
                    stype = "Лектосик\n"
                teacher = i_subject['teacher']+"\n"
                time = i_subject['time']
                room = "Аудитория "+i_subject['room']+'\n'
            output_message+=str(i+1)+"ая пара:\n"+stype+name+teacher+room+time+'\n'+' '+'\n'
        bot.send_message(message.chat.id, text=output_message, parse_mode='HTML')


bot.infinity_polling()
