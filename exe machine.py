import PyInstaller.__main__
import os
from pathlib import Path

# Get the path to the user's home directory
home_directory = Path.home()

# Construct the path to the Downloads directory
downloads_directory = home_directory / "Downloads"

# Change the current working directory to the Downloads directory
os.chdir(downloads_directory)

print(f"Successfully navigated to: {os.getcwd()}")

# Run the script to make Python file into an EXE file
PyInstaller.__main__.run([
'Rift of Memories and Regrets.py',
'--add-data=music.mp3:.',
'--onefile',
'--windowed',
'--icon=icon3.ico'
])