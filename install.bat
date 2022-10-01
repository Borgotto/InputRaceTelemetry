@echo off

echo - Installing fonts...
copy %~dp0\res\Mont-HeavyDEMO.otf %systemroot%\Fonts >nul 2>&1
if ERRORLEVEL 1 (
    echo Error: Could not install Font. Please run as Administrator.
    pause
    exit /b 1)
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "Mont Heavy DEMO (OpenType)" /t REG_SZ /d %~dp0\res\Mont-HeavyDEMO.otf /f >nul
echo - Font installed successfully
echo - Installing modules...
pip install -r %~dp0\res\requirements.txt >nul
echo - Modules installed successfully
echo Installation completed
pause