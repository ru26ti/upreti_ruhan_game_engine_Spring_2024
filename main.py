# This file was created by: Ruhan Upreti
# per 4 is the best period
# import libraries and modules
# my first source control edit
# Create a fun, challenging, and engaging game for all!
# Goal is for sonic to defeat egmgman, hop into a portal and escape!
'''
Game design truths:
goals, rules, feedback, freedom, what the verb, and will it form a sentence 

Sources: 
Mr. Cozort's course code files and GitHub
Kids can code: https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2001 
'''
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path
import time

# added this math function to round down the clock
from math import floor

# this 'cooldown' class is designed to help  control time
class Cooldown():
    # sets all properties to zero when instantiated...
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # resets event time to zero - cooldown reset
    def countdown(self, x):
        x = x - self.delta
        if x != None:
            return x
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # sets current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)


# Define game class...
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
        self.victory = False
        # added images folder and image in the load_data method for use with the player and enemy
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'Sonic.png')).convert_alpha()
        self.map_data = []
        self.mob_img = pg.image.load(path.join(img_folder, 'eggman.png')).convert_alpha()
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    # Create run method which runs the whole GAME
    def new(self):
        # create timer
        self.test_timer = Cooldown()
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.portal = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        # Gave denomination for tile, coin, mob, player, and powerup to put on map
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row, self.player, 100)
                if tile == 'U':
                    PowerUp(self, col, row)

    def run(self):
        # code to run clock and game once game has started
        self.playing = True
        while self.playing:
            if g.victory: g.show_end_screen()
            else:
                self.dt = self.clock.tick(FPS) / 1000
                self.events()
                self.update()
                self.draw()
            # quit once quit button is pressed
    def quit(self):
         pg.quit()
         sys.exit()

    def update(self):
        # tick the test timer
        self.test_timer.ticking()
        self.all_sprites.update()
    # dimensions of map with sizes imported from settings
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    # font for healthnumber ticker
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)
    # countdown and color variation for health number and how much health coins add once collected
    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            # draw the timer
            self.draw_text(self.screen, str(self.test_timer.countdown(45)), 24, WHITE, WIDTH/2 - 32, 2)
            self.draw_text(self.screen, str(self.player.hitpoints), 100, WHITE, WIDTH/2 - 400,0)
            if self.player.hitpoints >= 51:
                self.draw_text(self.screen, str(self.player.hitpoints), 100, GREEN, WIDTH/2 - 400,0)
            if self.player.hitpoints <= 50:
                self.draw_text(self.screen, str(self.player.hitpoints), 100, YELLOW, WIDTH/2 - 400,0)
            if self.player.hitpoints <= 30:
                self.draw_text(self.screen, str(self.player.hitpoints), 100, RED, WIDTH/2 - 400,0)

            for mob in self.mobs.sprites():
                pg.draw.rect(self.screen, LIGHTGREY, pg.Rect(*Vector2(mob.rect.left, mob.rect.bottom+8), TILESIZE, 5))
                pg.draw.rect(self.screen, RED, pg.Rect(*Vector2(mob.rect.left, mob.rect.bottom+8), mob.hitpoints/mob.max_hitpoints*TILESIZE*2, 5))

            pg.display.flip()

#Power Up
            
    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)
            
    # Switch to Victory screen once player enters portal
    def show_end_screen(self):
        print('Victory')
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, 'Victory!', 60, WHITE, WIDTH/2 - 32, HEIGHT/2)
        pg.display.flip()

        time.sleep(2)

        while True:
            # Check if player presses key
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    g.new()
                    self.victory = False
                    return
                if event.type == pg.QUIT:
                    self.quit()

# Instantiate the game... 
g = Game()
# use game method run to run
# g.show_start_screen()
while True:
    g.new()
    g.run()
    

