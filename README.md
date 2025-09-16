# Get Shot at by a Nine Year Old Similator
yeah thats it :3

https://thecrazy8.github.io/Get-Shot-at-by-a-Nine-Year-Old-Similator/ (github pages version)

# WARNING: THE GITHUB PAGES VERSION IS NOT ADVISED, AS IT MAY CRASH YOUR DEVICE/BROWSER ON GAME OVER.  USE THE ITCH.IO VERSION (IF NO WINDOWS SYSTEM) OR WINDOWS VERSION, AS WINDOWS VERSION IS THE MAIN VERSION

## Controller Support (Steam Input / Switch Pro Controller)

Native gamepad support has been added via `pygame.joystick`.

How to use a Nintendo Switch Pro Controller:
- Add the game (EXE or a simple batch that launches the Python script) to Steam as a Non-Steam Game.
- In Steam Big Picture / Settings > Controller, enable Steam Input for the Pro Controller.
- Launch the game through Steam so Steam Input exposes the pad as an XInput device.
- Left stick / D-Pad moves the player. (Right now: movement only.)

Tweaks:
- Default movement speed: 15 pixels per frame (adjust `self.player_speed`).
- Deadzone set to 0.25 (edit `deadzone` in `poll_gamepad`).

Notes:
- If “No gamepad detected.” appears in console, ensure Steam is running and controller is recognized.
- Disconnect/reconnect: the game only grabs the first joystick at start; restart game to re-detect.
