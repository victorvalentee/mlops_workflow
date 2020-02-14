FROM python:3.7-slim

MAINTAINER Victor Valente "victorvalentee@gmail.com"

COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

COPY automated_workflow /usr/local/automated_workflow
WORKDIR /usr/local/automated_workflow

EXPOSE 5000

ENTRYPOINT chmod +x start.sh && ./start.sh && /bin/bash