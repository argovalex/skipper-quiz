FROM node:20-slim
WORKDIR /app
RUN npm install -g http-server
COPY . .
EXPOSE 8080
# Railway injects $PORT. -c-1 disables http caching so the service worker owns caching.
CMD http-server . -p ${PORT:-8080} -c-1 --silent
