FROM node:14.2-alpine

RUN apk update && \
    apk upgrade && \
    apk add \
    vim \
    nano \
    man

RUN mkdir /code

RUN npm install -g @vue/cli

COPY package*.json ./

RUN npm install

WORKDIR /code

COPY . /code/

CMD npm run serve