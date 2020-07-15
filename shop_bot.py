import logging
from conf import TOKEN
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(levelname)-8s [%(asctime)s] %(message)s')
logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Привет!')
    context.bot.send_message(chat_id=update.effective_chat.id, text="Я бот, который поможет тебе!")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.error('error "%s" was caused by "%s"', context.error, update)
    context.bot.send_message(chat_id=update.effective_chat.id, text="error occured! "+context.error)


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
