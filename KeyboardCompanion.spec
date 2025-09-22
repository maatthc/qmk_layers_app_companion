# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2

a = Analysis(
    ['main.py'],
    hiddenimports=["zeroconf._utils.ipaddress","zeroconf._handlers.answers",'pkg_resources.extern'],
    pathex=[],
    binaries=[('hidapi.dll','.')],
    datas=[],
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
	*[Tree(p) for p in (sdl2.dep_bins)],
    [],
    name='Keyboard Companion',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	icon='./assets/icon.ico'
)
