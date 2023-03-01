import os
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# from dotenv import load_dotenv

# load_dotenv()

# Set up the OpenAI API credentials
openai.api_key = os.environ.get('OPEN_AI_API_KEY')


# Define the Telegram bot handler functions
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hi! I am your OpenAI bot. How can I help you?'
    )


def echo(update, context):
    response = get_response(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def get_response(text):
    # Use the OpenAI API to generate a response
    response = openai.Completion.create(
        engine="davinci", prompt=text, max_tokens=50
    )
    return response.choices[0].text.strip()


# Set up the Telegram bot updater and start the bot
def main():

    # Create the Telegram bot updater
    updater = Updater(
        token=os.environ.get('TELEGRAM_BOT_TOKEN'),
        use_context=True
        )

    # Add the Telegram bot handler functions
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # Start the Telegram bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
