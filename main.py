import telegram

from modules import updater
from modules import disp

import logging

from modules import command

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main():
    for handler in command.Command.handlers:
        disp.add_handler(handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()