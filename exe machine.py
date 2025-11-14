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
		f"uneasy type beat.wav{sep}.",
	]
	# Note: Python source modules (config.py, resources.py) are bundled automatically.
	# Explicit --add-data ensures non-Python assets are accessible to resource_path().
	PyInstaller.__main__.run([
		'Rift of Memories and Regrets.py',
		*[f'--add-data={d}' for d in data_args],
		'--onefile',
		'--windowed',
		'--icon=icon3.ico',
		'--name=RiftOfMemories'
	])

if __name__ == '__main__':
	build()

