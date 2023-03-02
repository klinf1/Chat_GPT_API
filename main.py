import os
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


openai.api_key = os.environ.get('OPEN_AI_API_KEY')


class Chat:

    def __init__(self):
        self.messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'}
        ]

    def start_chat(self, message):
        self.messages.append(
            {'role': 'user', 'content': message}
        )
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self.messages,
            temperature=0.5,
        )
        self.messages.append(
            {
                'role': 'assistant',
                'content': response['choices'][0]['message'].content
            }
        )
        print(self.messages)
        return response['choices'][0]['message'].content


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hi! I am your OpenAI bot. How can I help you?'
    )


def initialize_class(update, context):
    new_instance = Chat()
    response = new_instance.start_chat(update.message.text)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response
    )


def main():
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
