FROM node:14-alpine
WORKDIR ./frontend
COPY . .
RUN npm install
RUN npm run build

