FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /crud_api
WORKDIR /crud_api
ADD . /crud_api/
RUN pip install -r requirements.txt
