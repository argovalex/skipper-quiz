#!/bin/bash
# render-batch.sh <license> <num...> : re-render questions one by one (voice v2 via render server),
# commit locally per question, push once at the end (pull --rebase --autostash survives a dirty tree).
# Stops at the first failed render (EAGAIN = redeploy the render server, then rerun the rest).
cd "$(dirname "$0")/../.."
LIC="$1"; shift
export PYTHONIOENCODING=utf-8
ok=()
for n in "$@"; do
  if node tools/quiz-app/update-question.js "$n" --license "$LIC" --vo-ok --no-push > "output/render-$n.log" 2>&1 \
     && grep -q "committed" "output/render-$n.log"; then
    ok+=("$n"); echo "OK $n $(date +%H:%M)"
  else
    echo "FAIL $n (see output/render-$n.log)"; tail -n 5 "output/render-$n.log"; break
  fi
done
for i in 1 2 3; do git pull -q --rebase --autostash && git push -q && break; sleep 5; done
echo "rendered: ${ok[*]}"
