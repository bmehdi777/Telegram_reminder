# Telegram_rappel

A bot for Telegram written in python. Its main purpose is to remember you when a program tv is up.

## Getting started
### Prerequisites
Install pip package :
- xmltodict
- python-telegram-bot

You can install them manually or use the :
>pip install -r requirement

### Installing
You need to add a "bdd.db" in the bdd folder. This database use sqlite3.
You can install it by doing this : 

>sqlite3 bdd.db
>.database (to see if it has been created)
>.exit

## Built with

- Python
- Telegram-API

## Command of the bot

- >/help
    - Show the list of command
- >/chaine
    - Show the list of channel available
- >/prime \[channel\]
    - Show the TV program of all the channel available or of the \[channel\] tonight 
