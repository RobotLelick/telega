import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram.ext import CallbackQueryHandler
from help_function import create_list_for_keyboard
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)
up = 0
con = 0


async def echo(update, context):
    await update.message.reply_text(f"Я получил сообщение {update.message.text}")


async def start(update, context):
    global up, con
    up = update
    con = context
    con = sqlite3.connect("basa.sqlite")
    cur = con.cursor()
    print( cur.execute(f"""SELECT name FROM sqlite_master WHERE type='table';""").fetchall())
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}, какой предмет ты выберешь для подготовки?",
    )
    return 1


async def help(update, context):
    await update.message.reply_text(
        "Я бот, который поможет тебе в подготовке к ЕГЭ, доступные предметы: русский язык, информатика")


async def for_id(update, context):
    s = update.callback_query.data
    global up
    con = sqlite3.connect("basa.sqlite")
    cur = con.cursor()
    table = s[3:s.find('a')]
    id = s[s.find('a') + 1]
    if table == '1':
        table = 'информатика_теория'
    elif table == '2':
        table = 'русский_язык_теория'
    result = cur.execute(f"""SELECT rule FROM {table}
                             WHERE id == {id}""").fetchall()
    await up.message.reply_text(f'{result[0]}')


async def first_response(update, context):
    subject = update.message.text
    if subject == 'информатика' or subject == 'русский язык':
        if subject == 'русский язык':
            context.user_data['subject'] = 'русский_язык'
        else:
            context.user_data['subject'] = subject
        await update.message.reply_text(
            "Как ты хочешь начать подготовку: посмотреть теорию или решить тест?",
        )
        return 2
    else:
        await update.message.reply_text(
            "Я не знаю такого предмета, попробуй ещё раз ответить на мой вопрос",
        )
        return 1


async def second_response(update, context):
    activity = update.message.text
    if activity == 'посмотреть теорию' or activity == 'решить тест':
        context.user_data['activity'] = activity
        await update.message.reply_text(
            "Введите любое сообщение для продолжения",
        )
        return 3
    else:
        await update.message.reply_text(
            "Я меня нет такой функции, попробуй ещё раз ответить на мой вопрос",
        )
        return 2


async def create_keyboard(update, context):
    mas = create_list_for_keyboard(context.user_data['subject'], context.user_data['activity'])
    buttons = []
    for i in mas:
        button = InlineKeyboardButton(i[0], callback_data=i[1])
        buttons.append([button])
    #button = [[InlineKeyboardButton('fsdfds', callback_data='/id2a2')]]
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        "Я бот-справочник. Какая информация вам нужна?", reply_markup=markup
    )


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    application = Application.builder().token("5984109328:AAFeAFoXxCUNjBDexEhkd3SZBldAp4bX1_A").build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_keyboard)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CallbackQueryHandler(for_id))
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(MessageHandler(filters.Regex(r'/id'), for_id))
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()