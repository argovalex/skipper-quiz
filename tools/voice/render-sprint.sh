#!/bin/bash
# render-sprint.sh <license> <num...> : render-batch.sh in chunks of 15, redeploying the render
# server between chunks (EAGAIN after ~18 renders, see memory render-server-eagain). On a failed
# render: redeploy once and retry the rest; a second failure in a row stops the sprint.
cd "$(dirname "$0")/../.."
LIC="$1"; shift
nums=("$@"); CH=15; fails=0
redeploy() {
  (cd publisher && git pull -q --rebase && git commit -q --allow-empty -m "redeploy: clear EAGAIN (voice-v2 sprint)" && git push -q) \
    && echo "redeploy pushed $(date +%H:%M)"
  sleep 240
  until curl -s -o /dev/null -w "%{http_code}" https://skipper-quiz-publisher-production.up.railway.app/health | grep -q 200; do sleep 15; done
  echo "server up $(date +%H:%M)"
}
i=0
[ -n "$FIRST_REDEPLOY" ] && redeploy
while [ $i -lt ${#nums[@]} ]; do
  chunk=("${nums[@]:$i:$CH}")
  out=$(bash tools/voice/render-batch.sh "$LIC" "${chunk[@]}"); echo "$out"
  done_n=$(echo "$out" | grep -c "^OK ")
  i=$((i + done_n))
  if echo "$out" | grep -q "^FAIL"; then
    fails=$((fails + 1)); [ $fails -ge 2 ] && { echo "STOP: two failures in a row at ${nums[$i]}"; exit 1; }
  else
    fails=0
  fi
  [ $i -lt ${#nums[@]} ] && redeploy
done
echo "SPRINT DONE"
