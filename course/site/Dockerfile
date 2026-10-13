FROM node:20-slim
WORKDIR /site
RUN npm install -g http-server
COPY . .
EXPOSE 8080
# Railway injects $PORT.
# Indexing is decided here by the environment, never in the HTML:
#   STAGING=1 (staging service only) -> robots.txt Disallow, a single noindex,nofollow tag on every page
#   (replacing any page-level robots tag, so there is never a duplicate), a staging ribbon, no caching.
#   Production (STAGING unset) -> pages ship as built (indexable; only empty placeholder sections carry
#   their own noindex), cached for CACHE_SECONDS (default 1 hour).
CMD if [ "$STAGING" = "1" ]; then \
      printf 'User-agent: *\nDisallow: /\n' > robots.txt; \
      for f in $(find . -name '*.html'); do \
        sed -i '/<meta name="robots"[^>]*>/d; s|<head>|<head><meta name="robots" content="noindex,nofollow">|; s|</body>|<div style="position:fixed;bottom:12px;left:12px;z-index:9999;background:#f0a94a;color:#0a1428;font:600 12px/1 sans-serif;padding:6px 10px;border-radius:6px">STAGING · redesign</div></body>|' "$f"; \
      done; \
      CACHE=-1; \
    else \
      CACHE=${CACHE_SECONDS:-3600}; \
    fi; \
    http-server . -p ${PORT:-8080} -c$CACHE --silent
