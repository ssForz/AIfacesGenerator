import time

import secret
import bot_producer
import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# import os
# import pika
# import asyncio

# import bot_producer

bot = Bot(token=secret.TOKEN)
dispatch = Dispatcher(bot)

user_task = {}


def get_markup_eye(prefix = ""):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)

    item1 = types.KeyboardButton(prefix + "eye_gray")
    item2 = types.KeyboardButton(prefix + "eye_black")
    item3 = types.KeyboardButton(prefix + "eye_orange")
    item4 = types.KeyboardButton(prefix + "eye_pink")
    item5 = types.KeyboardButton(prefix + "eye_yellow")
    item6 = types.KeyboardButton(prefix + "eye_aqua")
    item7 = types.KeyboardButton(prefix + "eye_purple")
    item8 = types.KeyboardButton(prefix + "eye_green")
    item9 = types.KeyboardButton(prefix + "eye_brown")
    item10 = types.KeyboardButton(prefix + "eye_red")
    item11 = types.KeyboardButton(prefix + "eye_blue")
    markup.add(
			item1, 
			item2, 
			item3, 
			item4, 
			item5, 
			item6, 
			item7,
			item8,
			item9,
			item10,
			item11
            )
    return markup

def get_markup_hair(prefix = ""):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)

    item1 = types.KeyboardButton(prefix + "hair_orange")
    item2 = types.KeyboardButton(prefix + "hair_white")
    item3 = types.KeyboardButton(prefix + "hair_aqua")
    item4 = types.KeyboardButton(prefix + "hair_gray")
    item5 = types.KeyboardButton(prefix + "hair_green")
    item6 = types.KeyboardButton(prefix + "hair_red")
    item7 = types.KeyboardButton(prefix + "hair_purple")
    item8 = types.KeyboardButton(prefix + "hair_pink")
    item9 = types.KeyboardButton(prefix + "hair_blue")
    item10 = types.KeyboardButton(prefix + "hair_black")
    item11 = types.KeyboardButton(prefix + "hair_brown")
    item12 = types.KeyboardButton(prefix + "hair_blonde")
    markup.add(
			item1, 
			item2, 
			item3, 
			item4, 
			item5, 
			item6, 
			item7,
			item8,
			item9,
			item10,
			item11,
            item12
            )
    return markup

@dispatch.message_handler(commands=['start'])
async def welcome(message):
    user_task.clear()
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton("/generate")
    item2 = types.KeyboardButton("/project_GitHub")
    markup.add(item1, item2)
    await bot.send_message(message.chat.id,
                        "Hello! I can generate Anime Faces for you with your parameters. There are my options:\n-- <generate> option will ask you parameters and generate face\n-- <project_GitHub> will show you github link with all necessary project info",
                        reply_markup = markup)

@dispatch.message_handler(commands=['project_GitHub'])
async def show_git_link(message):
    user_task.clear()
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton("/generate")
    item2 = types.KeyboardButton("/project_GitHub")
    markup.add(item1, item2)
    await bot.send_message(message.chat.id,
                           "https://github.com/ssForz/AIfacesGenerator",
                           reply_markup = markup)

@dispatch.message_handler(commands=['generate'])
async def generate_mod(message):
    user_task.clear()
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton("/fix_noise")
    item2 = types.KeyboardButton("/fix_hair_eye")
    item3 = types.KeyboardButton("/change_hair")
    item4 = types.KeyboardButton("/change_eye")
    item5 = types.KeyboardButton("/interpolate")
    markup.add(item1, item2, item3, item4, item5)
    await bot.send_message(message.chat.id,
                           "Choose mod",
                           reply_markup = markup)

@dispatch.message_handler(commands=['interpolate'])
async def interpolate_mod(message):
    user_task["user_id"] = str(message.chat.id)
    user_task["mod"] = "interpolate"
    # add queue sending with params
    # 
    await bot.send_message(message.chat.id, "Generating faces... Please wait...")
    await bot_producer.publish(json.dumps(user_task))

@dispatch.message_handler(commands=['fix_noise'])
async def fix_noise_mod(message):
    user_task["user_id"] = str(message.chat.id)
    user_task["mod"] = "fix_noise"
    # add queue sending with params
    # 
    await bot.send_message(message.chat.id, "Generating faces... Please wait...")
    await bot_producer.publish(json.dumps(user_task))

@dispatch.message_handler(commands=['fix_hair_eye'])
async def fix_hair_eye_mod(message):
    user_task["user_id"] = str(message.chat.id)
    user_task["mod"] = "fix_hair_eye"
    markup = get_markup_eye()

    await bot.send_message(message.chat.id, "Please, choose eye color", reply_markup = markup)

@dispatch.message_handler(commands=['change_hair'])
async def change_hair_mod(message):
    user_task["user_id"] = str(message.chat.id)
    user_task["mod"] = "fix_hair"
    markup = get_markup_eye("fix_")

    await bot.send_message(message.chat.id, "Please, choose fixed eye color", reply_markup = markup)
    
@dispatch.message_handler(commands=['change_eye'])
async def change_eye_mod(message):
    user_task["user_id"] = str(message.chat.id)
    user_task["mod"] = "fix_eye"
    markup = get_markup_hair("fix_")

    await bot.send_message(message.chat.id, "Please, choose fixed hair color", reply_markup = markup)
    
@dispatch.message_handler(regexp = '^eye_')
async def eye_color(message):
    color = message.text[4:]
    user_task["eye_color"] = color
    markup = get_markup_hair()
    # add queue sending with params
    # 
    await bot.send_message(message.chat.id, "Please, choose hair color", reply_markup = markup)

@dispatch.message_handler(regexp = '^hair_')
async def hair_color(message):
    color = message.text[5:]
    user_task["hair_color"] = color
    # add queue sending with params
    # 
    await bot.send_message(message.chat.id, "Generating... Please wait")
    # await bot.send_message(message.chat.id, "Settings (opt for testing): hair - " + user_task['hair_color'] + ", eye - " + user_task['eye_color'])
    await bot_producer.publish(json.dumps(user_task))
   
@dispatch.message_handler(regexp = '^fix_eye_')
async def fix_eye_color(message):
    color = message.text[8:]
    user_task["eye_color"] = color
    # add queue sending with params
    # 
    await bot.send_message(message.chat.id, "Generating... Please wait...")
    await bot_producer.publish(json.dumps(user_task))

@dispatch.message_handler(regexp = '^fix_hair_')
async def fix_hair_color(message):
    color = message.text[9:]
    user_task["hair_color"] = color
    await bot.send_message(message.chat.id, "Generating... Please wait...")
    await bot_producer.publish(json.dumps(user_task))

if __name__ == "__main__":
    executor.start_polling(dispatch)
