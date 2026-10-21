"""Lesson narration in Alex's voice: thin wrapper over tools/voice/voice.js (the one VO pipeline:
lexicon -> ElevenLabs clone -> mastering -> length check, answer letters as alphabet names,
3s pause after "התשובה הנכונה היא").
usage: python el_tts.py <vo.txt> <aud_dir>      -> <aud_dir>/seg_<sid>.mp3 for every '## sid' section
Skips sections whose seg file already exists for the same text (cache key in <aud_dir>/raw/<sid>.txt).
Module attributes (env, KEY, VOICE, MODEL, CHAIN) stay for radio_sim.py."""
import os, re, sys, json, subprocess
import nowin  # child processes (ffmpeg, node, python) without a console window
ROOT = r'C:/Users/argov/OneDrive/Co-Work OS/SkipperQuiz'
CFG = json.load(open(ROOT + '/tools/voice/voice-config.json', encoding='utf-8'))

env = {}
for ln in open(ROOT + '/.env', encoding='utf-8'):
    m = re.match(r'\s*(ELEVENLABS_[A-Z0-9_]+)\s*=\s*(.*?)\s*$', ln)
    if m: env[m.group(1)] = m.group(2).strip('"\'')
KEY, VOICE = env['ELEVENLABS_API_KEY'], env['ELEVENLABS_VOICE_ID']
MODEL = env.get('ELEVENLABS_MODEL', CFG['models']['default'])
CHAIN = CFG['masterChain']


def main(vo, aud):
    subprocess.run(['node', ROOT + '/tools/voice/voice.js', 'segments', vo, aud], check=True)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
