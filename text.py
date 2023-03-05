import logging

import openai

import database

logger = logging.getLogger('logger')


class Chat:

    def __init__(self):
        pass

    def mix_messages(self, chat_id, current_message):
        try:
            system = database.get_system_message(chat_id)
            sent = database.get_sent_messages(chat_id)
            recieved = database.get_recieved_messages(chat_id)
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
                temperature=database.get_temperature(
                    update.effective_chat.id
                ),
            )
            logger.info(f'api request success from {update.effective_chat.id}')
        except Exception as error:
            logger.error(error)
        return response


def initialize_class(update, context):
    new_instance = Chat()
    if not database.check_user_exists(update.effective_chat.id):
        database.insert_new_user(update.effective_chat.id)
    response = new_instance.start_chat(update)
    token_usage = response['usage']['total_tokens']
    new_data = {
        'message_sent': update.message.text,
        'message_recieved': response['choices'][0]['message'].content
    }
    try:
        database.update_user_data(
            new_data,
            update.effective_chat.id
        )
    except Exception as error:
        logger.error(error)
    try:
        database.check_current_user_tokens(
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
