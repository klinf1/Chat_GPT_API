from telegram import KeyboardButton, ReplyKeyboardMarkup


def main_menu():
    buttons = [
        [KeyboardButton('/info')],
        [KeyboardButton('/viewsettings')],
        [KeyboardButton('/clearsettings')],
        [KeyboardButton('/clearhistory')]
    ]
    return ReplyKeyboardMarkup(buttons)
