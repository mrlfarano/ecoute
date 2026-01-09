#!/bin/bash
# Create macOS DMG installer

echo "================================================"
echo " Creating macOS DMG Installer"
echo "================================================"

APP_NAME="Ecoute"
VERSION="2.0.0"
DMG_NAME="${APP_NAME}-${VERSION}.dmg"

# Check if app exists
if [ ! -d "dist/${APP_NAME}.app" ]; then
    echo "ERROR: Application not built yet!"
    echo "Please run build_macos.sh first."
    exit 1
fi

# Install create-dmg if not available
if ! command -v create-dmg &> /dev/null; then
    echo "Installing create-dmg..."
    brew install create-dmg
fi

# Clean previous DMG
rm -f "dist/${DMG_NAME}"

# Create DMG
echo "Creating DMG..."
create-dmg \
  --volname "${APP_NAME}" \
  --volicon "assets/icon.icns" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "${APP_NAME}.app" 200 190 \
  --hide-extension "${APP_NAME}.app" \
  --app-drop-link 600 185 \
  "dist/${DMG_NAME}" \
  "dist/${APP_NAME}.app"

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo " DMG created successfully!"
    echo " Location: dist/${DMG_NAME}"
    echo "================================================"
else
    echo "DMG creation failed!"
    exit 1
fi
