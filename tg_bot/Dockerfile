FROM python:3.10
# set work directory
# copy project

# install dependencies
RUN pip install --upgrade pip
RUN pip install --user aiogram==2.2
RUN pip install pika
COPY . /src/tg_bot
# run app
ENTRYPOINT ["python", "./src/tg_bot/bot.py"]