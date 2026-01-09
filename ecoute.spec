# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Ecoute AI Research Assistant

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('custom_speech_recognition', 'custom_speech_recognition'),
        ('tiny.en.pt', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'pyaudiowpatch',
        'openai',
        'numpy',
        'faster_whisper',
        'ctranslate2',
        'torch',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Ecoute',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to False for no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Ecoute',
)

# For macOS app bundle
app = BUNDLE(
    coll,
    name='Ecoute.app',
    icon='assets/icon.icns' if os.path.exists('assets/icon.icns') else None,
    bundle_identifier='com.ecoute.airesearchassistant',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'CFBundleName': 'Ecoute AI Research Assistant',
        'CFBundleDisplayName': 'Ecoute',
        'CFBundleGetInfoString': "AI-powered research and transcription assistant",
        'CFBundleIdentifier': 'com.ecoute.airesearchassistant',
        'CFBundleVersion': '2.0.0',
        'CFBundleShortVersionString': '2.0.0',
        'NSMicrophoneUsageDescription': 'Ecoute needs access to your microphone for live transcription.',
    },
)
