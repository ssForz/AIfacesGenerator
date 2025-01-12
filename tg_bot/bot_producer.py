import pika
import os
import asyncio



async def publish(chat_id):
    amqp_url = os.environ['AMQP_URL_FROM_BOT']
    url_params = pika.URLParameters(amqp_url)
    connection = pika.BlockingConnection(url_params)
    channel = connection.channel()

    channel.queue_declare(queue='frombot')

    channel.basic_publish(exchange='', routing_key='frombot', body=chat_id)
    connection.close()