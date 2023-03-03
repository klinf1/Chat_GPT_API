import os
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from database import message_history


openai.api_key = os.environ.get('OPEN_AI_API_KEY')


class Chat:

    def __init__(self):
        pass

    def mix_messages(self, chat_id):
        system = message_history.get_system_message(chat_id)
        sent = message_history.get_sent_messages(chat_id)
        recieved = message_history.get_recieved_messages(chat_id)
        messages = []
        if system[0].get('content'):
            messages.append(system[0])
        for i in range(0, len(sent)-1):
            messages.append(sent[i])
            messages.append(recieved[i])
        return messages

    def start_chat(self, update):
        messages = self.mix_messages(update.effective_chat.id)
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=message_history.get_temperature(
                update.effective_chat.id
            ),
        )
        token_usage = response['usage']['total_tokens']
        new_data = {
            'message_sent': update.message.text,
            'message_recieved': response['choices'][0]['message'].content
        }
        message_history.update_user_data(
            new_data,
            update.effective_chat.id
        )
        message_history.check_current_user_tokens(
            update.effective_chat.id,
            token_usage
        )
        return response['choices'][0]['message'].content


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hi! I am your OpenAI bot. How can I help you?'
    )
    message_history.insert_new_user(update.effective_chat.id)


def initialize_class(update, context):
    new_instance = Chat()
    response = new_instance.start_chat(update)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response
    )


def main():
    if not os.path.isfile('./message_history.db'):
        message_history.establish_database()
    updater = Updater(
        token=os.environ.get('TELEGRAM_BOT_TOKEN'),
        use_context=True
        )
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, initialize_class))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
