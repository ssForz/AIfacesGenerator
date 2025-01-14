FROM python:3.10
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
RUN pip install --user aiogram==2.2
RUN pip install pika


COPY . /src/app
RUN mkdir -p /src/app/gen
ENTRYPOINT ["python", "/src/app/src/consumer.py"]
