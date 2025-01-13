import os, sys, pika
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import time
import asyncio
import secret
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=secret.TOKEN)
dispatch = Dispatcher(bot)

def collect_task(body: dict):
    uid = body["user_id"]
    outpath = "./results/" + uid + "/"
    if body["mod"] == "interpolate":
        os.system("python test.py --type interpolate --gen_model_dir \'../results/checkpoints/ACGAN-[64]-[50000]/G_68.ckpt\' -s " + outpath)

    if body["mod"] == "fix_noise":
        os.system("python test.py --type fix_noise --gen_model_dir \'../results/checkpoints/ACGAN-[64]-[50000]/G_68.ckpt\' -s " + outpath)

    if body["mod"] == "fix_hair_eye":
        eye_color = body["eye_color"]
        hair_color = body["hair_color"]
        os.system("python test.py --type fix_hair_eye --hair " + 
            hair_color + 
            " --eye " + 
            eye_color + 
            " --gen_model_dir \'../results/checkpoints/ACGAN-[64]-[50000]/G_68.ckpt\' -s " + outpath)
    if body["mod"] == "change_eye":
        hair_color = body["hair_color"]
        os.system("python test.py --type change_eye --hair " + 
            hair_color + 
            " --gen_model_dir \'../results/checkpoints/ACGAN-[64]-[50000]/G_68.ckpt\' -s " + outpath)
    if body["mod"] == "change_hair":
        eye_color = body["eye_color"]
        os.system("python test.py --type change_hair --eye " + 
            eye_color + 
            " --gen_model_dir \'../results/checkpoints/ACGAN-[64]-[50000]/G_68.ckpt\' -s " + outpath)
    flag = 1
    while(flag):
        try:
            audio = open('/results/' + uid + "/res.png", 'rb')
            flag = 0
        except:
            continue
    # time.sleep(10)
    bot.send_photo(chat_id=int(uid),
                     photo=FSInputFile(path='/results/' + uid + '/res.png'))




def callback(ch, method, properties, body: dict):
    # task = collect_task(body)
    # chatid = body.decode("utf-8")
    print(body["mod"])
    # U.generate(models_ls,chatid)
    # uploadgoogle(chatid)
    # os.remove("/src/app/generations/snd" + chatid + ".wav")

amqp_url = os.environ['AMQP_URL_FROM_BOT']
url_params = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(url_params)
channel = connection.channel()
channel.queue_declare(queue='GenerateQuery')
channel.basic_consume(queue='GenerateQuery', auto_ack=True, on_message_callback=callback)
channel.start_consuming()