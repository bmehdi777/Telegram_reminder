import telegram 
from telegram.ext import Updater

t = open("file/token", 'r').read().rstrip()
updater = Updater(token=t)
disp = updater.dispatcher
bt = telegram.Bot(token=t)
job = updater.job_queue