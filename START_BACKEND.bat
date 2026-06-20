@echo off
title Podar LMS - Backend
echo Starting Podar LMS Backend on http://localhost:8000 ...
echo.
cd backend
venv\Scripts\python manage.py runserver
pause
