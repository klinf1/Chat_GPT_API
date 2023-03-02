import os
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


openai.api_key = os.environ.get('OPEN_AI_API_KEY')


class Chat:

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.message_history = []

    def __repr__(self) -> str:
        return str(self.chat_id)

    def check_history(self):
        if len(self.message_history) > 6:
            self.message_history.pop(0)

    def start_chat(self, message):
        self.check_history()
        self.message_history.append(message)
        response = openai.Completion.create(
            model='gpt-3.5-turbo',
            prompt=str(self.message_history)+' '+message,
            max_tokens=4000,
            temperature=0.5,
        )
        self.check_history()
        self.message_history.append(response.choices[0].text.strip())
        return response.choices[0].text.strip()


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hi! I am your OpenAI bot. How can I help you?'
    )


def initialize_class(update, context):
    new_instance = Chat(update.effective_chat.id)
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
