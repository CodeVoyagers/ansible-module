FROM python:3.11

COPY ./requirements.txt /tmp/

RUN apt-get update && \
    apt-get install rsync -y && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt && \
    apt-get install docker.io -y

ENV ANSIBLE_STDOUT_CALLBACK=community.general.yaml

WORKDIR /root/workstation
