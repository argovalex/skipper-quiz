detect(){
  local num=$1 url=$2
  local out=$("$FF" -i "$url" -vn -af silencedetect=noise=-30dB:d=0.8 -f null - 2>&1)
  local dur=$(echo "$out" | grep -oE "Duration: [0-9:.]+" | head -1 | grep -oE "[0-9:.]+")
  echo "$out" | awk -v num="$num" -v dur="$dur" '
    /silence_start/ {s=$NF}
    /silence_end/ {
      match($0,/silence_end: [0-9.]+/); e=substr($0,RSTART+13,RLENGTH-13);
      match($0,/silence_duration: [0-9.]+/); d=substr($0,RSTART+18,RLENGTH-18);
      if(s>1.5 && d+0>best){best=d+0; bs=s}
    }
    END{printf "Q%s  dur=%s  PAUSE_at=%.2f  gap=%.2fs\n", num, dur, bs, best}'
}
