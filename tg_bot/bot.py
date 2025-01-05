import time

import secret

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

bot = Bot(
	    token=secret.TOKEN
	)

dp = Dispatcher(
	    bot
	)


@dp.message_handler(commands=['start'])
async def echo_message(message):
	await bot.send_message(
			chat_id=message.chat.id,
			text="Bot not working yet"
		)

if __name__ == "__main__":
	executor.start_polling(dp)