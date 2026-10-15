"""Lesson 13 s16: 9:16 phone version of the range video card -> cards/<lesson>/_v/s16_range.mp4.
Phone poster (_v/s16_range.png) + the AI clip (assets/u13_range.mp4) + the Tailwind overlay (_tw/s16_overlay.png), both scaled into the
phone card's photo area. Same aspect as the wide panel, so the overlay needs no relayout.
usage: python u13_vvideo.py"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import nowin, twcard as T
OUT = os.path.join(HERE, '..', 'cards', 'גלי רדיו ומכשיר VHF', '_v')
poster, vid, ov = os.path.join(OUT, 's16_range.png'), os.path.join(HERE, 'assets', 'u13_range.mp4'), os.path.join(HERE, '_tw', 's16_overlay.png')
X, Y, VW, VH = 57, 180, 980, 880   # photo area of this (pre-u17 layout) phone card, same aspect as the wide panel
fc = (f'[1:v]scale={VW}:{VH}:force_original_aspect_ratio=increase,crop={VW}:{VH},setsar=1[v];[2:v]scale={VW}:{VH}[o];'
      f'[0:v][v]overlay={X}:{Y}[b];[b][o]overlay={X}:{Y},format=yuv420p[out]')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-i', poster, '-stream_loop', '-1', '-i', vid, '-loop', '1', '-i', ov,
                '-filter_complex', fc, '-map', '[out]', '-t', '8', '-r', '25', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', os.path.join(OUT, 's16_range.mp4')], check=True)
print('ok _v/s16_range.mp4')
