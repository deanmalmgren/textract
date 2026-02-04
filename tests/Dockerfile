FROM ubuntu:20.04
MAINTAINER Shawn Milochik <shawn@milochik.com>
ENV DEBIAN_FRONTEND noninteractive
ENV REFRESHED_AT 2022-08-17
RUN apt-get update
RUN apt-get install python3-pip -y
ADD . /app
WORKDIR /app
RUN /bin/bash /app/provision/debian.sh
RUN /bin/bash /app/provision/python.sh
RUN adduser --disabled-password --gecos "" --home=/home/textract textract
ENV PATH $PATH:/home/textract/src/bin
ENV PYTHONPATH /home/textract/src
USER textract
ENTRYPOINT ["/home/textract/src/tests/docker_entry.sh"]
