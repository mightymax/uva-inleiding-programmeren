import tkinter
from tkinter import Label, Button
import sys
import os
import random

root = tkinter.Tk()
root.title("Small Shark, Big Pond!")

canvas_width = 1000
canvas_height = 800
canvas = tkinter.Canvas(root, width=canvas_width, height=canvas_height)
canvas.config(bg="lightskyblue")
canvas.pack()
canvas.focus_set()
time = 0
planktons = []
fish_list = []
game_valid = True

class Keyboard:
    def __init__(self):
        self.keys = {}
    
    def key_down(self, key):
        self.keys[key] = True
    
    def key_up(self, key):
        self.keys[key] = False
    
    def is_down(self, key):
        if key in self.keys:
            return self.keys[key]
        return False

keyboard = Keyboard()

class PosRad:
    def __init__(self, x, y, rad):
        self.x = x
        self.y = y
        self.rad = rad

    def is_in_collision(self, p2):
        dx = self.x-p2.x
        dy = self.y-p2.y
        sr = self.rad+p2.rad
        return dx*dx+dy*dy<sr*sr

class Plankton:
    min_speed = 1
    max_speed = 3

    def __init__(self, x, y):
        self.posrad = PosRad(x, y, 2)
        self.speed = random.uniform(Plankton.min_speed, Plankton.max_speed)

    def time_step(self):
        self.posrad.x -= self.speed
        if self.posrad.x < 0:
            planktons.remove(self)

    def draw(self):
        canvas.create_oval(self.posrad.x - self.posrad.rad, self.posrad.y - self.posrad.rad, \
                            self.posrad.x + self.posrad.rad, self.posrad.y + self.posrad.rad, \
                            fill="dark green", outline="dark green")

class Fish:
    min_size = 7
    max_size = 40
    min_speed = 2
    max_speed = 6
    colors = ['red', 'darkblue', 'darkorange', 'purple', 'darkgreen', 'coral', 'midnightblue', 'darkgoldenrod', 'chocolate', \
                'lightcoral', 'blueviolet', 'deeppink']

    def __init__(self, x, y):
        if Shark.size > 30:
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
            fish_list.remove(self)

    def draw(self):
        canvas.create_oval(self.posrad.x - self.posrad.rad, self.posrad.y - self.posrad.rad, \
                            self.posrad.x + self.posrad.rad, self.posrad.y + self.posrad.rad, \
                            fill=self.color, outline='black')

def game_loss():
    global game_valid
    canvas.create_text(canvas_width/2,canvas_height/2,text="Game Over", \
                            font=('arial 60 bold'), fill='firebrick')
    game_valid = False

def game_won():
    global game_valid
    canvas.create_text(canvas_width/2,canvas_height/2,text="You Win!", \
                            font=('arial 60 bold'), fill='firebrick')
    game_valid = False

class Shark:
    size_start = 10
    size = 10
    speed = 0.2
    air_resistance = 0.985
    counter = 0

    def __init__(self, x, y):
        self.posrad = PosRad(x, y, Shark.size_start)
        self.vx = 0
        self.vy = 0

    def time_step(self):
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

    def collision_detect(self, fish_list, planktons):
        for i in fish_list:
            if self.posrad.is_in_collision(i.posrad) and self.posrad.rad > i.posrad.rad:
                fish_list.remove(i)
                Shark.size += 0.75
                Shark.counter += 1
            elif self.posrad.is_in_collision(i.posrad) and self.posrad.rad < i.posrad.rad:
                game_loss()
        for i in planktons:
            if self.posrad.is_in_collision(i.posrad) and self.posrad.rad > i.posrad.rad:
                planktons.remove(i)
                Shark.size += 0.15
                Shark.counter += 1
    
    def detect_win_condition(self):
        if Shark.size == 51:
            game_won()

    def draw(self):
        canvas.create_oval(self.posrad.x - self.posrad.rad, self.posrad.y - self.posrad.rad, \
                            self.posrad.x + self.posrad.rad, self.posrad.y + self.posrad.rad, \
                            fill="royalblue", outline = "navy", width=4)

    def growth(self):
        self.posrad = PosRad(self.posrad.x, self.posrad.y, Shark.size)
        canvas.create_oval(self.posrad.x - self.posrad.rad, self.posrad.y - self.posrad.rad, \
                            self.posrad.x + self.posrad.rad, self.posrad.y + self.posrad.rad, \
                            fill="royalblue", outline = "navy", width=4)

avr_plankton_time = 20
avr_fish_time = 11
if Shark.size > 30:
    avr_fish_time = 30
shark = Shark(canvas_width/2, canvas_height/2)

def time_step():
    global time, game_valid

    if False == game_valid:
        return
    canvas.delete("all")
    if random.randint(0, avr_plankton_time)==0:
        plankton = Plankton(canvas.winfo_width(), random.randint(0, canvas.winfo_height()))
        planktons.append(plankton)
    if random.randint(0, avr_fish_time)==0:
        fish = Fish(canvas.winfo_width(), random.randint(0, canvas.winfo_height()))
        fish_list.append(fish)
    for i in planktons:
        i.time_step()
        i.draw()
    if shark.counter == 0:
        shark.draw() 
        shark.time_step()
    elif shark.counter > 0:
        shark.growth()
        shark.time_step()
    for i in fish_list:
        i.time_step()
        i.draw()
    shark.collision_detect(fish_list, planktons)
    shark.detect_win_condition()
    time += 1
    root.after(10, time_step)

def key_down(e):
    keyboard.key_down(e.keysym)

def key_up(e):
    keyboard.key_up(e.keysym)

#def restart_program():
#    python = sys.executable
#    os.execl(python, python * sys.argv)

def main():
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    root.update()
    root.after(100, time_step)
    #print("calling mainloop()")
    root.mainloop()
    #print("the end!")

if __name__ == '__main__':
    main()