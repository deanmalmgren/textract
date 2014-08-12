FROM ubuntu:12.04
MAINTAINER Shawn Milochik <shawn@milochik.com>
ENV DEBIAN_FRONTEND noninteractive
ENV REFRESHED_AT 2014-08-12b
RUN apt-get update
RUN apt-get install python-pip -y
ADD . /requirements
RUN /bin/bash /requirements/debian.sh
RUN /bin/bash /requirements/python.sh
RUN mkdir /textract
VOLUME ["/textract"]
ENV PATH $PATH:/textract/bin
ENV PYTHONPATH /textract
ENV SRC /textract
ENTRYPOINT ["/textract/requirements/run_tests.sh"]
