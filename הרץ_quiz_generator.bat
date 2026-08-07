@echo off
cd /d "%~dp0"
echo מייצר סרטוני Skipper Quiz...
python generate_quiz_video.py raspen_5_diverse.json --all
echo.
echo סיום! פתח את תיקיית quiz_videos
pause
explorer quiz_videos
