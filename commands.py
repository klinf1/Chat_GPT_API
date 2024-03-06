import logging

import database
import messages
import menu


logger = logging.getLogger('logger')


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hi! I am your OpenAI bot. How can I help you?',
        reply_markup=menu.main_menu()
    )
    if not database.check_user_exists(update.effective_chat.id):
        database.insert_new_user(update.effective_chat.id)


def set_temperature(update, context):
    tempr = context.args[0]
    if type(context.args[0]) is str:
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
            database.update_user_data(
                {'temperature': tempr},
                update.effective_chat.id
            )
            temp = database.get_temperature(update.effective_chat.id)
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


def set_system(update, context):
    new_system = ' '.join(context.args)
    to_update = {'system_message': new_system}
    try:
        database.update_user_data(to_update, update.effective_chat.id)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=('New system message saved!')
        )
        logger.info(f'new system message "{new_system}" '
                    f'for {update.effective_chat.id} set')
    except Exception as error:
        logger.error(error)


def info(update, context):
    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=messages.INFO_MESSAGE
        )


def view_settings(update, context):
    cur_message = database.get_system_message(
        update.effective_chat.id
    )[0].get('content')
    cur_temp = database.get_temperature(update.effective_chat.id)
    try:
        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=('Your cuurent system message is:\n'
                      f'{cur_message}.\n'
                      'Your current temperature is '
                      f'{cur_temp}.')
            )
        logger.info(f'settings {cur_message}, {cur_temp} shown to '
                    f'{update.effective_chat.id}')
    except Exception as error:
        logger.error(error)


def clear_user_history(update, context):
    try:
        database.clean_user_history(update.effective_chat.id)
        logger.info(f'user {update.effective_chat.id} history cleaned')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=('Your message history has '
                  'been cleared successfully.')
        )
    except Exception as error:
        logger.error(error)


def clear_user_settings(update, context):
    try:
        database.clean_user_settings(update.effective_chat.id)
        logger.info(f'user {update.effective_chat.id} settings cleaned')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=('Your settings have '
                  'been cleared successfully.')
        )
    except Exception as error:
        logger.error(error)
