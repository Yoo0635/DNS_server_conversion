# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# 프로젝트 루트 디렉토리
project_root = Path(os.getcwd())

# 데이터 파일들
datas = [
    (str(project_root / 'backend'), 'backend'),
    (str(project_root / 'frontend'), 'frontend'),
    (str(project_root / 'requirements.txt'), '.'),
    (str(project_root / 'README.md'), '.'),
]

# 숨겨진 imports
hiddenimports = [
    'fastapi',
    'uvicorn',
    'dnspython',
    'pandas',
    'numpy',
    'requests',
    'matplotlib',
    'PyQt5',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'pydantic',
    'starlette',
    'python-dateutil',
    'certifi',
    'charset-normalizer',
    'idna',
    'urllib3',
    'typing_extensions',
    'annotated-types',
    'anyio',
    'h11',
    'sniffio',
    'click',
    'colorama',
    'six',
    'pytz',
    'tzdata',
    'matplotlib.backends.backend_qt5agg',
    'matplotlib.figure',
    'matplotlib.pyplot',
    'matplotlib.animation',
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
]

# 바이너리 파일들
binaries = []

# 분석
a = Analysis(
    ['run_app.py'],
    pathex=[str(project_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# PYZ
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# EXE
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NetworkOptimizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onefile=False,  # onedir 모드로 변경하여 안정성 향상
)

# macOS용 .app 번들 (macOS에서만)
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='NetworkOptimizer.app',
        icon=None,
        bundle_identifier='com.networkoptimizer.app',
        info_plist={
            'CFBundleName': 'Network Optimizer',
            'CFBundleDisplayName': 'Network Optimizer',
            'CFBundleVersion': '2.0.1',
            'CFBundleShortVersionString': '2.0.1',
            'CFBundleIdentifier': 'com.networkoptimizer.app',
            'CFBundleExecutable': 'NetworkOptimizer',
            'CFBundleIconFile': 'AppIcon',
            'LSMinimumSystemVersion': '10.13.0',
            'NSHighResolutionCapable': True,
            'NSRequiresAquaSystemAppearance': False,
        },
    )