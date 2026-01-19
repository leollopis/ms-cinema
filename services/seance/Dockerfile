# multi-stage build for NestJS (production)

FROM node:20-alpine AS builder
WORKDIR /usr/src/app

# install build deps
COPY package*.json ./
RUN npm ci

# copy and build
COPY . .
RUN npm run build --if-present

# production image
FROM node:20-alpine AS runner
WORKDIR /usr/src/app
ENV NODE_ENV=production
ENV PORT=3000

# only production deps
COPY package*.json ./
RUN npm ci --omit=dev --no-audit --no-fund

# copy built artifacts + healthcheck
COPY --from=builder /usr/src/app/dist ./dist
COPY healthcheck.sh ./healthcheck.sh
RUN chmod +x ./healthcheck.sh

# runtime port (compose overrides PORT)
EXPOSE 3000 4004

# basic healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD sh ./healthcheck.sh || exit 1

CMD ["node", "dist/main.js"]
