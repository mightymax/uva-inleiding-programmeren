from Tools import PosRad
import random

class Plankton:
    min_speed = 1
    max_speed = 3

    def __init__(self, game, x, y):
        self.game = game
        self.posrad = PosRad(x, y, 2)
        self.speed = random.uniform(Plankton.min_speed, Plankton.max_speed)

    def time_step(self):
        self.posrad.x -= self.speed
        if self.posrad.x < 0:
            self.game.planktons.remove(self)

    def draw(self):
        self.game.canvas.create_oval(self.posrad.x - self.posrad.rad, self.posrad.y - self.posrad.rad, \
                            self.posrad.x + self.posrad.rad, self.posrad.y + self.posrad.rad, \
                            fill="dark green", outline="dark green")

class Shark:
    size_start = 10
    size = 10
    speed = 0.2
    air_resistance = 0.985
    counter = 0

    def __init__(self, game, x, y):
        self.game = game
        self.posrad = PosRad(x, y, Shark.size_start)
        self.vx = 0
        self.vy = 0

    def time_step(self):
        keyboard = self.game.keyboard
        canvas = self.game.canvas

        if keyboard.is_down("Left") or keyboard.is_down("z"):
            self.vx -= Shark.speed
        if keyboard.is_down("Right") or keyboard.is_down("x"):
            self.vx += Shark.speed
        if keyboard.is_down("Up") or keyboard.is_down("'"):
            self.vy -= Shark.speed
        if keyboard.is_down("Down") or keyboard.is_down("/"):
            self.vy += Shark.speed

        self.posrad.x += self.vx
        self.posrad.y += self.vy
        if self.posrad.x < 0:
            self.vx *= -0.9
        if self.posrad.y < 0:
            self.vy *= -0.9
        if self.posrad.x > canvas.winfo_width():
            self.vx *= -0.9
        if self.posrad.y > canvas.winfo_height():
            self.vy *= -0.9 
        self.vx *= Shark.air_resistance
        self.vy *= Shark.air_resistance

    def collision_detect(self):
        for i in self.game.fishes:
            if self.posrad.is_in_collision(i.posrad) and self.posrad.rad > i.posrad.rad:
                self.game.fishes.remove(i)
                Shark.size += 0.75
                Shark.counter += 1
            elif self.posrad.is_in_collision(i.posrad) and self.posrad.rad < i.posrad.rad:
                self.game.loose()
        for i in self.game.planktons:
            if self.posrad.is_in_collision(i.posrad) and self.posrad.rad > i.posrad.rad:
                self.game.planktons.remove(i)
                Shark.size += 0.15
                Shark.counter += 1
    
    def detect_win_condition(self):
        if Shark.size == 51:
            self.game.win()

    def draw(self):
        self.game.canvas.create_oval(self.posrad.x - self.posrad.rad, self.posrad.y - self.posrad.rad, \
                            self.posrad.x + self.posrad.rad, self.posrad.y + self.posrad.rad, \
                            fill="royalblue", outline = "navy", width=4)

    def growth(self):
        self.posrad = PosRad(self.posrad.x, self.posrad.y, Shark.size)
        self.game.canvas.create_oval(self.posrad.x - self.posrad.rad, self.posrad.y - self.posrad.rad, \
                            self.posrad.x + self.posrad.rad, self.posrad.y + self.posrad.rad, \
                            fill="royalblue", outline = "navy", width=4)

class Fish:
    min_size = 7
    max_size = 40
    min_speed = 2
    max_speed = 6
    colors = ['red', 'darkblue', 'darkorange', 'purple', 'darkgreen', 'coral', 'midnightblue', 'darkgoldenrod', 'chocolate', \
                'lightcoral', 'blueviolet', 'deeppink']

    def __init__(self, game, x, y):
        self.game = game
        if game.shark.size > 30:
            Fish.min_size = 25
            Fish.max_size = 50
            Fish.min_speed = 1
            Fish.max_speed = 4
        r = random.uniform(0, 1)
        self.posrad = PosRad(x, y, Fish.min_size + r * (Fish.max_size - Fish.min_size))
        self.vx = Fish.min_speed + r * (Fish.max_speed - Fish.min_speed)
        self.color = (random.choice(Fish.colors))
    
    def time_step(self):
        self.posrad.x -= self.vx
        if self.posrad.x < 0:
            self.game.fishes.remove(self)

    def draw(self):
        self.game.canvas.create_oval(self.posrad.x - self.posrad.rad, self.posrad.y - self.posrad.rad, \
                            self.posrad.x + self.posrad.rad, self.posrad.y + self.posrad.rad, \
                            fill=self.color, outline='black')


