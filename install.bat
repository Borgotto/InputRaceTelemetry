@echo off

echo - Installing modules...
pip install -r %~dp0\res\requirements.txt >nul
echo - Modules installed successfully
echo Installation completed
pause