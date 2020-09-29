import telegram
import logging
import datetime
import os

from modules import command
from bdd import database


def main():
    actualDir = os.path.dirname(os.path.realpath(__file__))
    token = open(actualDir+"/file/token","r").read().rstrip()
    bot = telegram.Bot(token=token)
    send_rappel(bot)

def send_rappel(bot):
    planning = command.get_planning()
    chaine = dict(planning[0])
    routine = database.get_routines_enabled()
    chats = database.get_chats_with_routine()
    if (len(routine) > 0):
        for k in chats:
            resp = datetime.datetime.today().strftime('%d/%m/%Y') +"\nCe soir il y a : \n"
            for i in routine:
                if(k[0] == i[2]):
                    for j in planning[1]:
                        if(i[1].lower() in j[0].lower()):
                            resp += " - " +j[0] + " sur la " + chaine[j[2]] + " à " + j[1] + "\n"
            bot.send_message(chat_id=k[0], text=resp)


if __name__ == "__main__":
    main()