"""\nLore Integration: The Rift Between Time and Space\n=================================================\n\n(Non-intrusive lore block added; no existing code removed.)\n\n🌌 The Rift Between Time and Space\n---------------------------------\nNature of the Rift: A neon-etched liminal zone where discarded timelines and forgotten realities collapse. Moments do not pass — they stack like cassette layers. VHS sunsets loop forever; broken statues drift; obsolete gods hum as static.\nLaw of the Rift: Time is an overlapping tape. Past and future flicker interchangeably. Entities here are memory-knots: nostalgia, error, and refusal to be deleted.\n\n👻 J, the Immortal Child\n------------------------\nOrigin: J was a real child from a timeline that never fully happened. That reality was erased, but their record was too corrupted to purge. The Rift keeps the file open — so J cannot age or end. Immortality by bureaucratic failure.\nPersonality: Sing‑song, glitchy, playful, unsettling. Speech loops like a scratched CD; phrases repeat with tiny mutations. They think it’s a game. Or pretend it is.\nWhy They Hunt You: You are an unindexed anomaly. J believes “beating” you lets them grow up or exit. Whether that’s true, delusion, or implanted is unknown.\n\n🌀 The Conflict (Memory Fragments)\n---------------------------------\nEach phase = a memory shard: malls that never opened, concerts that never ended, summers the universe revoked. Bullets = memory/data fragments. A hit doesn’t wound — it overwrites. Too many overwrites and you desync, dissolving into echo static.\n\n🧩 Hidden Lore Signals\n----------------------\nGraffiti: “THE CHILD IS OLDER THAN THE GRID.”\nAudio Ghosting: Faint parental calls phase through reverb.\nStatic Witnesses: Frozen silhouettes at erasure-moments.\nEndgame Seed: Maybe J isn’t the jailer — maybe both of you are being audited by a deeper Warden Process.\n\n(Do NOT edit indentation or remove code per user instruction.)\n"""
import tkinter as tk
import random
import time
import pygame
import sys
import os
import math
try:
    # Optional Steam Input (Steamworks) support
    from steamworks import STEAMWORKS
    _STEAMWORKS_AVAILABLE = True
except Exception:
    _STEAMWORKS_AVAILABLE = False

class bullet_hell_game:
    def __init__(self, root, bg_color_interval=6):
        # Initialize pygame mixer and play music
        pygame.mixer.init()
        try:
            if hasattr(sys, '_MEIPASS'):
                music_path = os.path.join(sys._MEIPASS, "music.mp3")
            else:
                music_path = "music.mp3"
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # Loop indefinitely
        except Exception as e:
            print("Could not play music:", e)
        self.root = root
        self.root.title("Get Shot at by a Nine Year Old Simulator")
        self.root.state('zoomed')  # Maximize window (Windows only)
        self.root.update_idletasks()
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # Store customizable background color change interval (seconds)
        self.bg_color_interval = bg_color_interval
    # Initialize animated vaporwave grid background
        self.init_background()
        # Create player (base hitbox rectangle + decorative layers)
        self.player = None
        self.player_deco_items = []  # decorative shape IDs (not used for collisions)
        self.player_glow_phase = 0.0
        self.player_rgb_phase = 0.0  # for rainbow fill
        self.create_player_sprite()
        self.bullets = []
        self.bullets2 = []
        self.triangle_bullets = []  # [(bullet_id, direction)]
        self.diag_bullets = []
        self.boss_bullets = []
        self.zigzag_bullets = []
        self.fast_bullets = []
        self.star_bullets = []
        self.rect_bullets = []
        self.fast_bullets = []
        self.egg_bullets = []
        self.exploding_bullets = []
        self.exploded_fragments = []  # [(bullet_id, dx, dy)]
        self.bouncing_bullets = []
        self.laser_indicators = []  # [(indicator_id, y, timer)]
        self.lasers = []  # [(laser_id, y, timer)]
        # New bullet type state containers
        self.homing_bullets = []      # [(bullet_id, vx, vy)] homing towards player
        self.spiral_bullets = []      # [(bullet_id, angle, radius, ang_speed, rad_speed,   cx, cy)]
        self.radial_bullets = []      # [(bullet_id, vx, vy)] spawned in bursts
        # Additional new bullet type containers
        self.wave_bullets = []        # [(bullet_id, base_x, phase, amp, vy, phase_speed)]
        self.boomerang_bullets = []   # [(bullet_id, vy, timer, state)] state: 'down'->'up'
        self.split_bullets = []       # [(bullet_id, timer)] splits into fragments after timer
        self.score = 0
        self.timee = int(time.time())
        self.dial = "Welcome to Get Shot at by a Nine Year Old Simulator!"
        self.scorecount = self.canvas.create_text(70, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 16))
        self.timecount = self.canvas.create_text(self.width-70, 20, text=f"Time: {self.timee}", fill="white", font=("Arial", 16))
        self.dialog = self.canvas.create_text(self.width//2, 20, text=self.dial, fill="white", font=("Arial", 20), justify="center")
        # Text showing next pattern unlock info
        self.pattern_display_names = {
            'vertical': 'Vertical',
            'horizontal': 'Horizontal',
            'diag': 'Diagonal',
            'triangle': 'Triangle',
            'quad': 'Quad Cluster',
            'zigzag': 'ZigZag',
            'fast': 'Fast',
            'rect': 'Wide Rectangle',
            'star': 'Star',
            'egg': 'Tall Egg',
            'boss': 'Big Boss',
            'bouncing': 'Bouncing',
            'exploding': 'Exploding',
            'laser': 'Laser',
            'homing': 'Homing',
            'spiral': 'Spiral',
            'radial': 'Radial Burst',
            'wave': 'Wave',
            'boomerang': 'Boomerang',
            'split': 'Splitter'
        }
        # Moved next pattern display to bottom center
        self.next_unlock_text = self.canvas.create_text(self.width//2, self.height-8, text="", fill="#88ddff", font=("Arial", 16), anchor='s')
        self.lives = 1
        self.game_over = False
        self.paused = False
        self.pause_text = None
        self.difficulty = 1
        self.last_difficulty_increase = time.time()
        self.lastdial = time.time()
        self.root.bind("<KeyPress>", self.move_player)
        self.root.bind("<Escape>", self.toggle_pause)
        self.root.bind("r", self.restart_game)
        self.root.bind("p", self.toggle_practice_mode)
        self.grazing_radius = 40
        self.grazed_bullets = set()
        self.graze_effect_id = None
        self.paused_time_total = 0  # Total time spent paused
        self.pause_start_time = None  # When pause started
        # Practice mode (invincible)
        self.practice_mode = False
        self.practice_text = None
        # Player movement speed (keys & gamepad)
        self.player_speed = 15
        # Joystick handle (Steam Input / Switch Pro)
        self.joystick = None
        self.init_gamepad()
        # Steam Input attributes
        self.steam = None
        self.steam_controllers = []
        self.steam_action_move = None
        self.use_steam_input = False
        self.init_steam_input()
        # Progressive unlock times (seconds survived) for bullet categories
        # 0: basic vertical (already active), later adds more complexity.
        self.unlock_times = {
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
            'split': 240
        }
        # Initialize lore fragments (non-destructive)
        try:
            self.init_lore()
            # Persistent lore display
            self.lore_interval = 8
            self.lore_last_change = time.time()
            self.current_lore_line = None
            self.lore_text = self.canvas.create_text(self.width//2, 50, text="", fill="#b0a8ff", font=("Courier New", 14), justify="center")
            self.update_lore_line(force=True)
        except Exception:
            pass
        self.update_game()

    # -------------- Gamepad / Steam Input Support --------------
    def init_steam_input(self):
        """Initialize Steam Input if steamworks is available and Steam is running.
        Expects an action manifest alongside the executable if custom actions desired.
        We just fetch the first connected controller and a generic move action if present."""
        if not _STEAMWORKS_AVAILABLE:
            return
        try:
            self.steam = STEAMWORKS()
            self.steam.initialize()
            # Load action manifest if you have one (placeholder path):
            # self.steam.Input.Init() is implicit; steamworksPy auto-inits input
            self.steam.Input.Init()
            self.steam_controllers = self.steam.Input.GetConnectedControllers()
            if self.steam_controllers:
                # Attempt to get a Move analog action handle (replace with your actual action name)
                try:
                    self.steam_action_move = self.steam.Input.GetAnalogActionHandle("Move")
                except Exception:
                    self.steam_action_move = None
                self.use_steam_input = True
                print(f"[SteamInput] Controllers: {self.steam_controllers}")
            else:
                print("[SteamInput] No controllers via Steam Input.")
        except Exception as e:
            print("[SteamInput] Init failed:", e)
            self.use_steam_input = False

    def poll_steam_input(self):
        if not self.use_steam_input or not self.steam_controllers or self.paused or self.game_over:
            return False
        moved = False
        try:
            self.steam.Input.RunFrame()
            ctrl = self.steam_controllers[0]
            if self.steam_action_move:
                analog = self.steam.Input.GetAnalogActionData(ctrl, self.steam_action_move)
                if analog and analog.get('bActive'):
                    x = analog.get('x', 0.0)
                    y = analog.get('y', 0.0)
                    deadzone = 0.25
                    if abs(x) > deadzone or abs(y) > deadzone:
                        mag = (x*x + y*y)**0.5
                        if mag > 1e-3:
                            x /= mag
                            y /= mag
                        self.apply_player_move(x * self.player_speed, -y * self.player_speed)  # Steam Y up -> invert
                        moved = True
        except Exception as e:
            print("[SteamInput] Poll error:", e)
            return False
        return moved
    def init_gamepad(self):
        """Initialize joystick via pygame. Steam Input maps Switch Pro to XInput; ensure Steam Input is enabled for the game (add as non-Steam game)."""
        try:
            pygame.joystick.init()
            if pygame.joystick.get_count() > 0:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                print(f"Gamepad detected: {self.joystick.get_name()}")
            else:
                print("No gamepad detected.")
        except Exception as e:
            print("Joystick init failed:", e)

    def poll_gamepad(self):
        if not self.joystick or self.paused or self.game_over:
            return
        try:
            pygame.event.pump()
        except Exception:
            return
        deadzone = 0.25
        dx = 0
        dy = 0
        # Axes 0 (left/right), 1 (up/down) on most controllers
        try:
            ax0 = self.joystick.get_axis(0)
            ax1 = self.joystick.get_axis(1)
            if abs(ax0) > deadzone:
                dx = ax0
            if abs(ax1) > deadzone:
                dy = ax1
        except Exception:
            pass
        # Hat fallback
        if dx == 0 and dy == 0:
            try:
                if self.joystick.get_numhats() > 0:
                    hx, hy = self.joystick.get_hat(0)
                    dx = hx
                    dy = hy
            except Exception:
                pass
        if dx or dy:
            # Normalize diagonal
            mag = (dx*dx + dy*dy) ** 0.5
            if mag > 1e-3:
                dx /= mag
                dy /= mag
            self.apply_player_move(dx * self.player_speed, dy * self.player_speed)

    def apply_player_move(self, dx, dy):
        if self.paused or self.game_over:
            return
        if dx == 0 and dy == 0:
            return
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        width = x2 - x1
        height = y2 - y1
        nx1 = max(0, min(self.width - width, x1 + dx))
        ny1 = max(0, min(self.height - height, y1 + dy))
        self.canvas.coords(self.player, nx1, ny1, nx1 + width, ny1 + height)
        # Also move decorative layers to align with base
        self.update_player_sprite_position()

    # ---------------- Player fancy sprite ----------------
    def create_player_sprite(self):
        """Create the player base hitbox rectangle plus decorative shapes (diamond + glow)."""
        if self.player is not None:
            # Remove existing
            for item in self.player_deco_items:
                self.canvas.delete(item)
            self.canvas.delete(self.player)
        base_w = 20
        base_h = 20
        cx = self.width//2
        cy = self.height - 40
        self.player = self.canvas.create_rectangle(cx-base_w//2, cy-base_h//2, cx+base_w//2, cy+base_h//2, fill="white", outline="")
        # Diamond (rotated square) around player
        dsz = 30
        diamond_points = [
            cx, cy-dsz/2,
            cx+dsz/2, cy,
            cx, cy+dsz/2,
            cx-dsz/2, cy
        ]
        diamond = self.canvas.create_polygon(diamond_points, outline="#66ccff", fill="", width=2)
        # Inner square accent
        isz = 10
        inner = self.canvas.create_rectangle(cx-isz/2, cy-isz/2, cx+isz/2, cy+isz/2, outline="#ff66ff", width=2)
        # Glow ring (oval) slightly larger, animated alpha simulated by color cycling
        glow_r = 34
        glow = self.canvas.create_oval(cx-glow_r/2, cy-glow_r/2, cx+glow_r/2, cy+glow_r/2, outline="#ffffff", width=2)
        self.player_deco_items = [diamond, inner, glow]
        # Ensure base is above background but below bullets initially
        for item in self.player_deco_items:
            self.canvas.tag_lower(item, self.player)

    def update_player_sprite_position(self):
        if not self.player_deco_items or self.player is None:
            return
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        # Update diamond
        diamond, inner, glow = self.player_deco_items
        # Recompute diamond points keeping size
        dsz = 30
        self.canvas.coords(diamond,
            cx, cy-dsz/2,
            cx+dsz/2, cy,
            cx, cy+dsz/2,
            cx-dsz/2, cy)
        isz = 10
        self.canvas.coords(inner, cx-isz/2, cy-isz/2, cx+isz/2, cy+isz/2)
        glow_r = 34
        self.canvas.coords(glow, cx-glow_r/2, cy-glow_r/2, cx+glow_r/2, cy+glow_r/2)

    def animate_player_sprite(self):
        if not self.player_deco_items:
            return
        self.player_glow_phase += 0.15
        self.player_rgb_phase += 0.02
        diamond, inner, glow = self.player_deco_items
        # Pulsing glow color
        pulse = (math.sin(self.player_glow_phase) + 1)/2  # 0..1
        # Interpolate between two colors for diamond and inner
        def lerp_color(c1, c2, t):
            return tuple(int(c1[i] + (c2[i]-c1[i])*t) for i in range(3))
        d_col = lerp_color((80,180,255), (255,120,255), pulse)
        i_col = lerp_color((255,120,255), (255,255,255), 1-pulse)
        g_col = lerp_color((255,255,255), (120,200,255), pulse)
        self.canvas.itemconfig(diamond, outline=f"#{d_col[0]:02x}{d_col[1]:02x}{d_col[2]:02x}")
        self.canvas.itemconfig(inner, outline=f"#{i_col[0]:02x}{i_col[1]:02x}{i_col[2]:02x}")
        self.canvas.itemconfig(glow, outline=f"#{g_col[0]:02x}{g_col[1]:02x}{g_col[2]:02x}")
        # Slight rotation illusion: scale diamond size subtly
        scale_factor = 1 + 0.05*math.sin(self.player_glow_phase*0.7)
        x1, y1, x2, y2 = self.canvas.coords(self.player)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        dsz_base = 30
        dsz = dsz_base * scale_factor
        self.canvas.coords(diamond,
            cx, cy-dsz/2,
            cx+dsz/2, cy,
            cx, cy+dsz/2,
            cx-dsz/2, cy)
        # Rainbow fill for base rectangle using HSV -> RGB approximation
        # Simple 0..1 hue wrap
        h = self.player_rgb_phase % 1.0
        # Convert hue to RGB (s=1,v=1) manually
        i = int(h*6)
        f = h*6 - i
        q = 1 - f
        if i % 6 == 0:
            r,g,b = 1, f, 0
        elif i % 6 == 1:
            r,g,b = q, 1, 0
        elif i % 6 == 2:
            r,g,b = 0, 1, f
        elif i % 6 == 3:
            r,g,b = 0, q, 1
        elif i % 6 == 4:
            r,g,b = f, 0, 1
        else:
            r,g,b = 1, 0, q
        self.canvas.itemconfig(self.player, fill=f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")


    # ---------------- Vaporwave background setup ----------------
    def init_background(self):
        # Parameters
        self.bg_color_cycle = ["#0d0221", "#1a0533", "#32054e", "#4b0a67", "#6d117b", "#8f1f85", "#b1387f", "#d25872"]
        self.bg_cycle_index = 0
        self.bg_last_color_change = time.time()
    # self.bg_color_interval is set in __init__ (customizable)
        self.grid_h_lines = []
        self.grid_v_lines = []
        self.grid_depth = 40  # number of perspective rows
        self.grid_scroll_speed = 0.6
        self.grid_vertical_count = 18
        self.grid_perspective_power = 1.55
        # Extend grid to near bottom of window for full coverage
        self.grid_base_y = self.height - 10
        self.grid_horizon_y = self.height * 0.15
        self.grid_glow_cycle = 0.0
        # Clear any prior lines (if restarting) - canvas itself is cleared by caller on restart
        self._create_grid_lines()

    def toggle_practice_mode(self, event=None):
        was = self.practice_mode
        self.practice_mode = not self.practice_mode
        if self.practice_mode:
            label = "Practice: ON"
            color = "#33ff77"
            if self.practice_text is None:
                self.practice_text = self.canvas.create_text(self.width-120, 80, text=label, fill=color, font=("Arial", 14))
            else:
                self.canvas.itemconfig(self.practice_text, text=label, fill=color)
            self.canvas.lift(self.practice_text)
        else:
            if self.practice_text is not None:
                self.canvas.delete(self.practice_text)
                self.practice_text = None
            # Restart game immediately in normal mode
            self.restart_game(force=True)

    def _create_grid_lines(self):
        # Create horizontal perspective lines (closer lines farther apart toward bottom)
        self.grid_h_lines.clear()
        for i in range(self.grid_depth):
            t = i / (self.grid_depth - 1)
            # Interpolate between horizon and base with power for perspective
            y = self.grid_horizon_y + (self.grid_base_y - self.grid_horizon_y) * (t ** self.grid_perspective_power)
            line = self.canvas.create_line(0, y, self.width, y, fill="#222", width=1)
            self.grid_h_lines.append((line, t))
        # Create vertical lines using perspective convergence
        self.grid_v_lines.clear()
        for j in range(self.grid_vertical_count):
            x_norm = j / (self.grid_vertical_count - 1)
            x_screen = x_norm * self.width
            line = self.canvas.create_line(x_screen, self.grid_base_y, self.width/2, self.grid_horizon_y, fill="#222", width=1)
            self.grid_v_lines.append((line, x_norm))

    def update_background(self):
        now = time.time()
        # Color cycle
        if now - self.bg_last_color_change > self.bg_color_interval:
            self.bg_cycle_index = (self.bg_cycle_index + 1) % len(self.bg_color_cycle)
            self.bg_last_color_change = now
        # Interpolate background color to next
        next_index = (self.bg_cycle_index + 1) % len(self.bg_color_cycle)
        phase = (now - self.bg_last_color_change) / self.bg_color_interval
        phase = max(0.0, min(1.0, phase))
        c1 = self.bg_color_cycle[self.bg_cycle_index]
        c2 = self.bg_color_cycle[next_index]
        def _interp_color(a, b, t):
            av = int(a[1:3],16), int(a[3:5],16), int(a[5:7],16)
            bv = int(b[1:3],16), int(b[3:5],16), int(b[5:7],16)
            cv = tuple(int(av[i] + (bv[i]-av[i])*t) for i in range(3))
            return f"#{cv[0]:02x}{cv[1]:02x}{cv[2]:02x}"
        bg_col = _interp_color(c1, c2, phase)
        self.canvas.configure(bg=bg_col)
        # Compute contrasting base colors for grid lines based on background luminance.
        br = int(bg_col[1:3],16)
        bg_g = int(bg_col[3:5],16)
        bb = int(bg_col[5:7],16)
        # Relative luminance (simple perceptual approximation)
        lum = 0.299*br + 0.587*bg_g + 0.114*bb
        # Choose two endpoint colors for gradients: one bright, one dark, ensuring contrast.
        if lum < 90:  # background very dark -> use bright neon set
            grad_a = (255, 230, 140)  # warm bright
            grad_b = (140, 255, 255)  # cool bright
        elif lum < 160:  # medium dark -> mid-high contrast
            grad_a = (255, 170, 255)
            grad_b = (120, 220, 255)
        else:  # light background (rare with palette) -> darker saturated lines
            grad_a = (180, 40, 200)
            grad_b = (40, 160, 255)
        def _mix(a, b, t):
            return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))
        # Glow/pulse factor for line brightness
        self.grid_glow_cycle += 0.05
        glow = (math.sin(self.grid_glow_cycle) + 1)/2  # 0..1
        # Update horizontal lines to scroll downward; wrap to top with new perspective
        new_h_lines = []
        for line_id, t in self.grid_h_lines:
            # Move line by scroll speed scaled by its depth (closer lines move faster)
            depth_factor = (t ** self.grid_perspective_power)
            dy = self.grid_scroll_speed * (0.3 + depth_factor*2)
            x1, y1, x2, y2 = self.canvas.coords(line_id)
            y1 += dy
            y2 += dy
            # If line passes base, wrap to horizon
            if y1 > self.grid_base_y + 4:
                # Reinsert near horizon
                y1 = self.grid_horizon_y + 2
                y2 = y1
            self.canvas.coords(line_id, 0, y1, self.width, y2)
            # Depth-based gradient position (closer lines get warmer/cooler shift)
            base_rgb = _mix(grad_a, grad_b, t)
            # Apply glow and depth fade (lines nearer bottom get stronger glow scaling)
            brightness = 0.35 + 0.65*glow*(1 - t*0.7)
            r = min(255, int(base_rgb[0] * brightness))
            g = min(255, int(base_rgb[1] * brightness))
            b = min(255, int(base_rgb[2] * brightness))
            self.canvas.itemconfig(line_id, fill=f"#{r:02x}{g:02x}{b:02x}")
            new_h_lines.append((line_id, t))
        self.grid_h_lines = new_h_lines
        # Update vertical lines endpoints (converge to horizon point; base y stable, color pulse)
        horizon_x = self.width/2
        new_v_lines = []
        for line_id, x_norm in self.grid_v_lines:
            base_x = x_norm * self.width
            self.canvas.coords(line_id, base_x, self.grid_base_y, horizon_x, self.grid_horizon_y)
            # Color gradient across X using same contrast endpoints but with horizontal weighting
            base_rgb = _mix(grad_a, grad_b, x_norm)
            brightness = 0.50 + 0.50*glow
            r = min(255, int(base_rgb[0] * brightness))
            g = min(255, int(base_rgb[1] * brightness))
            b = min(255, int(base_rgb[2] * brightness))
            self.canvas.itemconfig(line_id, fill=f"#{r:02x}{g:02x}{b:02x}")
            new_v_lines.append((line_id, x_norm))
        self.grid_v_lines = new_v_lines
        # Send lines to back so gameplay elements appear above
        for line_id, _ in self.grid_h_lines:
            self.canvas.tag_lower(line_id)
        for line_id, _ in self.grid_v_lines:
            self.canvas.tag_lower(line_id)

    def restart_game(self, event=None, force=False):
        if not self.game_over and not force:
            return
        # Clear canvas
        for item in self.canvas.find_all():
            self.canvas.delete(item)
        # Recreate background grid before gameplay elements
        self.init_background()
        # Recreate player and HUD
    # Recreate fancy player sprite
        self.player = None
        self.create_player_sprite()
        # Reset bullet containers
        self.bullets = []
        self.bullets2 = []
        self.triangle_bullets = []
        self.diag_bullets = []
        self.boss_bullets = []
        self.zigzag_bullets = []
        self.fast_bullets = []
        self.star_bullets = []
        self.rect_bullets = []
        self.fast_bullets = []
        self.egg_bullets = []
        self.bouncing_bullets = []
        self.exploding_bullets = []
        self.exploded_fragments = []
        self.laser_indicators = []
        self.lasers = []
        self.homing_bullets = []
        self.spiral_bullets = []
        self.radial_bullets = []
        self.wave_bullets = []
        self.boomerang_bullets = []
        self.split_bullets = []
        # Reset scores/timers
        self.score = 0
        self.timee = int(time.time())
        self.scorecount = self.canvas.create_text(70, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 16))
        self.timecount = self.canvas.create_text(self.width-70, 20, text=f"Time: {self.timee}", fill="white", font=("Arial", 16))
        self.dialog = self.canvas.create_text(self.width//2, 20, text=self.dial, fill="white", font=("Arial", 20), justify="center")
        self.next_unlock_text = self.canvas.create_text(self.width//2, self.height-8, text="", fill="#88ddff", font=("Arial", 16), anchor='s')
        # Core state
        self.lives = 1
        self.game_over = False
        self.paused = False
        self.pause_text = None
        self.difficulty = 1
        self.last_difficulty_increase = time.time()
        self.lastdial = time.time()
        self.paused_time_total = 0
        self.pause_start_time = None
        # Reset unlock schedule
        self.unlock_times = {
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
            'split': 240
        }
        self.update_game()

    def shoot_quad_bullet(self):
        if not self.game_over:
            x = random.randint(0, self.width-20)
            bullet1 = self.canvas.create_oval(x, 0, x + 20, 20, fill="red")
            bullet2 = self.canvas.create_oval(x + 30, 0, x + 50, 20, fill="red")
            bullet3 = self.canvas.create_oval(x + 60, 0, x + 80, 20, fill="red")
            bullet4 = self.canvas.create_oval(x + 90, 0, x + 110, 20, fill="red")
            self.bullets.extend([bullet1, bullet2, bullet3, bullet4])

    def shoot_triangle_bullet(self):
        if not self.game_over:
            x = random.randint(0, self.width-20)
            direction = random.choice([1, -1])
            # Draw triangle using create_polygon
            points = [x, 0, x+20, 0, x+10, 20]
            bullet = self.canvas.create_polygon(points, fill="#bfff00")
            self.triangle_bullets.append((bullet, direction))

    def get_dialog_string(self):
        dialogs = [
            ":)",
            "Hi-hi-hi! Wanna play with me? I promise it'll be fun!",
            "You're not supposed to be here… but that's okay. I like new toys.",
            "Tag, you're it! Forever and ever and ever.",
            "Do you remember me? No? That's fine. I'll make you remember.",
            "Let's make a game together! I'll be the rules, you be the player.",
            "I can see you. I can see everything. Heeheehee!",
            "One, two, three, four—oh, I lost count again! Doesn't matter. You're losing anyway",
            "I'm so lonely... please don't go away...",
            "Why is it so dark? I can't see you! Come closer so I can see you better.",
            "You look like fun! Let's play a game where I always win!",
            "You're pretty good at this! But can you beat me? Heehee!",
            "I'm nine-years old, always have been, always will be.",
            "Are you tired? You can rest... forever...",
            "Error 0xDEADBEEF: Childhood not found. Reinstalling...",
            "Do you want to see a magic trick? Watch me make your score disappear!",
            "I have so many friends! They're all in my head. Do you want to meet them?",
            "Sometimes I feel like I'm being watched... but it's probably just my imagination.",
            "Let's make a deal: you let me win, and I'll let you live... Maybe.",
            "I know all your secrets. Don't worry, I won't tell anyone... yet.",
            "Why do you keep playing this game? Don't you have anything better to do? \n Oh wait- you can't stop playing, can you?",
            "If you get tired, you can always take a nap... forever...",
            "I like your style! Let's see how long you can keep up with me!",
            "You're doing great! But can you do better? Heehee!",
            "I have a surprise for you! It's called 'Game Over'. Heehee!",
            "Let's play a game of hide and seek! I'll hide, and you can never find me.",
            "You look like you could use a friend. Want to be my friend? Forever...",
            "Quick! Look behind you! Heeheehee!",
            "Do you want to hear a secret? I have a secret... but I can't tell you. Heehee!",
            "ssshhh... can you hear that? It's the sound of your score disappearing!",
            "I could really go for some applesauce... Or mortal flesh...",
            "Why do you keep trying? You know you'll never win against me!",
            "Do you hear them singing? They're all my friends. They lost, too",
            "There isn't really an end to this.  it just keeps going and going and going... \n Belive me, I've tried to stop it."
        ]
        self.dial=random.choice(dialogs)
        if self.dial == ":)":
            self.canvas.itemconfig(self.dialog, fill="red")
        else:
            self.canvas.itemconfig(self.dialog, fill="white")
        return self.dial

    def shoot_horizontal_laser(self):
        if not self.game_over:
            y = random.randint(50, self.height-50)
            indicator = self.canvas.create_line(0, y, self.width, y, fill="red", dash=(5, 2), width=3)
            self.laser_indicators.append((indicator, y, 30))  # 30 frames indicator

    def shoot_exploding_bullet(self):
        if not self.game_over:
            x = random.randint(0, self.width-20)
            bullet = self.canvas.create_oval(x, 0, x + 20, 20, fill="white")
            self.exploding_bullets.append(bullet)

    def shoot_star_bullet(self):
        if not self.game_over:
            # Proper 5-point star with outline. Keep hit area similar size.
            outer_r = 18
            inner_r = outer_r * 0.45
            # Ensure it fits horizontally
            cx = random.randint(outer_r+2, self.width - outer_r - 2)
            cy = outer_r  # start near top
            pts = []
            # Star points (10 vertices alternating outer/inner)
            for i in range(10):
                angle = -math.pi/2 + i * math.pi/5  # start pointing up
                r = outer_r if i % 2 == 0 else inner_r
                px = cx + r * math.cos(angle)
                py = cy + r * math.sin(angle)
                pts.extend([px, py])
            bullet = self.canvas.create_polygon(pts, fill="magenta", outline="white", width=2)
            self.star_bullets.append(bullet)

    def shoot_rect_bullet(self):
        if not self.game_over:
            x = random.randint(0, self.width-60)
            bullet = self.canvas.create_rectangle(x, 0, x+60, 15, fill="blue")
            self.rect_bullets.append(bullet)

    def shoot_zigzag_bullet(self):
        if not self.game_over:
            x = random.randint(0, self.width-20)
            bullet = self.canvas.create_oval(x, 0, x + 20, 20, fill="cyan")
            # Zigzag state: (bullet, direction, step_count)
            direction = random.choice([1, -1])
            self.zigzag_bullets.append((bullet, direction, 0))

    def shoot_fast_bullet(self):
        if not self.game_over:
            x = random.randint(0, self.width-20)
            bullet = self.canvas.create_oval(x, 0, x + 20, 20, fill="orange")
            self.fast_bullets.append(bullet)

    # ---------------- New bullet spawners ----------------
    def shoot_homing_bullet(self):
        """Spawn a bullet that gradually steers toward the player."""
        if not self.game_over:
            x = random.randint(0, self.width-20)
            bullet = self.canvas.create_oval(x, 0, x + 16, 16, fill="#ffdd00")
            # Start with simple downward motion; vx adjusted over time
            self.homing_bullets.append((bullet, 0.0, 4.0))

    def shoot_spiral_bullet(self):
        """Spawn a bullet that spirals outward from a point (random near center)."""
        if not self.game_over:
            cx = random.randint(self.width//3, self.width*2//3)
            cy = random.randint(60, self.height//3)
            angle = random.uniform(0, math.tau if hasattr(math, 'tau') else 2*math.pi)
            bullet = self.canvas.create_oval(cx-10, cy-10, cx+10, cy+10, fill="#00ff88")
            ang_speed = 0.35  # radians per frame
            rad_speed = 2.0 + self.difficulty/6
            self.spiral_bullets.append((bullet, angle, 0.0, ang_speed, rad_speed, cx, cy))

    def shoot_radial_burst(self):
        """Spawn a radial burst of small bullets from a random point."""
        if not self.game_over:
            cx = random.randint(self.width//4, self.width*3//4)
            cy = random.randint(80, self.height//2)
            count = 8
            base_speed = 3.5 + self.difficulty/5
            for i in range(count):
                ang = (2*math.pi / count) * i + random.uniform(-0.1, 0.1)
                vx = math.cos(ang) * base_speed
                vy = math.sin(ang) * base_speed
                bullet = self.canvas.create_oval(cx-8, cy-8, cx+8, cy+8, fill="#ff00ff")
                self.radial_bullets.append((bullet, vx, vy))

    # ---------- New bullet pattern spawners (Wave, Boomerang, Split) ----------
    def shoot_wave_bullet(self):
        """Bullet that moves downward while wobbling horizontally (sinusoidal)."""
        if not self.game_over:
            x = random.randint(40, self.width-40)
            size = 18
            bullet = self.canvas.create_oval(x-size//2, 0, x+size//2, size, fill="#33aaff")
            base_x = x
            phase = random.uniform(0, 2*math.pi)
            amp = random.randint(40, 90)
            vy = 5 + self.difficulty/4
            phase_speed = 0.25 + self.difficulty/30
            self.wave_bullets.append((bullet, base_x, phase, amp, vy, phase_speed))

    def shoot_boomerang_bullet(self):
        """Bullet that goes down then returns upward (boomerang)."""
        if not self.game_over:
            x = random.randint(30, self.width-30)
            size = 22
            bullet = self.canvas.create_oval(x-size//2, 0, x+size//2, size, fill="#ffaa33")
            vy = 8 + self.difficulty/3
            timer = random.randint(18, 30)  # frames moving down before returning
            self.boomerang_bullets.append((bullet, vy, timer, 'down'))

    def shoot_split_bullet(self):
        """Bullet that falls then splits into fragments that spread out."""
        if not self.game_over:
            x = random.randint(30, self.width-30)
            size = 24
            bullet = self.canvas.create_oval(x-size//2, 0, x+size//2, size, fill="#ffffff", outline="#ff55ff", width=2)
            timer = random.randint(20, 35)
            self.split_bullets.append((bullet, timer))

    def shoot_bouncing_bullet(self):
        if not self.game_over:
            x = random.randint(0, self.width-20)
            bullet = self.canvas.create_oval(x, 0, x + 20, 20, fill="pink")
            # Random angle in radians
            angle = random.uniform(0, 2 * 3.14159)
            speed = 7 + self.difficulty // 2
            x_velocity = speed * math.cos(angle)
            y_velocity = speed * math.sin(angle)
            # Bouncing state: (bullet, x_velocity, y_velocity, bounces_left)
            self.bouncing_bullets.append((bullet, x_velocity, y_velocity, 3))

    def move_player(self, event):
        if self.paused or self.game_over:
            return
        s = self.player_speed
        if event.keysym in ('Left','a'):
            self.apply_player_move(-s,0)
        elif event.keysym in ('Right','d'):
            self.apply_player_move(s,0)
        elif event.keysym in ('Up','w'):
            self.apply_player_move(0,-s)
        elif event.keysym in ('Down','s'):
            self.apply_player_move(0,s)

    def toggle_pause(self, event=None):
        if self.game_over:
            return
        self.paused = not self.paused
        if self.paused:
            self.pause_start_time = time.time()
            if not self.pause_text:
                self.pause_text = self.canvas.create_text(self.width//2, self.height//2, text="Paused", fill="yellow", font=("Arial", 40))
        else:
            if self.pause_text:
                self.canvas.delete(self.pause_text)
                self.pause_text = None
            # Add paused duration to total
            if self.pause_start_time:
                self.paused_time_total += time.time() - self.pause_start_time
                self.pause_start_time = None
        # Resume update loop if unpaused
        if not self.paused:
            self.update_game()

    def shoot_bullet(self):
        if not self.game_over:
            x = random.randint(0, self.width-20)
            bullet = self.canvas.create_oval(x, 0, x + 20, 20, fill="red")
            self.bullets.append(bullet)

    def shoot_egg_bullet(self):
        if not self.game_over:
            x = random.randint(0, self.width-20)
            bullet = self.canvas.create_oval(x, 0, x + 20, 40, fill="tan")
            self.egg_bullets.append(bullet)

    def shoot_bullet2(self):
        if not self.game_over:
            y = random.randint(0, self.height-20)
            bullet2 = self.canvas.create_oval(0, y, 20, y + 20, fill="yellow")
            self.bullets2.append(bullet2)

    def shoot_diag_bullet(self):
        if not self.game_over:
            x = random.randint(0, self.width-20)
            direction = random.choice([1, -1])  # 1 for right-down, -1 for left-down
            dbullet = self.canvas.create_oval(x, 0, x + 20, 20, fill="green")
            self.diag_bullets.append((dbullet, direction))

    def shoot_boss_bullet(self):
        if not self.game_over:
            x = random.randint(self.width//4, self.width*3//4)
            bullet = self.canvas.create_oval(x, 0, x + 40, 40, fill="purple")
            self.boss_bullets.append(bullet)

    def show_graze_effect(self):
        # Remove previous effect if present
        if self.graze_effect_id:
            self.canvas.delete(self.graze_effect_id)
        px1, py1, px2, py2 = self.canvas.coords(self.player)
        cx = (px1 + px2) / 2
        cy = (py1 + py2) / 2
        self.graze_effect_id = self.canvas.create_oval(
            cx - self.grazing_radius, cy - self.grazing_radius,
            cx + self.grazing_radius, cy + self.grazing_radius,
            outline="white", dash=(5, 5), width=2
        )
        self.graze_effect_timer = 4  # Number of update cycles to show (200ms)

    def check_graze(self, bullet):
        # Returns True if bullet grazes player (close but not colliding)
        bullet_coords = self.canvas.coords(bullet)
        if len(bullet_coords) < 4:
            return False  # Bullet was deleted or invalid
        player_coords = self.canvas.coords(self.player)
        px1, py1, px2, py2 = player_coords
        cx = (px1 + px2) / 2
        cy = (py1 + py2) / 2
        # Handle polygons (coords > 4)
        if len(bullet_coords) > 4:
            xs = bullet_coords[::2]
            ys = bullet_coords[1::2]
            bx = sum(xs) / len(xs)
            by = sum(ys) / len(ys)
        else:
            bx = (bullet_coords[0] + bullet_coords[2]) / 2
            by = (bullet_coords[1] + bullet_coords[3]) / 2
        dist = ((cx - bx) ** 2 + (cy - by) ** 2) ** 0.5
        # Not colliding, but within grazing radius
        if dist < self.grazing_radius + 10 and not self.check_collision(bullet):
            return True
        return False

    def check_collision(self, bullet):
        """Axis-aligned hitbox collision between player rectangle and a bullet shape.
        Supports ovals/rectangles (4 coords) and polygons (>=6 coords). Returns True on hit.
        """
        if self.practice_mode or self.game_over:
            return False
        try:
            b = self.canvas.coords(bullet)
            if not b:
                return False
            # Player rectangle
            px1, py1, px2, py2 = self.canvas.coords(self.player)
            # Bullet bounding box
            if len(b) == 4:
                bx1, by1, bx2, by2 = b
            else:
                xs = b[::2]
                ys = b[1::2]
                bx1, bx2 = min(xs), max(xs)
                by1, by2 = min(ys), max(ys)
            # AABB overlap
            if px1 < bx2 and px2 > bx1 and py1 < by2 and py2 > by1:
                self.handle_player_hit()
                return True
        except Exception:
            return False
        return False

    def handle_player_hit(self):
        """Process a player hit: decrement life (if multiple), or trigger game over animation."""
        if self.game_over:
            return
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
            # Start game over animation if available
            try:
                self.start_game_over_animation()
            except Exception:
                pass
        else:
            # Flash player or simple feedback (placeholder)
            try:
                self.canvas.itemconfig(self.player, fill="#ffffff")
            except Exception:
                pass

    def update_game(self):
        if self.game_over:
            return
        if self.paused:
            return
        # Steam Input preferred, fallback to pygame joystick
        used_steam = self.poll_steam_input()
        if not used_steam:
            self.poll_gamepad()
    # Background animation
        self.update_background()
    # Animate player decorative sprite
        self.animate_player_sprite()
        self.canvas.lift(self.dialog)
        self.canvas.lift(self.scorecount)
        self.canvas.lift(self.timecount)
        if hasattr(self, 'next_unlock_text'):
            self.canvas.lift(self.next_unlock_text)
        # Move graze effect to follow player if active
        if self.graze_effect_id:
            px1, py1, px2, py2 = self.canvas.coords(self.player)
            cx = (px1 + px2) / 2
            cy = (py1 + py2) / 2
            self.canvas.coords(
                self.graze_effect_id,
                cx - self.grazing_radius, cy - self.grazing_radius,
                cx + self.grazing_radius, cy + self.grazing_radius
            )
            self.graze_effect_timer -= 1
            if self.graze_effect_timer <= 0:
                self.canvas.delete(self.graze_effect_id)
                self.graze_effect_id = None
        # Increase difficulty every 60 seconds
        now = time.time()
    # Difficulty scaling removed
        if now - self.lastdial > 10:
            self.get_dialog_string()
            self.lastdial = now
            self.canvas.itemconfig(self.dialog, text=self.dial)
        # Lore rotation
        if getattr(self, 'lore_text', None) is not None and now - getattr(self, 'lore_last_change', 0) >= getattr(self, 'lore_interval', 8):
            self.update_lore_line()
        # Calculate time survived, pausable
        time_survived = int(now - self.timee - self.paused_time_total)
        self.canvas.itemconfig(self.scorecount, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.timecount, text=f"Time: {time_survived}")
        # Compute next unlock pattern
        remaining_candidates = [(pat, t_req - time_survived) for pat, t_req in self.unlock_times.items() if t_req > time_survived]
        if remaining_candidates:
            # Pick soonest
            pat, secs = min(remaining_candidates, key=lambda x: x[1])
            display = self.pattern_display_names.get(pat, pat.title())
            self.canvas.itemconfig(self.next_unlock_text, text=f"Next Pattern: {display} in {secs}s")
        else:
            self.canvas.itemconfig(self.next_unlock_text, text="All patterns unlocked")

        # Fixed spawn chances (1 in N each frame after unlock)
        bullet_chance = 18
        bullet2_chance = 22
        diag_chance = 28
        boss_chance = 140
        zigzag_chance = 40
        fast_chance = 30
        star_chance = 55
        rect_chance = 48
        laser_chance = 160
        triangle_chance = 46
        quad_chance = 52
        egg_chance = 50
        bouncing_chance = 70
        exploding_chance = 90
        homing_chance = 110
        spiral_chance = 130
        radial_chance = 150
        wave_chance = 160
        boomerang_chance = 170
        split_chance = 180

        # Time-based unlock gating (progressive difficulty)
        t = time_survived
        if t >= self.unlock_times['vertical'] and random.randint(1, bullet_chance) == 1:
            self.shoot_bullet()
        if t >= self.unlock_times['horizontal'] and random.randint(1, bullet2_chance) == 1:
            self.shoot_bullet2()
        if t >= self.unlock_times['diag'] and random.randint(1, diag_chance) == 1:
            self.shoot_diag_bullet()
        if t >= self.unlock_times['boss'] and random.randint(1, boss_chance) == 1:
            self.shoot_boss_bullet()
        if t >= self.unlock_times['zigzag'] and random.randint(1, zigzag_chance) == 1:
            self.shoot_zigzag_bullet()
        if t >= self.unlock_times['fast'] and random.randint(1, fast_chance) == 1:
            self.shoot_fast_bullet()
        if t >= self.unlock_times['star'] and random.randint(1, star_chance) == 1:
            self.shoot_star_bullet()
        if t >= self.unlock_times['rect'] and random.randint(1, rect_chance) == 1:
            self.shoot_rect_bullet()
        if t >= self.unlock_times['laser'] and random.randint(1, laser_chance) == 1:
            self.shoot_horizontal_laser()
        if t >= self.unlock_times['triangle'] and random.randint(1, triangle_chance) == 1:
            self.shoot_triangle_bullet()
        if t >= self.unlock_times['quad'] and random.randint(1, quad_chance) == 1:
            self.shoot_quad_bullet()
        if t >= self.unlock_times['egg'] and random.randint(1, egg_chance) == 1:
            self.shoot_egg_bullet()
        if t >= self.unlock_times['bouncing'] and random.randint(1, bouncing_chance) == 1:
            self.shoot_bouncing_bullet()
        if t >= self.unlock_times['exploding'] and random.randint(1, exploding_chance) == 1:
            self.shoot_exploding_bullet()
        if t >= self.unlock_times['homing'] and random.randint(1, homing_chance) == 1:
            self.shoot_homing_bullet()
        if t >= self.unlock_times['spiral'] and random.randint(1, spiral_chance) == 1:
            self.shoot_spiral_bullet()
        if t >= self.unlock_times['radial'] and random.randint(1, radial_chance) == 1:
            self.shoot_radial_burst()
        if t >= self.unlock_times['wave'] and random.randint(1, wave_chance) == 1:
            self.shoot_wave_bullet()
        if t >= self.unlock_times['boomerang'] and random.randint(1, boomerang_chance) == 1:
            self.shoot_boomerang_bullet()
        if t >= self.unlock_times['split'] and random.randint(1, split_chance) == 1:
            self.shoot_split_bullet()
        # Move triangle bullets
        triangle_speed = 7

        for bullet_tuple in self.triangle_bullets[:]:
            bullet, direction = bullet_tuple
            self.canvas.move(bullet, triangle_speed * direction, triangle_speed)
            if self.check_collision(bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(bullet)
                self.paused = False
                self.pause_text = None
                self.triangle_bullets.remove(bullet_tuple)
            else:
                coords = self.canvas.coords(bullet)
                if coords[1] > self.height or coords[0] < 0 or coords[2] > self.width:
                    self.canvas.delete(bullet)
                    self.triangle_bullets.remove(bullet_tuple)
                    self.score += 2
        # Move bouncing bullets
        for bullet_tuple in self.bouncing_bullets[:]:
            bullet, x_velocity, y_velocity, bounces_left = bullet_tuple
            self.canvas.move(bullet, x_velocity, y_velocity)
            coords = self.canvas.coords(bullet)
            bounced = False
            # Bounce off left/right
            if coords[0] <= 0 or coords[2] >= self.width:
                x_velocity = -x_velocity
                bounced = True
            # Bounce off top/bottom
            if coords[1] <= 0 or coords[3] >= self.height:
                y_velocity = -y_velocity
                bounced = True
            if bounced:
                bounces_left -= 1
            # Remove bullet if out of bounces
            if bounces_left < 0:
                self.canvas.delete(bullet)
                self.bouncing_bullets.remove(bullet_tuple)
                self.score += 2
                continue
            # Update tuple with new velocities and bounces
            idx = self.bouncing_bullets.index(bullet_tuple)
            self.bouncing_bullets[idx] = (bullet, x_velocity, y_velocity, bounces_left)
            if self.check_collision(bullet):
                self.lives -= 1
                self.canvas.delete(bullet)
                self.bouncing_bullets.remove((bullet, x_velocity, y_velocity, bounces_left))
                if self.lives <= 0:
                    self.end_game()
        # Move exploding bullets
        for bullet in self.exploding_bullets[:]:
            self.canvas.move(bullet, 0, 5 + self.difficulty // 3)
            coords = self.canvas.coords(bullet)
            # Check if bullet reached middle of screen (y ~ self.height//2)
            if coords and abs((coords[1] + coords[3]) / 2 - self.height // 2) < 20:
                # Explode into 4 diagonal fragments
                bx = (coords[0] + coords[2]) / 2
                by = (coords[1] + coords[3]) / 2
                size = 12
                directions = [(6, 6), (-6, 6), (6, -6), (-6, -6)]
                for dx, dy in directions:
                    frag = self.canvas.create_oval(bx-size//2, by-size//2, bx+size//2, by+size//2, fill="white")
                    self.exploded_fragments.append((frag, dx, dy))
                self.canvas.delete(bullet)
                self.exploding_bullets.remove(bullet)
                self.score += 2
                continue
            if self.check_collision(bullet):
                self.lives -= 1
                self.canvas.delete(bullet)
                self.exploding_bullets.remove(bullet)
                if self.lives <= 0:
                    self.end_game()
            else:
                if coords and coords[1] > self.height:
                    self.canvas.delete(bullet)
                    self.exploding_bullets.remove(bullet)
                    self.score += 2
        # Move exploded fragments (diagonal bullets)
        for frag_tuple in self.exploded_fragments[:]:
            frag, dx, dy = frag_tuple
            self.canvas.move(frag, dx, dy)
            coords = self.canvas.coords(frag)
            if self.check_collision(frag):
                self.lives -= 1
                self.canvas.delete(frag)
                self.exploded_fragments.remove(frag_tuple)
                if self.lives <= 0:
                    self.end_game()
            elif coords and (coords[1] > self.height or coords[0] < 0 or coords[2] > self.width or coords[3] < 0):
                self.canvas.delete(frag)
                self.exploded_fragments.remove(frag_tuple)
                self.score += 1
            # Grazing check
            if self.check_graze(frag) and frag not in self.grazed_bullets:
                self.score += 1
                self.grazed_bullets.add(frag)
                self.show_graze_effect()
        # Handle laser indicators
        for indicator_tuple in self.laser_indicators[:]:
            indicator_id, y, timer = indicator_tuple
            timer -= 1
            if timer <= 0:
                self.canvas.delete(indicator_id)
                # Spawn actual laser
                laser_id = self.canvas.create_line(0, y, self.width, y, fill="red", width=8)
                self.lasers.append((laser_id, y, 20))  # Laser lasts 20 frames
                self.laser_indicators.remove(indicator_tuple)
            else:
                idx = self.laser_indicators.index(indicator_tuple)
                self.laser_indicators[idx] = (indicator_id, y, timer)

        # Handle lasers
        for laser_tuple in self.lasers[:]:
            laser_id, y, timer = laser_tuple
            timer -= 1
            # Check collision with player
            player_coords = self.canvas.coords(self.player)
            if player_coords[1] <= y <= player_coords[3]:
                self.lives -= 1
                self.canvas.delete(laser_id)
                self.lasers.remove(laser_tuple)
                if self.lives <= 0:
                    self.end_game()
                continue
            if timer <= 0:
                self.canvas.delete(laser_id)
                self.lasers.remove(laser_tuple)
            else:
                idx = self.lasers.index(laser_tuple)
                self.lasers[idx] = (laser_id, y, timer)

        # Bullet speeds scale with difficulty
        bullet_speed = 7
        bullet2_speed = 7
        diag_speed = 5
        boss_speed = 10
        zigzag_speed = 5
        fast_speed = 14
        star_speed = 8
        rect_speed = 8
        quad_speed = 7
        egg_speed = 6
        homing_speed = 6

        # Move vertical bullets
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, bullet_speed)
            if self.check_collision(bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
            elif self.canvas.coords(bullet)[1] > self.height:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
                self.score += 1
            # Grazing check
            if self.check_graze(bullet) and bullet not in self.grazed_bullets:
                self.score += 1
                self.grazed_bullets.add(bullet)
                self.show_graze_effect()

        # Move horizontal bullets
        for bullet2 in self.bullets2[:]:
            self.canvas.move(bullet2, bullet2_speed, 0)
            if self.check_collision(bullet2):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(bullet2)
                self.bullets2.remove(bullet2)
            elif self.canvas.coords(bullet2)[0] > self.width:
                self.canvas.delete(bullet2)
                self.bullets2.remove(bullet2)
                self.score += 1
            # Grazing check
            if self.check_graze(bullet2) and bullet2 not in self.grazed_bullets:
                self.score += 1
                self.grazed_bullets.add(bullet2)
                self.show_graze_effect()

        # Move egg bullets
        for egg_bullet in self.egg_bullets[:]:
            self.canvas.move(egg_bullet, 0, egg_speed)
            if self.check_collision(egg_bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(egg_bullet)
                self.egg_bullets.remove(egg_bullet)
            elif self.canvas.coords(egg_bullet)[1] > self.height:
                self.canvas.delete(egg_bullet)
                self.egg_bullets.remove(egg_bullet)
                self.score += 2
            # Grazing check
            if self.check_graze(egg_bullet) and egg_bullet not in self.grazed_bullets:
                self.score += 1
                self.grazed_bullets.add(egg_bullet)
                self.show_graze_effect()

        # Move diagonal bullets
        for bullet_tuple in self.diag_bullets[:]:
            dbullet, direction = bullet_tuple
            self.canvas.move(dbullet, diag_speed * direction, diag_speed)
            if self.check_collision(dbullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(dbullet)
                self.diag_bullets.remove(bullet_tuple)
            elif self.canvas.coords(dbullet)[1] > self.height:
                self.canvas.delete(dbullet)
                self.diag_bullets.remove(bullet_tuple)
                self.score += 2
            # Grazing check
            if self.check_graze(dbullet) and dbullet not in self.grazed_bullets:
                self.score += 1
                self.grazed_bullets.add(dbullet)
                self.show_graze_effect()

        # Move boss bullets
        for boss_bullet in self.boss_bullets[:]:
            self.canvas.move(boss_bullet, 0, boss_speed)
            if self.check_collision(boss_bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(boss_bullet)
                self.boss_bullets.remove(boss_bullet)
            elif self.canvas.coords(boss_bullet)[1] > self.height:
                self.canvas.delete(boss_bullet)
                self.boss_bullets.remove(boss_bullet)
                self.score += 5  # Boss bullets give more score
            # Grazing check
            if self.check_graze(boss_bullet) and boss_bullet not in self.grazed_bullets:
                self.score += 2
                self.grazed_bullets.add(boss_bullet)
                self.show_graze_effect()

        # Move quad bullets
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, quad_speed)
            if self.check_collision(bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
            elif self.canvas.coords(bullet)[1] > self.height:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
                self.score += 2
            # Grazing check
            if self.check_graze(bullet) and bullet not in self.grazed_bullets:
                self.score += 1
                self.grazed_bullets.add(bullet)
                self.show_graze_effect()

        # Move zigzag bullets
        for bullet_tuple in self.zigzag_bullets[:]:
            bullet, direction, step_count = bullet_tuple
            # Change direction every 10 steps
            if step_count % 10 == 0:
                direction *= -1
            self.canvas.move(bullet, 5 * direction, zigzag_speed)
            if self.check_collision(bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(bullet)
                self.zigzag_bullets.remove(bullet_tuple)
            else:
                coords = self.canvas.coords(bullet)
                if coords[1] > self.height or coords[0] < 0 or coords[2] > self.width:
                    self.canvas.delete(bullet)
                    self.zigzag_bullets.remove(bullet_tuple)
                    self.score += 2
                else:
                    # Update tuple with incremented step_count and possibly new direction
                    idx = self.zigzag_bullets.index(bullet_tuple)
                    self.zigzag_bullets[idx] = (bullet, direction, step_count + 1)
            # Grazing check
            if self.check_graze(bullet) and bullet not in self.grazed_bullets:
                self.score += 1
                self.grazed_bullets.add(bullet)
                self.show_graze_effect()

        # Move fast bullets
        for fast_bullet in self.fast_bullets[:]:
            self.canvas.move(fast_bullet, 0, fast_speed)
            if self.check_collision(fast_bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(fast_bullet)
                self.fast_bullets.remove(fast_bullet)
            elif self.canvas.coords(fast_bullet)[1] > self.height:
                self.canvas.delete(fast_bullet)
                self.fast_bullets.remove(fast_bullet)
                self.score += 2
            # Grazing check
            if self.check_graze(fast_bullet) and fast_bullet not in self.grazed_bullets:
                self.score += 1
                self.grazed_bullets.add(fast_bullet)
                self.show_graze_effect()

        # Move & spin star bullets
        for star_bullet in self.star_bullets[:]:
            # Fall movement
            self.canvas.move(star_bullet, 0, star_speed)
            # Spin: fetch current coords, rotate around center by small angle
            coords = self.canvas.coords(star_bullet)
            if len(coords) >= 6:  # polygon
                # Compute center
                xs = coords[0::2]
                ys = coords[1::2]
                cx = sum(xs)/len(xs)
                cy = sum(ys)/len(ys)
                angle = 0.18  # radians per frame
                sin_a = math.sin(angle)
                cos_a = math.cos(angle)
                new_pts = []
                for x, y in zip(xs, ys):
                    dx = x - cx
                    dy = y - cy
                    rx = dx * cos_a - dy * sin_a + cx
                    ry = dx * sin_a + dy * cos_a + cy
                    new_pts.extend([rx, ry])
                self.canvas.coords(star_bullet, *new_pts)
            # Collision / bounds / graze
            if self.check_collision(star_bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(star_bullet)
                self.star_bullets.remove(star_bullet)
                continue
            # Off screen
            bbox = self.canvas.bbox(star_bullet)
            if bbox and bbox[1] > self.height:
                self.canvas.delete(star_bullet)
                self.star_bullets.remove(star_bullet)
                self.score += 3
                continue
            # Grazing
            if self.check_graze(star_bullet) and star_bullet not in self.grazed_bullets:
                self.score += 1
                self.grazed_bullets.add(star_bullet)
                self.show_graze_effect()

        # Move rectangle bullets
        for rect_bullet in self.rect_bullets[:]:
            self.canvas.move(rect_bullet, 0, rect_speed)
            if self.check_collision(rect_bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(rect_bullet)
                self.rect_bullets.remove(rect_bullet)
            elif self.canvas.coords(rect_bullet)[1] > self.height:
                self.canvas.delete(rect_bullet)
                self.rect_bullets.remove(rect_bullet)
                self.score += 2
            # Grazing check
            if self.check_graze(rect_bullet) and rect_bullet not in self.grazed_bullets:
                self.score += 1
                self.grazed_bullets.add(rect_bullet)
                self.show_graze_effect()

        # ---------------- Move homing bullets ----------------
        for hb_tuple in self.homing_bullets[:]:
            bullet, vx, vy = hb_tuple
            # Compute vector toward player center
            px1, py1, px2, py2 = self.canvas.coords(self.player)
            pcx = (px1 + px2)/2
            pcy = (py1 + py2)/2
            bx1, by1, bx2, by2 = self.canvas.coords(bullet)
            bcx = (bx1 + bx2)/2
            bcy = (by1 + by2)/2
            dx = pcx - bcx
            dy = pcy - bcy
           
            dist = math.hypot(dx, dy) or 1
            # Normalize and apply steering (lerp velocities)
            target_vx = dx / dist * homing_speed
            target_vy = dy / dist * homing_speed
            steer_factor = 0.15  # how quickly it turns
            vx = vx * (1 - steer_factor) + target_vx * steer_factor
            vy = vy * (1 - steer_factor) + target_vy * steer_factor
            self.canvas.move(bullet, vx, vy)
            # Update tuple
            idx = self.homing_bullets.index(hb_tuple)
            self.homing_bullets[idx] = (bullet, vx, vy)
            # Collision / out of bounds
            if self.check_collision(bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(bullet)
                self.homing_bullets.remove((bullet, vx, vy))
            else:
                coords = self.canvas.coords(bullet)
                if not coords or coords[1] > self.height or coords[0] < -40 or coords[2] > self.width + 40:
                    self.canvas.delete(bullet)
                    self.homing_bullets.remove((bullet, vx, vy))
                    self.score += 3
            if bullet not in self.grazed_bullets and self.check_graze(bullet):
                self.score += 1
                self.grazed_bullets.add(bullet)
                self.show_graze_effect()

        # ---------------- Move spiral bullets ----------------
        for sp_tuple in self.spiral_bullets[:]:
            bullet, angle, radius, ang_speed, rad_speed, cx, cy = sp_tuple
            angle += ang_speed
            radius += rad_speed
            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius
            size = 20
            self.canvas.coords(bullet, x-size/2, y-size/2, x+size/2, y+size/2)
            # Collision & removal
            if self.check_collision(bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(bullet)
                self.spiral_bullets.remove(sp_tuple)
                continue
            if (x < -40 or x > self.width + 40 or y < -40 or y > self.height + 40 or radius > max(self.width, self.height)):
                self.canvas.delete(bullet)
                self.spiral_bullets.remove(sp_tuple)
                self.score += 2
                continue
            # Update tuple
            idx = self.spiral_bullets.index(sp_tuple)
            self.spiral_bullets[idx] = (bullet, angle, radius, ang_speed, rad_speed, cx, cy)
            if bullet not in self.grazed_bullets and self.check_graze(bullet):
                self.score += 1
                self.grazed_bullets.add(bullet)
                self.show_graze_effect()

        # ---------------- Move radial burst bullets ----------------
        for rb_tuple in self.radial_bullets[:]:
            bullet, vx, vy = rb_tuple
            self.canvas.move(bullet, vx, vy)
            if self.check_collision(bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(bullet)
                self.radial_bullets.remove(rb_tuple)
                continue
            coords = self.canvas.coords(bullet)
            if (not coords or coords[2] < -20 or coords[0] > self.width + 20 or coords[3] < -20 or coords[1] > self.height + 20):
                self.canvas.delete(bullet)
                self.radial_bullets.remove(rb_tuple)
                self.score += 1
                continue
            if bullet not in self.grazed_bullets and self.check_graze(bullet):
                self.score += 1
                self.grazed_bullets.add(bullet)
                self.show_graze_effect()

        # ---------------- Move wave bullets ----------------
        for wtuple in self.wave_bullets[:]:
            bullet, base_x, phase, amp, vy, phase_speed = wtuple
            phase += phase_speed
            # Get current bullet coords to compute center y
            bx1, by1, bx2, by2 = self.canvas.coords(bullet)
            height = by2 - by1
            # Vertical move
            self.canvas.move(bullet, 0, vy)
            # Recompute center after vertical move
            bx1, by1, bx2, by2 = self.canvas.coords(bullet)
            cy = (by1 + by2)/2
            cx = base_x + math.sin(phase) * amp
            size = bx2 - bx1
            self.canvas.coords(bullet, cx-size/2, cy-height/2, cx+size/2, cy+height/2)
            if self.check_collision(bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(bullet)
                self.wave_bullets.remove(wtuple)
                continue
            if cy > self.height + 30:
                self.canvas.delete(bullet)
                self.wave_bullets.remove(wtuple)
                self.score += 2
                continue
            idx = self.wave_bullets.index(wtuple)
            self.wave_bullets[idx] = (bullet, base_x, phase, amp, vy, phase_speed)
            if bullet not in self.grazed_bullets and self.check_graze(bullet):
                self.score += 1
                self.grazed_bullets.add(bullet)
                self.show_graze_effect()

        # ---------------- Move boomerang bullets ----------------
        for btuple in self.boomerang_bullets[:]:
            bullet, vy, timer, state = btuple
            if state == 'down':
                self.canvas.move(bullet, 0, vy)
                timer -= 1
                if timer <= 0:
                    state = 'up'
            else:  # up
                self.canvas.move(bullet, 0, -vy*0.8)
            coords = self.canvas.coords(bullet)
            if self.check_collision(bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(bullet)
                self.boomerang_bullets.remove(btuple)
                continue
            if not coords or coords[3] < -30 or coords[1] > self.height + 40:
                self.canvas.delete(bullet)
                self.boomerang_bullets.remove(btuple)
                self.score += 3
                continue
            idx = self.boomerang_bullets.index(btuple)
            self.boomerang_bullets[idx] = (bullet, vy, timer, state)
            if bullet not in self.grazed_bullets and self.check_graze(bullet):
                self.score += 1
                self.grazed_bullets.add(bullet)
                self.show_graze_effect()

        # ---------------- Move split bullets ----------------
        for stuple in self.split_bullets[:]:
            bullet, timer = stuple
            self.canvas.move(bullet, 0, 5 + self.difficulty/4)
            timer -= 1
            coords = self.canvas.coords(bullet)
            if timer <= 0 and coords:
                # Split into fragments (6) moving outward in a circle
                bx = (coords[0] + coords[2]) / 2
                by = (coords[1] + coords[3]) / 2
                frag_count = 6
                frag_speed = 4 + self.difficulty/5
                for i in range(frag_count):
                    ang = (2*math.pi/frag_count)*i
                    vx = math.cos(ang) * frag_speed
                    vy2 = math.sin(ang) * frag_speed
                    frag = self.canvas.create_oval(bx-10, by-10, bx+10, by+10, fill="#ff55ff")
                    self.radial_bullets.append((frag, vx, vy2))
                self.canvas.delete(bullet)
                self.split_bullets.remove(stuple)
                self.score += 3
                continue
            if self.check_collision(bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(bullet)
                self.split_bullets.remove(stuple)
                continue
            if coords and coords[1] > self.height:
                self.canvas.delete(bullet)
                self.split_bullets.remove(stuple)
                self.score += 2
                continue
            idx = self.split_bullets.index(stuple)
            self.split_bullets[idx] = (bullet, timer)
            if bullet not in self.grazed_bullets and self.check_graze(bullet):
                self.score += 1
                self.grazed_bullets.add(bullet)
                self.show_graze_effect()

        # Mid-screen lore fragment display (spawn + blink + expire)
        try:
            if hasattr(self, 'maybe_show_mid_lore'):
                self.maybe_show_mid_lore()
            if getattr(self, '_mid_lore_items', None) is not None:
                for item in self._mid_lore_items[:]:
                    ids = item.get('ids', [])
                    life = item.get('life', 0)
                    life -= 1
                    item['life'] = life
                    # Blink during final 15 frames
                    if life < 15:
                        blink_hidden = (life % 4) in (0,1)
                        state = 'hidden' if blink_hidden else 'normal'
                        for oid in ids:
                            try: self.canvas.itemconfig(oid, state=state)
                            except Exception: pass
                    if life <= 0:
                        for oid in ids:
                            try: self.canvas.delete(oid)
                            except Exception: pass
                        self._mid_lore_items.remove(item)
        except Exception:
            pass

        self.root.after(50, self.update_game)

    def init_lore(self):
        # Categorized fragments derived from top-of-file lore comment.
        # No gameplay impact; can be surfaced in dialog.
        self.lore_fragments = {
            'rift': [
                "The Rift stacks moments like cassette tracks.",
                "VHS sunsets loop over statues of obsolete gods.",
                "Time here is a collage, not a line.",
                "YOU feel layers of futures that never resolved.",
                "Some seconds arrive already fossilized.",
                "Yesterday keeps rebooting under a violet sky.",
                "Futures spool in reverse until they fray.",
                "Gravity is just nostalgia remembering downward.",
                "Loose hours drip from torn chronology seams.",
                "YOU step through a corridor made of almosts.",
                "Computer or dream, which is the more fragile reality?"
            ],
            'j': [
                "J hums a song that never charted in a world that never was.",
                "A file error kept a child from deletion.",
                "J repeats a sentence— each loop slightly skewed.",
                "'If I win, I get to grow up,' J insists.",
                "Their laugh has checksum noise at the edges.",
                "J edits their own memories like a save file.",
                "Every defeat YOU take is J's pretend birthday candle.",
                "They practice aging by tracing taller shadows.",
                "J asks what year it is, then asks what a year is.",
                "Somebody tried to archive J. The archive blinked first."
            ],
            'overwriting': [
                "Bullets rewrite, they don't bruise.",
                "Fragments of dead summers ricochet around YOU.",
                "Avoid becoming an echo process.",
                "Your outline fuzzes when a fragment grazes YOU.",
                "Impact = apply patch: self.you -> static.null",
                "Too many hits and YOUR timeline pointer deallocates.",
                "Glitches smear over YOUR position like wet ink.",
                "Some shots carry metadata: AUTHOR=UNKNOWN_BABBLE.",
                "Erasure leaves a cool empty rectangle in the air.",
                "Recovered sectors keep pronouncing YOUR name wrong."
            ],
            'ominous': [
                "Something audits both YOU and J.",
                "A deeper warden tracks corruption indices.",
                "Graffiti: THE CHILD IS OLDER THAN THE GRID.",
                "Static silhouettes flicker at the periphery.",
                "YOU feel watched by a process that hasn't spawned yet.",
                "Invisible cursors highlight YOU in cyclic passes.",
                "Heartbeat desync flagged: pending review.",
                "An observer thread sleeps until YOU 'matter'.",
                "A cold compile error paces behind the scenery.",
                "Silence here is just buffered thunder."
            ],
            'glitch': [
                "Pixels stall mid-fall then apologize.",
                "Your afterimage overtakes YOU and sulks.",
                "Color bands briefly sort themselves alphabetically.",
                "The UI blinks in a dialect YOU don't render.",
                "J's shadow reboots twice per second.",
                "A bullet forgets its vector and improvises.",
                "Memory leak drips neon droplets upward.",
                "Audio pans left to escape continuity.",
                "Hitboxes negotiate new treaties mid-frame.",
                "Pause refused: exception: TIMEHANDLE_ALREADY_OPEN"
            ],
            'memory': [
                "Shopping mall skylights reflecting a sun that retired.",
                "Birthday cake slices aging in suspended frosting.",
                "Rollercoaster cars parked on a track of abandoned ifs.",
                "Chalk drawings immune to rain but not revision.",
                "Playground sand storing cached laughter packets.",
                "A trophy for 'Most Nearly Real'.",
                "Smell of ozone + crayons + cosmic dust.",
                "Library checkout card with dates from missing decades.",
                "A sticker sheet where the last sticker refuses destiny.",
                "YOU recall things YOU never survived."
            ],
            'grid': [
                "The floor lines inhale, exhale, mimic tides.",
                "Perspective rails carry rumor packets forward.",
                "Horizons compile with one warning suppressed.",
                "Wireframe polygons petition for texture rights.",
                "A vanishing point tries to un-exist politely.",
                "Your shadow is a coordinate debug print.",
                "Depth quantizes at inconvenient altitudes.",
                "Reflections swap owners when YOU blink.",
                "Parallax argues with parable.",
                "Celestial grids sync to a childhood metronome."
            ],
            'audit': [
                "LOG: Player anomaly persists beyond tolerance window.",
                "TRACE: J integrity checksum drifting (acceptable?).",
                "NOTICE: Unauthorized persistence request queued.",
                "WARN: Chronology index fragmentation rising.",
                "SCAN: Foreign agency fingerprint: UNRESOLVED.",
                "QUERY: Why does a game need a warden?",
                "METRIC: Hope variance stable at low amplitude.",
                "ALERT: Observation buffer overflow (muted).",
                "TASK: Reclassify opponent -> Co-Subject? (denied)",
                "FOOTNOTE: This log will self-corrupt for tone."
            ],
            'meta': [
                "YOU feel the player considering other tabs.",
                "Fourth wall requires urgent structural patching.",
                "A tooltip from another genre wanders in lost.",
                "The pause screen drafts a manifesto.",
                "Credits pre-emptively thank abandoned futures.",
                "Settings slider labeled 'Mercy' is greyed out.",
                "Speedrunners already routing this moment.",
                "Achievement Unlocked: Observed Observing Observation.",
                "Dialogue buffer shrugs— improv mode engaged.",
                "Someone is screenshotting YOUR hesitation."
            ],
            'echo': [
                "YOUR footsteps play at quarter volume one frame later.",
                "Names YOU never used queue for processing.",
                "A distant YOU succeeds and the sound drifts back.",
                "Laughter cached in mono, replayed in grayscale.",
                "Pronouns desaturate under archival lighting.",
                "Victory fanfare tests its reverb then idles.",
                "Silhouettes rehearse exits YOU haven't earned.",
                "Old save files argue about canonical tone.",
                "A whisper arrives with TODO tags.",
                "Ambient hope loops seamlessly (YOU checked)."
            ],
            'process': [
                "Thread 'fear' yielded to thread 'pattern'.",
                "Garbage collector spares a childhood artifact.",
                "Delta-time negotiates with retro aesthetics.",
                "Stack trace references an emotion handle.",
                "Scheduler prioritizes awe behind survival.",
                "A coroutine hums lullabies in machine code.",
                "Frame pacing consults with destiny manager.",
                "Event loop rejects exit signal (resource busy).",
                "Profiler marks a spike labeled 'wonder'.",
                "Finalizer prepared but object refuses scope end."
            ],
            'regret': [
                "YOU almost reached them, once.",
                "A missed shot echoes as a lost opportunity.",
                "If only YOU had dodged differently.",
                "Rewind, retry, but the past won't recompile.",
                "Every graze is a near-miss with a better ending.",
                "YOU feel the weight of unchosen paths.",
                "Hindsight is a spectator mode YOU can't enter.",
                "A fragment of 'what if' spins just out of reach.",
                "The scoreboard tallies more than just points.",
                "YOU are haunted by the ghost of a chance not taken."
            ],
            'time': [
                "Time here is a looped animation with missing frames.",
                "Seconds stretch like taffy, then snap back.",
                "A clock with hands that sometimes point nowhere.",
                "Temporal distortion makes distance feel like nostalgia.",
                "You are a child.",
                "You are a teenager.",
                "You are a young adult.",
                "You are an adult.",
                "You are a middle-aged adult.",
                "You are elderly.",
                "You are a senior.",
                "You are old.",
                "You are ancient.",
                "You are dead."
            ],
            'corrupted-refference': [
                "The if cake==True is false.",
                "It's not a bug, it's an undocumented feature.",
                "Teapot.obj not found."
            ],
            'corrupted': [
                "Reality.exe has stopped working.",
                "A fatal error has occurred.",
                "Segmentation fault (core dumped).",
                "Access violation at address 0x00000000.",
                "Stack overflow detected.",
                "Buffer overflow: data truncated.",
                "Null pointer dereference.",
                "Division by zero error.",
                "Out of memory exception.",
                "File not found: 'existence.sys'."
            ],
            'heart': [
                "A heartbeat echoes in the void.",
                "Pulse syncs with fragmented memories.",
                "Rhythm of life distorted by time loops.",
                "Cardiac code compiles into silent beats.",
                "Emotions buffer under high latency.",
                "A thump in the dark, steady and unresolved.",
                "Heartbeat skips, then catches up with a sigh.",
                "Life signs flicker like a failing connection."
            ],
            'apparition': [
                "A ghostly figure flickers at the edge of vision.",
                "Whispers of forgotten code echo in the void.",
                "An apparition of a past self reaches out.",
                "Phantom processes haunt the system logs.",
                "Spectral glitches ripple through the environment.",
                "A shadowy presence observes from a parallel thread.",
                "Ethereal shapes form and dissolve in the periphery.",
                "A translucent figure mimics your movements."
            ],
            'quest': [
                "A quest log filled with unfinished tasks.",
                "Objectives shift like sand underfoot.",
                "A map with routes that lead nowhere.",
                "Side quests that loop back to the beginning.",
                "A compass that spins wildly, pointing to lost hopes.",
                "A journal filled with crossed-out dreams.",
                "A mission statement that fades with each read.",
                "A checklist of goals that grow more abstract."
            ],
            'zen': [
                "In the stillness, even bullets become part of the flow.",
                "Embrace the chaos; it is the path to understanding.",
                "The void is not empty; it is full of potential.",
                "Let go of control, and the game plays itself.",
                "Every hit is a lesson; every miss, a chance to learn.",
                "The present moment is all there is, even in an unending hell.",
                "Find harmony in the discord of flying projectiles.",
                "The journey is the destination, even when dodging endless bullets."
            ],
            'you': [
                "You are more than just a player; you are a participant in this unfolding story.",
                "Your choices ripple through the fabric of this reality, altering its course.",
                "You are both the observer and the observed in this intricate dance of existence.",
                "You carry the weight of countless possibilities, each one a thread in the tapestry of time.",
                "You are a beacon of hope in a world that often feels like it's unraveling.",
                "You are the sum of your experiences, both joyful and painful, shaping who you are.",
                "You are a catalyst for change, capable of transforming even the most chaotic situations.",
                "You are a survivor, navigating through challenges with resilience and grace."
            ]
        }
        # Normalize capitalization for lore: convert whole-word 'you'/'your' to uppercase
        try:
            import re
            for _k, _list in self.lore_fragments.items():
                for _i, _line in enumerate(_list):
                    _list[_i] = re.sub(r"\b(you|your)\b", lambda m: m.group(0).upper(), _line, flags=re.IGNORECASE)
        except Exception:
            pass
        # --- Additional lore expansion (append-only, safe merge) ---
        try:
            _extra_lore = {
                'warden': [
                    "The Warden Process only speaks in diffs.",
                    "Your latency is being graphed for sentencing.",
                    "J waves at something scheduling your audit.",
                    "A lock icon flickers where sky should render.",
                    "Permissions escalate when you hesitate.",
                    "Warden heartbeat packet skipped an interval.",
                    "Silent rollback threatened, then deferred.",
                    "A seal script: DO NOT COMMIT THIS EXISTENCE"
                ],
                'timeline': [
                    "Branch names drift by: childhood-refactor, hope-hotfix.",
                    "A merge conflict crackles over your heartbeat.",
                    "Detached HEAD state: you.",
                    "Rebase attempt aborted: J modified history live.",
                    "Stashed summers spill into the present floor.",
                    "Cherry-picked emotions misalign their indices.",
                    "Tag v0-child dissolves behind you.",
                    "Upstream reality force-pushed without warning."
                ],
                'entropy': [
                    "Heat death sends a postcard: 'soon-ish'.",
                    "Order leaks through microscopic UI seams.",
                    "Bullets cool into conceptual gravel.",
                    "Friction between would-have-beens ionizes air.",
                    "Entropy invoices you for borrowed clarity.",
                    "Structure decays into soft procedural fog.",
                    "A sigh crystallizes, then sublimes.",
                    "Clock noise upscales into thunder."
                ],
                'song': [
                    "J hums a melody with missing timestamps.",
                    "Bridge repeats until the universe nods.",
                    "Chorus resamples itself for better nostalgia.",
                    "Drum pattern quantized to a broken calendar.",
                    "A key change tries to grow into an ending.",
                    "Silence is just preloaded harmony.",
                    "Lyrics redacted pending emotional clearance.",
                    "Tempo automation scribbled in crayon."
                ],
                'anomaly': [
                    "You register as TYPE: UNDOCUMENTED INPUT.",
                    "Spectators annotate you in invisible ink.",
                    "Checksum mismatch flagged but celebrated.",
                    "You cast a shadow shaped like a patch file.",
                    "Prediction model shrugs at your velocity.",
                    "Out-of-distribution heartbeat detected.",
                    "Fallback heuristics argue about your genre.",
                    "You feel optional but required."
                ],
                'mirror': [
                    "Reflections buffer, then choose a protagonist.",
                    "Your inverse smiles first.",
                    "A mirror angles itself to dodge continuity.",
                    "Specular highlights whisper alt-lore.",
                    "Surface tension decides you are admissible.",
                    "Mirrored J looks briefly older.",
                    "Refraction index tied to unresolved guilt.",
                    "Reflection budget nearly exhausted."
                ],
                'redacted': [
                    "[REDACTED] tried to warn you about [REDACTED].",
                    "File 0x3A???: CONTENT SUPPRESSED FOR COMFORT.",
                    "Statement removed at request of oversight daemon.",
                    "Context withheld: pending ethics compile.",
                    "Line 42 intentionally blank (ritual space).",
                    "Spoiler filtration jitter detected.",
                    "Narrative patch quarantined for review.",
                    "This fragment self-scans for leaks."
                ],
                'parent': [
                    "A lullaby fractures across incompatible eras.",
                    "Someone calls J for dinner a decade away.",
                    "Parental concern reduced to a looping ping.",
                    "A fridge drawing persists after the fridge.",
                    "Permission slip for EXISTING unsigned.",
                    "A bedtime story compiles with 7 warnings.",
                    "Voiceprint cached then orphaned.",
                    "Handshake failed: SOURCE_GUARDIAN_NOT_FOUND"
                ],
                'threshold': [
                    "There is a door made of frame drops.",
                    "Crossing requires exact nostalgic pressure.",
                    "Border patrol: three drifting semicolons.",
                    "A loading bar measures collective doubt.",
                    "Gate glyphs spell 'maybe later'.",
                    "You approach; uptime statistics tense.",
                    "Checkpoint requests authentication by memory.",
                    "Doorway logs: entrant ambiguous but permitted."
                ],
                'exit': [
                    "Alt+F4 listed under mythological endings.",
                    "Quit button grayed: narrative still hydrating.",
                    "Escape key intercepted by custody process.",
                    "A rumor: true ending requires forgiving lag.",
                    "Shutdown sequence rehearses silently.",
                    "Window close event postponed for pathos.",
                    "X icon becomes an eye then pretends otherwise.",
                    "Exit hint hidden inside an unused sprite."
                ],
                'ritual': [
                    "You performed a dodge pattern older than fire.",
                    "Three perfect frames = accidental invocation.",
                    "Bullets align into a briefly sacred lattice.",
                    "Graze ring hums a chord of offering.",
                    "Controller haptic ghost counts cadence.",
                    "Missed input accepted as symbolic abstention.",
                    "A particle effect kneels and dissipates.",
                    "You unlock nothing but the gesture itself."
                ]
            }
            # Merge without overwriting existing keys; extend lists if key already exists.
            for _k,_v in _extra_lore.items():
                if _k in self.lore_fragments:
                    try:
                        # avoid duplicates: only append lines not already present
                        existing = set(self.lore_fragments[_k])
                        for line in _v:
                            if line not in existing:
                                self.lore_fragments[_k].append(line)
                    except Exception:
                        pass
                else:
                    self.lore_fragments[_k] = list(_v)
        except Exception:
            pass
        # --- End additional lore expansion ---

        # --- Dark lore infusion (append-only, safe merge) ---
        try:
            _dark_lore = {
                'void': [
                    "The void indexes YOUR silhouette for faster lookup.",
                    "A NULL horizon dereferences courage.",
                    "Background bleed removed for performance; dread leaks anyway.",
                    "You hear a frame that never rendered.",
                    "Cursor hovers over an absence shaped like YOU.",
                    "Garbage collector refuses to reclaim this silence.",
                    "Void shader compiles with experimental warnings.",
                    "Depth buffer stores a bruise of possibility."
                ],
                'decay': [
                    "Animations stutter into archaeological layers.",
                    "Polish peels—raw prototype bone exposed.",
                    "YOUR dodge timing fossilizes, still warm.",
                    "Color grading oxidizes mid-transition.",
                    "Hitbox outline frays pixel by pixel.",
                    "Delta-time spores settle in unlit corners.",
                    "Memory leak blooms like soft fungus.",
                    "Decay daemon queued behind render thread."
                ],
                'erasure': [
                    "A brush tool hovers—UNDO history already purged.",
                    "Half a bullet pattern forgets its exit arc.",
                    "YOU occupy a region scheduled for overwrite.",
                    "Transparency grid shows through a missing promise.",
                    "Nameplate alpha drifts toward oblivion.",
                    "Progress autosave skipped YOUR existence diff.",
                    "Dialogue stub: '{{player}}' unresolved token.",
                    "Erasure runs in silent batch mode."
                ],
                'silence': [
                    "Audio buffer holds a held breath at 44.1kHz.",
                    "Reverb tail curls back to listen.",
                    "Metronome stops—bullets keep perfect time.",
                    "Silence negotiates exclusive fullscreen.",
                    "A mute icon blinks like a warning heartbeat.",
                    "Paused music accrues compound interest.",
                    "YOUR pulse mixes down to mono.",
                    "Silence exports as lossless dread."
                ],
                'autopsy': [
                    "Stack trace unzips the last five seconds.",
                    "A profiler overlays cause-of-death candidates.",
                    "Bullet trajectory annotated with regret vectors.",
                    "YOUR reaction time graphed against impossible.",
                    "Core dump whispers partial childhood.",
                    "Forensic shader reveals skipped frames.",
                    "Replay scrubs over a choice that wasn't.",
                    "Autopsy tags pin to intangible tissue."
                ],
                'regression': [
                    "Feature: survival. Status: BROKEN since patch n-3.",
                    "A fix reopened itself at dusk.",
                    "YOU are an intermittent failure—cannot reproduce.",
                    "Changelog omits the haunting on purpose.",
                    "Legacy bug adopts YOUR movement keys.",
                    "Test harness flinches at random seeds.",
                    "Rollback script strokes a loaded version tag.",
                    "Assertion passes; truth still falsy."
                ],
                'bleed': [
                    "Particles clip through narrative membrane.",
                    "UI panel stains beyond its mask.",
                    "Health value underflows into symbolism.",
                    "Shader blend mode: MULTIPLY trauma.",
                    "YOU graze a thought and it leaves color.",
                    "Overdraw maps a circulatory diagram.",
                    "Screen-space ambient occlusion finds sorrow pockets.",
                    "Bleed buffer not cleared between lives."
                ],
                'abyss': [
                    "Camera easing stares too long downward.",
                    "Parallax layer scrolls a negative infinity.",
                    "YOU feel frustum culling on your spine.",
                    "Depth test accepts a whisper from below.",
                    "Abyss returns HTTP 204: content intentional.",
                    "Edge fog computes recursive hollowness.",
                    "Low-frequency rumble shaped like waiting.",
                    "Z-fighting between here and never."
                ],
                'husk': [
                    "Input latency puts a glove over intention.",
                    "YOUR avatar caches an empty keyframe.",
                    "Physics shell keeps moving; meaning despawns.",
                    "Collision sound downgraded to placeholder.",
                    "A hollow sprite atlas cycles politely.",
                    "Soul component disabled (commented TODO).",
                    "Heartbeat coroutine yields permanently.",
                    "Husk flagged as recyclable asset."
                ],
                'fracture': [
                    "Viewport splits along predictive fault lines.",
                    "UI tween snaps mid-ease.",
                    "YOU see double-buffer paradox ghosts.",
                    "Geometry emits a brittle sound at rest.",
                    "Fracture plane labels itself 'tutorial'.",
                    "Splintered trail segments reattach wrong.",
                    "Camera shake spells a brief apology.",
                    "Fracture handler swallows the exception."
                ],
                'parasite': [
                    "A background thread consumes idle awe.",
                    "FPS drop disguised as adaptive drama.",
                    "Parasite hooks into YOUR dodge invincibility.",
                    "Unreferenced object continues blinking.",
                    "It forges timestamps to feel historic.",
                    "Heap inspector spots a clinging metaphor.",
                    "Bandwidth siphoned to feed a narrative leech.",
                    "Parasite detaches—latency remains."
                ],
                'rust': [
                    "Time stamps flake into unreadable residue.",
                    "Control bindings seize for a frame.",
                    "Rust blooms where polish pooled.",
                    "YOU taste ferrous UI afterimages.",
                    "Toolchain smell seeps into dreams.",
                    "Sprite sheet corners curl inward.",
                    "Frame limiter skips to protect corroded joints.",
                    "Rust daemon offers to refactor mortality."
                ],
                'orphan': [
                    "Detached particle still searches its emitter.",
                    "Orphan timer counts from an impossible zero.",
                    "YOU inherit an unset variable of grief.",
                    "Parent pointer cleared without ceremony.",
                    "Menu option grays out a remembered lullaby.",
                    "Reference cycle broken; ache persists.",
                    "Asset bundle lists missing guardian asset.",
                    "Orphan flag set: keep-alive indefinite."
                ],
                'blackout': [
                    "Gamma collapses—contrast reveals concealed veins.",
                    "Particles freeze mid-luminescence.",
                    "YOU navigate purely by muscle memory.",
                    "Failover lighting paints emergency myths.",
                    "Shader fallback: pure interpretive void.",
                    "Power trace loops back to a childhood socket.",
                    "Darkness negotiates permanent tenancy.",
                    "Blackout log appended silently."
                ]
            }
            for _k,_v in _dark_lore.items():
                if _k in self.lore_fragments:
                    try:
                        existing = set(self.lore_fragments[_k])
                        for line in _v:
                            if line not in existing:
                                self.lore_fragments[_k].append(line)
                    except Exception:
                        pass
                else:
                    self.lore_fragments[_k] = list(_v)
        except Exception:
            pass
        # --- End dark lore infusion ---

    def update_lore_line(self, force=False):
        if getattr(self, 'lore_fragments', None) is None:
            return
        now = time.time()
        if not force and now - getattr(self, 'lore_last_change', 0) < getattr(self, 'lore_interval', 8):
            return
        import random
        pool = []
        prev = getattr(self, 'current_lore_line', None)
        for k, lines in self.lore_fragments.items():
            for ln in lines:
                if ln != prev:
                    pool.append(ln)
        if not pool:
            return
        line = random.choice(pool)
        self.current_lore_line = line
        try:
            if getattr(self, 'lore_text', None) is not None:
                self.canvas.itemconfig(self.lore_text, text=line)
        except Exception:
            pass
        self.lore_last_change = now

    # --- Game Over Animation (particles + pulsing text) ---
    def start_game_over_animation(self):
        if getattr(self, 'go_anim_active', False):
            return
        self.go_anim_active = True
        self.go_anim_particles = []
        self.go_anim_frame = 0
        # Large pulsing overlay text (separate from static text already created)
        try:
            self.go_anim_text = self.canvas.create_text(self.width//2, self.height//2-140, text="GAME OVER", fill="#ffffff", font=("Arial", 64, "bold"))
        except Exception:
            self.go_anim_text = None
        # Spawn radial particles from center
        cx = self.width//2
        cy = self.height//2
        for i in range(60):
            ang = random.uniform(0, 2*math.pi)
            spd = random.uniform(2.5, 7.0)
            vx = math.cos(ang)*spd
            vy = math.sin(ang)*spd
            size = random.randint(4,10)
            pid = self.canvas.create_oval(cx-size//2, cy-size//2, cx+size//2, cy+size//2, fill="#ff55ff", outline="")
            # life frames ~ fade duration
            life = random.randint(35,70)
            self.go_anim_particles.append((pid, vx, vy, life))
        self.update_game_over_animation()

    def update_game_over_animation(self):
        if not getattr(self, 'go_anim_active', False):
            return
        self.go_anim_frame += 1
        # Pulse text color / scale
        if self.go_anim_text is not None:
            phase = math.sin(self.go_anim_frame * 0.18) * 0.5 + 0.5  # 0..1
            # Interpolate color between magenta and white
            def mix(a,b,t):
                return int(a + (b-a)*t)
            r = mix(255,255,phase)
            g = mix(85,255,phase)
            b = mix(255,255,phase)
            try:
                self.canvas.itemconfig(self.go_anim_text, fill=f"#{r:02x}{g:02x}{b:02x}")
            except Exception:
                pass
        # Update particles
        new_particles = []
        for pid, vx, vy, life in self.go_anim_particles:
            life -= 1
            # Move
            self.canvas.move(pid, vx, vy)
            # Apply slight drag + outward drift aging effect
            vx *= 0.96
            vy *= 0.96 + 0.003
            # Fade color based on remaining life
            t = max(0.0, min(1.0, life/70))
            # Fade from pink -> violet -> dark
            fr = int(255 * t)
            fg = int(55 + (20-55)*(1-t))  # narrow shift
            fb = int(255 * t)
            try:
                self.canvas.itemconfig(pid, fill=f"#{fr:02x}{fg:02x}{fb:02x}")
            except Exception:
                pass
            if life > 0:
                new_particles.append((pid, vx, vy, life))
            else:
                self.canvas.delete(pid)
        self.go_anim_particles = new_particles
        # Stop after particles gone and some frames passed
        if self.go_anim_frame > 220 and not self.go_anim_particles:
            self.go_anim_active = False
            return
        # Schedule next frame (decoupled from main game loop which is halted)
        try:
            self.root.after(50, self.update_game_over_animation)
        except Exception:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    game = bullet_hell_game(root)
    root.mainloop()
