# This file was created by: Ruhan Upreti
 
# Libraries imported here
import pygame as pg
from settings import *
from sprites import *
import sys
from random import randint
from os import path
 
# Game class is created here
class Game:
    # Methods
    def __init__(self):
        pg.init()
        # Sets the mode of the screen to width and height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # writes text on the display
        pg.display.set_caption("My First Video Game")
        # sets the clock
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.running = True
        # Game info will be stored here later on
        self.load_data()
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        '''
        With statement - content manager
        Used to make sure resources are closed properly
        after they are used. Can prevent errors.
        '''
        #opens the folder map.txt
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
                print(self.map_data)
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        #self.player = Player(self, 10, 10)
       # self.all_sprites.add(self.player)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 'e':
                    self.enemy = Enemy(self, col, row)
#defines when the game is running
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # input
            self.events()
            #  processing
            self.update()
            #  output
            self.draw()
#defs the quit function
    def quit(self):
        pg.quit()
        sys.exit()
    # methods
    def input(self):
        pass
    def update(self):
        self.all_sprites.update()
   #draws the grid of the screen
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
#sets the color of the screen
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
 
    def events(self):
            # listen for events on the keyboard here
            for event in pg.event.get():
                # whit red x = game closes
                if event.type == pg.QUIT:
                    self.quit()
                    print("the game has ended..")
                # controls (keyboard events)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_LEFT:
                #         self.player.move(dx=-1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_RIGHT:
                #         self.player.move(dx=1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_UP:
                #         self.player.move(dy=-1)
                # if event.type == pg.KEYDOWN:
                #     if event.key == pg.K_DOWN:
                #         self.player.move(dy=1)
    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass
#Activates Game
g = Game()
# g.show_go_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()
 
