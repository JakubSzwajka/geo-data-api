FROM python:3.8.2

ENV CONFIG_TYPE=dev
ENV IP_STACK_KEY=your_ip_stack_key
ENV SECRET_KEY=my_secret_key

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt 
RUN pip install -r requirements.txt

ADD . /app 

EXPOSE 5000
CMD python manage.py run