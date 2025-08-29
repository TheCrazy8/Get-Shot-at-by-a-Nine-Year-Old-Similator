import tkinter as tk
import random
import time

class bullet_hell_game:
    def __init__(self, root):
        self.root = root
        self.root.title("Bullet Hell Game")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="black")
        self.canvas.pack()
        self.player = self.canvas.create_rectangle(390, 550, 410, 570, fill="blue")
        self.bullets = []
        self.bullets2 = []
        self.diag_bullets = []
        self.boss_bullets = []
        self.zigzag_bullets = []
        self.fast_bullets = []
        self.score = 0
        self.lives = 1
        self.game_over = False
        self.root.bind("<KeyPress>", self.move_player)
        self.update_game()

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

    def shoot_bullet(self):
        if not self.game_over:
            x = random.randint(0, 780)
            bullet = self.canvas.create_oval(x, 0, x + 20, 20, fill="red")
            self.bullets.append(bullet)

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
        if not self.game_over:
            if random.randint(1, 20) == 1:
                self.shoot_bullet()
            if random.randint(1, 20) == 1:
                self.shoot_bullet2()
            if random.randint(1, 40) == 1:
                self.shoot_diag_bullet()
            if random.randint(1, 100) == 1:
                self.shoot_boss_bullet()
            if random.randint(1, 60) == 1:
                self.shoot_zigzag_bullet()
            if random.randint(1, 30) == 1:
                self.shoot_fast_bullet()

            # Move vertical bullets
            for bullet in self.bullets[:]:
                self.canvas.move(bullet, 0, 10)
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
                self.canvas.move(bullet2, 10, 0)
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

            # Move diagonal bullets
            for bullet_tuple in self.diag_bullets[:]:
                bullet, direction = bullet_tuple
                self.canvas.move(bullet, 7 * direction, 7)
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
                self.canvas.move(boss_bullet, 0, 15)
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

            # Move zigzag bullets
            for bullet_tuple in self.zigzag_bullets[:]:
                bullet, direction, step_count = bullet_tuple
                # Change direction every 10 steps
                if step_count % 10 == 0:
                    direction *= -1
                self.canvas.move(bullet, 5 * direction, 8)
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
                self.canvas.move(fast_bullet, 0, 20)
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
        self.canvas.create_text(400, 300, text="Game Over", fill="white", font=("Arial", 30))
        self.canvas.create_text(400, 350, text=f"Score: {self.score}", fill="white", font=("Arial", 20))

if __name__ == "__main__":
    root = tk.Tk()
    game = bullet_hell_game(root)
    root.mainloop()