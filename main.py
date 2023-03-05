import os

import openai
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import commands
import database
import text
import logs

load_dotenv()
openai.api_key = os.getenv('OPEN_AI_API_KEY')


def main():
    if not os.path.isfile('./message_history.db'):
        try:
            database.establish_database()
        except Exception as error:
            logger.error(error)

    updater = Updater(
        token=os.getenv('TELEGRAM_BOT_TOKEN'),
        use_context=True
        )
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler(
        'info',
        commands.info
    ))
    dispatcher.add_handler(CommandHandler(
        'setsystem',
        commands.set_system,
        pass_args=True
    ))
    dispatcher.add_handler(CommandHandler(
        'start',
        commands.start
    ))
    dispatcher.add_handler(CommandHandler(
        'settemperature',
        commands.set_temperature,
        pass_args=True
    ))
    dispatcher.add_handler(MessageHandler(Filters.text, text.initialize_class))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logger = logs.set_up_logger('logger')
    main()
