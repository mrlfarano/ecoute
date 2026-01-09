#!/bin/bash
# Build script for macOS

echo "================================================"
echo " Building Ecoute AI Research Assistant"
echo " Platform: macOS"
echo "================================================"

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build the application
echo "Building application..."
pyinstaller ecoute.spec --clean

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo " Build complete!"
    echo " Application location: dist/Ecoute.app"
    echo "================================================"
    echo ""
    echo "To run the app:"
    echo "  open dist/Ecoute.app"
    echo ""
    echo "To create a DMG installer:"
    echo "  ./build_dmg.sh"
    echo ""
else
    echo "Build failed!"
    exit 1
fi
