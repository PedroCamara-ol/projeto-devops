FROM python:3.9.12-alpine3.15

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py . 

CMD [ "python", "app.py"]