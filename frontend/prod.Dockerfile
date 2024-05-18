FROM node:20-alpine

RUN mkdir /app

WORKDIR /app/

RUN npm install -g npm

COPY package.prod.json /app/package.json

COPY . .

RUN npm install

CMD [ "npm", "start" ]