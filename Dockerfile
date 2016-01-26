FROM python:2.7

RUN mkdir /root/.chamberlain

ADD     . /opt/chamberlain
WORKDIR /opt/chamberlain
RUN make
