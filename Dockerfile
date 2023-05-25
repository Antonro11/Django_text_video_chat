FROM python:3.10-slim

RUN  apt update && mkdir /django_chat && python -m pip install --upgrade pip
COPY ./requirements.txt ./django_chat/requirements.txt
COPY ./src ./django_chat/src



RUN pip install -r django_chat/requirements.txt
RUN pip install twisted[http2,tls]
RUN apt-get install -y curl
RUN apt-get install -y wget




CMD ["bash"]


