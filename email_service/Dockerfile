from python:3.12.5

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt


RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8003

CMD ["python", "manage.py", "runserver", "0.0.0.0:8003"]