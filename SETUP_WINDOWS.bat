@echo off
title Podar LMS Setup
echo.
echo  ==========================================
echo       PODAR LMS - Windows Quick Setup
echo  ==========================================
echo.

python setup_local.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo  [ERROR] Setup failed. Make sure Python 3.10+ and Node.js 18+ are installed.
    echo  Python: https://www.python.org/downloads/
    echo  Node:   https://nodejs.org/
    pause
    exit /b 1
)

pause
