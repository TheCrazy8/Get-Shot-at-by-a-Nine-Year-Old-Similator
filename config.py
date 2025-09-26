"""Central configuration constants for Rift of Memories and Regrets.
Extracted to reduce magic numbers in the main game class and prepare for
future balancing / dynamic difficulty adjustments.
"""

# Player related tuning
PLAYER_SPEED = 15
GRAZING_RADIUS = 40
FOCUS_PULSE_RADIUS = 140
FOCUS_CHARGE_RATE = 0.004          # per frame while focusing
FOCUS_PULSE_COOLDOWN = 2.0         # seconds

# Bullet related
HOMING_BULLET_MAX_LIFE = 180       # frames (~9s at 50ms)

# Visual / effect tuning
FREEZE_TINT_FADE_SPEED = 0.08

# Progressive pattern unlock times (seconds survived)
UNLOCK_TIMES = {
    'vertical': 0,
    'horizontal': 8,
    'diag': 15,
    'triangle': 25,
    'quad': 35,
    'zigzag': 45,
    'fast': 55,
    'rect': 65,
    'star': 75,
    'egg': 85,
    'boss': 95,
    'bouncing': 110,
    'exploding': 125,
    'laser': 140,
    'homing': 155,
    'spiral': 175,
    'radial': 195,
    'wave': 210,
    'boomerang': 225,
    'split': 240,
}

# (Future) default spawn chances (1 in N per frame) kept here for pattern registry refactor
SPAWN_CHANCES = {
    'vertical': 18,
    'horizontal': 22,
    'diag': 28,
    'boss': 140,
    'zigzag': 40,
    'fast': 30,
    'star': 55,
    'rect': 48,
    'laser': 160,
    'triangle': 46,
    'quad': 52,
    'egg': 50,
    'bouncing': 70,
    'exploding': 90,
    'homing': 110,
    'spiral': 130,
    'radial': 150,
    'wave': 160,
    'boomerang': 170,
    'split': 180,
}
