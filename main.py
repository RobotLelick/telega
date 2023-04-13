import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(f"Я получил сообщение {update.message.text}")


def main():
    application = Application.builder().token("5984109328:AAFeAFoXxCUNjBDexEhkd3SZBldAp4bX1_A").build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(text_handler)

    application.run_polling()


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}, какой предмет ты выберешь для подготовки?",
    )
    return 1


async def help(update, context):
    await update.message.reply_text(
        "Я бот, который поможет тебе в подготовке к ЕГЭ, доступные предметы: русский язык, математика")


async def first_response(update, context):
    subject = update.message.text
    if subject == 'математика' or subject == 'русский язык':
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
        context.user_data['subject'] = activity
        return 3
    else:
        await update.message.reply_text(
            "Я меня нет такой функции, попробуй ещё раз ответить на мой вопрос",
        )
        return 2


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END

if __name__ == '__main__':
    main()