FROM ubuntu:14.04
MAINTAINER Shawn Milochik <shawn@milochik.com>
ENV DEBIAN_FRONTEND noninteractive
ENV REFRESHED_AT 2014-08-10
RUN apt-get update
RUN apt-get install python2.7-dev python2.7 -y
RUN apt-get install python-pip -y
RUN apt-get install libxml2-dev libxslt1-dev -y
RUN apt-get install lib32z1-dev -y
RUN apt-get install antiword tesseract-ocr -y
RUN apt-get install pstotext -y
RUN mkdir /textract
RUN pip install lxml
RUN pip install pdf2text
VOLUME ["/textract"]
ENV PATH $PATH:/textract/bin
ENV PYTHONPATH /textract
ENV SRC /textract
ENTRYPOINT ["/textract/docker/run_tests.sh"]
