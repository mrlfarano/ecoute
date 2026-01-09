#!/bin/bash
# Build script for Linux

echo "================================================"
echo " Building Ecoute AI Research Assistant"
echo " Platform: Linux"
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
    echo " Executable location: dist/Ecoute/Ecoute"
    echo "================================================"
    echo ""
    echo "To run the app:"
    echo "  cd dist/Ecoute && ./Ecoute"
    echo ""
    echo "To create a .deb package:"
    echo "  ./build_deb.sh"
    echo ""
else
    echo "Build failed!"
    exit 1
fi
