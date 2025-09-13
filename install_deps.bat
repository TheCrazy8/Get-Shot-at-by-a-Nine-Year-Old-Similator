@echo off
REM Install required Python libraries for the game
REM Only external dependency currently used is pygame (tkinter is built-in)

ECHO Detecting Python executable...
set PY_CMD=
for %%P in (py python python3) do (
  where %%P >nul 2>nul && (set PY_CMD=%%P & goto :foundpy)
)

echo Python not found in PATH. Install Python 3 from https://www.python.org/downloads/
pause
exit /b 1

:foundpy
echo Using %PY_CMD%

REM Ensure pip is available and updated
%PY_CMD% -m ensurepip --upgrade >nul 2>nul
%PY_CMD% -m pip install --upgrade pip

ECHO Installing dependencies...
%PY_CMD% -m pip install pygame

ECHO.
ECHO All done! You can now run the game.
pause
