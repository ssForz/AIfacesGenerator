FROM python:3.9
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
RUN pip install --user aiogram==2.2
RUN pip install pika

COPY . /src/app

ENTRYPOINT ["python", "/src/app/src/app_consumer.py"]