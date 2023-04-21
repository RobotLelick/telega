import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def create_list_for_keyboard(subject, activity):
    con = sqlite3.connect("basa.sqlite")
    cur = con.cursor()
    if activity == 'решить тест':
        act = f'{subject}_тест'
    else:
        act = f'{subject}_теория'
    ans = []
    ids = create_id(subject, activity)
    for i in ids:
        id_topic = int(i[i.find('a') + 1:])
        s = cur.execute(f"""SELECT topic FROM {act}
                            WHERE id == {id_topic}""").fetchone()
        ans.append([s[0], i])
    return ans


def create_id(subject, activity):
    con = sqlite3.connect("basa.sqlite")
    cur = con.cursor()
    if activity == 'решить тест':
        act = f'{subject}_тест'
    else:
        act = f'{subject}_теория'

    result = cur.execute(f"""SELECT id FROM {act}""").fetchall()
    if subject == 'информатика':
        n = 1
    elif subject == 'русский_язык':
        n = 2
    ans = []
    for i in result:

        ans.append(f'/id{n}a{i[0]}')
    return ans



#Update(message=Message(channel_chat_created=False, chat=Chat(first_name='Кирилл', id=1335956971, type=<ChatType.PRIVATE>, username='Robot_Lelick'), date=datetime.datetime(2023, 4, 21, 13, 39, 18, tzinfo=<UTC>), delete_chat_photo=False, entities=(MessageEntity(length=5, offset=0, type=<MessageEntityType.BOT_COMMAND>),), from_user=User(first_name='Кирилл', id=1335956971, is_bot=False, language_code='ru', username='Robot_Lelick'), group_chat_created=False, message_id=1420, supergroup_chat_created=False, text='/help'), update_id=900667246)
#Update(callback_query=CallbackQuery(chat_instance='7788077369452036630', data='/id2a2', from_user=User(first_name='Кирилл', id=1335956971, is_bot=False, language_code='ru', username='Robot_Lelick'), id='5737891500879244313', message=Message(channel_chat_created=False, chat=Chat(first_name='Кирилл', id=1335956971, type=<ChatType.PRIVATE>, username='Robot_Lelick'), date=datetime.datetime(2023, 4, 21, 13, 40, 2, tzinfo=<UTC>), delete_chat_photo=False, from_user=User(first_name='Бот для подготовки к ЕГЭ', id=5984109328, is_bot=True, username='lelick_and_omarik_exam_bot'), group_chat_created=False, message_id=1429, reply_markup=InlineKeyboardMarkup(inline_keyboard=((InlineKeyboardButton(callback_data='/id2a2', text='fsdfds'),),)), supergroup_chat_created=False, text='Я бот-справочник. Какая информация вам нужна?')), update_id=900667251)
