import telebot
from telebot import types
from datetime import date
import calendar
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta
import requests
from flask import Flask, render_template, request
import psycopg2

conn = psycopg2.connect(database="telebot_1",
                        user="postgres",
                        password="1m7v89c1w",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


token = '5624212170:AAH3qUDxpMg8SXh_I7XTooCNbG_ee6Cxr8k'

bot = telebot.TeleBot(token,  threaded=False)

my_date = date.today()

@bot.message_handler(commands=['mtuci'])
def answer(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru/')


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("/help", "/mtuci", "/weekparity" , "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Week", "NextWeek")
    bot.send_message(message.chat.id, 'Hi! Find out your timetable', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    inform = 'This telegram bot is designed to display the timetable. \n' \
             'The list of commands and their purpose: \n' \
             '/mtuci - link to the mtuci website. \n' \
             '/weekparity - whether the current week is even or odd. \n' \
             'Monday - schedule for Monday.\n ' \
             'Tuesday - schedule for Tuesday.\n' \
             'Wednesday - schedule for Wednesday.\n' \
             'Thursday - schedule for Thursday.\n' \
             'Friday - schedule for Friday.\n' \
             'Saturday - schedule for Saturday.\n' \
             'Week - schedule for the current week.\n' \
             'Next Week - the schedule for the next week.\n'
    bot.send_message(message.chat.id, inform)

@bot.message_handler(commands=['weekparity'])
def week_par(message):
    # chetnost'
    #############
    now = datetime.now()
    sep = datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)

    d1 = sep - timedelta(days=sep.weekday())
    d2 = now - timedelta(days=now.weekday())

    even = 0  # nechetnoe
    parity = ((d2 - d1).days // 7) % 2
    if (parity):
        even = 1  # chetnoe

    if even:
        bot.send_message(message.chat.id, "It's an even week")
    else:
        bot.send_message(message.chat.id, "It's an odd week")

    #############

@bot.message_handler(content_types=['text'])
def day_week(message):
    # chetnost'
    #############
    now = datetime.now()
    sep = datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)

    d1 = sep - timedelta(days=sep.weekday())
    d2 = now - timedelta(days=now.weekday())

    even = 0  # nechetnoe
    parity = ((d2 - d1).days // 7) % 2
    if (parity):
        even = 1  # chetnoe

    #############

    if message.text.lower() == 'monday':
        if even:
            cursor.execute("SELECT * FROM timetable_ch WHERE day='Monday'")
            records = list(cursor.fetchall())
            print(records)

            sub = records[0][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher1 = list(cursor.fetchall())

            sub = records[1][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher2 = list(cursor.fetchall())

            monday = 'Monday' + '\n' + '1. ' + records[0][2] + ' ' + \
                     records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] +\
            '\n' + '2. ' + records[1][2] + ' ' + \
            records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1]

            bot.send_message(message.chat.id, monday)
        else:
            cursor.execute("SELECT * FROM timetable_nech WHERE day='Monday'")
            records = list(cursor.fetchall())
            print(records)

            sub = records[0][2].strip()
            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher1 = list(cursor.fetchall())



            sub = records[1][2].strip()
            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher2 = list(cursor.fetchall())



            sub = records[2][2].strip()
            cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
            teacher3 = list(cursor.fetchall())

            monday = 'Monday' + '\n' + '1. ' + records[0][2] + ' ' + \
                     records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] +\
            '\n' + '2. ' + records[1][2] + ' ' + \
            records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1] +\
            '\n' + '3. ' + records[2][2] + ' ' +\
            records[2][3] + ' ' + records[2][4] + ' ' + teacher3[0][1]
            print(monday)

            bot.send_message(message.chat.id, monday)

    elif message.text.lower() == 'tuesday':
        if (even):
            cursor.execute("SELECT * FROM timetable_ch WHERE day='Tuesday'")
            records = list(cursor.fetchall())

            sub = records[0][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher1 = list(cursor.fetchall())

            sub = records[1][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher2 = list(cursor.fetchall())

            monday = 'Tuesday' + '\n' + '1. ' + records[0][2] + ' ' + \
                     records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] +\
            '\n' + '2. ' + records[1][2] + ' ' + \
            records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1]

            bot.send_message(message.chat.id, monday)
        else:
            bot.send_message(message.chat.id, "There are no classes on this day");

    elif message.text.lower() == 'wednesday':
        if (even):
            cursor.execute("SELECT * FROM timetable_ch WHERE day='Wednesday'")
            records = list(cursor.fetchall())


            sub = records[0][2].strip() # records[0][2] - nazvanie predmeta

            # dostau iz tablici prepoda nuzhnogo predmeta
            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher1 = list(cursor.fetchall())

            sub = records[1][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher2 = list(cursor.fetchall())

            sub = records[2][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
            teacher3 = list(cursor.fetchall())

            sub = records[3][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
            teacher4 = list(cursor.fetchall())
            #print(records)

            monday = 'Wednesday' + '\n' + '1. ' + records[0][2] + ' ' + \
                     records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] +\
            '\n' + '2. ' + records[1][2] + ' ' + \
            records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1] + \
            '\n' + '3. ' + records[2][2] + ' ' + \
            records[2][3] + ' ' + records[2][4] + ' ' + teacher3[0][1] + \
            '\n' + '4. ' + records[3][2] + ' ' + \
            records[3][3] + ' ' + records[3][4] + ' ' + teacher4[0][1]


            bot.send_message(message.chat.id, monday)

        else:
            cursor.execute("SELECT * FROM timetable_nech WHERE day='Wednesday'")
            records = list(cursor.fetchall())

            sub = records[0][2].strip()
            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher1 = list(cursor.fetchall())



            sub = records[1][2].strip()
            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher2 = list(cursor.fetchall())



            sub = records[2][2].strip()
            cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
            teacher3 = list(cursor.fetchall())

            monday = 'Monday' + '\n' + '1. ' + records[0][2] + ' ' + \
                     records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] +\
            '\n' + '2. ' + records[1][2] + ' ' + \
            records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1] +\
            '\n' + '3. ' + records[2][2] + ' ' +\
            records[2][3] + ' ' + records[2][4] + ' ' + teacher3[0][1]
            print(monday)

            bot.send_message(message.chat.id, monday)

    elif message.text.lower() == 'thursday':
        if even:
            cursor.execute("SELECT * FROM timetable_ch WHERE day='Thursday'")
            records = list(cursor.fetchall())


            sub = records[0][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher1 = list(cursor.fetchall())

            sub = records[1][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher2 = list(cursor.fetchall())

            monday = 'Thursday' + '\n' + '1. ' + records[0][2] + ' ' + \
                     records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] +\
            '\n' + '2. ' + records[1][2] + ' ' + \
            records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1]

            bot.send_message(message.chat.id, monday)
        else:
            cursor.execute("SELECT * FROM timetable_nech WHERE day='Thursday'")
            records = list(cursor.fetchall())

            sub = records[0][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
            teacher1 = list(cursor.fetchall())

            sub = records[1][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
            teacher2 = list(cursor.fetchall())

            monday = 'Thursday' + '\n' + '1. ' + records[0][2] + ' ' + \
                     records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] + \
                     '\n' + '2. ' + records[1][2] + ' ' + \
                     records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1]

            bot.send_message(message.chat.id, monday)


    elif message.text.lower() == 'friday':
        if even:
            cursor.execute("SELECT * FROM timetable_ch WHERE day='Friday'")
            records = list(cursor.fetchall())

            sub = records[0][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher1 = list(cursor.fetchall())

            sub = records[1][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher2 = list(cursor.fetchall())

            monday = 'Friday' + '\n' + '1. ' + records[0][2] + ' ' + \
                     records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] +\
            '\n' + '2. ' + records[1][2] + ' ' + \
            records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1]

            bot.send_message(message.chat.id, monday)
        else:
            cursor.execute("SELECT * FROM timetable_nech WHERE day='Friday'")
            records = list(cursor.fetchall())

            sub = records[0][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
            teacher1 = list(cursor.fetchall())

            sub = records[1][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
            teacher2 = list(cursor.fetchall())

            sub = records[2][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
            teacher3 = list(cursor.fetchall())

            sub = records[3][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
            teacher4 = list(cursor.fetchall())

            monday = 'Friday' + '\n' + '1. ' + records[0][2] + ' ' + \
                     records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] + \
                     '\n' + '2. ' + records[1][2] + ' ' + \
                     records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1] + \
                     '\n' + '3. ' + records[2][2] + ' ' + \
                     records[2][3] + ' ' + records[2][4] + ' ' + teacher3[0][1] + \
                     '\n' + '4. ' + records[3][2] + ' ' + \
                     records[3][3] + ' ' + records[3][4] + ' ' + teacher4[0][1]

            bot.send_message(message.chat.id, monday)


    elif message.text.lower() == 'saturday':
        if even:
            cursor.execute("SELECT * FROM timetable_ch WHERE day='Saturday'")
            records = list(cursor.fetchall())


            sub = records[0][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher1 = list(cursor.fetchall())

            sub = records[1][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'"% sub)
            teacher2 = list(cursor.fetchall())

            monday = 'Saturday' + '\n' + '1. ' + records[0][2] + ' ' + \
                    records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] +\
            '\n' + '2. ' + records[1][2] + ' ' + \
            records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1]

            bot.send_message(message.chat.id, monday)
        else:
            cursor.execute("SELECT * FROM timetable_nech WHERE day='Saturday'")
            records = list(cursor.fetchall())

            sub = records[0][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
            teacher1 = list(cursor.fetchall())

            sub = records[1][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
            teacher2 = list(cursor.fetchall())

            sub = records[2][2].strip()

            cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
            teacher3 = list(cursor.fetchall())

            monday = 'Saturday' + '\n' + '1. ' + records[0][2] + ' ' + \
                     records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] + \
                     '\n' + '2. ' + records[1][2] + ' ' + \
                     records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1] + \
                     '\n' + '3. ' + records[2][2] + ' ' + \
                     records[2][3] + ' ' + records[2][4] + ' ' + teacher3[0][1]

            bot.send_message(message.chat.id, monday)

    elif message.text.lower() == 'week' or message.text.lower() == 'nextweek':
        #monday
            if message.text.lower() == 'nextweek':
                if even: #menyaem chetnost'
                    even = 0
                else:
                    even = 1

            if even:
                #ponedelnik
                cursor.execute("SELECT * FROM timetable_ch WHERE day='Monday'")
                records = list(cursor.fetchall())
                print(records)

                sub = records[0][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher1 = list(cursor.fetchall())

                sub = records[1][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher2 = list(cursor.fetchall())

                monday = 'Monday' + '\n' + '1. ' + records[0][2] + ' ' + \
                         records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] + \
                         '\n' + '2. ' + records[1][2] + ' ' + \
                         records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1]

                ###########################################
                #vtornik
                cursor.execute("SELECT * FROM timetable_ch WHERE day='Tuesday'")
                records = list(cursor.fetchall())

                sub = records[0][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher1 = list(cursor.fetchall())

                sub = records[1][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher2 = list(cursor.fetchall())

                tuesday = 'Tuesday' + '\n' + '1. ' + records[0][2] + ' ' + \
                         records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] + \
                         '\n' + '2. ' + records[1][2] + ' ' + \
                         records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1]


                ###########################################
                # wednesday

                cursor.execute("SELECT * FROM timetable_ch WHERE day='Wednesday'")
                records = list(cursor.fetchall())

                sub = records[0][2].strip()  # records[0][2] - nazvanie predmeta

                # dostau iz tablici prepoda nuzhnogo predmeta
                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher1 = list(cursor.fetchall())

                sub = records[1][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher2 = list(cursor.fetchall())

                sub = records[2][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher3 = list(cursor.fetchall())

                sub = records[3][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher4 = list(cursor.fetchall())

                wednesday = 'Wednesday' + '\n' + '1. ' + records[0][2] + ' ' + \
                         records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] + \
                         '\n' + '2. ' + records[1][2] + ' ' + \
                         records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1] + \
                         '\n' + '3. ' + records[2][2] + ' ' + \
                         records[2][3] + ' ' + records[2][4] + ' ' + teacher3[0][1] + \
                         '\n' + '4. ' + records[3][2] + ' ' + \
                         records[3][3] + ' ' + records[3][4] + ' ' + teacher4[0][1]

                ############################################
                #chetverg
                cursor.execute("SELECT * FROM timetable_ch WHERE day='Thursday'")
                records = list(cursor.fetchall())

                sub = records[0][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher1 = list(cursor.fetchall())

                sub = records[1][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher2 = list(cursor.fetchall())

                thursday = 'Thursday' + '\n' + '1. ' + records[0][2] + ' ' + \
                         records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] + \
                         '\n' + '2. ' + records[1][2] + ' ' + \
                         records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1]

                ##########################################
                #pyatnica
                cursor.execute("SELECT * FROM timetable_ch WHERE day='Friday'")
                records = list(cursor.fetchall())

                sub = records[0][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher1 = list(cursor.fetchall())

                sub = records[1][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher2 = list(cursor.fetchall())

                friday = 'Friday' + '\n' + '1. ' + records[0][2] + ' ' + \
                         records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] + \
                         '\n' + '2. ' + records[1][2] + ' ' + \
                         records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1]

                #######################################
                #subbota
                cursor.execute("SELECT * FROM timetable_ch WHERE day='Saturday'")
                records = list(cursor.fetchall())

                sub = records[0][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher1 = list(cursor.fetchall())

                sub = records[1][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher2 = list(cursor.fetchall())

                saturday = 'Saturday' + '\n' + '1. ' + records[0][2] + ' ' + \
                         records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] + \
                         '\n' + '2. ' + records[1][2] + ' ' + \
                         records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1]

                week_ch = monday + '\n' + '---------------------' + '\n' + tuesday + '\n' + '---------------------' \
                          + '\n' + wednesday + '\n'+ '---------------------' + '\n' +\
                    thursday + '\n' + '---------------------' + '\n' + friday + '\n' + '---------------------'\
                          + '\n' + saturday + '\n'

                bot.send_message(message.chat.id, week_ch)
            else:
                # ponedelnik
                cursor.execute("SELECT * FROM timetable_nech WHERE day='Monday'")
                records = list(cursor.fetchall())
                print(records)

                sub = records[0][2].strip()
                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher1 = list(cursor.fetchall())

                sub = records[1][2].strip()
                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher2 = list(cursor.fetchall())

                sub = records[2][2].strip()
                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher3 = list(cursor.fetchall())

                monday = 'Monday' + '\n' + '1. ' + records[0][2] + ' ' + \
                         records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] + \
                         '\n' + '2. ' + records[1][2] + ' ' + \
                         records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1] + \
                         '\n' + '3. ' + records[2][2] + ' ' + \
                         records[2][3] + ' ' + records[2][4] + ' ' + teacher3[0][1]

                #####################
                #vtornik
                tuesday = "There are no classes on this day"
                ###########################

                #sreda
                cursor.execute("SELECT * FROM timetable_nech WHERE day='Wednesday'")
                records = list(cursor.fetchall())

                sub = records[0][2].strip()
                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher1 = list(cursor.fetchall())

                sub = records[1][2].strip()
                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher2 = list(cursor.fetchall())

                sub = records[2][2].strip()
                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher3 = list(cursor.fetchall())

                wednesday = 'Wednesday' + '\n' + '1. ' + records[0][2] + ' ' + \
                         records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] + \
                         '\n' + '2. ' + records[1][2] + ' ' + \
                         records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1] + \
                         '\n' + '3. ' + records[2][2] + ' ' + \
                         records[2][3] + ' ' + records[2][4] + ' ' + teacher3[0][1]
                ###############################

                #chetverg
                cursor.execute("SELECT * FROM timetable_nech WHERE day='Thursday'")
                records = list(cursor.fetchall())

                sub = records[0][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher1 = list(cursor.fetchall())

                sub = records[1][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher2 = list(cursor.fetchall())

                thursday = 'Thursday' + '\n' + '1. ' + records[0][2] + ' ' + \
                         records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] + \
                         '\n' + '2. ' + records[1][2] + ' ' + \
                         records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1]
                #########################################################3

                #pyatnica
                cursor.execute("SELECT * FROM timetable_nech WHERE day='Friday'")
                records = list(cursor.fetchall())

                sub = records[0][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher1 = list(cursor.fetchall())

                sub = records[1][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher2 = list(cursor.fetchall())

                sub = records[2][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher3 = list(cursor.fetchall())

                sub = records[3][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher4 = list(cursor.fetchall())

                friday = 'Friday' + '\n' + '1. ' + records[0][2] + ' ' + \
                         records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] + \
                         '\n' + '2. ' + records[1][2] + ' ' + \
                         records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1] + \
                         '\n' + '3. ' + records[2][2] + ' ' + \
                         records[2][3] + ' ' + records[2][4] + ' ' + teacher3[0][1] + \
                         '\n' + '4. ' + records[3][2] + ' ' + \
                         records[3][3] + ' ' + records[3][4] + ' ' + teacher4[0][1]
                #########################################

                #subbota
                cursor.execute("SELECT * FROM timetable_nech WHERE day='Saturday'")
                records = list(cursor.fetchall())

                sub = records[0][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher1 = list(cursor.fetchall())

                sub = records[1][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher2 = list(cursor.fetchall())

                sub = records[2][2].strip()

                cursor.execute("SELECT * FROM teacher WHERE subject='%s'" % sub)
                teacher3 = list(cursor.fetchall())


                saturday = 'Saturday' + '\n' + '1. ' + records[0][2] + ' ' + \
                         records[0][3] + ' ' + records[0][4] + ' ' + teacher1[0][1] + \
                         '\n' + '2. ' + records[1][2] + ' ' + \
                         records[1][3] + ' ' + records[1][4] + ' ' + teacher2[0][1] + \
                         '\n' + '3. ' + records[2][2] + ' ' + \
                         records[2][3] + ' ' + records[2][4] + ' ' + teacher3[0][1]


                week_nech = monday + '\n' + '---------------------' + '\n' + tuesday + '\n' + '---------------------' \
                            + '\n' + wednesday + '\n' + '---------------------' + '\n' + \
                          thursday + '\n' + '---------------------' + '\n' + friday + '\n' + '---------------------' \
                            + '\n' + saturday + '\n'

                bot.send_message(message.chat.id, week_nech)

            if message.text.lower() == 'nextweek':
                if even: # menyaem chetnost'
                    even = 0
                else:
                    even = 1

    else:
        bot.send_message(message.chat.id, "Please, enter an existing command!")


bot.polling()
