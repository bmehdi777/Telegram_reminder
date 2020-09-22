# Telegram_rappel

A bot for Telegram written in python. Its main purpose is to remember you when a program tv is up.

## Getting started
### Prerequisites
Install pip package :
- xmltodict
- python-telegram-bot

You can install them manually or use the :
>pip install -r requirement

### Start the project

First of all, you need to put your token in the file file/token (it is IMPORTANT).

You have to execute main.py to start the bot. If you want to have the reminder part, you need to launch with cron the routine.py. It'll send message to every chat with a reminder set up.


## Built with

- Python
- Telegram-API

## Command of the bot

- >/start
    - Start the bot (important)
- >/stop
    - Stop the bot

- >/help
    - Show the list of command
- >/chaine
    - Show the list of channel available
- >/prime \[channel\]
    - Show the TV program of all the channel available or of the \[channel\] tonight
- >/rappel \<program\>
    - Add a program to the reminder
- >/showrappel
    - Show all of the reminder that the user has set up
- >/removerappel \<number of the reminder\>
    - Remove the reminder with this number
