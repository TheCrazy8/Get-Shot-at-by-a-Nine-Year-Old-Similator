# Get Shot at by a Nine Year Old Similator

yeah thats it :3

[GitHub Pages version](https://thecrazy8.github.io/Get-Shot-at-by-a-Nine-Year-Old-Similator/) (not recommended for stability)

## WARNING

THE GITHUB PAGES VERSION IS NOT ADVISED, AS IT MAY CRASH YOUR DEVICE/BROWSER ON GAME OVER. USE THE ITCH.IO VERSION (IF NO WINDOWS SYSTEM) OR WINDOWS VERSION; WINDOWS BUILD IS PRIMARY.

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

## 2025 Refactor Summary

Core script was re-architected for performance and maintainability:

- Unified Bullet System: Data-driven `BulletSpec` + generic movers (spiral, homing, wave, boomerang, split, exploding, bouncing, star, etc.) replacing dozens of bespoke loops.
- Delta-Time Engine: Movement & spawn rates scaled by real elapsed time (via `perf_counter`) instead of frame assumptions.
- Optimized Collision & Graze: Cached player hitbox/center each frame; graze uses squared distance; collision adds early rejection.
- Scoring Centralization: `award_score()` normalizes HUD updates; all manual `score +=` replaced.
- Elapsed Time HUD: Displays survival seconds (pause-aware) instead of static start timestamp.
- Debug Metrics: Frame counter & bullet peak (`enable_debug(True)` to log every 300 frames).
- Restart Consistency: Resets unified containers, HUD, lore safely.

### Optional / Future Enhancements

- Integrate lasers into the same bullet registry.
- Externalize pattern config (JSON/dict) for balance tuning.
- Difficulty scaling hook based on elapsed time & bullet density.
- Automated headless tests (mocked Canvas) for movers.

### Quick Start (Desktop Python)

```bash
pip install pygame
python "Rift of Memories and Regrets.py"
```

### Debug Mode

Inside the script after creating the game instance:

```python
game.enable_debug(True)
```

Shows periodic metrics: frame count, active bullets, peak, score.

---
This refactor improves determinism, extensibility, and performance under high bullet counts.
