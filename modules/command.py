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

def get_planning():
    pl = getGuide.get_guide()
    chaine=[]
    planning=[]

    for i in pl["tv"]["channel"]:
        chaine.append((i['@id'], i["display-name"]))

    for j in pl["tv"]["programme"]:
        start = j["@start"][0:12]
        # On ne prend qu'au dela de 20h
        if(start[0:8] == time.strftime('%Y%m%d') and int(start[8:12]) >= 2050):
            planning.append((j["title"], start[8:10]+"h"+start[10:12], j["@channel"]))

    return (chaine, planning)
#Command

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(*args, **kwargs):
        bot, update = args
        if(database.get_chat_enable(update.message.chat_id) == 1):
            bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
            func(bot, update, **kwargs)
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Bot pas activé.\n/start pour activé ce dernier.")

    return command_func

######## ON/OFF COMMAND ###########

def cstart(bot, update):
    if (database.get_chat(update.message.chat_id) == [] or database.get_chat_enable(update.message.chat_id) == 0):
        bot.send_message(chat_id=update.message.chat_id, text="Démarrage du bot...")
        database.insert_chat(update.message.chat_id, 1)
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
        planning = get_planning()
        chaineExist, chaineId = False, None
        word = ""
        for i in args:
            word += i + " "
        word = word.strip()
        for i in planning[0]:
            if (word == i[1]):
                chaineExist, chaineId = True, i[0]
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
    planning = get_planning()

    if (len(args)>0):
        cinfo(bot, update, args)
    else:
        text_pl = "Le prime pour le {dt} est : \n\n".format(dt=datetime.datetime.now().strftime('%d/%m/%Y') )
        for i in planning[0]:
            text_pl += "*{}* : \n".format(i[1])
            elem = 0
            for j in planning[1]:
                #Si id de la chaine correspond a id de la chaine du programme
                if(i[0] == j[2]):
                    if (elem < 1):
                        text_pl += j[0] + " - " + j[1]+"\n"
                    elem += 1
        bot.send_message(chat_id=update.message.chat_id, text=text_pl,  parse_mode=telegram.ParseMode.MARKDOWN)

@send_typing_action
def cgetchaine(bot, update):
    planning = get_planning()
    
    text_ch = "Les chaines disponibles sont les suivantes : \n\n"
    for i in planning[0]:
        text_ch += i[1]+"\n"
    bot.send_message(chat_id=update.message.chat_id, text=text_ch)
    logging.info("/chaine a été entré.")

@send_typing_action
def crappel(bot, update, args):
    if(len(args)> 0):
        word = ""
        for i in args:
            word += i + " "
        word = word.strip()
        routine = database.get_routine(update.message.chat_id)
        found = False
        i = 0
        while (not found and i < len(routine)):
            if (routine[i][1].lower() == word.lower()):
                found = True
            i+=1
        if (not found):
            database.insert_routine(word, update.message.chat_id)
            bot.send_message(chat_id=update.message.chat_id, text="Le rappel pour '"+word+"' a été créée.")
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Le rappel existe déjà.")
    else:
        wrongFormatCommand(bot, update)

@send_typing_action
def cshowRappel(bot, update):
    routine = database.get_routine(update.message.chat_id)
    txt = "La liste des rappels est la suivante : \n\n"
    if (len(routine) <= 0):
        txt = "Aucun rappels n'est enregistré."
    else:
        for i in range(len(routine)):
            txt += str(i) + " - " + routine[i][1] + "\n"
    bot.send_message(chat_id=update.message.chat_id, text=txt)
    
@send_typing_action
def cremoveRappel(bot, update, args):
    routine = database.get_routine(update.message.chat_id)
    if (len(args)<= 1):
        try:
            num = int(args[0])
            if(num <= len(routine)-1):
                database.remove_routine(update.message.chat_id, routine[num][0])
                cshowRappel(bot, update)
            else:
                bot.send_message(chat_id=update.message.chat_id, text="Le numéro doit être dans la liste.")
        except ValueError:
            bot.send_message(chat_id=update.message.chat_id, text="Vous devez mettre le numéro du rappel à supprimer.")
    else:
        wrongFormatCommand(bot, update)

        


class Command:
    handlers = (
        CommandHandler('stop', cstop),
        CommandHandler('start', cstart),
        CommandHandler('help', chelp),
        CommandHandler('chaine', cgetchaine),
        CommandHandler('prime', cprime, pass_args=True),
        CommandHandler('showrappel', cshowRappel),
        CommandHandler('removerappel', cremoveRappel, pass_args=True),
        CommandHandler('rappel', crappel, pass_args=True)
    )