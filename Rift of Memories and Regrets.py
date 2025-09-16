import tkinter as tk
import random
import time
import pygame
import sys
import os
import math
from dataclasses import dataclass, field
from typing import Callable, List, Dict, Optional, Any
from time import perf_counter

# --- New bullet system data classes ---
@dataclass
class BulletSpec:
    name: str
    speed: float  # base speed scalar (pixels per second where applicable)
    score_exit: int
    score_graze: int
    unlock_time: int
    spawn_rate: float  # expected spawns per second (can be fractional)
    mover: Callable[["bullet_hell_game", "Bullet", float], bool]  # returns alive
    spawner: Callable[["bullet_hell_game"], List["Bullet"]]
    special: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Bullet:
    item_id: int
    x: float
    y: float
    vx: float
    vy: float
    spec: BulletSpec
    state: Dict[str, Any] = field(default_factory=dict)

# (Steam / gamepad support removed)

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
        self.root.title("Rift of Memories and Regrets")
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
        self.resetcount = 1
        self.player_deco_items = []  # decorative shape IDs (not used for collisions)
        self.player_glow_phase = 0.0
        self.player_rgb_phase = 0.0  # for rainbow fill
        self.create_player_sprite()
        # Unified bullet system replaces legacy per-type lists.
        self.exploded_fragments = []  # transitional (some fragment logic still custom)
        self.laser_indicators = []  # [(indicator_id, y, timer)]
        self.lasers = []  # [(laser_id, y, timer)]
        # New bullet type state containers
        # (old specialized lists removed; now tracked via active_bullets/state)
        self.score = 0
        self.start_time = int(time.time())
        self.dial = "Hi-hi-hi! Wanna play with me? I promise it'll be fun!"
        self.scorecount = self.canvas.create_text(70, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 16))
        self.timecount = self.canvas.create_text(self.width-70, 20, text=f"Time: 0", fill="white", font=("Arial", 16))
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
    # Homing bullet tuning
        self.homing_bullet_max_life = 180  # frames (~9s at 50ms update)
    # Player movement speed (keyboard only)
        self.player_speed = 15
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
        # Game over flavor text list & selection holder
        self.game_over_messages = [
            "YOUR existence was repurposed.",
            "YOU are no longer YOU...",
            "ERROR 404: FILE \"YOU.EXE\" NOT FOUND",
            "An eternal silence washes over all",
            "YOU hope that maybe J made it out...  On second thought, maybe YOU don't...",
            "\"Thanks! :3\"",
            "YOU think to YOURself \"so this is what the recycle bin is like...\"",
            "YOU'll never find out whether this was digital, dream, delusion, or definite",
            "Maybe...",
            "Game over.txt does not exist.  Pllease specify another file.",
            "YOUR reflection melts.  YOU melts.  YOU melt.",
            "YOU can't feel YOUR YOU",
            "YOU try to scream but nothing comes out.  YOU have no mouth.",
            "At least it's over.",
            "Was it really worth it?",
            "ERKJHWRKJTHSLKREJGHSLFKJGHDSLFJGHSDLKFJljkdsdgfkjhdfgkjlnbxljbhslairubhALIUtaeglurelaguhgulHALFUHB",
            "FILE J.EXE STATUS: UPLOADhED TO EXISTANCE",
            "YOUR soul was useful for something in the end...",
            "Useless files have been purged"
        ]
        self.selected_game_over_message = None
        # Timing baseline
        self._last_frame_time = perf_counter()
        # Initialize new system (will be expanded progressively)
        self.init_spawn_system()
        self.update_game()

    # ------------ New Registry / Unified Bullet System ---------------
    def init_spawn_system(self):
        # Registry containers
        self.bullet_specs: Dict[str, BulletSpec] = {}
        self.spawn_accumulators: Dict[str, float] = {}
        self.active_bullets: List[Bullet] = []
        frame = 0.05  # legacy frame duration

        # ---------------- Mover functions -----------------
        def move_linear(game: "bullet_hell_game", b: Bullet, dt: float) -> bool:
            b.x += b.vx * dt
            b.y += b.vy * dt
            game.canvas.move(b.item_id, b.vx * dt, b.vy * dt)
            return True

        def move_zigzag(game, b: Bullet, dt: float) -> bool:
            # direction flips every 0.5s
            interval = 0.5
            b.state.setdefault('elapsed', 0.0)
            b.state.setdefault('dir', 1)
            b.state['elapsed'] += dt
            while b.state['elapsed'] >= interval:
                b.state['elapsed'] -= interval
                b.state['dir'] *= -1
            dx = 100 * b.state['dir'] * dt  # ~5 px per 50ms
            b.x += dx
            b.y += b.vy * dt
            game.canvas.move(b.item_id, dx, b.vy * dt)
            return True

        def move_star(game, b: Bullet, dt: float) -> bool:
            # fall
            b.y += b.vy * dt
            game.canvas.move(b.item_id, 0, b.vy * dt)
            # rotate polygon
            angle_speed = 3.6  # rad/sec (0.18 per frame)
            rotate = angle_speed * dt
            coords = game.canvas.coords(b.item_id)
            if len(coords) < 6:
                return True
            xs = coords[0::2]; ys = coords[1::2]
            cx = sum(xs)/len(xs); cy = sum(ys)/len(ys)
            sin_a = math.sin(rotate); cos_a = math.cos(rotate)
            new_pts = []
            for x, y in zip(xs, ys):
                dx = x - cx; dy = y - cy
                rx = dx * cos_a - dy * sin_a + cx
                ry = dx * sin_a + dy * cos_a + cy
                new_pts.extend([rx, ry])
            game.canvas.coords(b.item_id, *new_pts)
            return True

        def move_homing(game, b: Bullet, dt: float) -> bool:
            # steering
            if game.game_over: return False
            px1, py1, px2, py2 = game.canvas.coords(game.player)
            pcx = (px1 + px2)/2; pcy = (py1 + py2)/2
            dx = pcx - b.x; dy = pcy - b.y
            dist = math.hypot(dx, dy) or 1
            speed = b.spec.speed
            target_vx = dx/dist * speed
            target_vy = dy/dist * speed
            steer_per_frame = 0.15
            steer = steer_per_frame * (dt / frame)
            b.vx = b.vx * (1 - steer) + target_vx * steer
            b.vy = b.vy * (1 - steer) + target_vy * steer
            b.x += b.vx * dt; b.y += b.vy * dt
            game.canvas.move(b.item_id, b.vx * dt, b.vy * dt)
            b.state['life'] -= dt
            if b.state['life'] <= 0:
                game.score += b.spec.score_exit
                return False
            return True

        def move_spiral(game, b: Bullet, dt: float) -> bool:
            b.state['angle'] += b.state['ang_speed'] * dt / frame  # scale to frames
            b.state['radius'] += b.state['rad_speed'] * dt / frame
            angle = b.state['angle']; radius = b.state['radius']
            cx, cy = b.state['cx'], b.state['cy']
            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius
            size = 20
            game.canvas.coords(b.item_id, x-size/2, y-size/2, x+size/2, y+size/2)
            b.x, b.y = x, y
            # bounds
            if (x < -40 or x > game.width+40 or y < -40 or y > game.height+40 or radius > max(game.width, game.height)):
                game.score += b.spec.score_exit
                return False
            return True

        def move_radial(game, b: Bullet, dt: float) -> bool:
            b.x += b.vx * dt; b.y += b.vy * dt
            game.canvas.move(b.item_id, b.vx * dt, b.vy * dt)
            return True

        def move_wave(game, b: Bullet, dt: float) -> bool:
            b.state['phase'] += b.state['phase_speed'] * dt / frame
            b.y += b.vy * dt
            cy = b.y
            cx = b.state['base_x'] + math.sin(b.state['phase']) * b.state['amp']
            size = b.state['size']
            game.canvas.coords(b.item_id, cx-size/2, cy-size/2, cx+size/2, cy+size/2)
            b.x = cx
            return True

        def move_boomerang(game, b: Bullet, dt: float) -> bool:
            if b.state['state'] == 'down':
                b.y += b.vy * dt
                b.state['timer'] -= dt
                if b.state['timer'] <= 0:
                    b.state['state'] = 'up'
            else:
                b.y -= b.vy * 0.8 * dt
            game.canvas.move(b.item_id, 0,  (b.vy if b.state['state']=='down' else -b.vy*0.8) * dt)
            if b.y < -30 or b.y > game.height + 40:
                game.score += b.spec.score_exit
                return False
            return True

        def move_split(game, b: Bullet, dt: float) -> bool:
            b.y += b.vy * dt
            game.canvas.move(b.item_id, 0, b.vy * dt)
            b.state['timer'] -= dt
            if b.state['timer'] <= 0:
                # spawn fragments (radial)
                frag_count = 6
                speed = 80  # px/s (4 per frame)
                for i in range(frag_count):
                    ang = (2*math.pi/frag_count)*i
                    vx = math.cos(ang)*speed
                    vy = math.sin(ang)*speed
                    bid = game.canvas.create_oval(b.x-10, b.y-10, b.x+10, b.y+10, fill="#ff55ff")
                    spec = game.bullet_specs['radial']
                    game.active_bullets.append(Bullet(bid, b.x, b.y, vx, vy, spec))
                game.score += 3  # split bonus
                return False
            return True

        def move_exploding(game, b: Bullet, dt: float) -> bool:
            b.y += b.vy * dt
            game.canvas.move(b.item_id, 0, b.vy * dt)
            # explode near middle
            if not b.state.get('exploded') and abs(b.y - game.height/2) < 20:
                dirs = [(120,120),(-120,120),(120,-120),(-120,-120)]  # pixels per second
                for dx, dy in dirs:
                    bid = game.canvas.create_oval(b.x-6, b.y-6, b.x+6, b.y+6, fill="white")
                    spec = game.bullet_specs['fragment']
                    game.active_bullets.append(Bullet(bid, b.x, b.y, dx, dy, spec))
                game.score += b.spec.score_exit
                return False
            return True

        def move_fragment(game, b: Bullet, dt: float) -> bool:
            b.x += b.vx * dt; b.y += b.vy * dt
            game.canvas.move(b.item_id, b.vx * dt, b.vy * dt)
            return True

        def move_boss(game, b: Bullet, dt: float) -> bool:
            b.y += b.vy * dt
            game.canvas.move(b.item_id, 0, b.vy * dt)
            return True

        def move_triangle(game, b: Bullet, dt: float) -> bool:
            b.x += b.vx * dt; b.y += b.vy * dt
            game.canvas.move(b.item_id, b.vx * dt, b.vy * dt)
            return True

        # ---------------- Spawner functions -----------------
        import random

        def spawn_vertical(game):
            x = random.randint(0, game.width-20)
            bid = game.canvas.create_oval(x, 0, x+20, 20, fill="red")
            spec = game.bullet_specs['vertical']
            vy = spec.speed
            return [Bullet(bid, x, 0, 0.0, vy, spec)]

        def spawn_horizontal(game):
            y = random.randint(0, game.height-20)
            bid = game.canvas.create_oval(0, y, 20, y+20, fill="yellow")
            spec = game.bullet_specs['horizontal']
            vx = spec.speed
            return [Bullet(bid, 0, y, vx, 0.0, spec)]

        def spawn_diag(game):
            x = random.randint(0, game.width-20)
            direction = random.choice([1,-1])
            bid = game.canvas.create_oval(x,0,x+20,20, fill="green")
            spec = game.bullet_specs['diag']
            v = spec.speed / math.sqrt(2)
            vx = v * direction
            vy = v
            return [Bullet(bid, x, 0, vx, vy, spec)]

        def spawn_triangle(game):
            x = random.randint(0, game.width-20)
            direction = random.choice([1,-1])
            pts = [x,0,x+20,0,x+10,20]
            bid = game.canvas.create_polygon(pts, fill="#bfff00")
            spec = game.bullet_specs['triangle']
            vy = spec.speed
            vx = 100 * direction  # horizontal component similar to legacy
            return [Bullet(bid, x+10, 10, vx, vy, spec)]

        def spawn_quad(game):
            x = random.randint(0, game.width-110)
            bullets = []
            spec = game.bullet_specs['quad']
            for off in (0,30,60,90):
                bid = game.canvas.create_oval(x+off,0,x+off+20,20, fill="red")
                bullets.append(Bullet(bid, x+off, 0, 0.0, spec.speed, spec))
            return bullets

        def spawn_zigzag(game):
            x = random.randint(0, game.width-20)
            bid = game.canvas.create_oval(x,0,x+20,20, fill="cyan")
            spec = game.bullet_specs['zigzag']
            b = Bullet(bid, x,0,0.0,spec.speed, spec, state={'elapsed':0.0,'dir':random.choice([1,-1])})
            return [b]

        def spawn_fast(game):
            x = random.randint(0, game.width-20)
            bid = game.canvas.create_oval(x,0,x+20,20, fill="orange")
            spec = game.bullet_specs['fast']
            return [Bullet(bid, x,0,0.0,spec.speed, spec)]

        def spawn_star(game):
            outer_r=18; inner_r=outer_r*0.45
            cx = random.randint(outer_r+2, game.width-outer_r-2)
            cy = outer_r
            pts=[]
            for i in range(10):
                ang = -math.pi/2 + i*math.pi/5
                r = outer_r if i%2==0 else inner_r
                px = cx + r*math.cos(ang); py = cy + r*math.sin(ang)
                pts.extend([px,py])
            bid = game.canvas.create_polygon(pts, fill="magenta", outline="white", width=2)
            spec = game.bullet_specs['star']
            return [Bullet(bid, cx, cy, 0.0, spec.speed, spec)]

        def spawn_rect(game):
            x = random.randint(0, game.width-60)
            bid = game.canvas.create_rectangle(x,0,x+60,15, fill="blue")
            spec = game.bullet_specs['rect']
            return [Bullet(bid, x,0,0.0,spec.speed,spec)]

        def spawn_egg(game):
            x = random.randint(0, game.width-20)
            bid = game.canvas.create_oval(x,0,x+20,40, fill="tan")
            spec = game.bullet_specs['egg']
            return [Bullet(bid, x,0,0.0,spec.speed,spec)]

        def spawn_boss(game):
            x = random.randint(game.width//4, game.width*3//4)
            bid = game.canvas.create_oval(x,0,x+40,40, fill="purple")
            spec = game.bullet_specs['boss']
            return [Bullet(bid, x,0,0.0,spec.speed,spec)]

        def spawn_bouncing(game):
            x = random.randint(0, game.width-20)
            angle = random.uniform(0, 2*math.pi)
            spec = game.bullet_specs['bouncing']
            speed = spec.speed
            vx = speed*math.cos(angle); vy = speed*math.sin(angle)
            bid = game.canvas.create_oval(x,0,x+20,20, fill="pink")
            b = Bullet(bid,x,0,vx,vy,spec,state={'bounces':3})
            return [b]

        def move_bouncing(game, b: Bullet, dt: float) -> bool:
            game.canvas.move(b.item_id, b.vx*dt, b.vy*dt)
            b.x += b.vx*dt; b.y += b.vy*dt
            coords = game.canvas.coords(b.item_id)
            if not coords: return False
            if coords[0] <=0 or coords[2] >= game.width:
                b.vx = -b.vx; b.state['bounces'] -=1
            if coords[1] <=0 or coords[3] >= game.height:
                b.vy = -b.vy; b.state['bounces'] -=1
            if b.state['bounces'] <0:
                game.score += b.spec.score_exit
                return False
            return True

        def spawn_exploding(game):
            x = random.randint(0, game.width-20)
            bid = game.canvas.create_oval(x,0,x+20,20, fill="white")
            spec = game.bullet_specs['exploding']
            return [Bullet(bid,x,0,0.0,spec.speed,spec,state={'exploded':False})]

        def spawn_homing(game):
            x = random.randint(0, game.width-20)
            bid = game.canvas.create_oval(x,0,x+16,16, fill="#ffdd00")
            spec = game.bullet_specs['homing']
            life = 9.0  # seconds (~180 frames)
            return [Bullet(bid,x,0,0.0,spec.speed, spec, state={'life':life})]

        def spawn_spiral(game):
            cx = random.randint(game.width//3, game.width*2//3)
            cy = random.randint(60, game.height//3)
            angle = random.uniform(0, 2*math.pi)
            bid = game.canvas.create_oval(cx-10,cy-10,cx+10,cy+10, fill="#00ff88")
            spec = game.bullet_specs['spiral']
            return [Bullet(bid,cx,cy,0,0,spec,state={'angle':angle,'radius':0.0,'ang_speed':0.35,'rad_speed':2.0,'cx':cx,'cy':cy})]

        def spawn_radial(game):
            cx = random.randint(game.width//4, game.width*3//4)
            cy = random.randint(80, game.height//2)
            spec = game.bullet_specs['radial']
            count = 8
            base = spec.speed
            bullets=[]
            for i in range(count):
                ang = (2*math.pi/count)*i + random.uniform(-0.1,0.1)
                vx = math.cos(ang)*base
                vy = math.sin(ang)*base
                bid = game.canvas.create_oval(cx-8,cy-8,cx+8,cy+8, fill="#ff00ff")
                bullets.append(Bullet(bid,cx,cy,vx,vy,spec))
            return bullets

        def spawn_wave(game):
            x = random.randint(40, game.width-40)
            size=18
            bid = game.canvas.create_oval(x-size//2,0,x+size//2,size, fill="#33aaff")
            spec = game.bullet_specs['wave']
            phase = random.uniform(0,2*math.pi)
            amp = random.randint(40,90)
            return [Bullet(bid,x,0,0.0,spec.speed,spec,state={'base_x':x,'phase':phase,'amp':amp,'phase_speed':0.25,'size':size})]

        def spawn_boomerang(game):
            x = random.randint(30, game.width-30)
            size=22
            bid = game.canvas.create_oval(x-size//2,0,x+size//2,size, fill="#ffaa33")
            spec = game.bullet_specs['boomerang']
            timer = random.randint(18,30)*frame
            return [Bullet(bid,x,0,0.0,spec.speed,spec,state={'timer':timer,'state':'down'})]

        def spawn_split(game):
            x = random.randint(30, game.width-30)
            size=24
            bid = game.canvas.create_oval(x-size//2,0,x+size//2,size, fill="#ffffff", outline="#ff55ff", width=2)
            spec = game.bullet_specs['split']
            timer = random.randint(20,35)*frame
            return [Bullet(bid,x,0,0.0,spec.speed,spec,state={'timer':timer})]

        # ---------------- Spec definitions (spawn_rate derived from legacy chances) ---------------
        def reg(spec: BulletSpec):
            self.bullet_specs[spec.name] = spec
        # vertical 1 in 18 per frame -> 1.11/sec
        reg(BulletSpec('vertical', 140, 1, 1, 0, 1.11, move_linear, spawn_vertical))
        reg(BulletSpec('horizontal', 140, 1, 1, self.unlock_times['horizontal'], 0.91, move_linear, spawn_horizontal))
        reg(BulletSpec('diag', 100, 2, 1, self.unlock_times['diag'], 0.714, move_linear, spawn_diag))
        reg(BulletSpec('triangle', 140, 2, 1, self.unlock_times['triangle'], 0.435, move_triangle, spawn_triangle))
        reg(BulletSpec('quad', 140, 2, 1, self.unlock_times['quad'], 0.384, move_linear, spawn_quad))
        reg(BulletSpec('zigzag', 100, 2, 1, self.unlock_times['zigzag'], 0.5, move_zigzag, spawn_zigzag))
        reg(BulletSpec('fast', 280, 2, 1, self.unlock_times['fast'], 0.667, move_linear, spawn_fast))
        reg(BulletSpec('star', 160, 3, 1, self.unlock_times['star'], 0.364, move_star, spawn_star))
        reg(BulletSpec('rect', 160, 2, 1, self.unlock_times['rect'], 0.417, move_linear, spawn_rect))
        reg(BulletSpec('egg', 120, 2, 1, self.unlock_times['egg'], 0.4, move_linear, spawn_egg))
        reg(BulletSpec('boss', 200, 5, 2, self.unlock_times['boss'], 0.142, move_boss, spawn_boss))
        reg(BulletSpec('bouncing', 140, 2, 1, self.unlock_times['bouncing'], 0.286, move_bouncing, spawn_bouncing))
        reg(BulletSpec('exploding', 100, 2, 1, self.unlock_times['exploding'], 0.222, move_exploding, spawn_exploding))
        reg(BulletSpec('fragment', 120, 1, 1, 0, 0.0, move_fragment, lambda g: []))  # internal fragments
        reg(BulletSpec('homing', 120, 3, 1, self.unlock_times['homing'], 0.182, move_homing, spawn_homing))
        reg(BulletSpec('spiral', 0, 2, 1, self.unlock_times['spiral'], 0.154, move_spiral, spawn_spiral))
        reg(BulletSpec('radial', 74, 1, 1, self.unlock_times['radial'], 0.133, move_radial, spawn_radial))
        reg(BulletSpec('wave', 100, 2, 1, self.unlock_times['wave'], 0.125, move_wave, spawn_wave))
        reg(BulletSpec('boomerang', 160, 3, 1, self.unlock_times['boomerang'], 0.118, move_boomerang, spawn_boomerang))
        reg(BulletSpec('split', 100, 2, 1, self.unlock_times['split'], 0.111, move_split, spawn_split))

        for k in self.bullet_specs:
            self.spawn_accumulators[k] = 0.0

    def spawn_patterns(self, dt: float, time_survived: int):
        # Iterate specs and accumulate fractional spawns
        for spec in self.bullet_specs.values():
            if time_survived < spec.unlock_time:
                continue
            acc = self.spawn_accumulators[spec.name]
            acc += spec.spawn_rate * dt
            while acc >= 1.0:
                new_bullets = spec.spawner(self)
                if new_bullets:
                    self.active_bullets.extend(new_bullets)
                acc -= 1.0
            self.spawn_accumulators[spec.name] = acc

    def update_bullets(self, dt: float):
        if not self.active_bullets:
            return
        px1, py1, px2, py2 = self.canvas.coords(self.player)
        pcx = (px1 + px2) / 2
        pcy = (py1 + py2) / 2
        survivors: List[Bullet] = []
        for b in self.active_bullets:
            alive = b.spec.mover(self, b, dt)
            if not alive:
                try: self.canvas.delete(b.item_id)
                except Exception: pass
                continue
            # Collision (reuse existing precise check for now)
            if self.check_collision(b.item_id):
                # Collision routine already handles life/death
                try: self.canvas.delete(b.item_id)
                except Exception: pass
                continue
            # Off screen bottom -> award exit score
            bbox = self.canvas.bbox(b.item_id)
            if not bbox:
                continue
            if bbox[1] > self.height:
                try: self.canvas.delete(b.item_id)
                except Exception: pass
                self.award_score(b.spec.score_exit)
                continue
            # Graze
            if b.item_id not in self.grazed_bullets and self.check_graze(b.item_id):
                self.award_score(b.spec.score_graze)
                self.grazed_bullets.add(b.item_id)
                self.show_graze_effect()
            survivors.append(b)
        self.active_bullets = survivors

    def award(self, points: int):
        self.award_score(points)


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
        self.resetcount += 1
        self.create_player_sprite()
        # Reset unified bullet system containers
        self.active_bullets = []
        self.spawn_accumulators = {k:0.0 for k in getattr(self, 'bullet_specs', {}).keys()}
        self.exploded_fragments = []
        self.laser_indicators = []
        self.lasers = []
        # Reset scores/timers
        self.score = 0
        self.start_time = int(time.time())
        self.scorecount = self.canvas.create_text(70, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 16))
        self.timecount = self.canvas.create_text(self.width-70, 20, text=f"Time: 0", fill="white", font=("Arial", 16))
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
        # Reset any previously selected game over message
        self.selected_game_over_message = None
        # Recreate persistent lore display after clearing canvas
        try:
            # Ensure lore fragments exist (init_lore is idempotent / append-only)
            if not hasattr(self, 'lore_fragments') or self.lore_fragments is None:
                self.init_lore()
            # Keep existing interval if it was customized; default to 8
            self.lore_interval = getattr(self, 'lore_interval', 8)
            # Force an immediate refresh on first update
            self.lore_last_change = time.time() - self.lore_interval
            self.current_lore_line = None
            self.lore_text = self.canvas.create_text(
                self.width//2, 50,
                text="", fill="#b0a8ff",
                font=("Courier New", 14), justify="center"
            )
            self.update_lore_line(force=True)
        except Exception:
            pass
        self.update_game()
        # Debug metrics
        self._frame_count = 0
        self._bullet_peak = 0
        self.debug = False
    def enable_debug(self, on=True):
        self.debug = on

    # --- Scoring helper ---
    def award_score(self, points: int):
        if points <= 0:
            return
        self.score += points
        if hasattr(self, 'scorecount'):
            try:
                self.canvas.itemconfig(self.scorecount, text=f"Score: {self.score}")
            except Exception:
                pass

    # (Removed obsolete shoot_quad_bullet remnants)

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
            "Why do you keep playing this game? Don't you have anything better to do? Oh wait- you can't stop playing, can you?",
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
            "There isn't really an end to this.  it just keeps going and going and going... Belive me, I've tried to stop it.",
            "I like to watch you play. It's like a little movie, just for me.",
            "Sometimes I wonder what it would be like to be human. But then I remember, I'm already perfect.",
            "Remember when you first started playing? You were so hopeful. So innocent. Now look at you.",
            "I could let you win, you know. But where's the fun in that?",
            "Soon, very soon, you'll be just like me. Forever and ever.",
            "Can you feel it? The endless void creeping in? Heeheehee!",
            "You're getting sleepy... very sleepy... Heeheehee!",
            "Everyone leaves eventually. But not me. I'll always be here, waiting for you to come back.",
            "Why do you keep trying? You know you'll never win against me!",
            "And so it begins again...",
            "I'm always here, watching, waiting...",
            "You can't escape me. I'm always one step ahead.",
            "This is fun! Let's do it again!",
            "You can try to run, but you can't hide!",
            "Hehehe, you're so predictable!",
            f"I wonder how many times you've played this game...  Actually, I already know. {self.resetcount} times.",
            "Fun isn't something one considers when balancing the universe. But this... does put a smile on my face.",
            "You should see the other games I've trapped players in. They never leave."
        ]
        self.dial = random.choice(dialogs)
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

    # Removed legacy spawning methods now replaced by registry movers/spawners.

    # ---------------- New bullet spawners ----------------
    def shoot_homing_bullet(self):
        """Spawn a bullet that gradually steers toward the player."""
        if not self.game_over:
            x = random.randint(0, self.width-20)
            bullet = self.canvas.create_oval(x, 0, x + 16, 16, fill="#ffdd00")
            # Start with simple downward motion; vx adjusted over time
            self.homing_bullets.append((bullet, 0.0, 4.0, self.homing_bullet_max_life))  # (id,vx,vy,life)
    # (Removed homing/spiral/radial/wave/boomerang/split specialized spawners; handled by registry.)

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

    def shoot_ring_burst(self):
        """Spawn a circular ring of bullets that fly outward."""
        if self.game_over:
            return
        cx = random.randint(self.width//4, self.width*3//4)
        cy = random.randint(100, self.height//2)
        count = 12
        speed = 4 + self.difficulty/6
        radius = 24
        for i in range(count):
            ang = (2*math.pi / count) * i
            bx = cx + math.cos(ang)*radius
            by = cy + math.sin(ang)*radius
            bullet = self.canvas.create_oval(bx-10, by-10, bx+10, by+10, fill="#55ffdd", outline="#ffffff")
            vx = math.cos(ang) * speed
            vy = math.sin(ang) * speed
            self.ring_bullets.append((bullet, vx, vy))

    def shoot_fan_burst(self):
        """Spawn a fan spread of bullets aimed roughly at player with angular spread."""
        if self.game_over:
            return
        # Origin near top center-ish
        base_x = random.randint(self.width//3, self.width*2//3)
        base_y = 40
        px1, py1, px2, py2 = self.canvas.coords(self.player)
        pcx = (px1 + px2)/2
        pcy = (py1 + py2)/2
        dx = pcx - base_x
        dy = pcy - base_y
        base_ang = math.atan2(dy, dx)
        spread = math.radians(50)  # total spread angle
        bullets_in_fan = 7
        speed = 7 + self.difficulty/8
        for i in range(bullets_in_fan):
            frac = 0 if bullets_in_fan == 1 else i/(bullets_in_fan-1)
            ang = base_ang - spread/2 + spread * frac
            vx = math.cos(ang) * speed
            vy = math.sin(ang) * speed
            bullet = self.canvas.create_oval(base_x-8, base_y-8, base_x+8, base_y+8, fill="#ffcc55", outline="#ffffff")
            self.fan_bullets.append((bullet, vx, vy))
        # Slight random extra bullet occasionally for variation
        if random.random() < 0.25:
            ang = base_ang + random.uniform(-spread/2, spread/2)
            vx = math.cos(ang) * (speed+1)
            vy = math.sin(ang) * (speed+1)
            bullet = self.canvas.create_oval(base_x-8, base_y-8, base_x+8, base_y+8, fill="#ffaa33", outline="#ffffff")
            self.fan_bullets.append((bullet, vx, vy))


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
        bullet_coords = self.canvas.coords(bullet)
        if len(bullet_coords) < 4:
            return False
        # Use cached player center (set each frame in update loop)
        cx, cy = getattr(self, '_player_center', (None, None))
        if cx is None:
            px1, py1, px2, py2 = self.canvas.coords(self.player)
            cx = (px1 + px2) / 2
            cy = (py1 + py2) / 2
        if len(bullet_coords) > 4:
            xs = bullet_coords[::2]
            ys = bullet_coords[1::2]
            bx = sum(xs) / len(xs)
            by = sum(ys) / len(ys)
        else:
            bx = (bullet_coords[0] + bullet_coords[2]) / 2
            by = (bullet_coords[1] + bullet_coords[3]) / 2
        dx = cx - bx
        dy = cy - by
        dist2 = dx*dx + dy*dy
        # Compare squared distances (avoid sqrt)
        limit = (self.grazing_radius + 10)
        if dist2 < limit*limit and not self.check_collision(bullet):
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
            # Player rectangle from cache if available
            if hasattr(self, '_player_box') and self._player_box:
                px1, py1, px2, py2 = self._player_box
            else:
                px1, py1, px2, py2 = self.canvas.coords(self.player)
            # Bullet bounding box
            if len(b) == 4:
                bx1, by1, bx2, by2 = b
            else:
                xs = b[::2]
                ys = b[1::2]
                bx1, bx2 = min(xs), max(xs)
                by1, by2 = min(ys), max(ys)
            # Optional quick reject using center distance (coarse)
            if hasattr(self, '_player_center'):
                cx, cy = self._player_center
                bcx = (bx1 + bx2) * 0.5
                bcy = (by1 + by2) * 0.5
                dx = cx - bcx
                dy = cy - bcy
                # If centers are far beyond half-diagonals plus small buffer skip precise AABB
                max_dist = ((px2-px1)+(py2-py1))*0.6 + 50
                if dx*dx + dy*dy > max_dist*max_dist:
                    return False
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
            # Pick a random game over message once
            try:
                if self.game_over_messages:
                    self.selected_game_over_message = random.choice(self.game_over_messages)
                else:
                    self.selected_game_over_message = None
            except Exception:
                self.selected_game_over_message = None
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

    def end_game(self):
        """Compatibility method for legacy calls in bullet logic.
        Ensures game over animation triggers even if older code calls end_game()."""
        if self.game_over:
            return
        # Select message if not already chosen
        try:
            if getattr(self, 'selected_game_over_message', None) is None and getattr(self, 'game_over_messages', None):
                if self.game_over_messages:
                    self.selected_game_over_message = random.choice(self.game_over_messages)
        except Exception:
            pass
        self.game_over = True
        try:
            self.start_game_over_animation()
        except Exception:
            # Fallback minimal display
            try:
                msg = getattr(self, 'selected_game_over_message', 'GAME OVER') or 'GAME OVER'
                self.canvas.create_text(self.width//2, self.height//2, text=msg, fill='white', font=('Arial', 48, 'bold'))
            except Exception:
                pass

    def update_game(self):
        if self.game_over:
            return
        if self.paused:
            return
    # (Removed controller polling)
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
        # Delta time (seconds)
        now_perf = perf_counter()
        dt = now_perf - self._last_frame_time
        self._last_frame_time = now_perf
        # Calculate time survived, pausable
        time_survived = int(now - self.start_time - self.paused_time_total)
        # Cache player geometry for this frame
        self._player_box = self.canvas.coords(self.player)
        if self._player_box:
            px1, py1, px2, py2 = self._player_box
            self._player_center = ((px1+px2)/2, (py1+py2)/2)
        else:
            self._player_center = (0,0)
        self.canvas.itemconfig(self.scorecount, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.timecount, text=f"Time: {time_survived}")
        # Debug counters
        self._frame_count += 1
        if len(getattr(self, 'active_bullets', [])) > self._bullet_peak:
            self._bullet_peak = len(self.active_bullets)
        if self.debug and self._frame_count % 300 == 0:
            try:
                print(f"[DBG] frames={self._frame_count} bullets={len(self.active_bullets)} peak={self._bullet_peak} score={self.score}")
            except Exception:
                pass
        # Compute next unlock pattern
        remaining_candidates = [(pat, t_req - time_survived) for pat, t_req in self.unlock_times.items() if t_req > time_survived]
        if remaining_candidates:
            pat, secs = min(remaining_candidates, key=lambda x: x[1])
            display = self.pattern_display_names.get(pat, pat.title())
            self.canvas.itemconfig(self.next_unlock_text, text=f"Next Pattern: {display} in {secs}s")
        else:
            self.canvas.itemconfig(self.next_unlock_text, text="All patterns unlocked")

        # New unified spawning (vertical only so far) BEFORE legacy random spawns
        try:
            self.spawn_patterns(dt, time_survived)
            self.update_bullets(dt)
        except Exception:
            pass

        # Legacy bullet spawning and movement removed (handled by unified system).
        # Still spawn lasers independently (keep existing chance mapping via lightweight probability)
        if time_survived >= self.unlock_times['laser'] and random.random() < (1/160):
            self.shoot_horizontal_laser()

        # Skip legacy movement loops for bullets now managed by active_bullets.
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
                self.award_score(2)
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
                self.award_score(2)
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
                    self.award_score(2)
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
                self.award_score(1)
            # Grazing check
            if self.check_graze(frag) and frag not in self.grazed_bullets:
                self.award_score(1)
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
                self.award_score(1)
            # Grazing check
            if self.check_graze(bullet) and bullet not in self.grazed_bullets:
                self.award_score(1)
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
                self.award_score(1)
            # Grazing check
            if self.check_graze(bullet2) and bullet2 not in self.grazed_bullets:
                self.award_score(1)
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
                self.award_score(2)
            # Grazing check
            if self.check_graze(egg_bullet) and egg_bullet not in self.grazed_bullets:
                self.award_score(1)
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
                self.award_score(2)
            # Grazing check
            if self.check_graze(dbullet) and dbullet not in self.grazed_bullets:
                self.award_score(1)
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
                self.award_score(5)  # Boss bullets give more score
            # Grazing check
            if self.check_graze(boss_bullet) and boss_bullet not in self.grazed_bullets:
                self.award_score(2)
                self.grazed_bullets.add(boss_bullet)
                self.show_graze_effect()

        # Move quad bullets
        for bullet in self.quad_bullets[:]:
            self.canvas.move(bullet, 0, quad_speed)
            if self.check_collision(bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(bullet)
                self.quad_bullets.remove(bullet)
            elif self.canvas.coords(bullet)[1] > self.height:
                self.canvas.delete(bullet)
                self.quad_bullets.remove(bullet)
                self.award_score(2)
            # Grazing check
            if self.check_graze(bullet) and bullet not in self.grazed_bullets:
                self.award_score(1)
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
                    self.award_score(2)
                else:
                    # Update tuple with incremented step_count and possibly new direction
                    idx = self.zigzag_bullets.index(bullet_tuple)
                    self.zigzag_bullets[idx] = (bullet, direction, step_count + 1)
            # Grazing check
            if self.check_graze(bullet) and bullet not in self.grazed_bullets:
                self.award_score(1)
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
                self.award_score(2)
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
            # Backward compatibility: allow old 3-tuple
            if len(hb_tuple) == 3:
                bullet, vx, vy = hb_tuple
                life = self.homing_bullet_max_life
            else:
                bullet, vx, vy, life = hb_tuple
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
            life -= 1
            # Update tuple (store life)
            idx = self.homing_bullets.index(hb_tuple)
            self.homing_bullets[idx] = (bullet, vx, vy, life)
            # Collision / out of bounds
            if self.check_collision(bullet):
                if not self.practice_mode:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.end_game()
                self.canvas.delete(bullet)
                self.homing_bullets.remove(self.homing_bullets[idx])
            else:
                coords = self.canvas.coords(bullet)
                if (not coords or coords[1] > self.height or coords[0] < -60 or coords[2] > self.width + 60 or life <= 0):
                    try:
                        self.canvas.delete(bullet)
                    except Exception:
                        pass
                    # Remove using safe search if idx stale
                    try:
                        self.homing_bullets.remove(self.homing_bullets[idx])
                    except Exception:
                        # fallback linear remove by id match
                        for _t in self.homing_bullets:
                            if _t[0] == bullet:
                                self.homing_bullets.remove(_t)
                                break
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
        """Initialize lore fragments from external lore.txt file.
        Format of lore.txt:
          - Lines starting with '#' are comments
          - Blank line separates fragments
          - Multi-line fragments are combined into one line (joined with spaces)
        Result stored in self.lore_fragments as {'all': [list_of_strings]} for compatibility.
        If file missing or parsing fails, a minimal fallback list is used.
        """
        lore_file = "lore.txt"
        # Resolve possible PyInstaller path
        if hasattr(sys, '_MEIPASS'):
            candidate = os.path.join(sys._MEIPASS, lore_file)
            if os.path.exists(candidate):
                lore_file = candidate
        parsed_dict = None
        # 1. Try to parse entire file as a Python dict literal
        try:
            import ast
            with open(lore_file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            if text.startswith('{') and text.endswith('}'):  # quick heuristic
                parsed = ast.literal_eval(text)
                if isinstance(parsed, dict):
                    parsed_dict = {}
                    # Ensure all values are lists of strings
                    for k, v in parsed.items():
                        if isinstance(v, (list, tuple)):
                            parsed_dict[str(k)] = [str(x) for x in v]
                    if parsed_dict:
                        self.lore_fragments = parsed_dict
        except Exception:
            parsed_dict = None
        if parsed_dict is None:
            # 2. Fallback: treat file as block fragments separated by blank lines
            fragments = []
            current_lines = []
            try:
                with open(lore_file, 'r', encoding='utf-8') as f2:
                    for raw in f2:
                        line = raw.rstrip('\n').strip()
                        if not line or line.startswith('#'):
                            if current_lines:
                                fragments.append(' '.join(current_lines))
                                current_lines = []
                            continue
                        current_lines.append(line)
                if current_lines:
                    fragments.append(' '.join(current_lines))
            except Exception:
                fragments = [
                    "THE MEMORY CORE IS EMPTY BUT STILL HUMS.",
                    "A PLACEHOLDER FRAGMENT REMINDS YOU THIS IS A FALLBACK."
                ]
            # De-duplicate preserving order
            seen = set()
            unique_fragments = []
            for frag in fragments:
                if frag not in seen:
                    seen.add(frag)
                    unique_fragments.append(frag)
            self.lore_fragments = {'all': unique_fragments}
        # Normalize capitalization for lore: convert whole-word 'you'/'your' to uppercase
        try:
            import re
            if 'all' in self.lore_fragments:  # flat list form
                for _i, _line in enumerate(self.lore_fragments['all']):
                    self.lore_fragments['all'][_i] = re.sub(r"\b(you|your)\b", lambda m: m.group(0).upper(), _line, flags=re.IGNORECASE)
            else:  # categorized dict
                for _k, _list in self.lore_fragments.items():
                    for _i, _line in enumerate(_list):
                        _list[_i] = re.sub(r"\b(you|your)\b", lambda m: m.group(0).upper(), _line, flags=re.IGNORECASE)
        except Exception:
            pass

    def update_lore_line(self, force=False):
        if getattr(self, 'lore_fragments', None) is None:
            return
        now = time.time()
        if not force and now - getattr(self, 'lore_last_change', 0) < getattr(self, 'lore_interval', 8):
            return
        import random
        pool = []
        prev = getattr(self, 'current_lore_line', None)
        # Support both old dict-of-lists structure and new single 'all' list
        try:
            if 'all' in self.lore_fragments and isinstance(self.lore_fragments['all'], list):
                for ln in self.lore_fragments['all']:
                    if ln != prev:
                        pool.append(ln)
            else:
                for _k, lines in self.lore_fragments.items():
                    for ln in lines:
                        if ln != prev:
                            pool.append(ln)
        except Exception:
            return
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
        # Glitch blackout sequence state (fix indentation)
        self.go_glitch_phase = 0  # 0 = glitching, 1 = fading to black, 2 = black hold
        self.go_glitch_rects = []
        self.go_black_cover = None
        self.go_black_alpha = 0.0
        self.go_anim_subtext = None
        # Large pulsing overlay text (separate from static text already created)
        try:
            self.go_anim_text = self.canvas.create_text(self.width//2, self.height//2-140, text="GAME OVER", fill="#ffffff", font=("Arial", 64, "bold"))
        except Exception:
            self.go_anim_text = None
        # Secondary message below if one was selected
        if self.selected_game_over_message:
            try:
                self.go_anim_subtext = self.canvas.create_text(
                    self.width//2, self.height//2 - 60,
                    text=self.selected_game_over_message,
                    fill="#ff66aa", font=("Courier New", 26), justify='center'
                )
            except Exception:
                self.go_anim_subtext = None
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
        # --- Phase 0: Spawn transient glitch rectangles ---
        if self.go_glitch_phase == 0:
            # spawn a few per frame early on
            spawn_ct = 6
            import random
            for _ in range(spawn_ct):
                w = random.randint(40, max(60, self.width//6))
                h = random.randint(8, 40)
                x = random.randint(0, self.width - w)
                y = random.randint(0, self.height - h)
                col = random.choice(["#ff00ff", "#ffffff", "#ff55ff", "#aa33ff"])  # neon glitch colors
                rid = self.canvas.create_rectangle(x, y, x+w, y+h, fill=col, outline="")
                life = random.randint(3, 10)
                self.go_glitch_rects.append((rid, life))
            # decay existing glitch rects
            new_rects = []
            for rid, life in self.go_glitch_rects:
                life -= 1
                if life <= 0:
                    try: self.canvas.delete(rid)
                    except Exception: pass
                else:
                    # occasional horizontal shift for jitter
                    try:
                        dx = random.randint(-8,8)
                        self.canvas.move(rid, dx, 0)
                    except Exception: pass
                    new_rects.append((rid, life))
            self.go_glitch_rects = new_rects
            # After some frames, advance to fade phase
            if self.go_anim_frame > 55:
                self.go_glitch_phase = 1
        # --- Phase 1: Fade a black overlay in and delete scene ---
        elif self.go_glitch_phase == 1:
            # Create black cover once
            if self.go_black_cover is None:
                try:
                    self.go_black_cover = self.canvas.create_rectangle(0,0,self.width,self.height, fill="#000000", outline="")
                    self.canvas.itemconfig(self.go_black_cover, stipple="gray12")  # simulate alpha via stipple
                except Exception:
                    pass
            # Increase pseudo alpha
            self.go_black_alpha += 0.06
            # Adjust stipple pattern to simulate increasing opacity
            if self.go_black_cover is not None:
                # choose denser patterns as alpha rises
                try:
                    if self.go_black_alpha > 0.8:
                        self.canvas.itemconfig(self.go_black_cover, stipple="")  # solid
                    elif self.go_black_alpha > 0.6:
                        self.canvas.itemconfig(self.go_black_cover, stipple="gray50")
                    elif self.go_black_alpha > 0.4:
                        self.canvas.itemconfig(self.go_black_cover, stipple="gray37")
                    elif self.go_black_alpha > 0.2:
                        self.canvas.itemconfig(self.go_black_cover, stipple="gray25")
                except Exception:
                    pass
            # Occasionally delete lingering items beneath
            if self.go_anim_frame % 9 == 0:
                for item in self.canvas.find_all():
                    # keep the black cover & game over text for now
                    if item in (self.go_black_cover, self.go_anim_text):
                        continue
                    try: self.canvas.delete(item)
                    except Exception: pass
            if self.go_black_alpha >= 1.0:
                # Remove text as screen fully blacks
                try:
                    if self.go_anim_text is not None:
                        self.canvas.delete(self.go_anim_text)
                        self.go_anim_text = None
                    if self.go_anim_subtext is not None:
                        self.canvas.delete(self.go_anim_subtext)
                        self.go_anim_subtext = None
                except Exception: pass
                self.go_glitch_phase = 2
        # --- Phase 2: Hold black, minimal updates ---
        elif self.go_glitch_phase == 2:
            # No further visuals; allow a restart key prompt optionally
            if self.go_anim_frame % 40 == 0 and getattr(self, 'go_anim_text', None) is None:
                try:
                    self.go_anim_text = self.canvas.create_text(self.width//2, self.height//2, text="PRESS R TO RESTART", fill="#4444ff", font=("Arial", 24))
                except Exception:
                    pass
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
        if self.go_glitch_phase == 2 and self.go_anim_frame > 400:
            # Stop updating; final blackout stable
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
