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
        self.root.title("Bullet Hell Game")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="black")
        self.canvas.pack()
        self.player = self.canvas.create_rectangle(390, 550, 410, 570, fill="white")
        self.bullets = []
        self.bullets2 = []
        self.triangle_bullets = []  # [(bullet_id, direction)]
        self.diag_bullets = []
        self.dialog_gmindex = -1
        self.dialognext = ["Yeah if you couldn't tell, this isn't like Touhou.",
                           "Because, well, Touhou is finite, and this, well, isn't.",
                           "And guess what?",
                           "It's not like undertale either.",
                           "Because you can't fight back!!!",
                           "Uhh- good luck.",
                           "...",
                           ". . .",
                           "I've run out of funny references."]
        self.boss_bullets = []
        self.zigzag_bullets = []
        self.fast_bullets = []
        self.star_bullets = []
        self.rect_bullets = []
        self.fast_bullets = []
        self.egg_bullets = []
        self.graze_distance = 150  # Distance for TP grazing
        self.laser_indicators = []  # [(indicator_id, y, timer)]
        self.lasers = []  # [(laser_id, y, timer)]
        self.score = 0
        self.gamerunning = False
        self.timee = int(time.time())
        self.scorecount = self.canvas.create_text(70, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 16))
        self.timecount = self.canvas.create_text(730, 20, text=f"Time: {self.timee}", fill="white", font=("Arial", 16))
        self.lives = 1
        self.game_over = False
        self.root.bind("<KeyPress>", self.on_key_press)

        # Dialog system
        self.dialog_list = []  # List of dialog strings
        self.dialog_index = 0
        self.dialog_active = False
        self.dialog_box = None
        self.dialog_text = None
        self.update_game()

    def shoot_quad_bullet(self):
        if not self.game_over:
            x = random.randint(0, 780)
            bullet1 = self.canvas.create_oval(x, 0, x + 20, 20, fill="red")
            bullet2 = self.canvas.create_oval(x + 30, 0, x + 50, 20, fill="red")
            bullet3 = self.canvas.create_oval(x + 60, 0, x + 80, 20, fill="red")
            bullet4 = self.canvas.create_oval(x + 90, 0, x + 110, 20, fill="red")
            self.bullets.extend([bullet1, bullet2, bullet3, bullet4])

    def shoot_triangle_bullet(self):
        if not self.game_over:
            x = random.randint(0, 780)
            direction = random.choice([1, -1])
            # Draw triangle using create_polygon
            points = [x, 0, x+20, 0, x+10, 20]
            bullet = self.canvas.create_polygon(points, fill="#bfff00")
            self.triangle_bullets.append((bullet, direction))

    def shoot_horizontal_laser(self):
        if not self.game_over:
            y = random.randint(50, 550)
            indicator = self.canvas.create_line(0, y, 800, y, fill="red", dash=(5, 2), width=3)
            self.laser_indicators.append((indicator, y, 30))  # 30 frames indicator

    def shoot_star_bullet(self):
        if not self.game_over:
            x = random.randint(20, 760)
            # Draw a star using create_polygon
            points = [x, 0, x+10, 30, x+20, 0, x+5, 20, x+15, 20]
            bullet = self.canvas.create_polygon(points, fill="magenta")
            self.star_bullets.append(bullet)

    def shoot_rect_bullet(self):
        if not self.game_over:
            x = random.randint(0, 740)
            bullet = self.canvas.create_rectangle(x, 0, x+60, 15, fill="blue")
            self.rect_bullets.append(bullet)

    def shoot_zigzag_bullet(self):
        if not self.game_over:
            x = random.randint(0, 780)
            bullet = self.canvas.create_oval(x, 0, x + 20, 20, fill="cyan")
            # Zigzag state: (bullet, direction, step_count)
            direction = random.choice([1, -1])
            self.zigzag_bullets.append((bullet, direction, 0))

    def shoot_fast_bullet(self):
        if not self.game_over:
            x = random.randint(0, 780)
            bullet = self.canvas.create_oval(x, 0, x + 20, 20, fill="orange")
            self.fast_bullets.append(bullet)

    def on_key_press(self, event):
        # Dialog navigation
        if self.dialog_active:
            if event.keysym == 'space':
                self.next_dialog()
            return
        self.move_player(event)

    def move_player(self, event):
        if event.keysym == 'Left' and not self.game_over:
            if self.canvas.coords(self.player)[0] > 0:
                self.canvas.move(self.player, -20, 0)
        elif event.keysym == 'Right' and not self.game_over:
            if self.canvas.coords(self.player)[2] < 800:
                self.canvas.move(self.player, 20, 0)
        elif event.keysym == 'Up' and not self.game_over:
            if self.canvas.coords(self.player)[1] > 0:
                self.canvas.move(self.player, 0, -20)
        elif event.keysym == 'Down' and not self.game_over:
            if self.canvas.coords(self.player)[3] < 600:
                self.canvas.move(self.player, 0, 20)

    def restart_game(self, event):
        if event.keysym == 'r':
            self.restartdialog()

    def restartdialog(self):
        self.gamerunning = False
        self.game_over = False
        self.lives = 1
        self.score = 0
        self.timee = int(time.time())
        self.dialog_gmindex += 1
        self.show_dialog([self.dialognext[self.dialog_gmindex]])
        self.gamerunning = True
        self.update_game()

    def show_dialog(self, dialog_list):
        """
        Call this method with a list of strings to display dialog.
        Example: self.show_dialog(["Hello!", "Welcome to Bullet Hell."])
        """
        if not dialog_list:
            return
        self.dialog_list = dialog_list
        self.dialog_index = 0
        self.dialog_active = True
        self.gamerunning = False
        self.display_dialog_box()

    def display_dialog_box(self):
        # Remove previous dialog box if exists
        if self.dialog_box:
            self.canvas.delete(self.dialog_box)
        if self.dialog_text:
            self.canvas.delete(self.dialog_text)
        # Draw dialog box (semi-transparent rectangle)
        self.dialog_box = self.canvas.create_rectangle(100, 450, 700, 590, fill="#222", outline="white", width=3)
        # Draw dialog text
        text = self.dialog_list[self.dialog_index]
        self.dialog_text = self.canvas.create_text(400, 520, text=text, fill="white", font=("Arial", 18), width=580)
        # Draw prompt
        self.dialog_prompt = self.canvas.create_text(400, 570, text="[Space] Next", fill="#aaa", font=("Arial", 12))

    def next_dialog(self):
        self.dialog_index += 1
        if self.dialog_index >= len(self.dialog_list):
            self.close_dialog()
        else:
            self.display_dialog_box()

    def close_dialog(self):
        self.dialog_active = False
        if self.dialog_box:
            self.canvas.delete(self.dialog_box)
            self.dialog_box = None
        if self.dialog_text:
            self.canvas.delete(self.dialog_text)
            self.dialog_text = None
        if hasattr(self, 'dialog_prompt') and self.dialog_prompt:
            self.canvas.delete(self.dialog_prompt)
            self.dialog_prompt = None
            self.gamerunning = True
        self.update_game()

    def shoot_bullet(self):
        if not self.game_over:
            x = random.randint(0, 780)
            bullet = self.canvas.create_oval(x, 0, x + 20, 20, fill="red")
            self.bullets.append(bullet)

    def shoot_egg_bullet(self):
        if not self.game_over:
            x = random.randint(0, 780)
            bullet = self.canvas.create_oval(x, 0, x + 20, 40, fill="tan")
            self.egg_bullets.append(bullet)

    def shoot_bullet2(self):
        if not self.game_over:
            y = random.randint(0, 780)
            bullet2 = self.canvas.create_oval(0, y, 20, y + 20, fill="yellow")
            self.bullets2.append(bullet2)

    def shoot_diag_bullet(self):
        if not self.game_over:
            x = random.randint(0, 780)
            direction = random.choice([1, -1])  # 1 for right-down, -1 for left-down
            bullet = self.canvas.create_oval(x, 0, x + 20, 20, fill="green")
            self.diag_bullets.append((bullet, direction))

    def shoot_boss_bullet(self):
        if not self.game_over:
            x = random.randint(200, 600)
            bullet = self.canvas.create_oval(x, 0, x + 40, 40, fill="purple")
            self.boss_bullets.append(bullet)

    def update_game(self):
        # Pause game updates if dialog is active
        if self.dialog_active:
            self.root.after(50, self.update_game)
            return
        if not self.game_over:
            if self.gamerunning:
                # Increase every 100 seconds
                now = time.time()
                self.canvas.itemconfig(self.scorecount, text=f"Score: {self.score}")
                self.canvas.itemconfig(self.timecount, text=f"Time: {int(now - self.timee)}")
            # Lower values mean higher spawn rate
            bullet_chance = max(4, 30)
            bullet2_chance = max(4, 30)
            diag_chance = max(10, 60)
            boss_chance = max(20, 150)
            zigzag_chance = max(10, 80)
            fast_chance = max(6, 50)
            star_chance = max(16, 80)
            rect_chance = max(12, 60)
            laser_chance = max(30, 120)
            triangle_chance = max(10, 70)
            quad_chance = max(8, 40)
            egg_chance = max(10, 60)

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
            # Move triangle bullets
            triangle_speed = 7
            for bullet_tuple in self.triangle_bullets[:]:
                bullet, direction = bullet_tuple
                self.canvas.move(bullet, triangle_speed * direction, triangle_speed)
                if self.check_collision(bullet):
                    self.lives -= 1
                    self.canvas.delete(bullet)
                    self.triangle_bullets.remove(bullet_tuple)
                    if self.lives <= 0:
                        self.end_game()
                else:
                    coords = self.canvas.coords(bullet)
                    if coords[1] > 600 or coords[0] < 0 or coords[2] > 800:
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
                    laser_id = self.canvas.create_line(0, y, 800, y, fill="red", width=8)
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

            # Bullet speeds
            bullet_speed = 6
            bullet2_speed = 6
            diag_speed = 4
            boss_speed = 8
            zigzag_speed = 5
            fast_speed = 12
            star_speed = 7
            rect_speed = 8
            quad_speed = 6
            egg_speed = 5

            # Move vertical bullets
            for bullet in self.bullets[:]:
                self.canvas.move(bullet, 0, bullet_speed)
                # TP Grazing check
                if self.check_graze(bullet):
                    self.score += 1
                if self.check_collision(bullet):
                    self.lives -= 1
                    self.canvas.delete(bullet)
                    self.bullets.remove(bullet)
                    if self.lives <= 0:
                        self.end_game()
                elif self.canvas.coords(bullet)[1] > 600:
                    self.canvas.delete(bullet)
                    self.bullets.remove(bullet)
                    self.score += 1

            # Move horizontal bullets
            for bullet2 in self.bullets2[:]:
                self.canvas.move(bullet2, bullet2_speed, 0)
                if self.check_graze(bullet2):
                    self.score += 1
                if self.check_collision(bullet2):
                    self.lives -= 1
                    self.canvas.delete(bullet2)
                    self.bullets2.remove(bullet2)
                    if self.lives <= 0:
                        self.end_game()
                elif self.canvas.coords(bullet2)[0] > 800:
                    self.canvas.delete(bullet2)
                    self.bullets2.remove(bullet2)
                    self.score += 1

            # Move egg bullets
            for egg_bullet in self.egg_bullets[:]:
                self.canvas.move(egg_bullet, 0, egg_speed)
                if self.check_graze(egg_bullet):
                    self.score += 1
                if self.check_collision(egg_bullet):
                    self.lives -= 1
                    self.canvas.delete(egg_bullet)
                    self.egg_bullets.remove(egg_bullet)
                    if self.lives <= 0:
                        self.end_game()
                elif self.canvas.coords(egg_bullet)[1] > 600:
                    self.canvas.delete(egg_bullet)
                    self.egg_bullets.remove(egg_bullet)
                    self.score += 2

            # Move diagonal bullets
            for bullet_tuple in self.diag_bullets[:]:
                bullet, direction = bullet_tuple
                self.canvas.move(bullet, diag_speed * direction, diag_speed)
                if self.check_graze(bullet):
                    self.score += 1
                if self.check_collision(bullet):
                    self.lives -= 1
                    self.canvas.delete(bullet)
                    self.diag_bullets.remove(bullet_tuple)
                    if self.lives <= 0:
                        self.end_game()
                else:
                    coords = self.canvas.coords(bullet)
                    if coords[1] > 600 or coords[0] < 0 or coords[2] > 800:
                        self.canvas.delete(bullet)
                        self.diag_bullets.remove(bullet_tuple)
                        self.score += 1

            # Move boss bullets
            for boss_bullet in self.boss_bullets[:]:
                self.canvas.move(boss_bullet, 0, boss_speed)
                if self.check_graze(boss_bullet):
                    self.score += 2  # Boss bullets give more TP
                if self.check_collision(boss_bullet):
                    self.lives -= 1
                    self.canvas.delete(boss_bullet)
                    self.boss_bullets.remove(boss_bullet)
                    if self.lives <= 0:
                        self.end_game()
                elif self.canvas.coords(boss_bullet)[1] > 600:
                    self.canvas.delete(boss_bullet)
                    self.boss_bullets.remove(boss_bullet)
                    self.score += 5  # Boss bullets give more score

            # Move quad bullets
            for bullet in self.bullets[:]:
                self.canvas.move(bullet, 0, quad_speed)
                if self.check_graze(bullet):
                    self.score += 1
                if self.check_collision(bullet):
                    self.lives -= 1
                    self.canvas.delete(bullet)
                    self.bullets.remove(bullet)
                    if self.lives <= 0:
                        self.end_game()
                elif self.canvas.coords(bullet)[1] > 600:
                    self.canvas.delete(bullet)
                    self.bullets.remove(bullet)
                    self.score += 2

            # Move zigzag bullets
            for bullet_tuple in self.zigzag_bullets[:]:
                bullet, direction, step_count = bullet_tuple
                # Change direction every 10 steps
                if step_count % 10 == 0:
                    direction *= -1
                self.canvas.move(bullet, 5 * direction, zigzag_speed)
                if self.check_graze(bullet):
                    self.score += 1
                if self.check_collision(bullet):
                    self.lives -= 1
                    self.canvas.delete(bullet)
                    self.zigzag_bullets.remove(bullet_tuple)
                    if self.lives <= 0:
                        self.end_game()
                else:
                    coords = self.canvas.coords(bullet)
                    if coords[1] > 600 or coords[0] < 0 or coords[2] > 800:
                        self.canvas.delete(bullet)
                        self.zigzag_bullets.remove(bullet_tuple)
                        self.score += 2
                    else:
                        # Update tuple with incremented step_count and possibly new direction
                        idx = self.zigzag_bullets.index(bullet_tuple)
                        self.zigzag_bullets[idx] = (bullet, direction, step_count + 1)

            # Move fast bullets
            for fast_bullet in self.fast_bullets[:]:
                self.canvas.move(fast_bullet, 0, fast_speed)
                if self.check_graze(fast_bullet):
                    self.score += 1
                if self.check_collision(fast_bullet):
                    self.lives -= 1
                    self.canvas.delete(fast_bullet)
                    self.fast_bullets.remove(fast_bullet)
                    if self.lives <= 0:
                        self.end_game()
                elif self.canvas.coords(fast_bullet)[1] > 600:
                    self.canvas.delete(fast_bullet)
                    self.fast_bullets.remove(fast_bullet)
                    self.score += 2

            # Move star bullets
            for star_bullet in self.star_bullets[:]:
                self.canvas.move(star_bullet, 0, star_speed)
                if self.check_graze(star_bullet):
                    self.score += 1
                if self.check_collision(star_bullet):
                    self.lives -= 1
                    self.canvas.delete(star_bullet)
                    self.star_bullets.remove(star_bullet)
                    if self.lives <= 0:
                        self.end_game()
                elif self.canvas.coords(star_bullet)[1] > 600:
                    self.canvas.delete(star_bullet)
                    self.star_bullets.remove(star_bullet)
                    self.score += 3

            # Move rectangle bullets
            for rect_bullet in self.rect_bullets[:]:
                self.canvas.move(rect_bullet, 0, rect_speed)
                if self.check_graze(rect_bullet):
                    self.score += 1
                if self.check_collision(rect_bullet):
                    self.lives -= 1
                    self.canvas.delete(rect_bullet)
                    self.rect_bullets.remove(rect_bullet)
                    if self.lives <= 0:
                        self.end_game()
                elif self.canvas.coords(rect_bullet)[1] > 600:
                    self.canvas.delete(rect_bullet)
                    self.rect_bullets.remove(rect_bullet)
                    self.score += 2
            self.root.after(50, self.update_game)


    def check_graze(self, bullet):
        """
        Returns True if player is close to the bullet (grazing), but not colliding.
        """
        bullet_coords = self.canvas.coords(bullet)
        player_coords = self.canvas.coords(self.player)
        # If already colliding, not grazing
        if self.check_collision(bullet):
            return False
        # Calculate closest distance between player and bullet
        px = (player_coords[0] + player_coords[2]) / 2
        py = (player_coords[1] + player_coords[3]) / 2
        bx = (bullet_coords[0] + bullet_coords[2]) / 2
        by = (bullet_coords[1] + bullet_coords[3]) / 2
        dist = ((px - bx) ** 2 + (py - by) ** 2) ** 0.5
        return dist < self.graze_distance


    def check_collision(self, bullet):
        bullet_coords = self.canvas.coords(bullet)
        player_coords = self.canvas.coords(self.player)
        return (bullet_coords[2] > player_coords[0] and
                bullet_coords[0] < player_coords[2] and
                bullet_coords[3] > player_coords[1] and
                bullet_coords[1] < player_coords[3])

    def end_game(self):
        self.game_over = True
        self.gamerunning = False
        ei = self.canvas.create_text(400, 300, text="Game Over", fill="white", font=("Arial", 30))
        er = self.canvas.create_text(400, 350, text=f"Score: {self.score}", fill="white", font=("Arial", 20))
        we = self.canvas.create_text(400, 400, text=f"Time Survived: {int(time.time() - self.timee)} seconds", fill="white", font=("Arial", 20))
        time.sleep(1)
        self.canvas.delete(ei)
        self.canvas.delete(er)
        self.canvas.delete(we)
        self.restartdialog()

if __name__ == "__main__":
    root = tk.Tk()
    game = bullet_hell_game(root)
    # Example usage: show dialog at start
    game.show_dialog([
        "Welcome to My Lair!",
        "Use arrow keys to move.",
        "Avoid my attacks and survive as long as you can!"
    ])
    root.mainloop()