"""Light up the unlit night vessel bases with the correct COLREGS light arrays (percent coords)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))  # media/vessels/night
from PIL import Image
from lightup import lightup

HERE = os.path.dirname(__file__)
OUT = r"C:\Users\argov\OneDrive\Co-Work OS\SkipperQuiz\media\vessels\night"
os.makedirs(OUT, exist_ok=True)

C_MH_F, C_MH_A, C_RED_SIDE = (14.2, 41), (82, 33), (80.8, 51.4)   # cargo port view
C_ANC_F, C_ANC_A = (14.2, 41), (95, 47)
st = lambda x, ys, c: [(x, y, c) for y in ys]

V = {
 "power_big_port":   ("cargo_port",  [(*C_MH_F, "w"), (*C_MH_A, "w"), (*C_RED_SIDE, "r")]),
 "power_big_bow":    ("cargo_bow",   [(50, 36, "w"), (50, 19.5, "w"), (38, 47, "g"), (62, 47, "r")]),
 "power_stern":      ("cargo_stern", [(50, 51, "w")]),
 "tow_stern":        ("cargo_stern", [(50, 46, "y"), (50, 51, "w")]),
 "power_small_port": ("motor_port",  [(62, 35, "w"), (40, 49.5, "r")]),
 "sail_port":        ("sail_port",   [(31.5, 72, "r")]),
 "sail_optional":    ("sail_port",   [(48.8, 8.5, "r"), (48.8, 12.5, "g"), (31.5, 72, "r")]),
 "pilot_port":       ("pilot_port",  [(56.5, 27, "w"), (56.5, 31.5, "r"), (41, 44, "r")]),
 "trawler_port":     ("trawler_port", [(26.5, 24.5, "g"), (26.5, 29.5, "w"), (41, 45, "r")]),
 "netfish_port":     ("netfish_port", [(37.8, 25, "r"), (37.8, 30, "w"), (56, 50, "r")]),
 "ram_port":         ("work_port",   [(35.8, 23.5, "w"), (35.8, 28.5, "r"), (35.8, 33, "w"), (35.8, 37.5, "r"), (25, 46, "r")]),
 "divers":           ("work_port",   [(35.8, 28.5, "r"), (35.8, 33, "w"), (35.8, 37.5, "r")]),
 "draft_port":       ("cargo_port",  [(*C_MH_F, "w"), (*C_MH_A, "w")] + st(82, [37.5, 41.5, 45.5], "r") + [(*C_RED_SIDE, "r")]),
 "mines_port":       ("mines_port",  [(46.8, 22, "g"), (42, 26.8, "g"), (51.5, 26.8, "g"), (46.3, 31.5, "w"), (38, 46, "r")]),
 "nuc_port":         ("cargo_port",  [(82, 33, "r"), (82, 37.5, "r"), (*C_RED_SIDE, "r")]),
 "aground_port":     ("cargo_port",  [(*C_ANC_F, "w"), (*C_ANC_A, "w"), (82, 33, "r"), (82, 37.5, "r")]),
 "anchor_port":      ("cargo_port",  [(*C_ANC_F, "w"), (*C_ANC_A, "w")]),
 "tow_port":         ("tug_port",    [(17.8, 37, "w"), (17.8, 43, "w"), (14.5, 54, "r"), (50.5, 58.5, "r")]),
 "hover_port":       ("hover_port",  [(37, 29.5, "y"), (37, 34, "w"), (24, 45, "r")]),
}

for name, (base, lights) in V.items():
    src = os.path.join(HERE, "src", base + ".jpg")
    W, H = Image.open(src).size
    r = max(9, int(W * 0.011))
    spec = ";".join(f"{int(x * W / 100)},{int(y * H / 100)},{c},{r}" for x, y, c in lights)
    lightup(src, os.path.join(OUT, name + ".jpg"), spec)
print(len(V), "images ->", OUT)
