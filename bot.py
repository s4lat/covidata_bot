from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue
from telegram import ReplyKeyboardMarkup, KeyboardButton
from update_stats import update_pages
import logging, os

with open('secret.token', 'r') as f:
	TOKEN = f.read().split()[1]

logging.basicConfig(filename='log.log',level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

jobQ = JobQueue()
jobQ.set_dispatcher(dispatcher)
jobQ.run_repeating(update_pages, interval=54000, first=0)
jobQ.start()

def start(update, context):
	with open('./pages/out1.jpg', 'rb') as img:
			context.bot.send_photo(chat_id=update.effective_chat.id,
			photo=img)
	
	num_of_images = len(os.listdir('./pages'))

	keyboard = [['/page 1', '/page 2'],
						['/page 1', '/page %s' % num_of_images]]
	reply_markup = ReplyKeyboardMarkup(keyboard)

	logging.info('[INFO] Start function executed successfully!')
	return context.bot.send_message(chat_id=update.effective_chat.id, 
		text="Use keyboard below", 
		reply_markup=reply_markup)

def show_data(update, context):
	msg = update.message.text.split()
	try:
		n = int(msg[1])

	except ValueError:
		logging.error('[ERROR][ValueError] User send bad query: %s' % ' '.join(msg))
		return context.bot.send_message(chat_id=update.effective_chat.id,
			text="[ERROR] Please use buttons, not manual commands")

	try:
		num_of_images = len(os.listdir('./pages'))
		n = 1 if n <= 0 else n
		n = num_of_images if n > num_of_images else n

		with open('./pages/out%s.jpg' % n, 'rb') as img:
			keyboard = [['/page %s' % (n-1), '/page %s' % (n+1)],
						['/page 1', '/page %s' % num_of_images]]

			reply_markup = ReplyKeyboardMarkup(keyboard)

			return context.bot.send_photo(chat_id=update.effective_chat.id,
				reply_markup=reply_markup,
				photo=img)

	except FileNotFoundError:
			logging.error('[ERROR][FileNotFoundError] User send wrong page number: %s' % ' '.join(msg))
			return context.bot.send_message(chat_id=update.effective_chat.id,
				text="[ERROR] Please use buttons, not manual commands")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

list_handler = CommandHandler('page', show_data)
dispatcher.add_handler(list_handler)

updater.start_polling()
updater.idle()