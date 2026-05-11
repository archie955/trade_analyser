# install node
FROM node:24-alpine as builder

# working directory
WORKDIR /client

ARG VITE_BASEURL
ENV VITE_BASEURL=${VITE_BASEURL}

# copy package.json deps and install deps
COPY package*.json ./
RUN npm install

# install app code
COPY . .
RUN npm run dev