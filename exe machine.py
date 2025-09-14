import PyInstaller.__main__
import os
import sys
from pathlib import Path

# Get the path to the user's home directory
home_directory = Path.home()

# Construct the path to the Downloads directory
downloads_directory = home_directory / "Downloads"

# Change the current working directory to the Downloads directory
os.chdir(downloads_directory)

print(f"Successfully navigated to: {os.getcwd()}")

def build():
	# PyInstaller uses different separator in --add-data (Windows=';', others=':')
	sep = ';' if os.name == 'nt' else ':'
	data_args = [
		f"music.mp3{sep}.",
		f"lore.txt{sep}."
	]
	PyInstaller.__main__.run([
		'Rift of Memories and Regrets.py',
		*[f'--add-data={d}' for d in data_args],
		'--onefile',
		'--windowed',
		'--icon=icon3.ico'
	])

if __name__ == '__main__':
	build()