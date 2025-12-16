FROM node:20-alpine

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install --legacy-peer-deps

COPY . .

EXPOSE 4003

# Use Nest dev server with watch so code changes are picked up during development.
CMD ["npm", "run", "start:dev"]
