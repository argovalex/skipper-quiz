"""Copy the full-bleed scene images of the first (Sept 2026) intro cards into the shared l30 assets folder as l40_*.jpg,
trimming letterbox bars. Source: lessons/l40/cards/מבוא ל-GMDSS/_old/<sid>.png"""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'cards', 'מבוא ל-GMDSS', '_old')
DST = os.path.join(HERE, '..', '..', 'l30', 'sources', 'assets')
MAP = {'s01_intro': 'l40_cockpit', 's02_titanic': 'l40_radio_room', 's03_gmdss_born': 'l40_signal', 's04_principle': 'l40_rcc',
       's05_who_needs': 'l40_handheld', 's06_areas_intro': 'l40_world_a1a2', 's08_area_a3a4': 'l40_world_a3a4', 's09_exam_trap': 'l40_rocky_coast',
       's10_summary': 'l40_sunset_vhf'}
for sid, name in MAP.items():
    im = Image.open(os.path.join(SRC, sid + '.png')).convert('RGB')
    g = im.convert('L').point(lambda v: 255 if v > 12 else 0)
    box = g.getbbox() or (0, 0, *im.size)
    im = im.crop((0, box[1], im.width, box[3]))
    im.save(os.path.join(DST, name + '.jpg'), quality=88)
    print(name, im.size)
