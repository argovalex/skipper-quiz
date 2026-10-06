FROM node:20-slim
WORKDIR /site
RUN npm install -g http-server
COPY . .
EXPOSE 8080
# Railway injects $PORT. -c-1 disables http caching (avoids stale deploys).
# STAGING=1 (set only on the staging service) blocks search engines and shows a staging ribbon,
# so the redesign branch can be deployed to its own URL without competing with www.alargov.com.
CMD if [ "$STAGING" = "1" ]; then \
      printf 'User-agent: *\nDisallow: /\n' > robots.txt; \
      for f in $(find . -name '*.html'); do \
        sed -i 's|<head>|<head><meta name="robots" content="noindex,nofollow">|; s|</body>|<div style="position:fixed;bottom:12px;left:12px;z-index:9999;background:#f0a94a;color:#0a1428;font:600 12px/1 sans-serif;padding:6px 10px;border-radius:6px">STAGING · redesign</div></body>|' "$f"; \
      done; \
    fi; \
    http-server . -p ${PORT:-8080} -c-1 --silent
