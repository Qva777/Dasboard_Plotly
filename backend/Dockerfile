FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app

EXPOSE 8000

RUN chmod +x ./start.sh
CMD ["/bin/bash", "/app/start.sh"]