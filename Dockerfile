FROM nvcr.io/nvidia/pytorch:22.08-py3

RUN apt-get update
RUN apt-get install python3-pygame -y
RUN pip3 install pygame
ENV DISPLAY=host.docker.internal:0.0