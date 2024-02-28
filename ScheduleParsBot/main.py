import re
import datetime
from math import ceil

import pyjokes
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import PyPDF2
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTRect
import pdfplumber
import os

from transliterate import translit

from tmp import extract_table, table_converter, transform_date, has_cyrillic, days

import telebot
from telebot import types

bot = telebot.TeleBot('token')


@bot.message_handler(commands=['mtuci'])
def answer(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru/')

@bot.message_handler(commands=['help'])
def answer(message):
    bot.send_message(message.chat.id, 'Бот с расписанием занятий для студентов МТУСИ\n'
                                      'Гайд по командам:\n'
                                      '/today - расписание на сегодня\n'
                                      '/tomorrow - расписание на завтра\n'
                                      '/week - расписание на неделю\n'
                                      '/nextweek - расписание на следующую неделю\n'
                                      '/group - выбор группы\n'
                                      '/joke - кринжовый айтишный анекдот\n'
                                      '/help - помощь\n'
                                      '/mtuci - сайт МТУСИ\n')


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    bot.send_message(message.chat.id, 'Привет, здесь ты сможешь узнать свое расписание!\n'
                                      'Для справки выбери кнопку "Помощь" или введи /help', reply_markup=keyboard)


waiting_for_group_name = set()
url_pdf = {}
schedule = {}
group_namel = {}


@bot.message_handler(commands=['group'])
def group_name(message):
    waiting_for_group_name.add(message.chat.id)
    keyboard = types.ReplyKeyboardMarkup()
    bot.send_message(message.chat.id, 'Введи название группы.\n'
                                    'Примеры ввода: bfi2201, BFI2201, Бфи2201, БФИ2201\n'
                                      'После отправления сообщения с наименованием группы дождись сообщения о выборе группы!', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.chat.id in waiting_for_group_name,
                         content_types=['text'])
def handle_group_name_reply(message):
    url = 'https://mtuci.ru/time-table/'  # url для второй страницы
    r = requests.get(url, headers={'User-Agent': UserAgent().edge})
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')

    obj = soup.find(href=re.compile((translit(message.text,"ru", reversed=True).upper() + ".pdf")))


    if obj == None:
      bot.send_message(message.chat.id, 'Группа не существует')
      return
    else:
      s = obj.get('href')
      result = 'https://mtuci.ru' + s

      group_namel[message.chat.id] = message.text
      url_pdf[message.chat.id] = result


      dirname = str(os.getcwd())
      filename = dirname + '\\tmp\\bfi2201.pdf'
      url = str(result)

      response = requests.get(url)

      with open(filename, 'wb') as f:
        f.write(response.content)

      pdf_path = filename

      pdfFileObj = open(pdf_path, 'rb')
      pdfReaded = PyPDF2.PdfReader(pdfFileObj)

      for pagenum, page in enumerate(extract_pages(pdf_path)):
        pageObj = pdfReaded.pages[pagenum]
        # Инициализируем количество исследованных таблиц
        table_num = 0
        first_element = True
        table_extraction_flag = False

        pdf = pdfplumber.open(pdf_path)

        page_tables = pdf.pages[pagenum]  # Находим исследуемую страницу
        tables = page_tables.find_tables()  # Количество страниц

        page_elements = [(element.y1, element) for element in page._objs]

        page_elements.sort(key=lambda a: a[0], reverse=True)

        for i, component in enumerate(page_elements):
          pos = component[0]
          element = component[1]

          if isinstance(element, LTRect):
            if first_element == True and (table_num + 1) <= len(tables):
              # Находим ограничивающий прямоугольник таблицы
              lower_side = page.bbox[3] - tables[table_num].bbox[3]
              upper_side = element.y1
              # Извлекаем информацию из таблицы
              table = extract_table(pdf_path, pagenum, table_num)
              # удалем первые две записи, так как они не представляют ценности
              table.pop(0)
              table.pop(0)
              table_text = table_converter(table)

              table_extraction_flag = True
              first_element = False



            # Проверка извлечения таблиц из страницы
            if element.y0 >= lower_side and element.y1 <= upper_side:
              pass
            elif not isinstance(page_elements[i + 1][1], LTRect):
              table_extraction_flag = False
              first_element = True
              table_num += 1

      pdfFileObj.close()
      ############ Упорядочивание данных ####################
      for i in range(6):
        for j in range(5):
          table_text[i][j].pop(0)

      table_res = [[], [], [], [], [], []]
      for i in range(6):
        for j in range(5):
          table_res[i].append(table_text[i][j][:6])
          table_res[i].append(table_text[i][j][6:])

      for i in range(6):
        for j in range(1, 11, 2):
          table_res[i][j].insert(0, table_res[i][j - 1][1])
          table_res[i][j].insert(0, table_res[i][j - 1][0])

      for i in range(6):
          for j in range(10):
              table_res[i][j][0] += '.'

      schedule[message.chat.id] = table_res

    waiting_for_group_name.clear()
    bot.send_message(message.chat.id, 'Твоя группа: ' + message.text)

@bot.message_handler(commands=['today', 'tomorrow'])
def today_schedule(message):
    if not group_namel:
        bot.send_message(message.chat.id, 'Ты не выбрал группу')
        return

    keyboard = types.ReplyKeyboardMarkup()

    d1 = datetime.datetime(2024, 1, 28)
    d2 = datetime.datetime.now()

    even = 'нечётная'
    parity = ceil((d2 - d1).days / 7)
    if not (parity) % 2:
        even = 'чётная'


    if message.text == '/tomorrow':
        day_week = (datetime.datetime.today().weekday() + 1) % 7
        if day_week == 0:
            parity += 1
            if (parity) % 2:
                even = 'нечётная'
    else:
        day_week = datetime.datetime.today().weekday()

    if day_week == 6:
        today = []
    else:
        today = [schedule[message.chat.id][day_week][i] for i in range(10) if (i % 2) != (parity % 2)]


    result = []
    for lesson in today:
        if has_cyrillic(' '.join(lesson)):
            result.append(lesson[0] + ' ' + lesson[1] + '\n')
            result.append(lesson[5] + '\n')
            result.append(lesson[2] + '\n')
            result.append(lesson[3] + ' ' + lesson[4] + '\n\n')
        else:
            result.append(lesson[0] + ' ' + lesson[1] + ' Нет пары' + '\n\n')

    result = ''.join(result)

    if result == '':
        result = 'НИКУДА НЕ НАДО, УРАА!'



    date = datetime.datetime.today()

    if message.text == '/tomorrow':
        bot.send_message(message.chat.id, f'*Расписание на завтра* \U0001F90D\n'
                                      f'{transform_date(str(date))}\n'
                                      f'{translit(group_namel[message.chat.id],"ru").upper()}\n'
                                      f'Неделя №{parity} {even}\n\n'
                                      f'*{days[day_week]}*\n'
                                      f'{result}', parse_mode= 'Markdown', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, f'*Расписание на сегодня* \U0001F90D\n'
                                          f'{transform_date(str(date))}\n'
                                          f'{translit(group_namel[message.chat.id], "ru").upper()}\n'
                                          f'Неделя №{parity} {even}\n\n'
                                          f'*{days[day_week]}*\n'
                                          f'{result}', parse_mode='Markdown', reply_markup=keyboard)



@bot.message_handler(commands=['week', 'nextweek'])
def today_schedule(message):
    if not group_namel:
        bot.send_message(message.chat.id, 'Ты не выбрал группу')
        return

    keyboard = types.ReplyKeyboardMarkup()

    d1 = datetime.datetime(2024, 1, 28)
    d2 = datetime.datetime.now()

    even = 'нечётная'
    parity = ceil((d2 - d1).days / 7)

    if message.text == '/nextweek':
        parity += 1

    if not (parity) % 2:
        even = 'чётная'




    result = []
    for day in range(len(schedule[message.chat.id])):
        result.append(f'{days[day]}\n')
        for lesson in range(len(schedule[message.chat.id][day])):
            if lesson % 2 != parity % 2:
                if has_cyrillic(' '.join(schedule[message.chat.id][day][lesson])):
                    result.append(schedule[message.chat.id][day][lesson][0] + ' ' + schedule[message.chat.id][day][lesson][1] + '\n')
                    result.append(schedule[message.chat.id][day][lesson][5] + '\n')
                    result.append(schedule[message.chat.id][day][lesson][2] + '\n')
                    result.append(schedule[message.chat.id][day][lesson][3] + ' ' + schedule[message.chat.id][day][lesson][4] + '\n\n')
                else:
                    result.append(schedule[message.chat.id][day][lesson][0] + ' ' + schedule[message.chat.id][day][lesson][1] + ' Нет пары' + '\n\n')
        result.append('\n')

    result = ''.join(result)


    if result == '':
        result = 'НИКУДА НЕ НАДО, УРАА!'

    date = datetime.datetime.today()

    if message.text == '/nextweek':
        bot.send_message(message.chat.id, f'*Расписание на следующую неделю* \U0001F90D\n'
                                          f'{transform_date(str(date))}\n'
                                          f'{translit(group_namel[message.chat.id], "ru").upper()}\n'
                                          f'Неделя №{parity} {even}\n\n'
                                          f'{result}', parse_mode='Markdown', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, f'*Расписание на неделю* \U0001F90D\n'
                                          f'{transform_date(str(date))}\n'
                                          f'{translit(group_namel[message.chat.id], "ru").upper()}\n'
                                          f'Неделя №{parity} {even}\n\n'
                                          f'{result}', parse_mode='Markdown', reply_markup=keyboard)

@bot.message_handler(commands=['joke'])
def unknown_command(message):
    joke = pyjokes.get_joke()
    bot.send_message(message.chat.id, joke)

@bot.message_handler(content_types=['text'])
def unknown_command(message):
    bot.send_message(message.chat.id, 'Неизвестная команда')

bot.infinity_polling()
