"""Windows: child processes (ffmpeg, node, python) start without a console window of their own.
Alex 2026-10-14: a black window flashed on screen for every render step. Import once at the top of an entry script."""
import subprocess, sys
if sys.platform == 'win32' and not getattr(subprocess.Popen, '_nowin', False):
    _init = subprocess.Popen.__init__
    def __init__(self, *a, **k):
        k['creationflags'] = k.get('creationflags', 0) | subprocess.CREATE_NO_WINDOW
        _init(self, *a, **k)
    subprocess.Popen.__init__ = __init__
    subprocess.Popen._nowin = True
