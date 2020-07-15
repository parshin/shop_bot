import logging
import os
from conf import TOKEN
from conf import ALLOWED_USERS
from conf import PRICE_FILE_NAME
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import BaseFilter

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(levelname)-8s [%(asctime)s] %(message)s')
logger = logging.getLogger(__name__)


class FilterPrice(BaseFilter):
    def filter(self, message):
        return PRICE_FILE_NAME in message.document.file_name and message.chat.username in ALLOWED_USERS


def start(update, context):
    update.message.reply_text('Привет!')
    context.bot.send_message(chat_id=update.effective_chat.id, text="Я бот, который поможет тебе!")


def help_cmd(update, context):
    update.message.reply_text('Help!')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.error('error "%s" was caused by "%s"', context.error, update)
    context.bot.send_message(chat_id=update.effective_chat.id, text="error occured! "+context.error)


def log_message(update, context):
    logger.info(str(update.effective_chat) + " " +
                update.message.text)


def upload_price(update, context):
    logger.info('start uploading price')

    file = update.message.document.get_file()
    dir_name = os.path.dirname(__file__)
    f_name = os.path.join(dir_name, os.path.join(dir_name+'/prices/', update.message.document.file_name))
    file.download(custom_path=f_name)

    logger.info('price uploaded!')


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_cmd))

    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), log_message))

    filter_price = FilterPrice()
    dp.add_handler(MessageHandler(filter_price, upload_price))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
