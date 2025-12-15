@echo off
cd /d "%~dp0"
echo アプリを起動しています... / Starting the app...
python -m streamlit run app.py
if errorlevel 1 (
   echo エラーが発生しました。 / An error occurred.
   pause
)
pause
