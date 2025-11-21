import PyInstaller.__main__
import os
import sys
from pathlib import Path

# Change working directory to project root (folder containing this script)
PROJECT_ROOT = Path(__file__).resolve().parent
os.chdir(PROJECT_ROOT)
print(f"Building from project root: {PROJECT_ROOT}")

def build():
	# PyInstaller uses different separator in --add-data (Windows=';', others=':')
	sep = ';' if os.name == 'nt' else ':'
	data_args = [
		f"music.mp3{sep}.",
		f"game_0v3r.mp3{sep}.",
		f"game_0v3r_g0n333333333333.mp3{sep}.",
		f"lore.txt{sep}.",
		f"icon3.ico{sep}.",
		f"icon3.png{sep}.",
		f"uneasy type beat.wav{sep}.",
		f"e.mp3{sep}.",
		f"[UN]Canny.mp3{sep}.",
		f"PauseLoop.mp3{sep}.",
	]
	# Note: Python source modules (config.py, resources.py) are bundled automatically.
	# Explicit --add-data ensures non-Python assets are accessible to resource_path().
	
	# Build PyInstaller args
	pyinstaller_args = [
		'Rift of Memories and Regrets.py',
		*[f'--add-data={d}' for d in data_args],
		'--onefile',
		'--windowed',
		'--icon=icon3.ico',
		'--name=RiftOfMemories'
	]
	
	# Add splash screen only on non-macOS platforms (incompatibility on macOS)
	if sys.platform != 'darwin':
		pyinstaller_args.append('--splash=icon3.png')
	
	PyInstaller.__main__.run(pyinstaller_args)

if __name__ == '__main__':
	build()

