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
        self.score = 0
        self.lives = 1
        self.game_over = False
        self.root.bind("<KeyPress>", self.move_player)
        self.update_game()

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

    def update_game(self):
        if not self.game_over:
            if random.randint(1, 20) == 1:
                self.shoot_bullet()
            elif random.randint(1, 20) == 1:
                self.shoot_bullet2()
            for bullet in self.bullets:
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
            for bullet2 in self.bullets2:
                self.canvas.move(bullet2, 10, 0)
                if self.check_collision(bullet2):
                    self.lives -= 1
                    self.canvas.delete(bullet2)
                    self.bullets2.remove(bullet2)
                    if self.lives <= 0:
                        self.end_game()
                elif self.canvas.coords(bullet2)[1] > 600:
                    self.canvas.delete(bullet2)
                    self.bullets2.remove(bullet2)
                    self.score += 1
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