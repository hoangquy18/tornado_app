FROM python:3.10-slim

WORKDIR /tornado_app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY . .
EXPOSE 8888

CMD [ "python", "./app.py" ]

