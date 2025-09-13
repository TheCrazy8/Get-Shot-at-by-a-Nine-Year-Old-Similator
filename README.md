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

## Lore: The Rift Between Time and Space

The arena is a liminal neon graveyard where discarded timelines collapse into a scrolling vaporwave grid. Moments don’t pass— they **stack** like cassette layers. Glitches, VHS sunsets, and archived gods form the backdrop while you dodge projectiles that are really shards of overwritten memory.

### J, the Immortal (Corrupted) Child

J is a nine‑year‑old who survived the deletion of a timeline that never “properly happened.” They’re not divine— just an undecodable record the Rift refuses to purge. They treat the encounter like a game of tag, believing “beating” you might finally let them grow up… or that’s the story they loop for themselves.

### What Bullets Really Are

Each pattern = a memory fragment type:

- Vertical / Horizontal: Basic structural tape strips.
- ZigZag / Triangle / Quad: Refracted childhood events that never stabilized.
- Star / Spiral / Radial: Celebration echoes (birthdays / summers) diffusing outward.
- Exploding / Split: Compressed years rupturing into micro-moments.
- Bouncing: Rejected possible decisions rebounding until entropy wins.
- Laser: Deletion cursors that fail to lock onto J’s corrupted slot.
- Homing: The Rift trying to categorize you— poorly.
- Boomerang: Exit attempts curve back: boundary enforcement.

Taking a hit isn’t “damage”— it’s partial overwrite. Lose enough integrity and you’d join the static silhouettes at the grid’s edges.

### Dynamic Lore Fragments

As new bullet types unlock, short lore strings flicker under the main dialog. They fade after a few seconds. Each unlock only triggers once per run.

### Hidden Atmospherics

Graffiti along the edges (e.g., “THE CHILD IS OLDER THAN THE GRID”) hints at systemic failure. Future versions may add whisper audio and rarer deep fragments if you survive extreme durations.

### Tone Modes

You can set an environment variable before launching to bias flavor text:

Windows (PowerShell):

```pwsh
$env:LORE_TONE = 'horror'; python "Get Shot at by a Nine Year Old Simulator.py"
```

Options: `horror`, `surreal`, or `blended` (default). This only affects suffix flavor tags like `(audio smear)` vs `(liminal hush)`.

### Endgame Possibility (Concept)

If you endure long enough, you may discover you and J are both anomalies— and something else in the Rift wants neither of you escaping. (Not fully implemented yet: planned.)

### Contribute More Lore

Open an issue or PR with:

- Fragment key (which pattern/time)
- One-line flavor (max ~90 chars)
- Optional tone variants (horror/surreal)

Keep it cryptic, evocative, and diegetic— no direct exposition dumps.
