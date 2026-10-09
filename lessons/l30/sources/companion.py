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
    # lesson 6
    's02_fluxgate_how': 'מצפן שער שטף', 's03_fluxgate_q78': 'איך שער שטף עובד', 's04_fluxgate_pros': 'שער שטף: יתרונות וחסרונות',
    's05_fluxgate_q141': 'מה אינו יתרון', 's06_gyro_how': "מצפן ג'יירו", 's07_gyro_pros': "ג'יירו: יתרונות וחסרונות",
    's08_gyro_q51': "חסרונות הג'יירו", 's09_gyro_q157': 'שאלה כמעט זהה', 's10_true_course_q187': 'הכיוון האמיתי',
    # lesson 7
    's02_log_history': 'למה קשר', 's03_speed_formula': 'מטר לשנייה', 's04_speed_q12': 'חישוב מהירות', 's05_speed_q13': 'החבל עם הקשרים',
    's06_impeller_log': 'אימפלר', 's07_log_gps_q48': 'מים מול קרקע', 's08_wind_true_apparent': 'רוח אמיתית ויחסית',
    's09_wind_q11': 'סירה עומדת', 's10_wind_q25': 'סירה בתנועה',
    # lesson 8
    's02_lead_line_q40': 'חבל ומשקולת', 's03_uses_q31_q35': 'שימושים', 's04_echo_principle': 'עקרון ההד',
    's05_transducer_q165': 'תפקיד הממיר', 's06_transducer_q32': 'איפה הממיר', 's07_care_q33_34_176': 'אחזקת הממיר',
    's08_accuracy_q37': 'דיוק', 's09_range_q135': 'טווח ופולסים', 's10_depth_formula': 'עומק, שוקע וגאות',
    's11_depth_q38': 'חישוב עומק במפה', 's12_depth_q36_q39': 'מאיפה ההבדל', 's13_depth_q178': 'מד עומק מכויל',
    # lesson 9
    's02_principle': 'עקרון הפעולה', 's03_detects_q50': 'מה המכ״מ רואה', 's04_uses_q49_q161': 'שימושי המכ״מ',
    's05_nav_q146': 'ניווט במכ״מ', 's06_display_ebl_vrm': 'המסך: EBL, VRM וסמן', 's07_range_q63': 'טווח הגילוי',
    's08_quality_q80_q164': 'מה משפיע על הקליטה', 's09_pulse_q163': 'אורך הפולס', 's10_discrimination_q114': 'הפרדה בטווח',
    's11_bands_beam': 'תדרים ואנטנה', 's12_refraction_q131': 'התעקמות הגל', 's13_gain_q76': 'GAIN',
    's14_rain_q79_q162': 'גשם', 's15_standby_q82': 'סטנד ביי', 's16_summary': 'סיכום',
    # lesson 10
    's02_relative_bearings': 'ירוק ואדום', 's03_head_up_north_up': 'תמונה אמיתית ויחסית', 's04_true_bearing_calc': 'מיחסי לאמיתי',
    's05_exam_turn': 'שאלה מהמבחן', 's06_collision_q189': 'סכנת התנגשות', 's07_plot_q81': 'שרטוט על המסך',
    's08_compass_q23': 'בדיקה במצפן', 's09_more_controls': 'TUNING ו-INTERFERENCE REJECTION',
    's10_antenna_location': 'מיקום האנטנה', 's11_reflector_q105': 'מחזיר הד מכ״מ', 's12_summary': 'סיכום',
    # lesson 11
    's02_system': 'חלקי המערכת', 's03_how_to_use': 'הפעלה', 's04_accuracy_q28': 'דיוק', 's05_advantage_q26': 'היתרון',
    's06_power_q10': 'צריכת חשמל', 's07_disadvantages_q29': 'החסרונות', 's08_windvane_q17': 'הגה רוח',
    's09_windvane_q30': 'הגה רוח: בעד ונגד',
    # shared
    's01_intro': 'פתיחה', 's10_summary': 'סיכום', 's11_summary': 'סיכום', 's14_summary': 'סיכום',
}

vo, out, title = sys.argv[1:4]
t = open(vo, encoding='utf-8').read()
for a, b in DISPLAY: t = t.replace(a, b)
t = apply(t, load_lexicon())
t = re.sub(r'(?<![\u0590-\u05FF])אֹ(?![\u0590-\u05FF])', 'א', t)
t = title + '\n\n' + re.sub(r'## (\S+)', lambda m: '# ' + HEADINGS.get(m.group(1), m.group(1)), t)
open(out, 'w', encoding='utf-8').write(t)
print('companion ok')
