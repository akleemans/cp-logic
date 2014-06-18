# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['/home/adrianus/github/cp-logic'],
	     hiddenimports=['PySide.QtCore','PySide.QtGui'],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
	  Tree('data', prefix='data'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          strip=None,
          upx=True,
          console=True )
