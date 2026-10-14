"""Mobile (9:16) version of an l30 lesson, built from the existing 16:9 cards and cached audio (nothing re-recorded).
Each card's left half (caption + visual) goes on top, its right block (title, text, question) below.
Output: <lesson>/<name> - נייד.mp4 ; vertical cards in <lesson>/_v/.
usage: python vertical.py <work_dir> <lesson-number> [...]"""
import os, re, sys, ast, subprocess, importlib.util
import nowin  # child processes (ffmpeg, node, python) without a console window
from PIL import Image, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
spec = importlib.util.spec_from_file_location('u01', os.path.join(HERE, 'u01_cards.py')); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
LESSONS = ast.literal_eval(re.search(r'^LESSONS = (\{.*\})$', open(os.path.join(HERE, 'render_course.py'), encoding='utf-8').read(), re.M).group(1))
VW, VH = 1080, 1920
LEFT = (0, 200, 1300, 1440)                     # caption + visual panel of a 2560x1440 card
RIGHT = (1270, 0, 2560, 1440)                   # title, text, question
BLANK = C.base()[0]
BGIMG = BLANK.crop(RIGHT).resize((VW, VH), Image.LANCZOS)

def right_bbox(im, x0r=RIGHT[0]):
    """Tight box around the right block: diff against an empty card background."""
    R = (x0r,) + RIGHT[1:]
    diff = ImageChops.difference(im.crop(R), BLANK.crop(R)).convert('L').point(lambda v: 255 if v > 24 else 0)
    x0, y0, x1, y1 = diff.getbbox() or (0, 0, R[2] - R[0], R[3] - R[1])
    m = 40
    return (R[0] + max(0, x0 - m), max(0, y0 - m), R[0] + min(R[2] - R[0], x1 + m), min(1440, y1 + m))

def vcard(src, dst):
    im = Image.open(src).convert('RGB')
    out = BGIMG.copy()
    top = im.crop(LEFT); top = top.resize((VW, round(top.height * VW / top.width)), Image.LANCZOS)
    out.paste(top, (0, 60))
    bb = right_bbox(im, 1305 if re.search(r'intro|summary', src) else RIGHT[0]); rb = im.crop(bb); room = VH - (60 + top.height) - 40
    mask = ImageChops.difference(rb, BLANK.crop(bb)).convert('L').point(lambda v: min(255, v * 6))   # content only, soft edges
    s = min(VW / rb.width, room / rb.height, 1.0)
    if s < 0.7: print(f'  small text {s:.2f}: {os.path.basename(src)}', flush=True)
    sz = (round(rb.width * s), round(rb.height * s)); rb = rb.resize(sz, Image.LANCZOS); mask = mask.resize(sz, Image.LANCZOS)
    out.paste(rb, ((VW - rb.width) // 2, 60 + top.height + (room - rb.height) // 2), mask)
    out.save(dst)

def scene_cuts(mp4, thr=0.08):
    r = subprocess.run(['ffmpeg', '-i', mp4, '-vf', f"select='gt(scene,{thr})',showinfo", '-f', 'null', '-'], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return [float(t) for t in re.findall(r'pts_time:([\d.]+)', r.stderr)]

def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)

q = lambda p: p.replace(chr(92), '/').replace("'", "'\\''")   # concat-demuxer quoting (lesson 6 has an apostrophe)

def from_video(d, name, v, wrk):
    """No audio cache: take card timing + audio straight from the approved 16:9 lesson (3s logo intro, 4s outro)."""
    src = os.path.join(d, name + '.mp4'); T = dur(src)
    sids = re.findall(r'^## (\S+)', open(os.path.join(d, 'vo.txt'), encoding='utf-8').read(), re.M)
    for thr in (0.08, 0.04, 0.02, 0.01, 0.005):          # near-identical consecutive cards need a lower threshold
        cuts = [t for t in scene_cuts(src, thr) if 3.3 < t < T - 4.3]
        if len(cuts) >= len(sids) - 1: break
    if len(cuts) != len(sids) - 1:
        raise SystemExit(f'{name}: {len(cuts)} scene cuts for {len(sids)} cards, cannot time the cards')
    edges = [3.0] + cuts + [T - 4.0]
    lst = os.path.join(wrk, 'cards.txt')
    with open(lst, 'w', encoding='utf-8') as f:
        for sid, a, b in zip(sids, edges, edges[1:]):
            f.write(f"file '{q(os.path.join(v, sid + '.png'))}'\nduration {b - a:.3f}\n")
        f.write(f"file '{q(os.path.join(v, sids[-1] + '.png'))}'\n")
    raw = os.path.join(wrk, 'lesson_raw_v.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-ss', '3', '-t', f'{T - 7:.3f}', '-i', src,
                    '-map', '0:v', '-map', '1:a', '-vf', f'fps=25,scale={VW}:{VH},setsar=1', '-c:v', 'libx264', '-tune', 'stillimage', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-ar', '44100', '-ac', '2', '-b:a', '192k', '-t', f'{T - 7:.3f}', raw], check=True)
    return raw

def light(full, out):
    """Phone encode: 720x1280, 10 fps stills, mono voice -> ~0.5 MB/min."""
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', full, '-vf', 'scale=720:1280', '-r', '10', '-c:v', 'libx264', '-crf', '30', '-preset', 'slow',
                    '-tune', 'stillimage', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ac', '1', '-b:a', '48k', '-movflags', '+faststart', out], check=True)

if __name__ == '__main__':
    W = sys.argv[1]; py = sys.executable
    for n in map(int, sys.argv[2:]):
        name = LESSONS[n]; d = os.path.join(HERE, '..', 'cards', name); v = os.path.join(d, '_v'); os.makedirs(v, exist_ok=True)
        aud = os.path.join(W, f'l30u{n}el', 'aud'); wrk = os.path.join(W, f'l30u{n}el'); os.makedirs(wrk, exist_ok=True)
        for sid in re.findall(r'^## (\S+)', open(os.path.join(d, 'vo.txt'), encoding='utf-8').read(), re.M):
            if True:
                src, dst = os.path.join(d, sid + '.png'), os.path.join(v, sid + '.png')
                if not (os.path.isfile(dst) and os.path.getmtime(dst) >= os.path.getmtime(src)):   # native vertical card (u16+) wins
                    vcard(src, dst)
        print('cards', n, flush=True)
        if os.path.isdir(aud):          # cached segments (same run as the 16:9 video)
            raw = os.path.join(wrk, 'lesson_raw_v.mp4')
            subprocess.run([py, ROOT + '/tools/lesson/assemble.py', '--vo', d + '/vo.txt', '--audio', aud, '--cards', v, '--out', raw,
                            '--workdir', os.path.join(aud, 'wrk_v'), '--size', f'{VW}x{VH}'], check=True)
        else:
            raw = from_video(d, name, v, wrk)
        full = os.path.join(wrk, 'lesson_v_branded.mp4')
        subprocess.run([py, ROOT + '/tools/lesson/brand.py', raw, full, '--size', f'{VW}x{VH}'], check=True)
        light(full, os.path.join(d, name + ' - נייד.mp4'))
        print('DONE vertical', n, flush=True)