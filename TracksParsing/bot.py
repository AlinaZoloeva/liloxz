import time

from main import *
import getpass
import os
import sys
from pathlib import Path


import requests
from bs4 import BeautifulSoup
from colorama import init, Fore
from tqdm import tqdm

init(autoreset=True)
import telebot
from telebot import types

bot = telebot.TeleBot('6705707173:AAHRN9iMKFYvzQncKNDk-XX20xFZpdcyPeo')
tracks = []

@bot.message_handler(commands=['mtuci'])
def answer(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru/')

@bot.message_handler(commands=['help'])
def answer(message):
    bot.send_message(message.chat.id, 'Бот для получения случайного трека из чарта\n'
                                      'Гайд по командам:\n'
                                      '/track - скинуть случайный трек\n')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я бот для получения случайного трека из чарта".format(message.from_user), reply_markup=markup)

    url = 'https://rus.hitmotop.com/songs/top-today'
    dir_path = Path.cwd()
    path = Path(dir_path, 'music')

    count_list = 10
    bot.send_message(message.chat.id, 'Подождем загрузки треков....', reply_markup=markup)
    temp = get_links(path, count_list * 48, url)
    btn1 = types.KeyboardButton("Трек")
    markup.add(btn1)
    bot.send_message(message.chat.id, 'Жми "Трек"!', reply_markup=markup)

    tracks.extend(temp[0])


@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Трек"):
        dir_path = Path.cwd()
        path = Path(dir_path, 'music')

        i = random.randint(1, len(tracks))

        filename = track_download(tracks[i], path)
        path = Path(dir_path, 'music', str(filename))
        f = open(path, "rb")

        bot.send_document(message.chat.id, f)
        f.close()

        os.remove(path)

    else:
        bot.send_message(message.chat.id, text="Я не знаю эту команду((")



bot.polling()
