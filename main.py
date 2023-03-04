import os
import logging

from logging.handlers import RotatingFileHandler

import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

from database import message_history

load_dotenv()
openai.api_key = os.getenv('OPEN_AI_API_KEY')
logger = logging.getLogger(__name__)


class Chat:

    def __init__(self):
        pass

    def mix_messages(self, chat_id, current_message):
        try:
            system = message_history.get_system_message(chat_id)
            sent = message_history.get_sent_messages(chat_id)
            recieved = message_history.get_recieved_messages(chat_id)
        except Exception as error:
            logger.error(error)
        messages = []
        if system[0].get('content'):
            messages.append(system[0])
        if len(sent) != 0 and len(recieved) != 0:
            for i in range(0, len(sent)-1):
                messages.append(sent[i])
                messages.append(recieved[i])
        messages.append({'role': 'user', 'content': current_message})
        return messages

    def start_chat(self, update):
        messages = self.mix_messages(
            update.effective_chat.id,
            update.message.text
        )
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=messages,
                temperature=message_history.get_temperature(
                    update.effective_chat.id
                ),
            )
            logger.info(f'api request success from {update.effective_chat.id}')
        except Exception as error:
            logger.error(error)
        return response


def set_temperature(update, context):
    tempr = context.args[0]
    if type(context.args[0]) == str:
        if int(context.args[0][0]) > 1 or int(context.args[0][0]) < 0:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=('Temperature should be between 0 and 1, '
                      'please provide a valid number')
                )
        if context.args[0][1] == ',':
            tempr = context.args[0].replace(',', '.')
    if 0 <= float(tempr) <= 1:
        try:
            message_history.update_user_data(
                {'temperature': tempr},
                update.effective_chat.id
            )
            temp = message_history.get_temperature(update.effective_chat.id)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'Temperature setting {temp} saved'
            )
            logger.info(
                f'temprerature setting {update.effective_chat.id} {temp} saved'
            )
        except Exception as error:
            logger.error(error)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=('Temperature should be between 0 and 1, '
                  'please provide a valid number')
        )


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hi! I am your OpenAI bot. How can I help you?'
    )
    if not message_history.check_user_exists(update.effective_chat.id):
        message_history.insert_new_user(update.effective_chat.id)


def initialize_class(update, context):
    new_instance = Chat()
    if not message_history.check_user_exists(update.effective_chat.id):
        message_history.insert_new_user(update.effective_chat.id)
    response = new_instance.start_chat(update)
    token_usage = response['usage']['total_tokens']
    new_data = {
        'message_sent': update.message.text,
        'message_recieved': response['choices'][0]['message'].content
    }
    try:
        message_history.update_user_data(
            new_data,
            update.effective_chat.id
        )
    except Exception as error:
        logger.error(error)
    try:
        message_history.check_current_user_tokens(
            update.effective_chat.id,
            token_usage
        )
    except Exception as error:
        logger.error(error)
    try:
        message = response['choices'][0]['message'].content
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )
        logger.info(f'message sent to {update.effective_chat.id}')
    except Exception as error:
        logger.error(error)


def main():
    if not os.path.isfile('./message_history.db'):
        try:
            message_history.establish_database()
        except Exception as error:
            logger.error(error)

    updater = Updater(
        token='5566222876:AAGH46ramuGEjqQ14iQyyIT9vTThSELGXsU',
        use_context=True
        )
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler(
        'settemperature',
        set_temperature,
        pass_args=True
    ))
    dispatcher.add_handler(MessageHandler(Filters.text, initialize_class))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(
        'my_logger.log',
        maxBytes=50000000,
        backupCount=5
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(lineno)s - %(funcName)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    main()
