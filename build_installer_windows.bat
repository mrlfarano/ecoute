@echo off
REM Windows Installer Builder using Inno Setup
REM Download Inno Setup from: https://jrsoftware.org/isinfo.php

echo ================================================
echo  Creating Windows Installer
echo ================================================

REM Check if Inno Setup is installed
if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo ERROR: Inno Setup not found!
    echo.
    echo Please download and install Inno Setup from:
    echo https://jrsoftware.org/isinfo.php
    echo.
    pause
    exit /b 1
)

REM Check if build exists
if not exist "dist\Ecoute\Ecoute.exe" (
    echo ERROR: Application not built yet!
    echo Please run build_windows.bat first.
    echo.
    pause
    exit /b 1
)

REM Run Inno Setup compiler
echo Building installer...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_windows.iss

if errorlevel 1 (
    echo Installer build failed!
    pause
    exit /b 1
)

echo.
echo ================================================
echo  Installer created successfully!
echo  Location: dist\EcouteSetup.exe
echo ================================================
echo.

pause
