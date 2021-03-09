FROM python:3.8.2

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt 
RUN pip install -r requirements.txt

ADD . /app 

# RUN ["chmod", "+x", "startapplication.sh"]