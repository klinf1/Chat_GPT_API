import sqlite3
import functools
import operator

from . import utils


FIELDS_TO_EDIT = ('messages_sent', 'messages_recieved', 'system_message', 'temperature')


def get_connection():
    con = sqlite3.connect('message_history.db')
    cur = con.cursor()
    return con, cur


def establish_database():
    con, cur = get_connection()
    cur.execute('''CREATE TABLE message_history
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id NOT NULL,
                    messages_sent DEFAULT ' ',
                    messages_recieved DEFAULT ' ',
                    system_message DEFAULT 'You are a helpful assistant',
                    temperature DEFAULT 0.5,
                    tokens_used INTEGER)
    ''')
    con.commit()
    con.close()


def update_user_data(data: dict, chat_id):
    con, cur = get_connection()
    if 'temperature' in data.keys():
        to_update = [data.get('temperature'), chat_id]
        cur.execute('''UPDATE message_history SET temperature = ? WHERE chat_id = ? ''', to_update)
        con.commit()
    if 'message_sent' in data.keys():
        to_update = [data.get('message_sent'), chat_id]
        cur.execute('''UPDATE message_history SET messages_sent = messages_sent||'<&>'||? WHERE chat_id = ?''', to_update)
        con.commit()
    if 'message_recieved' in data.keys():
        to_update = [data.get('message_recieved'), chat_id]
        cur.execute('''UPDATE message_history SET messages_recieved = messages_recieved||'<&>'||? WHERE chat_id = ?''', to_update)
        con.commit()
    if 'system_message' in data.keys():
        to_update = [data.get('system_message'), chat_id]
        cur.execute('''UPDATE message_history SET system_message = ? WHERE chat_id = ? ''', to_update)
        con.commit()
    con.close()


def get_current_user_tokens(chat_id: int, cur):
    chat_id = [chat_id]
    current_tokens = cur.execute('''SELECT tokens_used FROM message_history WHERE chat_id = ?''', chat_id).fetchall()
    if current_tokens[0][0]:
        return current_tokens[0][0]
    return 0


def update_user_tokens(chat_id, usage, con, cur):
    current_usage = get_current_user_tokens(chat_id, cur)
    if current_usage != 0:
        total = usage + current_usage
    else:
        total = usage
    total = [total, chat_id]
    cur.execute('''UPDATE message_history SET tokens_used = ? WHERE chat_id = ? ''', total)
    con.commit()


def insert_new_user(chat_id):
    con, cur = get_connection()
    data = [chat_id]
    cur.execute('''INSERT INTO message_history (chat_id) VALUES (?)''', data)
    con.commit()
    con.close()


def clean_user_data(chat_id):
    con, cur = get_connection()
    data = [chat_id]
    cur.execute('''UPDATE message_history SET temperature = 0.5 WHERE chat_id = ? ''', data)
    cur.execute('''UPDATE message_history SET messages_sent = '' WHERE chat_id = ? ''', data)
    cur.execute('''UPDATE message_history SET messages_recieved = '' WHERE chat_id = ? ''', data)
    cur.execute('''UPDATE message_history SET system_message = '' WHERE chat_id = ? ''', data)
    con.commit()
    con.close()


def check_current_user_tokens(chat_id, usage):
    con, cur = get_connection()
    update_user_tokens(chat_id, usage, con, cur)
    current_usage = get_current_user_tokens(chat_id, cur)
    if current_usage > 2000:
        messages_sent = cur.execute('''SELECT messages_sent FROM message_history WHERE chat_id = ?''', [chat_id]).fetchall()
        messages_sent = functools.reduce(operator.add, messages_sent[0])
        messages_recieved = cur.execute('''SELECT messages_recieved FROM message_history WHERE chat_id = ?''', [chat_id]).fetchall()
        messages_recieved = functools.reduce(operator.add, messages_recieved[0])
        data_new_sent = [utils.cut_string_beginning(messages_sent), chat_id]
        data_new_recieved = [utils.cut_string_beginning(messages_recieved), chat_id]
        cur.execute('''UPDATE message_history SET messages_sent = ? WHERE chat_id = ? ''', data_new_sent)
        cur.execute('''UPDATE message_history SET messages_recieved = ? WHERE chat_id = ? ''', data_new_recieved)
        con.commit()
        deleted_sent = utils.cut_string_end(messages_sent)
        deleted_recieved = utils.cut_string_end(messages_recieved)
        freed_tokens = utils.get_token_count(deleted_sent) + utils.get_token_count(deleted_recieved)
        freed_tokens = (0 - freed_tokens)
        update_user_tokens(chat_id, freed_tokens, con, cur)
    con.close()


def get_sent_messages(chat_id):
    con, cur = get_connection()
    chat_id = [chat_id]
    sent = cur.execute('''SELECT messages_sent FROM message_history WHERE chat_id = ?''', chat_id).fetchall()
    if sent[0][0]:
        sent = str(sent).split('<&>')
    sent_journal = []
    for item in sent:
        sent_journal.append({'role': 'user', 'content': item})
    con.close()
    return sent_journal


def get_recieved_messages(chat_id):
    con, cur = get_connection()
    chat_id = [chat_id]
    recieved = cur.execute('''SELECT messages_recieved FROM message_history WHERE chat_id = ?''', chat_id).fetchall()
    if recieved[0][0]:
        recieved = str(recieved).split('<&>')
    recieved_journal = []
    for item in recieved:
        recieved_journal.append({'role': 'assistant', 'content': item})
    con.close()
    return recieved_journal


def get_system_message(chat_id):
    con, cur = get_connection()
    chat_id = [chat_id]
    system_message = cur.execute('''SELECT system_message FROM message_history WHERE chat_id = ?''', chat_id).fetchall()
    if system_message[0][0]:
        system_message = functools.reduce(operator.add, system_message[0])
        system_list = [{'role': 'system', 'content': system_message}]
    else:
        system_list = [{'role': 'system', 'content': None}]
    con.close()
    return system_list


def get_temperature(chat_id):
    con, cur = get_connection()
    chat_id = [chat_id]
    temp = cur.execute('''SELECT temperature FROM message_history WHERE chat_id = ?''', chat_id).fetchall()
    temp = float(functools.reduce(operator.add, temp[0]))
    con.close()
    return temp


def check_user_exists(chat_id):
    con, cur = get_connection()
    users = cur.execute('''SELECT chat_id FROM message_history''').fetchall()
    if (chat_id,) not in users:
        con.close()
        return False
    con.close()
    return True
