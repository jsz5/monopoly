FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

COPY ./requirements/requirements.txt /tmp/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    nano \
    man \
    nodejs \
    npm \
    gcc \
    libgcc-8-dev \
    python3-dev \
    && pip3 --no-cache-dir install -r /tmp/requirements.txt \
    && apt-get clean

WORKDIR /code

ENV PYTHONPATH /code:$PYTHONPATH
ENV DJANGO_SETTINGS_MODULE Monopoly.settings

COPY . /code/

# CMD tail -f /dev/null
