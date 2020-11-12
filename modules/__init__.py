import os
import telegram
from telegram.ext import Updater

actualDir = os.path.dirname(os.path.realpath(__file__))
parentDir = os.path.abspath(os.path.join(actualDir, os.pardir))
t = open(parentDir+"/file/token", 'r').read().rstrip()
updater = Updater(token=t)
disp = updater.dispatcher
bt = telegram.Bot(token=t)
job = updater.job_queue