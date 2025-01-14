import os, sys, pika
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import time
import asyncio
import secret
import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputFile

async def send_message(uid):
    flag = 1
    while(flag):
        try:
            audio = open('/src/app/gen/' + uid + '/res.png', 'rb')
            flag = 0
        except:
            continue
    operator = Bot(token=secret.TOKEN)
    await operator.send_photo(chat_id=int(uid),
                     photo=InputFile('/src/app/gen/' + uid + '/res.png'))
    await operator.close()


def respond(uid):
    asyncio.run(send_message(uid))


def collect_task(body: dict):
    uid = body["user_id"]
    outpath = "/src/app/gen/" + uid
    if body["mod"] == "interpolate":
        os.system("python /src/app/src/test.py --type interpolate --gen_model_dir \'/src/app/results/checkpoints/ACGAN-[64]-[50000]/G_32.ckpt\' -s " + outpath)

    if body["mod"] == "fix_noise":
        os.system("python /src/app/src/test.py --type fix_noise --gen_model_dir \'/src/app/results/checkpoints/ACGAN-[64]-[50000]/G_32.ckpt\' -s " + outpath)

    if body["mod"] == "fix_hair_eye":
        eye_color = body["eye_color"]
        hair_color = body["hair_color"]
        os.system("python /src/app/src/test.py --type fix_hair_eye --hair " + 
            hair_color + 
            " --eye " + 
            eye_color + 
            " --gen_model_dir \'/src/app/results/checkpoints/ACGAN-[64]-[50000]/G_32.ckpt\' -s " + outpath)
    if body["mod"] == "change_eye":
        hair_color = body["hair_color"]
        os.system("python /src/app/src/test.py --type change_eye --hair " + 
            hair_color + 
            " --gen_model_dir \'/src/app/results/checkpoints/ACGAN-[64]-[50000]/G_32.ckpt\' -s " + outpath)
    if body["mod"] == "change_hair":
        eye_color = body["eye_color"]
        os.system("python /src/app/src/test.py --type change_hair --eye " + 
            eye_color + 
            " --gen_model_dir \'/src/app/results/checkpoints/ACGAN-[64]-[50000]/G_32.ckpt\' -s " + outpath)
    respond(uid)



def callback(ch, method, properties, body):
    collect_task(json.loads(body))
    # chatid = body.decode("utf-8")
    # print(body["mod"])
    # U.generate(models_ls,chatid)
    # uploadgoogle(chatid)
    # os.remove("/src/app/generations/snd" + chatid + ".wav")

amqp_url = os.environ['AMQP_URL_FROM_BOT']
url_params = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(url_params)
channel = connection.channel()
channel.queue_declare(queue='frombot')
channel.basic_consume(queue='frombot', auto_ack=True, on_message_callback=callback)
channel.start_consuming()