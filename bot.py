# -*- coding: utf-8 -*-
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)
from telegram.ext import (Updater, CommandHandler, MessageHandler, 
							Filters, JobQueue, CallbackQueryHandler)
from telegram import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, 
			InlineKeyboardButton, InputMediaPhoto)
from update_stats import update_pages
import logging, os

with open('secret.token', 'r') as f:
	TOKEN = f.read().split()[1]

logging.basicConfig(filename='log.log',level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

jobQ = JobQueue()
jobQ.set_dispatcher(dispatcher)
jobQ.run_repeating(update_pages, interval=1800, first=0)
jobQ.start()

def start(update, context):
	num_of_images = len(os.listdir('./pages'))

	keyboard = [
				[
					InlineKeyboardButton('⬅', callback_data="p 0"),
					InlineKeyboardButton('🔄', callback_data="p 1"),
					InlineKeyboardButton('➡', callback_data="p 2")
				],
				[
					InlineKeyboardButton('⏮', callback_data="p 1"),
					InlineKeyboardButton('⏭', callback_data="p %s" % num_of_images)
				]
			]
	reply_markup = InlineKeyboardMarkup(keyboard)

	with open('./pages/out1.jpg', 'rb') as img:
			context.bot.send_photo(chat_id=update.effective_chat.id,
			reply_markup=reply_markup,
			photo=img)

	return logging.info('[INFO] Start function executed successfully!')

def button(update, context):
	query = update.callback_query

	if query.data[0] == 'p':
		n = int(query.data.split()[1])

		num_of_images = len(os.listdir('./pages'))
		n = 1 if n <= 0 else n
		n = num_of_images if n > num_of_images else n

		keyboard = [
				[
					InlineKeyboardButton('⬅', callback_data="p %s" % (n-1)),
					InlineKeyboardButton('🔄', callback_data="p %s" % n),
					InlineKeyboardButton('➡', callback_data="p %s" % (n+1))
				],
				[
					InlineKeyboardButton('⏮', callback_data="p 1"),
					InlineKeyboardButton('⏭', callback_data="p %s" % num_of_images)
				]
			]

		reply_markup = InlineKeyboardMarkup(keyboard)

		with open('./pages/out%s.jpg' % n, 'rb') as img:
			return context.bot.edit_message_media(chat_id=update.effective_chat.id,
				message_id=query.message.message_id,
				media=InputMediaPhoto(img),
				reply_markup=reply_markup)

def msgCallback(update, context):
	logging.info(update.message.text)
	return context.bot.send_message(chat_id=update.effective_chat.id, 
		text='Type /start to use bot')

def error(update, context):
    """Log Errors caused by Updates."""
    if 'Message is not modified' in context.error:
    	pass
    else:
    	logging.warning('Update "%s" caused error "%s" of type "%s"', update, context.error)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

msg_handler = MessageHandler(Filters.text, msgCallback)
dispatcher.add_handler(msg_handler)

dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()