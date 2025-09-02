import tkinter as tk
import random
import time
import pygame
import sys
import os

class bullet_hell_game:
    def __init__(self, root):
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
        self.player = self.canvas.create_rectangle(self.width//2-10, self.height-50, self.width//2+10, self.height-30, fill="white")
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
        self.laser_indicators = []  # [(indicator_id, y, timer)]
        self.lasers = []  # [(laser_id, y, timer)]
        self.score = 0
        self.timee = int(time.time())
        self.dial = "Welcome to Get Shot at by a Nine Year Old Simulator!"
        self.scorecount = self.canvas.create_text(70, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 16))
        self.timecount = self.canvas.create_text(self.width-70, 20, text=f"Time: {self.timee}", fill="white", font=("Arial", 16))
        self.dialog = self.canvas.create_text(self.width//2, 20, text=self.dial, fill="white", font=("Arial", 20), justify="center")
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
        self.grazing_radius = 40
        self.grazed_bullets = set()
        self.graze_effect_id = None
        self.update_game()

    def restart_game(self, event=None):
        if not self.game_over:
            return
        # Remove all canvas items
        for item in self.canvas.find_all():
            self.canvas.delete(item)
        # Reset all game state
        self.player = self.canvas.create_rectangle(self.width//2-10, self.height-50, self.width//2+10, self.height-30, fill="white")
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
        self.laser_indicators = []
        self.lasers = []
        self.score = 0
        self.timee = int(time.time())
        self.scorecount = self.canvas.create_text(70, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 16))
        self.timecount = self.canvas.create_text(self.width-70, 20, text=f"Time: {self.timee}", fill="white", font=("Arial", 16))
        self.dialog = self.canvas.create_text(self.width//2, 20, text=self.dial, fill="white", font=("Arial", 20), justify="center")
        self.lives = 1
        self.game_over = False
        self.paused = False
        self.pause_text = None
        self.difficulty = 1
        self.last_difficulty_increase = time.time()
        self.lastdial = time.time()
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
            "Dodge the bullets and survive as long as you can!",
            "Use arrow keys to move yourself.",
            "Good luck, and have fun!",
            "The bullets are getting faster!",
            "Stay sharp, the challenge increases!",
            "Can you beat your high score? (no)",
            "Keep going, you're doing great! (lie)",
            "Watch out for the lasers!",
            "Every second counts in Bullet Hell!",
            "This isn't like Undertale, you can't fight back!",
            "Remember, it's just a game. Have fun! (jk)",
            "Pro tip: Moving towards bullets can help dodge bullets.",
            "If you can read this, you're doing well!",
            "Try to survive for 5 minutes!",
            "The longer you survive, the harder it gets!",
            "Don't forget to take breaks! (but leave it running)",
            "You're a star at dodging bullets! (there arent stars)",
            "Keep your eyes on the screen! (tear them out)",
            "Practice makes perfect! (poggers)",
            "This doesn't really compare to Touhou, but it's fun!",
            "Feel free to suggest new bullet patterns!",
            "Remember to breathe and relax!",
            "You can do this, just keep dodging!",
            "Every bullet you dodge is a victory!",
            "Stay focused, and you'll go far!",
            "You're not just playing, you're mastering the art of dodging!",
            "Keep your reflexes sharp!",
            "Believe in yourself, you can do it!",
            "[FILTERED] You- you suck!",
            "If you can dodge a wrench, you can dodge a bullet.",
            "Y u try?",
            "Is this bullet hell or bullet heaven?",
            "Dodging bullets is my cardio.",
            "I hope you like pain.",
            "My bullets, my rules.",
            "You call that dodging?",
            "Too slow!",
            "Is that all you've got?",
            "You can't hide forever!",
            "Feel the burn of my bullets!",
            "You're making this too easy!",
            "Come on, show me what you've got!",
            "You can't escape your fate!",
            "This is just the beginning!",
            "Prepare to be overwhelmed!",
            "Your skills are impressive, but not enough!",
            "I could do this all day!",
            "You're in my world now!",
            "Let's see how long you can last!",
            "Every second you survive, I get stronger!",
            "You think you can outlast me?",
            "This is my domain!",
            "You can't win, but you can try!",
            "The harder you try, the more bullets you'll face!",
            "You may have dodged this time, but not next time!",
            "Is that fear I see in your eyes?",
            "You can't run from your destiny!",
            "Your efforts are futile!",
            "I admire your persistence!",
            "Persistence won't save you!",
            "You're just delaying the inevitable!",
            "E",
            "Stay determined!",
            "Skissue",
            "You can do it! /j",
            "This is getting intense, isn't it?",
            "Keep your head in the game!",
            "You're doing better than I expected!",
            "Song name is Juggerbeat, I made it in 3rd grade. :3",
            "BTW the dialog is canonically spoken by a nine year old girl named J.",
            "The bullets are getting faster, just like your heart rate!",
            "The person making the bullets is also a nine year old. (same person lol)",
            "Yeah im not okay!",
            "Murder! Yippee!!!",
            "The person making the game may or may not be a nine year old.",
            "Yes im self aware, and will actively break the 4th wall.",
            "\n I could really go for some applesauce... \n Or corpses...",
            "U just got beat up by a girl!",
            "Smug colon-three",
            "Get dunked on!!!",
            "\n Never gonna give you up,\n never gonna let you down.",
            "Who gave me a GUN?",
            "Blep",
            "\n\n My name is J, nice to meet you. \n I would ask your name, but I'm going to kill you, \n so it doesn't really matter."
        ]
        self.dial=random.choice(dialogs)
        if self.dial == ":)":
            self.canvas.itemconfig(self.dialog, fill="red")
        else:
            self.canvas.itemconfig(self.dialog, fill="white")
        if self.dial == "\n Never gonna give you up,\n never gonna let you down.":
            self.canvas.itemconfig(self.dialog, font=("Wingdings",20 ))
        else:
            self.canvas.itemconfig(self.dialog, font=("Arial",20 ))
        return self.dial

    def shoot_horizontal_laser(self):
        if not self.game_over:
            y = random.randint(50, self.height-50)
            indicator = self.canvas.create_line(0, y, self.width, y, fill="red", dash=(5, 2), width=3)
            self.laser_indicators.append((indicator, y, 30))  # 30 frames indicator

    def shoot_star_bullet(self):
        if not self.game_over:
            x = random.randint(20, self.width-40)
            # Draw a star using create_polygon
            points = [x, 0, x+10, 30, x+20, 0, x+5, 20, x+15, 20]
            bullet = self.canvas.create_polygon(points, fill="magenta")
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

    def move_player(self, event):
        if self.paused or self.game_over:
            return
        if event.keysym == 'Left':
            if self.canvas.coords(self.player)[0] > 0:
                self.canvas.move(self.player, -20, 0)
        elif event.keysym == 'Right':
            if self.canvas.coords(self.player)[2] < self.width:
                self.canvas.move(self.player, 20, 0)
        elif event.keysym == 'Up':
            if self.canvas.coords(self.player)[1] > 0:
                self.canvas.move(self.player, 0, -20)
        elif event.keysym == 'Down':
            if self.canvas.coords(self.player)[3] < self.height:
                self.canvas.move(self.player, 0, 20)

    def toggle_pause(self, event=None):
        if self.game_over:
            return
        self.paused = not self.paused
        if self.paused:
            if not self.pause_text:
                self.pause_text = self.canvas.create_text(self.width//2, self.height//2, text="Paused", fill="yellow", font=("Arial", 40))
        else:
            if self.pause_text:
                self.canvas.delete(self.pause_text)
                self.pause_text = None
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

    def update_game(self):
        if self.game_over:
            return
        if self.paused:
            return
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
        if now - self.last_difficulty_increase > 60:
            self.difficulty += 1
            self.last_difficulty_increase = now
        if now - self.lastdial > 15:
            self.get_dialog_string()
            self.lastdial = now
            self.canvas.itemconfig(self.dialog, text=self.dial)
        self.canvas.itemconfig(self.scorecount, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.timecount, text=f"Time: {int(now - self.timee)}")

        # Lower values mean higher spawn rate
        bullet_chance = max(4, 30 - self.difficulty)
        bullet2_chance = max(4, 30 - self.difficulty)
        diag_chance = max(10, 60 - self.difficulty * 2)
        boss_chance = max(20, 150 - self.difficulty * 5)
        zigzag_chance = max(10, 80 - self.difficulty * 2)
        fast_chance = max(6, 50 - self.difficulty)
        star_chance = max(16, 80 - self.difficulty * 2)
        rect_chance = max(12, 60 - self.difficulty * 2)
        laser_chance = max(30, 120 - self.difficulty * 4)
        triangle_chance = max(10, 70 - self.difficulty * 2)
        quad_chance = max(8, 40 - self.difficulty)
        egg_chance = max(10, 60 - self.difficulty * 2)

        if random.randint(1, bullet_chance) == 1:
            self.shoot_bullet()
        if random.randint(1, bullet2_chance) == 1:
            self.shoot_bullet2()
        if random.randint(1, diag_chance) == 1:
            self.shoot_diag_bullet()
        if random.randint(1, boss_chance) == 1:
            self.shoot_boss_bullet()
        if random.randint(1, zigzag_chance) == 1:
            self.shoot_zigzag_bullet()
        if random.randint(1, fast_chance) == 1:
            self.shoot_fast_bullet()
        if random.randint(1, star_chance) == 1:
            self.shoot_star_bullet()
        if random.randint(1, rect_chance) == 1:
            self.shoot_rect_bullet()
        if random.randint(1, laser_chance) == 1:
            self.shoot_horizontal_laser()
        if random.randint(1, triangle_chance) == 1:
            self.shoot_triangle_bullet()
        if random.randint(1, quad_chance) == 1:
            self.shoot_quad_bullet()
        if random.randint(1, egg_chance) == 1:
            self.shoot_egg_bullet()
        # Move triangle bullets
        triangle_speed = 7 + self.difficulty // 2
        for bullet_tuple in self.triangle_bullets[:]:
            bullet, direction = bullet_tuple
            self.canvas.move(bullet, triangle_speed * direction, triangle_speed)
            if self.check_collision(bullet):
                self.lives -= 1
                self.canvas.delete(bullet)
                self.paused = False
                self.pause_text = None
                self.triangle_bullets.remove(bullet_tuple)
                if self.lives <= 0:
                    self.end_game()
            else:
                coords = self.canvas.coords(bullet)
                if coords[1] > self.height or coords[0] < 0 or coords[2] > self.width:
                    self.canvas.delete(bullet)
                    self.triangle_bullets.remove(bullet_tuple)
                    self.score += 2
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
        bullet_speed = 6 + self.difficulty // 2
        bullet2_speed = 6 + self.difficulty // 2
        diag_speed = 4 + self.difficulty // 3
        boss_speed = 8 + self.difficulty // 2
        zigzag_speed = 5 + self.difficulty // 3
        fast_speed = 12 + self.difficulty
        star_speed = 7 + self.difficulty // 2
        rect_speed = 8 + self.difficulty // 2
        quad_speed = 6 + self.difficulty // 2
        egg_speed = 5 + self.difficulty // 3

        # Move vertical bullets
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, bullet_speed)
            if self.check_collision(bullet):
                self.lives -= 1
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
                if self.lives <= 0:
                    self.end_game()
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
                self.lives -= 1
                self.canvas.delete(bullet2)
                self.bullets2.remove(bullet2)
                if self.lives <= 0:
                    self.end_game()
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
                self.lives -= 1
                self.canvas.delete(egg_bullet)
                self.egg_bullets.remove(egg_bullet)
                if self.lives <= 0:
                    self.end_game()
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
                self.lives -= 1
                self.canvas.delete(dbullet)
                self.diag_bullets.remove(bullet_tuple)
                if self.lives <= 0:
                    self.end_game()
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
                self.lives -= 1
                self.canvas.delete(boss_bullet)
                self.boss_bullets.remove(boss_bullet)
                if self.lives <= 0:
                    self.end_game()
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
                self.lives -= 1
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
                if self.lives <= 0:
                    self.end_game()
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
                self.lives -= 1
                self.canvas.delete(bullet)
                self.zigzag_bullets.remove(bullet_tuple)
                if self.lives <= 0:
                    self.end_game()
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
                self.lives -= 1
                self.canvas.delete(fast_bullet)
                self.fast_bullets.remove(fast_bullet)
                if self.lives <= 0:
                    self.end_game()
            elif self.canvas.coords(fast_bullet)[1] > self.height:
                self.canvas.delete(fast_bullet)
                self.fast_bullets.remove(fast_bullet)
                self.score += 2
            # Grazing check
            if self.check_graze(fast_bullet) and fast_bullet not in self.grazed_bullets:
                self.score += 1
                self.grazed_bullets.add(fast_bullet)
                self.show_graze_effect()

        # Move star bullets
        for star_bullet in self.star_bullets[:]:
            self.canvas.move(star_bullet, 0, star_speed)
            if self.check_collision(star_bullet):
                self.lives -= 1
                self.canvas.delete(star_bullet)
                self.star_bullets.remove(star_bullet)
                if self.lives <= 0:
                    self.end_game()
            elif self.canvas.coords(star_bullet)[1] > self.height:
                self.canvas.delete(star_bullet)
                self.star_bullets.remove(star_bullet)
                self.score += 3
            # Grazing check
            if self.check_graze(star_bullet) and star_bullet not in self.grazed_bullets:
                self.score += 1
                self.grazed_bullets.add(star_bullet)
                self.show_graze_effect()

        # Move rectangle bullets
        for rect_bullet in self.rect_bullets[:]:
            self.canvas.move(rect_bullet, 0, rect_speed)
            if self.check_collision(rect_bullet):
                self.lives -= 1
                self.canvas.delete(rect_bullet)
                self.rect_bullets.remove(rect_bullet)
                if self.lives <= 0:
                    self.end_game()
            elif self.canvas.coords(rect_bullet)[1] > self.height:
                self.canvas.delete(rect_bullet)
                self.rect_bullets.remove(rect_bullet)
                self.score += 2
            # Grazing check
            if self.check_graze(rect_bullet) and rect_bullet not in self.grazed_bullets:
                self.score += 1
                self.grazed_bullets.add(rect_bullet)
                self.show_graze_effect()

        self.root.after(50, self.update_game)

    def check_collision(self, bullet):
        bullet_coords = self.canvas.coords(bullet)
        player_coords = self.canvas.coords(self.player)
        return (bullet_coords[2] > player_coords[0] and
                bullet_coords[0] < player_coords[2] and
                bullet_coords[3] > player_coords[1] and
                bullet_coords[1] < player_coords[3])

    def end_game(self):
        self.game_over = True
        self.canvas.create_text(self.width//2, self.height//2-50, text="Game Over", fill="white", font=("Arial", 30))
        self.canvas.create_text(self.width//2, self.height//2, text=f"Score: {self.score}", fill="white", font=("Arial", 20))
        self.canvas.create_text(self.width//2, self.height//2+50, text=f"Time Survived: {int(time.time() - self.timee)} seconds", fill="white", font=("Arial", 20))
        self.canvas.create_text(self.width//2, self.height//2+100, text="Press R to Restart", fill="yellow", font=("Arial", 18))
        self.root.bind("r", self.restart_game)

if __name__ == "__main__":
    root = tk.Tk()
    game = bullet_hell_game(root)
    root.mainloop()