echo off

cd %~dp0
call venv\Scripts\activate.bat
python main.py --setting rorona.json --imagedir %1
pause