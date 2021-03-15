FROM python:3.8.2

ENV CONFIG_TYPE=prod
ENV IP_STACK_KEY=1bb0ea2ed3aff161df72a1d45496741c
ENV SECRET_KEY=my_secret_key

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt 
RUN pip install -r requirements.txt

ADD . /app 

EXPOSE 5000
CMD python manage.py run