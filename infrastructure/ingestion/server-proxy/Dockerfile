FROM node:23

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 80

ENV KAFKAJS_NO_PARTITIONER_WARNING=1

CMD ["node", "app.js"]