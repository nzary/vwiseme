FROM ubuntu:20.04

USER root

RUN apt-get update
RUN apt-get -y install curl
RUN apt-get install -y gnupg2
RUN apt-get install -y g++
RUN apt-get install apt-transport-https

WORKDIR /app/frontend

COPY . /app/frontend/

# RUN apt install python3-pip

VOLUME /app/frontend

CMD [ "python","main.py"]

USER 1001