@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (
  py -3 account_manager.py
  goto :end
)
where python >nul 2>&1
if %errorlevel%==0 (
  python account_manager.py
  goto :end
)
echo Python 3 kurulumu gerekiyor. https://www.python.org/downloads/windows/
pause
:end
