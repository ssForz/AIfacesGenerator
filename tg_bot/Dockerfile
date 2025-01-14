FROM python:3.9
# set work directory
# copy project

# install dependencies
RUN pip install --user aiogram==2.2
RUN pip install pika
COPY . /src/bot
# run app
ENTRYPOINT ["python", "./src/tg_bot/bot.py"]