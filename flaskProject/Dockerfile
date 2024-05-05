FROM python:3.7-slim-buster

COPY sources.list /etc/apt/sources.list

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONIOENCODING=UTF-8
ENV TZ=Asia/Shanghai
ENV PROJECT_DIR=/srv/web

COPY ./ $PROJECT_DIR

WORKDIR $PROJECT_DIR

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

ENV PYTHONPATH=$PYTHONPATH:$PROJECT_DIR

EXPOSE 6060

WORKDIR $PROJECT_DIR/app

CMD python __init__.py
