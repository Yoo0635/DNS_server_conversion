# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['../main.py'],
    pathex=['..'],
    binaries=[],
    datas=[
        ('../dashboard.py', '.'),
        ('../traffic_graphs.py', '.'),
        ('../dns_status.py', '.'),
        ('../ticketing.py', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'dashboard',
        'traffic_graphs',
        'dns_status',
        'ticketing',
        'matplotlib.backends.backend_qt5agg',
        'PyQt5.QtCore',
        'PyQt5.QtWidgets',
        'PyQt5.QtGui',
        'matplotlib.figure',
        'matplotlib.backends.backend_qt5agg',
        'numpy',
        'random',
    ],
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
    [],
    exclude_binaries=True,
    name='NetworkOptimizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='NetworkOptimizer',
)
app = BUNDLE(
    coll,
    name='NetworkOptimizer.app',
    icon=None,
    bundle_identifier='com.networkoptimizer.app',
    codesign_identity=None,
    entitlements_file=None,
)