FROM node:20.4.0-alpine3.18

COPY ./webui ./app

WORKDIR /app

RUN npm install

EXPOSE 3000

CMD ["npm", "start"]
