# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['auto_clicker_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['selenium', 'webdriver_manager', 'selenium.webdriver.chrome.service', 'selenium.webdriver.common.by'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FlightSafety-AutoClicker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
