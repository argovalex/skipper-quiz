"""Build the niqqud'd companion .txt from a lesson vo.txt (TTS text), mapping TTS-only spellings back.
usage: python companion.py <vo.txt> <out.txt> "<title line>"
Section headings: '## sid' -> '# <readable title>' taken from HEADINGS (fallback: sid)."""
import re, sys
sys.path.insert(0, r'C:/Users/argov/OneDrive/Co-Work OS/SkipperQuiz/tools/lesson')
from niqqud import load_lexicon, apply

DISPLAY = [('גברַאלְטָר', 'גיברלטר'), ('הרָאם לַיְין', 'ה-Rhumb line'), ('רָאם לַיְין', 'Rhumb line'), ('U T C', 'UTC'), ('G M T', 'GMT'), ('Z D', 'ZD'), ('G P S', 'GPS'), ('C O G', 'COG')]
HEADINGS = {
    # lesson 1
    's02_axis': 'הציר והקטבים', 's03_equator': 'קו המשווה', 's04_great_circle': 'מעגל גדול', 's05_small_circle': 'מעגל קטן',
    's06_latitude': 'קווי רוחב', 's07_lat_distance': 'המרחק בין קווי רוחב', 's07b_lat_end': 'היכן מסתיים קו רוחב',
    's08_longitude': 'קווי אורך', 's08b_long_distance': 'המרחק בין קווי אורך', 's09_meridian_pair': 'קו אורך משלים',
    's09b_greenwich': "קו גריניץ'", 's10_position': 'אתר גיאוגרפי',
    # lesson 2
    's02_projection': 'היטל מרקטור', 's03_mercator_grid': 'ארבעת החוקים והמחיר', 's04_distortion': 'עיוות ומדידת מרחק',
    's05_rhumb': 'Rhumb line', 's06_gc_vs_rhumb': 'מעגל גדול מול קו ישר', 's07_nautical_mile': 'המייל הימי',
    's08_mile_length': 'אורך המייל', 's09_true_north': 'הצפון האמיתי והכיוונים',
    # lesson 3
    's02_rotation': 'סיבוב כדור הארץ', 's03_utc': "UTC וגריניץ'", 's04_zones': 'אזורי זמן', 's05_zone_time': 'זמן אזורי',
    's06_local_time': 'זמן מקומי', 's07_lmt': 'זמן מקומי ממוצע', 's08_utc_plus3': 'UTC+3', 's09_date_line': 'קו התאריך',
    's10_method': 'שיטת החישוב', 's11_q108': 'שאלת חישוב 108', 's12_q133': 'שאלת חישוב 133', 's13_summary': 'סיכום',
    # lesson 4
    's03_horizon': 'טווח האופק', 's04_seasons': 'עונות השנה', 's05_moon': 'הירח', 's06_polaris_axis': 'כוכב הצפון וציר כדור הארץ',
    's07_polaris_alt': 'גובה כוכב הצפון וקו הרוחב', 's08_q175': 'בין חיפה לקפריסין', 's09_same_angle': 'אותה זווית כל ערב',
    's10_south': 'חצי הכדור הדרומי', 's11_little_dipper': 'העגלה הקטנה', 's12_q102': 'שאלת ציורים', 's13_stars_far': 'למה הכוכבים נראים קטנים',
    's14_summary': 'סיכום',
    # lesson 5
    's02_parts': 'חלקי המצפן הימי', 's03_why': 'למה צריך מצפן', 's04_course_bearing': 'קורס מול כיוון', 's05_angle': 'מצפן הוא מד זווית',
    's06_how': 'איך המצפן עובד', 's07_errors': 'שגיאות המצפן', 's08_variation': 'וריאציה', 's09_deviation': 'דויאציה',
    's10_speakers': 'מכשירים עם מגנטים', 's11_table': 'טבלת דויאציה', 's12_gps': 'מצפן מול GPS', 's13_rotate': 'סיבוב במקום',
    # shared
    's01_intro': 'פתיחה', 's10_summary': 'סיכום', 's11_summary': 'סיכום',
}

vo, out, title = sys.argv[1:4]
t = open(vo, encoding='utf-8').read()
for a, b in DISPLAY: t = t.replace(a, b)
t = apply(t, load_lexicon())
t = re.sub(r'(?<![\u0590-\u05FF])אֹ(?![\u0590-\u05FF])', 'א', t)
t = title + '\n\n' + re.sub(r'## (\S+)', lambda m: '# ' + HEADINGS.get(m.group(1), m.group(1)), t)
open(out, 'w', encoding='utf-8').write(t)
print('companion ok')
