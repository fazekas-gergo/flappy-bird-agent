FROM python:3.10

RUN apt-get update
RUN apt-get install python3-pygame -y
RUN pip3 install pygame
ENV DISPLAY=host.docker.internal:0.0