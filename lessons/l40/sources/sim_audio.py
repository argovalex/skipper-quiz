"""Station replies for the GMDSS simulator (lessons/l40/simulator). Same VHF chain as the l30 lesson sims
(l30/sources/radio_sim.py: ElevenLabs voice -> band-limited, compressed, hiss, squelch burst), one mp3 per line.
usage: python sim_audio.py            -> lessons/l40/simulator/audio/<id>.mp3 (skips lines whose mp3 exists)"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'l30', 'sources'))
import nowin, radio_sim  # noqa: E401

radio_sim.VOICES['rescue'] = 'pNInz6obpgDQGcFmaJgB'  # second shore-side voice, so the rescue vessel is not Haifa Radio

SC = {  # extra scenarios: files are <pre><id>.mp3 (SONDRA keeps the bare names)
    '': dict(n='Sondra', P='four', cls='Sailing yacht', mmsi='four two eight one two three four five six'),
    'noa_': dict(n='Noa', P='six', cls='Motor yacht', mmsi='four two eight six five four three two one'),
    'dana_': dict(n='Dana', P='five', cls='Sailing yacht', mmsi='four two eight two three four five six seven'),
}
SHARED = {
    'haifa_sayagain': ('coast', 'Station calling MAYDAY, this is Haifa Radio. Say again your vessel name and position. Over.'),
    'haifa_generic': ('coast', 'Station calling Haifa Radio, this is Haifa Radio. Say again. Over.'),
}

def lines(pre, s):
    n = s['n']
    return {
        pre + 'haifa_ack': ('coast', f'MAYDAY. {n}, {n}, {n}. This is Haifa Radio, Haifa Radio, Haifa Radio. Received MAYDAY. Over.'),
        pre + 'haifa_task': ('coast', f'{n}, this is Haifa Radio. Rescue vessel is on the way to your position. If you abandon ship, activate your EPIRB and take your SART to the life raft. Report when in the life raft. Over.'),
        pre + 'haifa_raft': ('coast', f'{n}, this is Haifa Radio. Received, {s["P"]} persons in the life raft. Keep watch on channel one six. Out.'),
        pre + 'rcc_epirb': ('coast', f'{n}, {n}, {n}. This is RCC Haifa. Your four zero six EPIRB alert is received and your position is confirmed. Rescue vessel will be on scene in three zero minutes. Over.'),
        pre + 'rescue_sart': ('rescue', f'{n}, this is Rescue vessel. I have your SART on my radar, range eight miles. Keep the SART up high. Over.'),
        pre + 'rescue_sart_low': ('rescue', f'{n}, this is Rescue vessel. I have your SART on my radar, range five miles. Raise the SART higher. Over.'),
        pre + 'rescue_close': ('rescue', f'{n}, this is Rescue vessel. Visual contact with your life raft. Coming alongside. Out.'),
        pre + 'haifa_seelonce': ('coast', f'MAYDAY. All stations, all stations, all stations. This is Haifa Radio. Time one five four zero UTC. {s["cls"]} {n}, MMSI {s["mmsi"]}. SEELONCE FEENEE. Out.'),
    }

LINES = dict(SHARED)
for _pre, _s in SC.items(): LINES.update(lines(_pre, _s))

if __name__ == '__main__':
    out_dir = os.path.join(HERE, '..', 'simulator', 'audio'); wrk = os.path.join(HERE, '..', 'simulator', '_work')
    os.makedirs(out_dir, exist_ok=True); os.makedirs(wrk, exist_ok=True)
    for lid, (who, text) in LINES.items():
        mp3 = os.path.join(out_dir, f'{lid}.mp3')
        if os.path.isfile(mp3): continue
        fx = radio_sim.line(wrk, who, text)
        subprocess.run(['ffmpeg', '-y', '-i', fx, '-af', 'loudnorm=I=-16:TP=-1.5', '-ac', '1', '-c:a', 'libmp3lame', '-b:a', '96k', mp3],
                       check=True, capture_output=True)
        print(lid, flush=True)
