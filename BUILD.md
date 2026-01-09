# 📦 Building Ecoute as an Installable Application

This guide explains how to build Ecoute AI Research Assistant as a standalone installable application for Windows, macOS, and Linux.

---

## 🎯 Overview

Ecoute can be packaged into native applications for all major platforms:

- **Windows**: `.exe` standalone executable + optional installer
- **macOS**: `.app` bundle + optional `.dmg` installer
- **Linux**: Standalone executable + optional `.deb`/`.rpm` package

---

## 📋 Prerequisites

### All Platforms

1. **Python 3.8+** installed
2. **All dependencies** installed:
   ```bash
   pip install -r requirements.txt
   ```

3. **PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

4. **FFmpeg** installed on your system

### Platform-Specific Requirements

#### Windows
- **Inno Setup** (optional, for creating installer): https://jrsoftware.org/isinfo.php

#### macOS
- **Xcode Command Line Tools**:
  ```bash
  xcode-select --install
  ```
- **create-dmg** (optional, for DMG creation):
  ```bash
  brew install create-dmg
  ```

#### Linux
- **dpkg-deb** (usually pre-installed)
- Standard build tools

---

## 🏗️ Building the Application

### Windows

#### Quick Build
```bash
build_windows.bat
```

This creates:
- `dist/Ecoute/Ecoute.exe` - Standalone executable
- All required dependencies in `dist/Ecoute/` folder

#### Create Installer (Optional)
```bash
build_installer_windows.bat
```

Requirements:
- Inno Setup must be installed
- Creates `dist/EcouteSetup.exe` - Full installer

**Distribution:**
- Zip the `dist/Ecoute` folder for portable distribution
- Or distribute `EcouteSetup.exe` for easy installation

---

### macOS

#### Quick Build
```bash
chmod +x build_macos.sh
./build_macos.sh
```

This creates:
- `dist/Ecoute.app` - macOS application bundle

#### Create DMG (Optional)
```bash
./build_dmg.sh
```

Creates `dist/Ecoute-2.0.0.dmg` - Drag-and-drop installer

**Distribution:**
- Compress `Ecoute.app` to `.zip` for simple distribution
- Or distribute the `.dmg` for professional installer experience

**Note:** For distribution outside the App Store, you may need to:
1. Sign the app with your Apple Developer certificate
2. Notarize the app with Apple
3. Users may need to allow it in System Preferences > Security

---

### Linux

#### Quick Build
```bash
chmod +x build_linux.sh
./build_linux.sh
```

This creates:
- `dist/Ecoute/Ecoute` - Standalone executable
- All dependencies in `dist/Ecoute/` folder

**Distribution:**
- Create a `.tar.gz`:
  ```bash
  cd dist
  tar -czf Ecoute-2.0.0-linux-x64.tar.gz Ecoute/
  ```

---

## 📦 File Structure After Build

```
dist/
├── Ecoute/              # Standalone folder
│   ├── Ecoute(.exe)    # Main executable
│   ├── _internal/       # Dependencies
│   ├── custom_speech_recognition/
│   └── tiny.en.pt
│
├── Ecoute.app/         # macOS only
│   └── Contents/
│       └── MacOS/
│
├── EcouteSetup.exe     # Windows installer (optional)
└── Ecoute-2.0.0.dmg    # macOS DMG (optional)
```

---

## ⚙️ Configuration Options

### PyInstaller Spec File (`ecoute.spec`)

The spec file controls the build process. Key settings:

```python
# Console mode (shows terminal)
console=True   # Set to False to hide console window

# Icon (platform-specific)
icon='assets/icon.ico'  # Windows
icon='assets/icon.icns' # macOS

# Data files to include
datas=[
    ('custom_speech_recognition', 'custom_speech_recognition'),
    ('tiny.en.pt', '.'),
]

# Hidden imports (dependencies not auto-detected)
hiddenimports=[
    'customtkinter',
    'pyaudiowpatch',
    # ... etc
]
```

### Creating Icons

#### Windows (.ico)
- Required size: 256x256 pixels
- Use online converter or `pillow`:
  ```python
  from PIL import Image
  img = Image.open('icon.png')
  img.save('assets/icon.ico', format='ICO', sizes=[(256,256)])
  ```

#### macOS (.icns)
- Create iconset:
  ```bash
  mkdir icon.iconset
  sips -z 512 512 icon.png --out icon.iconset/icon_512x512.png
  sips -z 256 256 icon.png --out icon.iconset/icon_256x256.png
  # ... other sizes
  iconutil -c icns icon.iconset
  ```

---

## 🐛 Troubleshooting

### Build Fails with Missing Dependencies
**Solution:** Add to `hiddenimports` in `ecoute.spec`:
```python
hiddenimports=[
    'missing_module_name',
]
```

### "Cannot find FFmpeg" Error
**Solution:** FFmpeg must be installed on user's system:
- Windows: `choco install ffmpeg` or include in installer
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

### Large Executable Size
**Solutions:**
- Use `--onefile` for single executable (slower startup)
- Exclude unnecessary packages:
  ```python
  excludes=['matplotlib', 'scipy', ...]
  ```
- Use UPX compression (enabled by default)

### macOS "App is damaged" Warning
**Solution:** Remove quarantine attribute:
```bash
xattr -cr dist/Ecoute.app
```

For distribution, you need to sign and notarize the app.

### Windows Antivirus False Positives
**Solution:**
- Sign the executable with a code signing certificate
- Submit to Microsoft SmartScreen for reputation
- Users may need to allow in Windows Defender

---

## 🚀 Distribution Best Practices

### Version Management
Update version in:
1. `ecoute.spec` - `CFBundleVersion`
2. `installer_windows.iss` - `MyAppVersion`
3. `build_dmg.sh` - `VERSION`

### File Naming Convention
```
Ecoute-{version}-{platform}-{arch}.{ext}

Examples:
- Ecoute-2.0.0-windows-x64.zip
- Ecoute-2.0.0-macos-universal.dmg
- Ecoute-2.0.0-linux-x64.tar.gz
```

### GitHub Releases
1. Tag version:
   ```bash
   git tag v2.0.0
   git push origin v2.0.0
   ```

2. Create release with built artifacts:
   - Windows: `EcouteSetup.exe` + `Ecoute-windows.zip`
   - macOS: `Ecoute-2.0.0.dmg`
   - Linux: `Ecoute-linux-x64.tar.gz`

### checksums
Generate SHA256 checksums:
```bash
sha256sum Ecoute-* > checksums.txt
```

---

## 📝 Build Checklist

Before distributing:

- [ ] Test on clean machine (no Python installed)
- [ ] Verify all features work
- [ ] Check microphone/speaker permissions
- [ ] Test with/without internet
- [ ] Verify API key configuration methods work
- [ ] Test Deep Dive feature
- [ ] Check all UI panels render correctly
- [ ] Verify search functionality
- [ ] Test action item extraction
- [ ] Update version numbers
- [ ] Generate checksums
- [ ] Write release notes

---

## 🆘 Getting Help

### Common Issues

1. **Import errors**: Add missing modules to `hiddenimports`
2. **File not found**: Add to `datas` in spec file
3. **DLL errors**: Install Visual C++ Redistributable (Windows)
4. **Permission errors**: Check microphone/speaker access permissions

### Resources

- PyInstaller Docs: https://pyinstaller.org/
- Inno Setup: https://jrsoftware.org/isinfo.php
- create-dmg: https://github.com/create-dmg/create-dmg

---

## 🔄 Automated Builds (CI/CD)

### GitHub Actions Example

```yaml
name: Build Ecoute

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt pyinstaller
      - run: build_windows.bat
      - uses: actions/upload-artifact@v3
        with:
          name: Ecoute-Windows
          path: dist/Ecoute/

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt pyinstaller
      - run: ./build_macos.sh
      - uses: actions/upload-artifact@v3
        with:
          name: Ecoute-macOS
          path: dist/Ecoute.app

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt pyinstaller
      - run: ./build_linux.sh
      - uses: actions/upload-artifact@v3
        with:
          name: Ecoute-Linux
          path: dist/Ecoute/
```

---

Built with ❤️ for easy distribution across all platforms!
