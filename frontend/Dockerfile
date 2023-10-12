FROM node:20-alpine

RUN mkdir /app

WORKDIR /app/

RUN npm install -g npm

COPY package*.json /app/

COPY . .

RUN npm install

CMD [ "npm", "start" ]