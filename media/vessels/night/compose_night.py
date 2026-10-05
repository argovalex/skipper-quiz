"""Light up the unlit night vessel bases (src/*.jpg) with the correct COLREGS light arrays.
Output: <family>_<view>.jpg, view = bow | port | stern. Coordinates are percent of the base image.
Run: python media/vessels/night/compose_night.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
from lightup import lightup

HERE = os.path.dirname(__file__)
OUT = HERE

W_, R_, G_, Y_ = "w", "r", "g", "y"
stack = lambda x, ys, c: [(x, y, c) for y in ys]

# cargo ship (> 50 m)
CP_MH = [(14.2, 41, W_), (82, 33, W_)]; CP_SIDE = [(80.8, 51.4, R_)]
CB_MH = [(50, 36, W_), (50, 19.5, W_)]; CB_SIDE = [(38, 47, G_), (62, 47, R_)]
CS_STERN = [(50, 51, W_)]

V = {
 # power-driven > 50 m
 "power_big_bow":   ("cargo_bow",   CB_MH + CB_SIDE),
 "power_big_port":  ("cargo_port",  CP_MH + CP_SIDE),
 "power_big_stern": ("cargo_stern", CS_STERN),
 # power-driven < 50 m
 "power_small_bow":   ("motor_bow",   [(50, 33, W_), (38, 50, G_), (62, 50, R_)]),
 "power_small_port":  ("motor_port",  [(62, 35, W_), (40, 49.5, R_)]),
 "power_small_stern": ("motor_stern", [(50, 58, W_)]),
 # sailing
 "sail_bow":   ("sail_bow",   [(47, 72, G_), (53, 72, R_)]),
 "sail_port":  ("sail_port",  [(31.5, 72, R_)]),
 "sail_stern": ("sail_stern", [(49.5, 72, W_)]),
 "sail_optional_port": ("sail_port", [(48.8, 8.5, R_), (48.8, 12.5, G_), (31.5, 72, R_)]),
 "sail_optional_bow":  ("sail_bow",  [(50, 6.5, R_), (50, 10.5, G_), (47, 72, G_), (53, 72, R_)]),
 # pilot (white over red)
 "pilot_bow":   ("pilot_bow",   [(50, 22, W_), (50, 27, R_), (33, 52, G_), (67, 52, R_)]),
 "pilot_port":  ("pilot_port",  [(56.5, 27, W_), (56.5, 31.5, R_), (41, 44, R_)]),
 "pilot_stern": ("pilot_stern", [(50, 17, W_), (50, 22, R_), (50, 58, W_)]),
 # trawler (green over white)
 "trawler_bow":   ("trawler_bow",   [(50, 17, G_), (50, 22, W_), (41, 45, G_), (59, 45, R_)]),
 "trawler_port":  ("trawler_port",  [(26.5, 24.5, G_), (26.5, 29.5, W_), (41, 45, R_)]),
 "trawler_stern": ("trawler_stern", [(49.5, 20.5, G_), (49.5, 25.5, W_), (50, 62, W_)]),
 # fishing other than trawling (red over white)
 "netfish_bow":   ("netfish_bow",   [(50, 15, R_), (50, 20, W_), (41, 45, G_), (59, 45, R_)]),
 "netfish_port":  ("netfish_port",  [(37.8, 25, R_), (37.8, 30, W_), (56, 50, R_)]),
 "netfish_stern": ("netfish_stern", [(49.5, 22.5, R_), (49.5, 27.5, W_), (49.5, 58, W_)]),
 # restricted in ability to manoeuvre (red-white-red), making way
 "ram_bow":   ("work_bow",   [(50, 14.5, W_)] + [(50, 22, R_), (50, 26.5, W_), (50, 31, R_)] + [(37, 45, G_), (63, 45, R_)]),
 "ram_port":  ("work_port",  [(35.8, 23.5, W_), (35.8, 28.5, R_), (35.8, 33, W_), (35.8, 37.5, R_), (25, 46, R_)]),
 "ram_stern": ("work_stern", [(49.5, 22, R_), (49.5, 26.5, W_), (49.5, 31, R_), (50, 63, W_)]),
 # RAM with obstruction: 2 red = obstructed side (starboard), 2 green = side to pass (port)
 "dredge_bow":  ("work_bow",  [(50, 14.5, W_), (50, 22, R_), (50, 26.5, W_), (50, 31, R_),
                               (43.5, 22, R_), (43.5, 26.5, R_), (56.5, 22, G_), (56.5, 26.5, G_), (37, 45, G_), (63, 45, R_)]),
 "dredge_port": ("work_port", [(35.8, 23.5, W_), (35.8, 28.5, R_), (35.8, 33, W_), (35.8, 37.5, R_),
                               (38.6, 28.5, G_), (38.6, 33, G_), (25, 46, R_)]),
 "dredge_stern": ("work_stern", [(49.5, 22, R_), (49.5, 26.5, W_), (49.5, 31, R_),
                                 (43.5, 22, G_), (43.5, 26.5, G_), (55.5, 22, R_), (55.5, 26.5, R_), (50, 63, W_)]),
 # diving vessel, stopped: red-white-red only, no navigation lights
 "divers_bow":   ("dive_bow",   [(50, 21, R_), (50, 25, W_), (50, 29, R_)]),
 "divers_port":  ("dive_port",  [(45.3, 27.5, R_), (45.3, 31.5, W_), (45.3, 35.5, R_)]),
 "divers_stern": ("dive_stern", [(49.5, 24, R_), (49.5, 28, W_), (49.5, 32, R_)]),
 # constrained by draught: 3 red
 "draft_bow":   ("cargo_bow",   CB_MH + stack(50, [23.5, 27.5, 31.5], R_) + CB_SIDE),
 "draft_port":  ("cargo_port",  CP_MH + stack(82, [37.5, 41.5, 45.5], R_) + CP_SIDE),
 "draft_stern": ("cargo_stern", stack(50, [22, 26, 30], R_) + CS_STERN),
 # minesweeper (side view only, per Alex)
 "mines_port":  ("mines_port", [(46.8, 22, G_), (42, 26.8, G_), (51.5, 26.8, G_), (46.3, 31.5, W_), (38, 46, R_)]),
 # not under command, making way: 2 red + sidelights + stern, no masthead
 "nuc_bow":   ("cargo_bow",   stack(50, [20, 24.5], R_) + CB_SIDE),
 "nuc_port":  ("cargo_port",  stack(82, [33, 37.5], R_) + CP_SIDE),
 "nuc_stern": ("cargo_stern", stack(50, [20, 24.5], R_) + CS_STERN),
 # aground: 2 red + anchor lights, no navigation lights
 "aground_bow":   ("cargo_bow",   stack(50, [20, 24.5], R_) + [(50, 38, W_), (50, 45, W_)]),
 "aground_port":  ("cargo_port",  [(14.2, 41, W_), (82, 43, W_)] + stack(82, [33, 37.5], R_)),   # anchor light on the mast, not the stern (Alex)
 "aground_stern": ("cargo_stern", stack(50, [20, 24.5], R_)),   # no white from astern (Alex)
 # at anchor > 50 m: two white, forward higher
 "anchor_big_bow":   ("cargo_bow",   [(50, 38, W_), (50, 45, W_)]),
 "anchor_big_port":  ("cargo_port",  [(14.2, 41, W_), (82, 43, W_)]),   # aft anchor light on the mast (Alex)
 "anchor_big_stern": ("cargo_stern", [(50, 31, W_)]),   # on the mast
 # at anchor < 50 m: one white all-round
 "anchor_small_bow":   ("motor_bow",   [(50, 33, W_)]),
 "anchor_small_port":  ("motor_port",  [(62, 35, W_)]),
 "anchor_small_stern": ("motor_stern", [(49.5, 26, W_)]),
 # towing, tow <= 200 m: 2 masthead in a vertical line
 "tow_bow":   ("tug_bow",   stack(49.5, [13, 17.5], W_) + [(37, 50, G_), (62, 50, R_)]),
 "tow_port":  ("tug_port",  stack(17.8, [37, 43], W_) + [(14.5, 54, R_), (50.5, 58.5, R_)]),
 "tow_stern": ("tug_stern", [(49.5, 53.5, Y_), (49.5, 58, W_)]),
 # towing, tow > 200 m: 3 masthead in a vertical line
 "tow_long_bow":  ("tug_bow",      stack(49.5, [13, 17.5, 22], W_) + [(37, 50, G_), (62, 50, R_)]),
 "tow_long_port": ("tuglong_port", stack(8.3, [38, 43, 48], W_) + [(6, 53, R_), (70.5, 54.5, R_)]),
 # hovercraft: flashing yellow
 "hover_bow":   ("hover_bow",   [(49.5, 24.5, Y_), (49.5, 29, W_), (24, 52, G_), (75, 52, R_)]),
 "hover_port":  ("hover_port",  [(37, 29.5, Y_), (37, 34, W_), (24, 45, R_)]),
 "hover_stern": ("hover_stern", [(49.5, 26, Y_), (49.5, 50, W_)]),
}

if __name__ == "__main__":
    for name, (base, lights) in V.items():
        src = os.path.join(HERE, "src", base + ".jpg")
        W, H = Image.open(src).size
        r = max(9, int(W * (0.011 if base.endswith("_port") else 0.014)))
        spec = ";".join(f"{int(x * W / 100)},{int(y * H / 100)},{c},{r}" for x, y, c in lights)
        lightup(src, os.path.join(OUT, name + ".jpg"), spec)
    print(len(V), "images ->", OUT)
