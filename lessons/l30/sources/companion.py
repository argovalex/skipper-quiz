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
    # lesson 12
    's02_what': 'מה זה GPS', 's03_how': 'איך זה עובד', 's04_fix_q41': 'איך מתקבל אתר', 's05_name_q42': 'ממ"ג', 's06_sats_q45': 'כמה לוויינים',
    's07_features': 'מאפיינים', 's08_settings': 'הגדרות והתראות', 's09_position_only': 'מיקום בלבד', 's10_speed_q188': 'מדידת מהירות',
    's11_anchor_q47': 'עוגן בזרם', 's12_current_q104': 'זרם נגדי', 's13_compass': 'מצפן מול GPS', 's14_functions': 'פונקציות',
    's15_route_q160': 'ROUTE, TRACK, CTS', 's16_mob_q44': 'MOB מול MARK', 's17_errors': 'דיוק ודאטום', 's18_dop_q137': 'PDOP',
    's19_accuracy_q158': 'בדיקת דיוק', 's20_antenna_q46': 'האנטנה', 's21_summary': 'סיכום',
    # lesson 13
    's02_gmdss': 'GMDSS', 's03_waves': 'גל רדיו', 's04_antenna_q111': 'גודל האנטנה', 's05_antenna_q72': 'מה נדרש מהאנטנה', 's06_propagation': 'קרקע, רקיע, ישיר',
    's07_hf_night_q124': 'HF בלילה', 's08_bands': 'MF, VHF, UHF', 's08b_units': 'יחידות תדר', 's09_vhf_band_q125': 'ה-VHF הימי', 's10_why_band_q91': 'למה דווקא שם', 's11_modulation_q112': 'אפנון',
    's12_controls': 'הפקדים', 's13_dualwatch_q55': 'DUAL WATCH', 's14_dualwatch_q116': '16 וערוץ נבחר', 's15_squelch_q57': 'כיוון שדורש ניסיון', 's16_range': 'טווחי קשר',
    's17_range_q58': 'מה קובע את הטווח', 's18_handheld_q127': 'VHF נייד', 's19_summary': 'סיכום',
    # lesson 14
    's02_simplex': 'SIMPLEX', 's03_duplex': 'DUPLEX', 's04_q122': 'אוטומטי לפי הערוץ', 's05_channels': 'הערוצים החשובים', 's06_q120': 'ערוץ 25',
    's07_q68': 'ערוץ 26', 's08_q69': 'ערוץ 6', 's09_q56': 'ערוץ נקי למצוקה', 's10_q93': 'מחפשים את הטעות', 's11_q92': 'למה הוקצו ערוצים',
    's12_callsigns': 'אותות קריאה', 's13_q90': 'זיהוי בקשר בינלאומי', 's14_mmsi': 'MMSI', 's15_q52': 'MMSI של כלי שייט', 's16_q142': '428000500',
    's17_dsc': 'DSC', 's18_q53': 'המכלול DSC', 's19_q89': 'מכלול מול מספר', 's20_q143': 'מה יוצא בכל שידור', 's21_q74': 'עד שמאשרים', 's22_q54': 'הסמכה', 's23_summary': 'סיכום',
    # lesson 15
    's02_navtex': 'מה זה NAVTEX', 's03_q166': 'איך ההודעות מועברות', 's04_q144': 'שידור מהספינה', 's05_freq': 'תדרי NAVTEX', 's06_q117': 'תחום התדרים',
    's07_areas': 'אזורים ותחנות', 's08_q66': 'כל כמה זמן', 's09_q130': 'כמה ולכמה זמן', 's10_q167': 'שרשרת המשדרים', 's11_types': 'סוגי הודעות',
    's12_q83': 'מצוקה ב-NAVTEX', 's13_q168': 'מצוקה ב-NAVTEX, נוסח שני', 's14_priority': 'דרגות עדיפות', 's15_q84': 'VITAL, IMPORTANT, ROUTINE',
    's16_q119': 'VITAL, IMPORTANT, ROUTINE, נוסח שני', 's17_format': 'מבנה הודעה', 's18_q129': 'MA33', 's19_predeparture': 'הכנה לפני הפלגה',
    's20_q71': 'מה מתקינים', 's21_summary': 'סיכום',
    # lesson 16
    's02_epirb': 'משואת EPIRB', 's03_q6': 'FLOAT FREE', 's04_q170': 'FLOAT FREE, נוסח שני', 's05_q64': 'איפה שמים את המשואה', 's06_areas': 'אזורי שייט',
    's07_cospas': 'משואה לוויינית', 's08_q85': 'משואת Cospas-Sarsat', 's09_q169': 'משואת Cospas-Sarsat, נוסח שני', 's10_q145': 'בכל האזורים',
    's11_q150': 'אפקט דופלר', 's12_sart': 'משיב מכ״מ SART', 's13_q75': 'מה מעיר את ה-SART', 's14_q86': 'משיב מכ״מ', 's15_q106': 'מי קולט SART',
    's16_sart_screen': 'SART על המכ״מ', 's17_q88': 'מה רואים על המסך', 's18_q126': 'מה מחשבים', 's19_q87': 'מאפייני SART', 's20_q177': 'מאפייני SART, נוסח שני',
    's21_q62': 'מי קולט מצוקה', 's22_q107': 'מי קולט מצוקה, נוסח שני', 's23_q110': 'ציוד חובה ב-A1', 's24_ais': 'מערכת AIS', 's25_q128': 'מטרת ה-AIS', 's26_summary': 'סיכום',
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
