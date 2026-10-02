"""vo_display.txt (Alex's wording, digits, correct spelling) -> vo.txt (TTS) + companion.txt (display)."""
import re
src = open('vo_display.txt', encoding='utf-8').read()
NUM = {'0': 'אפס', '20': 'עשרים', '40': 'ארבעים', '45': 'ארבעים וחמש', '60': 'שישים', '90': 'תשעים',
       '100': 'מאה', '180': 'מאה ושמונים', '220': 'מאתיים ועשרים'}

def tts(t):
    t = t.replace('־', '')                                  # ב־0° -> ב0° -> באפס מעלות
    t = re.sub(r'(\d+)°', lambda m: NUM[m.group(1)] + ' מעלות', t)
    t = re.sub(r'(?<![\d.])(\d+)(?![\d])', lambda m: NUM[m.group(1)], t)
    t = t.replace(' = ', ' שווה ')
    # answer letter א: lexicon maps lone "א" -> "אֹ" (Latin O for SOS), so spell the letter name
    t = re.sub(r'(?<![֐-׿])א(?=[:\s,.])(?![֐-׿])', 'אָלֶף', t)
    return t

v = '\n'.join(l if l.startswith('## ') else tts(l) for l in src.split('\n'))
body = '\n'.join(l for l in v.split('\n') if not l.startswith('## '))
assert not re.search(r'\d', body), re.findall(r'.{10}\d.{10}', body)
open('vo.txt', 'w', encoding='utf-8').write(v)

H = {'s01_intro':'פתיחה','s02_axis':'הציר והסיבוב','s03_equator':'קו המשווה','s04_great_circle':'מעגל גדול','s05_small_circle':'מעגל קטן','s06_latitude':'קו רוחב','s07_lat_distance':'המרחק בין קווי רוחב','s07b_lat_end':'קו רוחב הוא מעגל סגור','s08_longitude':'קו אורך','s08b_long_distance':'המרחק בין קווי אורך','s09_meridian_pair':'מעגל שלם של קווי אורך','s09b_greenwich':"קו גריניץ'",'s10_position':'אתר גיאוגרפי','s11_summary':'סיכום'}
c = 'הרשת הגיאוגרפית · קורס ניווט חופי ומכשירים · שיעור 1\n\n' + re.sub(r'## (\S+)', lambda m: '# ' + H[m.group(1)], src)
c = c.replace('גברַאלְטָר', 'גיברלטר')
open('companion.txt', 'w', encoding='utf-8').write(c)
print('ok')
