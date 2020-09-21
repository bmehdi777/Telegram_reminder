import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from functools import wraps
import logging
import datetime
import time

from bdd import database
from cmd import getGuide

#Function
def read_f(path):
    f = open(path, 'r')
    return f.read()

def get_planning(pl):
    chaine=[]
    planning=[]

    for i in pl["tv"]["channel"]:
        chaine.append((i["display-name"], i['@id']))

    for j in pl["tv"]["programme"]:
        start = j["@start"][0:12]
        # On ne prend qu'au dela de 20h
        if(start[0:8] == time.strftime('%Y%m%d') and int(start[8:10]) >= 20):
            planning.append((j["title"], start[8:10]+"h"+start[10:12], j["@channel"]))

    return (chaine, planning)

#Command

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(*args, **kwargs):
        bot, update = args
        if(database.get_chat(update.message.chat_id) == []):
            database.insert_chat(update.message.chat_id, 0)
        if(database.get_chat_enable(update.message.chat_id) == 1):
            bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
            func(bot, update, **kwargs)
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Bot pas activé.\n/start pour activé ce dernier.")

    return command_func

######## ON/OFF COMMAND ###########
def cstart(bot, update):
    if (database.get_chat_enable(update.message.chat_id) == 0):
        bot.send_message(chat_id=update.message.chat_id, text="Démarrage du bot...")
        database.insert_chat(update.message.chat_id, 0)
        database.set_enable_chat(update.message.chat_id, 1)
        chelp(bot, update)
        logging.info("/start a été entré.")
    elif (database.get_chat_enable(update.message.chat_id) == 1):
        bot.send_message(chat_id=update.message.chat_id, text="Le bot est déjà allumé.")
        logging.info("/start a été entré alors que le bot est déjà allumé.")
def cstop(bot, update):
    if (database.get_chat_enable(update.message.chat_id) == 1):
        bot.send_message(chat_id=update.message.chat_id, text="Au revoir.")
        database.set_enable_chat(update.message.chat_id, 0)
        logging.info("/stop a été entré.")
    elif (database.get_chat_enable(update.message.chat_id) == 0):
        bot.send_message(chat_id=update.message.chat_id, text="Le bot est déjà éteint.")
        logging.info("/stop a été entré mais le bot est déjà éteint.")

######## MAIN COMMAND ############
@send_typing_action
def chelp(bot, update):
    help_str = read_f("file/helpcmd")
    bot.send_message(chat_id=update.message.chat_id, text=help_str, parse_mode=telegram.ParseMode.MARKDOWN)
    logging.info("/help a été entré.")

def wrongFormatCommand(bot, update):
    txt = "Mauvais format de commande.\nUtilisez /help pour plus d'information."
    bot.send_message(chat_id=update.message.chat_id, text=txt)

def cinfo(bot, update, args):
    if (len(args) > 0 and args[0] != ""):
        pl = getGuide.get_guide()
        planning = get_planning(pl)
        chaineExist, chaineId = False, None
        word = ""
        for i in args:
            word += i
        for i in planning[0]:
            if (word == i[0]):
                chaineExist, chaineId = True, i[1]
                break
            else:
                chaineExist = False
        if(chaineExist):
            text_pl = "Le planning pour {c} le {dt} est : \n\n".format(c=" ".join(args), dt=datetime.datetime.now().strftime('%d/%m/%Y') )
            for i in planning[1]:
                if(i[2] == chaineId):
                    text_pl += i[0] + " - " + i[1] +"\n"
            bot.send_message(chat_id=update.message.chat_id, text=text_pl, parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Cette chaine n'existe pas. Veuillez vous référer à la commande /chaine")
    else:
        wrongFormatCommand(bot, update)

@send_typing_action
def cprime(bot, update, args):
    pl = getGuide.get_guide()
    planning = get_planning(pl)

    if (len(args)>0):
        print(args)
        cinfo(bot, update, args)
    else:
        text_pl = "Le prime pour le {dt} est : \n\n".format(dt=datetime.datetime.now().strftime('%d/%m/%Y') )
        for i in planning[0]:
            text_pl += "*Programme sur {}* : \n".format(i[0])
            for j in planning[1]:
                #Si id de la chaine correspond a id de la chaine du programme
                if(i[1] == j[2]):
                    text_pl += j[0] + " - " + j[1]+"\n"
        bot.send_message(chat_id=update.message.chat_id, text=text_pl,  parse_mode=telegram.ParseMode.MARKDOWN)

@send_typing_action
def cgetchaine(bot, update):
    pl = getGuide.get_guide()
    planning = get_planning(pl)
    
    text_ch = "Les chaines disponibles sont les suivantes : \n\n"
    for i in planning[0]:
        text_ch += i[0]+"\n"
    bot.send_message(chat_id=update.message.chat_id, text=text_ch)
    logging.info("/chaine a été entré.")


class Command:
    handlers = (
        CommandHandler('stop', cstop),
        CommandHandler('start', cstart),
        CommandHandler('help', chelp),
        CommandHandler('chaine', cgetchaine),
        CommandHandler('prime', cprime, pass_args=True),
    )