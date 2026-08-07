@echo off
cd /d "%~dp0"
echo ======================================
echo   Skipper Quiz — מעדכן מאגר שאלות
echo ======================================
echo.
echo מוריד ומחלץ PDF-ים רשמיים מגוב"ל...
python scraper.py --source pdf
echo.
echo סורק אתרי שייט...
python scraper.py --source web
echo.
echo סטטיסטיקות:
python scraper.py --stats
echo.
echo ======================================
echo   קובץ questions.json עודכן!
echo ======================================
pause
