import os

from datetime import date
from dotenv import load_dotenv
import gspread
import logging
from links import *
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

load_dotenv()

secret_token = os.getenv('TOKEN')
mykey = os.getenv('KEY')
link = os.getenv('LINK')
googlesheet_id = os.getenv('GOOGLE')
gc = gspread.service_account(filename='service_account.json')

buttons = ReplyKeyboardMarkup([['/book'],
                                   ['/rebook', '/feedback']
                                  ], resize_keyboard=True)
updater = Updater(token=secret_token, use_context=True)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(update, context):
    chat = update.effective_chat
    buttn = ReplyKeyboardMarkup([['/start']], resize_keyboard=True)
    context.bot.send_message(chat_id=chat.id, text='Please push the start button 🚀', reply_markup=buttn
    )


def say_hi(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    context.bot.send_message(chat_id=chat.id, text=f'Hi {name} 👋, I\'m EgoClub Bot! Please choose the right option',
                             reply_markup=buttons)


def send_schedule(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat.id, links,
                             parse_mode='Markdown')


"""def polling_start(bot, update):
    bot.message.reply_text('What\'s your full name?', reply_markup=ReplyKeyboardRemove())
    return 'user_name'


def polling_get_name(bot, update):
    update.user_data['user_name'] = bot.message.text
    bot.message.reply_text('What is your email?')
    user_name = bot.message.text
    today = date.today().strftime("%d.%m.%Y")
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1IOAJVfXKZu0dIPT13zWw1_IMIeW2TubND2PMMlnuTMQ/edit#gid=0')
    sh.sheet1.append_row([today, user_name])
    return 'user_email'


def polling_get_email(bot, update):
    update.user_data['user_email'] = bot.message.text
    user_email = bot.message.text
    column = 3
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1IOAJVfXKZu0dIPT13zWw1_IMIeW2TubND2PMMlnuTMQ/edit#gid=0')
    last_row = len(sh.sheet1.get_all_values())
    sh.sheet1.update_cell(last_row, column, user_email)
    bot.message.reply_text('What is your phone number?'),
    return 'user_phone'


def polling_get_phone(bot, update):
    update.user_data['user_phone'] = bot.message.text
    user_phone = bot.message.text
    column = 4
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1IOAJVfXKZu0dIPT13zWw1_IMIeW2TubND2PMMlnuTMQ/edit#gid=0')
    last_row = len(sh.sheet1.get_all_values())
    sh.sheet1.update_cell(last_row, column, user_phone)
    bot.message.reply_text('What company do you work for?')
    return 'company_name'


def polling_get_company(bot, update):
    update.user_data['company_name'] = bot.message.text
    company_name = bot.message.text
    column = 5
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1IOAJVfXKZu0dIPT13zWw1_IMIeW2TubND2PMMlnuTMQ/edit#gid=0')
    last_row = len(sh.sheet1.get_all_values())
    sh.sheet1.update_cell(last_row, column, company_name)
    reply_keyboard = ReplyKeyboardMarkup([['/yes'],
                                          ['/no']
                                          ], resize_keyboard=True)
    bot.message.reply_text('Join the nearest club?', reply_markup=reply_keyboard)
    return 'come_soon'


def see_you(bot, update):
    update.user_data['come_soon'] = bot.message.text
    come_soon = bot.message.text
    column = 6
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1IOAJVfXKZu0dIPT13zWw1_IMIeW2TubND2PMMlnuTMQ/edit#gid=0')
    last_row = len(sh.sheet1.get_all_values())
    sh.sheet1.update_cell(last_row, column, come_soon)
    if bot.message.text == '/yes':
        bot.message.reply_text('See you at the club! ✅', reply_markup=buttons)
        return ConversationHandler.END
    else:
        bot.message.reply_text('When does it work for you to join? 📅', reply_markup=ReplyKeyboardRemove())
        return 'planned'


def polling_exit(bot, update):
    update.user_data['planned'] = bot.message.text
    planned = bot.message.text
    column = 7
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1IOAJVfXKZu0dIPT13zWw1_IMIeW2TubND2PMMlnuTMQ/edit#gid=0')
    last_row = len(sh.sheet1.get_all_values())
    sh.sheet1.update_cell(last_row, column, planned)
    bot.message.reply_text('All set! We\'ll send you the reminder! ✅', reply_markup=buttons)
    return ConversationHandler.END"""


def get_feedback(bot, update):
    bot.message.reply_text('I\'ll be glad to receive your feedback to get better 😸', reply_markup=ReplyKeyboardRemove())
    return 'get_feedback'


def feedback_taken(bot, update):
    update.user_data['get_feedback'] = bot.message.text
    get_feedback = bot.message.text
    name = bot.message.from_user.username
    today = date.today().strftime("%d.%m.%Y")
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1IOAJVfXKZu0dIPT13zWw1_IMIeW2TubND2PMMlnuTMQ/edit#gid=1928277420').worksheet('sheet2')
    sh.append_row([today, name,  get_feedback])
    bot.message.reply_text('Thanks for your feedback! 😸', reply_markup=buttons)
    return ConversationHandler.END


def get_unbooked(bot, update):
    bot.message.reply_text('Which of the booked classes would you like to rebook?')
    return 'get_unbooked'


def unbooking_taken(bot, update):
    update.user_data['get_unbooked'] = bot.message.text
    get_unbooked = bot.message.text
    name = bot.message.from_user.username
    today = date.today().strftime("%d.%m.%Y")
    sh = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1IOAJVfXKZu0dIPT13zWw1_IMIeW2TubND2PMMlnuTMQ/edit#gid=1928277420').worksheet(
        'sheet3')
    sh.append_row([today, name, get_unbooked])
    bot.message.reply_text('Done ✅ Our manager will contact you!', reply_markup=buttons)
    return ConversationHandler.END


def dontknow(bot, update):
    bot.message.reply_text('I don\t understand you, please type you answer!')


updater.dispatcher.add_handler(CommandHandler('start', say_hi))
updater.dispatcher.add_handler(CommandHandler('book', send_schedule))
updater.dispatcher.add_handler(
    ConversationHandler(entry_points=[CommandHandler('feedback', get_feedback)],
                        states={'get_feedback': [MessageHandler(Filters.text, feedback_taken)]},
                        fallbacks=[MessageHandler(
                                    Filters.video | Filters.photo | Filters.document | Filters.sticker, dontknow)]
                                )
)
updater.dispatcher.add_handler(
    ConversationHandler(entry_points=[CommandHandler('rebook', get_unbooked)],
                        states={'get_unbooked': [MessageHandler(Filters.text, unbooking_taken)]},
                        fallbacks=[MessageHandler(
                                    Filters.video | Filters.photo | Filters.document | Filters.sticker, dontknow)]
                                )
)
updater.dispatcher.add_handler(MessageHandler(Filters.text | Filters.sticker, start))
updater.start_polling()
updater.idle()
