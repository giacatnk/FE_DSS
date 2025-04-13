# Base stage with Node.js
FROM node:18-alpine as base
WORKDIR /app

# Dependencies stage - this can be built and cached
FROM base as deps
COPY package.json package-lock.json ./
RUN npm ci

# Build stage
FROM base as builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production stage with Nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]