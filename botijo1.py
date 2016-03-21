"""
This is a detailed example using almost every command of the API
"""

import telebot
from telebot import types
import time
import os

TOKEN = '180031801:AAFfIv8M62qyAyToYFJcvh5t9gsIcSj5Yhg'

knownUsers = [] # todo: save these in a file,
userStep = {} # so they won't reset every time the bot restarts

commands = { # command description used in the "help" command
             'start': 'Get used to the bot',
             'ayuda': 'Da informacion sobre los comandos disponibles',
             'exec': 'Ejecuta un comando',
             'reboot': 'Reinicia el servidor'
}

hideBoard = types.ReplyKeyboardHide() # if sent as reply_markup, will hide the keyboard

# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
# had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print "New user detected, who hasn't used \"/start\" yet"
        return 0

# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener) # register listener

# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:
        knownUsers.append(cid) 
        userStep[cid] = 0
        command_help(m) # show the new user the help page

# help page
@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    help_text = "Estos son los comandos disponibles: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)

# Reinicia servidor
@bot.message_handler(commands=['reboot'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Voy a reiniciar el servidor...")
    bot.send_chat_action(cid, 'typing')
    time.sleep(3)
    bot.send_message(cid, ".")
    os.system("reboot")

# Ejecuta un comando
@bot.message_handler(commands=['exec'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Ejecutando: "+m.text[len("/exec"):])
    bot.send_chat_action(cid, 'typing') # show the bot "typing" (max. 5 secs)
    time.sleep(2)
    f = os.popen(m.text[len("/exec"):])
    result = f.read()
    bot.send_message(cid, "Resultado: "+result)


# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "hi")
def command_text_hi(m):
    bot.send_message(m.chat.id, "I love you too!")
    # default handler for every other text


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "No te entiendo, prueba con /ayuda")

bot.polling()
