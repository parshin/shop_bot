import logging
import os
import telegram
from db import queries
from conf import TOKEN
from conf import ALLOWED_USERS
from conf import PRICE_FILE_NAME
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram.ext import BaseFilter

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(levelname)-8s [%(asctime)s] %(message)s')
logger = logging.getLogger(__name__)


class FilterPrice(BaseFilter):
    def filter(self, message):
        return PRICE_FILE_NAME in message.document.file_name and message.chat.username in ALLOWED_USERS


def start(update, context):
    # update.message.reply_text('Привет!')
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    button_list = [
        InlineKeyboardButton(u'\U0001F4D8'+" Каталог", callback_data='catalog'),
        InlineKeyboardButton(u'\U0001F4E6'+" Мои заказы", callback_data='orders')
    ]

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    update.message.reply_text("Привет, выбирай!", reply_markup=reply_markup)


def help_cmd(update, context):
    # todo написать текст справки
    update.message.reply_text('Help!')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.error('error "%s" was caused by "%s"', str(context.error), update)
    if update.message.chat.username in ALLOWED_USERS:
        context.bot.send_message(chat_id=update.effective_chat.id, text="error occured! "+str(context.error))


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


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def show_catalog(update, context):
    query = update.callback_query
    query.answer()
    button_list = []

    goods = queries.catalog()
    for row in goods:
        button_list.append(InlineKeyboardButton(text=u'\U0001f37a'+' '+row.good+', '+str(row.price)+'/'+row.measure,
                                                callback_data='cat'+row.good))

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    query.edit_message_text(
            text="Вот что мы можем тебе предложить:",
            reply_markup=reply_markup
        )


def button(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'catalog':
        show_catalog(update, context)
    elif query.data == 'orders':
        # todo orders
        pass


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_cmd))
    dp.add_handler(CommandHandler("show_catalog", show_catalog))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), log_message))
    dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_handler(CallbackQueryHandler(button))

    filter_price = FilterPrice()
    dp.add_handler(MessageHandler(filter_price, upload_price))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
