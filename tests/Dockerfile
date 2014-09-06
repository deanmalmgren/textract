FROM ubuntu:12.04
MAINTAINER Shawn Milochik <shawn@milochik.com>
ENV DEBIAN_FRONTEND noninteractive
ENV REFRESHED_AT 2014-08-12b
RUN apt-get update
RUN apt-get install python-pip -y
ADD . /provision
RUN /bin/bash /provision/debian.sh
RUN /bin/bash /provision/python.sh
RUN mkdir /textract
VOLUME ["/textract"]
ENV PATH $PATH:/textract/bin
ENV PYTHONPATH /textract
ENV SRC /textract
ENTRYPOINT ["/textract/tests/docker_entry.sh"]
