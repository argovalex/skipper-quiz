#!/bin/sh
# l12 background clip. Run from repo root:
#   sh tools/l12/clip.sh <num> <clip-url-or-local-path> <slug> [panel.png]
# Plain: saves media/bgclips/<num>-<slug>.mp4.
# With a panel (from tools/l12/panel.js): 1600x960 composite = clip cropped 960x960 + panel,
# saved as media/bgclips/l12_q<num>_night.mp4 (scenes.js shows *_night.mp4 with contain).
# Writes a check frame to output/l12-check/chk<num>.jpg.
M=media/bgclips; C=output/l12-check; mkdir -p "$C"
n=$1; src=$2; slug=$3; panel=$4
case "$src" in http*) tmp="$C/raw$n.mp4"; curl -sfL "$src" -o "$tmp" || exit 1; src="$tmp";; esac
if [ -n "$panel" ]; then
  out="l12_q${n}_night.mp4"
  ffmpeg -v error -y -i "$src" -i "$panel" -filter_complex "[0:v]scale=-2:960,crop=960:960,setsar=1,pad=1600:960[p];[p][1:v]overlay=960:0,format=yuv420p" -an -c:v libx264 -crf 23 -preset veryfast -t 8 "$M/$out" || exit 1
else
  out="$n-$slug.mp4"; cp "$src" "$M/$out" || exit 1
fi
ffmpeg -v error -y -ss 5 -i "$M/$out" -frames:v 1 -vf scale=480:-1 "$C/chk$n.jpg"
echo "$n $out"
