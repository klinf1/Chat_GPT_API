import logging

import database
import messages
import menu


logger = logging.getLogger('logger')


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте! Чем я могу помочь?',
        reply_markup=menu.main_menu()
    )
    if not database.check_user_exists(update.effective_chat.id):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=messages.INFO_MESSAGE
        )
        database.insert_new_user(update.effective_chat.id)


def set_temperature(update, context):
    tempr = context.args[0]
    if type(context.args[0]) is str:
        if int(context.args[0][0]) > 1 or int(context.args[0][0]) < 0:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=('Значение температуры должно быть между '
                      '0 и 1. Пожалуйста, введите подходящее'
                      'значение')
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
                text=f'Значение температуры {temp} сохранено'
            )
            logger.info(
                f'temprerature setting {update.effective_chat.id} {temp} saved'
            )
        except Exception as error:
            logger.error(error)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=('Значение температуры должно быть числом '
                  'от 0 до единицы.')
        )


def set_system(update, context):
    new_system = ' '.join(context.args)
    to_update = {'system_message': new_system}
    try:
        database.update_user_data(to_update, update.effective_chat.id)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=('Новое системное сообщение сохранено!')
        )
        logger.info(f'new system message '
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
                text=('Текущее системное сообщение:\n'
                      f'{cur_message}.\n'
                      'Текущее значение температуры: '
                      f'{cur_temp}.')
            )
        logger.info(f'settings shown to '
                    f'{update.effective_chat.id}')
    except Exception as error:
        logger.error(error)


def clear_user_history(update, context):
    try:
        database.clean_user_history(update.effective_chat.id)
        logger.info(f'user {update.effective_chat.id} history cleaned')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=('История сообщений была успешно очищена')
        )
    except Exception as error:
        logger.error(error)


def clear_user_settings(update, context):
    try:
        database.clean_user_settings(update.effective_chat.id)
        logger.info(f'user {update.effective_chat.id} settings cleaned')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=('Настройки успешно сброшены')
        )
    except Exception as error:
        logger.error(error)
