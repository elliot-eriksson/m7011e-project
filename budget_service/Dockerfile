from python:3.12.5

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate

ENV PYTHONUNBUFFERED=1

EXPOSE 8002

CMD ["/bin/sh", "-c", "python manage.py runserver 0.0.0.0:8002 & python manage.py start_consumer"]

