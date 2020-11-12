FROM ubuntu:19.10 as builder

ARG BACKEND_PORT

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get -y upgrade 
RUN apt-get -y install curl
RUN apt-get install -y python3.7
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt

EXPOSE ${BACKEND_PORT}

CMD python3 ./main_app.py