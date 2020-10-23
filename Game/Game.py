import tkinter
from tkinter import Label, Button
import sys
import os
import random
from Tools import Keyboard
from Ocean import Fish, Plankton, Shark

class Game:
    canvas_width = 1000
    canvas_height = 800
    avr_plankton_time = 20
    avr_fish_time = 11
    title = "Small Shark, Big Pond!"

    def __init__(self):
        self.lossed = False
        self.won = False
        self.planktons = []
        self.fishes = [] # was fish_list
        self.time = 0
        
        self.root = tkinter.Tk()
        self.root.title(Game.title)

        self.keyboard = Keyboard()

        self.init_canvas()

        if Shark.size > 30:
            Game.avr_fish_time = 30

        self.shark = Shark(self, Game.canvas_width/2, Game.canvas_height/2)

    def init_canvas(self):
        self.canvas = tkinter.Canvas(self.root, width=Game.canvas_width, height=Game.canvas_height)
        self.canvas.config(bg="lightskyblue")
        self.canvas.pack()
        self.canvas.focus_set()

    def loose(self):
        self.canvas.create_text(Game.canvas_width/2,Game.canvas_height/2,text="Game Over", font=('arial 60 bold'), fill='firebrick')
        self.lossed = True

    def win(self):
        self.canvas.create_text(Game.canvas_width/2,Game.canvas_height/2,text="You Win!", font=('arial 60 bold'), fill='firebrick')
        self.won = True

    def start(self):
        self.root.after(1000, self.time_step)
        self.root.mainloop()

    def play(self):
        self.root.update()

    def time_step(self):
        if True == self.won or True == self.lossed:
            return

        self.canvas.delete("all")
        if random.randint(0, Game.avr_plankton_time)==0:
            plankton = Plankton(self, self.canvas.winfo_width(), random.randint(0, self.canvas.winfo_height()))
            self.planktons.append(plankton)
        if random.randint(0, Game.avr_fish_time)==0:
            fish = Fish(self, self.canvas.winfo_width(), random.randint(0, self.canvas.winfo_height()))
            self.fishes.append(fish)
        for i in self.planktons:
            i.time_step()
            i.draw()

        if self.shark.counter == 0:
            self.shark.draw() 
            self.shark.time_step()

        elif self.shark.counter > 0:
            self.shark.growth()
            self.shark.time_step()

        for fish in self.fishes:
            fish.time_step()
            fish.draw()

        self.shark.collision_detect()
        self.shark.detect_win_condition()
        self.time += 1
        self.root.after(10, self.time_step)

    def key_down(self, e):
        self.keyboard.key_down(e.keysym)

    def key_up(self, e):
        self.keyboard.key_up(e.keysym)

if __name__ == '__main__':
    game = Game()
    game.root.bind("<KeyPress>", game.key_down)
    game.root.bind("<KeyRelease>", game.key_up)
    game.start()