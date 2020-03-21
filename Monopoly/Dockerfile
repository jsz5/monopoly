FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
COPY ./requirements/requirements.txt /tmp/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    nano \
    man \
    nodejs \
    npm \
    && pip install django \
    && pip install psycopg2 \
    && pip3 --no-cache-dir install -r /tmp/requirements.txt \
    && apt-get clean
CMD tail -f /dev/null
