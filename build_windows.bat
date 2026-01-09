@echo off
REM Build script for Windows

echo ================================================
echo  Building Ecoute AI Research Assistant
echo  Platform: Windows
echo ================================================

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>NUL
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build the application
echo Building application...
pyinstaller ecoute.spec --clean

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo ================================================
echo  Build complete!
echo  Executable location: dist\Ecoute\Ecoute.exe
echo ================================================
echo.
echo To create an installer, run:
echo   build_installer_windows.bat
echo.

pause
