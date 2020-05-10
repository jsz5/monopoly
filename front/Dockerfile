FROM node:14.2-alpine

RUN mkdir /code

RUN npm install -g @vue/cli

COPY package*.json ./

RUN npm install

RUN apk update && \
    apk upgrade && \
    apk add \
    vim \
    nano \
    man

WORKDIR /code

COPY . /code/

#CMD tail -f /dev/null