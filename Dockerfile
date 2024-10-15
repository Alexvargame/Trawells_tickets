FROM python:3.9

WORKDIR /Python39/django/trawells

COPY ./requirements.txt /Python39/django/trawells/requirements.txt
RUN pip install -r /Python39/django/trawells/requirements.txt

COPY . /Python39/django/trawells/
EXPOSE 8000
CMD ['python','manage.py','migrate']
CMD ['python','manage.py','runserver','127.0.0.1:8000']
