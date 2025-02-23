@echo off
title Nexus Radio Bot
chcp 65001 >nul
cd /d %~dp0
set BOT_SCRIPT=NexusRadioBot.py

:MENU
cls
echo ============================
echo      Nexus Radio Bot
echo ============================
echo [1] Starten
echo [2] Stoppen
echo [3] Beenden
echo ============================
set /p choice=Bitte eine Option waehlen: 

if "%choice%"=="1" (
    echo Starte den Bot...
    start "NexusRadioBot" cmd /c python %BOT_SCRIPT%
    echo Bot läuft nun.
    timeout /t 3 >nul
    goto MENU
)

if "%choice%"=="2" (
    echo Stoppe den Bot...
    for /f "tokens=2 delims= " %%A in ('tasklist ^| findstr /i "python.exe"') do taskkill /PID %%A /F
    echo Bot wurde gestoppt.
    timeout /t 2 >nul
    goto MENU
)

if "%choice%"=="3" (
    echo Beende das Programm...
    exit
)

echo Ungültige Eingabe, bitte erneut versuchen.
timeout /t 2 >nul
goto MENU
