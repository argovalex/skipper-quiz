FROM node:20-slim
WORKDIR /site
RUN npm install -g http-server
COPY . .
EXPOSE 8080
# Railway injects $PORT. -c-1 disables http caching (avoids stale deploys).
CMD http-server . -p ${PORT:-8080} -c-1 --silent
