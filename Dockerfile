FROM python:3

RUN mkdir /server
WORKDIR /server
COPY . /server/
RUN pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:8000