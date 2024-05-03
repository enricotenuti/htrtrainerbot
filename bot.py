# This example shows you how to create a custom QWERTY keyboard using reply keyboard markup
import telebot
from random import randint
import csv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "TOKEN"
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

myfilepath = "out.csv"
random_line = 0
response = 0

def keyboard(key_type="Scramble"):
    markup = ReplyKeyboardMarkup(row_width=1)
    if key_type == "Scramble":
        markup = ReplyKeyboardMarkup(row_width=2)
        markup.add(KeyboardButton("Scramble"),KeyboardButton("Done"))
    elif key_type == "Solution":
        markup = ReplyKeyboardMarkup(row_width=2)
        markup.add(KeyboardButton("Solution"),KeyboardButton("Done"))
    elif key_type == "Done":
        markup = ReplyKeyboardMarkup(row_width=2)
        markup.add(KeyboardButton("Scramble"),KeyboardButton("Done"))
    else:
        markup.add(KeyboardButton("Start"))
    return markup

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id,"Welcome to HTR trainer.",reply_markup=keyboard())

@bot.message_handler(func=lambda message:True)
def all_messages(message):
    if message.text == "Done" or message.text == "/done":
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id,"Done training.",reply_markup=markup)
    elif message.text == "Scramble" or message.text == "/scramble":
        global random_line
        random_line = randint(0,275)
        global response
        response = ''
        with open(myfilepath) as cards:
            csv_reader = csv.reader(cards)
            for index, row in enumerate(csv_reader):
                if index == random_line:
                    response = 'Optimal HTR: <span class=\"tg-spoiler\">' + str(row[2]).zfill(2) + '</span>\nSolutions found: <span class=\"tg-spoiler\">' + str(row[3]).zfill(3) + '</span>\n\nScramble: ' + row[0] + '\nPress to see the solution.'
        bot.send_message(message.from_user.id,response,reply_markup=keyboard("Solution"))
    elif message.text == "Solution" or message.text == "/solution":
        with open(myfilepath) as cards:
            csv_reader = csv.reader(cards)
            for index, row in enumerate(csv_reader):
                if index == random_line:
                    response2 = row[1]
                    response2 = response2.replace("\\n", "\n")
                    response2 = response2 + '\nPress to continue.'
        bot.send_message(message.from_user.id,response2,reply_markup=keyboard("Done"))
    elif message.text == "Start" or message.text == "/start":
        bot.send_message(message.from_user.id,"Press to get new scramble.",reply_markup=keyboard("Scramble"))
    elif message.text == "Help" or message.text == "/help":
        bot.send_message(message.chat.id,"This bot is going to help you practice HTR solutions given a DR state.\n\nWrite /start to start training.\nWrite /scramble to generate new DR state.\nWrite /solution to get the solutions of the previous scramble.\nWrite /done if you are done training.")
    else:
        bot.send_message(message.chat.id, message.text)
bot.infinity_polling(timeout=10, long_polling_timeout=5)