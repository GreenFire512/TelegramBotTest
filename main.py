from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
from token_file import token
import re

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

AGE_QUESTION, AGE_ANSWER, HEIGHT_QUESTION, HEIGHT_ANSWER = range(4)
age: int = 0
height: int = 0


def help(update, context):
    update.message.reply_text('Напишите комманду /start')


def start(update: Update, _: CallbackContext) -> int:
    keyboard = [
        [
            InlineKeyboardButton('Вычислить', callback_data='1')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Привет! Выбери пункт:', reply_markup=reply_markup)
    return AGE_QUESTION


def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_text('Отмена')
    return ConversationHandler.END


def user_age_question(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text('Введите свой возраст')
    return AGE_ANSWER


def user_age_answer(update: Update, _: CallbackContext) -> int:
    if re.match(r"^[0-9]+$", update.message.text):
        age = int(update.message.text)
        update.message.reply_text('Введи свой рост')
        return HEIGHT_ANSWER
    else:
        update.message.reply_text('Вы ввели неправильный возраст')
        return AGE_ANSWER


def user_height(update: Update, _: CallbackContext) -> int:
    if re.match(r'^[0-9]+$', update.message.text):
        height = int(update.message.text)
        result = 50 + 0.75*(height - 150) + (age - 20)/4
        update.message.reply_text(f'Ваш идеальный вес: {result}')
        return ConversationHandler.END
    else:
        update.message.reply_text('Вы ввели неправильный рост')
        return HEIGHT_ANSWER



def main():
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGE_QUESTION: [CallbackQueryHandler(user_age_question)],
            AGE_ANSWER: [MessageHandler(Filters.text, user_age_answer)],
            HEIGHT_ANSWER: [MessageHandler(Filters.text, user_height)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(conversation_handler)
    #
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()







