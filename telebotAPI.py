import time
import telebot
from telebot import types
from csmoney import collect_data
import json
import os
from key import keys
bot = telebot.TeleBot(keys)
oplata = "Спасибо, что решили поддержать автора\nЗадонатить можно через QIWI\n\nДля оплаты нажмите на кнопку оплатить и вас перекинет на страницу оплаты"
help = "🤖 Привет, этот бот умеет искать скины с хорошой скидкой!!!"
bio = "🤖 Этот бот умеет искать скины с хорошей скидкой на торговых платформах\n\n[!] Идеи по поводу бота присылать на https://t.me/Pixelhkgc "
@bot.message_handler(commands=['start'])
def start_mes(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item2 = types.KeyboardButton("Cs money")
    item3 = types.KeyboardButton("💻 Информация 💻")
    item4 = types.KeyboardButton("⚠ Поддержать автора ⚠")
    markup.row(item2)
    markup.row(item3)
    markup.row(item4)
    bot.send_message(message.chat.id,"Выберите категорию",reply_markup=markup)
@bot.message_handler(content_types=['text'])
def get_items_messages(message):
    global type
    global markup
    type = 0

    if message.text == "Cs money":

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        item1 = types.KeyboardButton("Штурмовые винтовки")
        item2 = types.KeyboardButton("Снайперские винтовки")
        item3 = types.KeyboardButton("Ножи")
        item4 = types.KeyboardButton("Назад в меню")
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id,"Выберите предмет", reply_markup=markup)
    elif message.text == "Штурмовые винтовки":
        type = 3
        min_price(message)
    elif message.text == "Снайперские винтовки":
        type = 4
        min_price(message)
    elif message.text == "Ножи":
        type = 2
        min_price(message)
    elif message.text == "Назад в меню":
        start_mes(message)
    elif message.text == "💻 Информация 💻":
        bot.send_message(message.from_user.id, bio)
    elif message.text == "⚠ Поддержать автора ⚠":
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Оплатить", url="https://qiwi.com/n/0TOMMY0")
        keyboard.add(url_button)
        bot.send_message(message.from_user.id, oplata,reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю")
def min_price(message):
    msg = bot.send_message(message.chat.id, '⚙ Введите минимальную цену предмета\nЦена в долорах:')
    bot.register_next_step_handler(msg, max_price)
def max_price(message):
    global min_pr
    min_pr = message.text
    msg = bot.send_message(message.chat.id, '⚙ Введите максимальную цену предмета\nЦена в доллоралах:')
    bot.register_next_step_handler(msg, find)
def find(message):
    max_pr = message.text
    bot.send_message(message.chat.id, '''Пожалуйста подождите, производится сбор данных...\nЭто может занять некоторое время''')

    a = collect_data(type=type, max_price=max_pr, min_price=min_pr)


    for temp in a:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Ссылка на предмет", url=temp.get("3d"))
        keyboard.add(url_button)
        data = f'Предмет : {temp.get("full_name")}\nЦена : {temp.get("item_price")}$ ~~ Скидка : {temp.get("overprice")}%'


        bot.send_message(message.chat.id, data, reply_markup=keyboard)
        time.sleep(0.8)




bot.polling(none_stop=True, interval=0)
