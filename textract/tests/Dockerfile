FROM ubuntu:12.04
MAINTAINER Shawn Milochik <shawn@milochik.com>
ENV DEBIAN_FRONTEND noninteractive
ENV REFRESHED_AT 2014-08-12b
RUN apt-get update
RUN apt-get install python-pip -y
ADD . /src
WORKDIR /src
RUN /bin/bash /src/provision/debian.sh
RUN /bin/bash /src/provision/python.sh
RUN adduser --disabled-password --gecos "" --home=/home/textract textract
VOLUME ["/home/textract/src"]
ENV PATH $PATH:/home/textract/src/bin
ENV PYTHONPATH /home/textract/src
USER textract
ENTRYPOINT ["/home/textract/src/tests/run.py"]
