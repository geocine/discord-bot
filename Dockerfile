FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

VOLUME /app

CMD ["python", "bot.py"]