# This file was created by: Ruhan Upreti
# This code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
from settings import *
from random import choice
import sys
from pygame import Vector2
# Player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # added player image to sprite from the game class...
        self.image = game.player_img
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 250
        self.status = ""
        self.hitpoints = 100
        self.material = True

    # What keys to press to make player move in the respected directions
    def get_keys(self):
        self.vx, self.vy = 0, 0 
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
            self.game.test_timer.event_reset()
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx, dy):
    #         self.x += dx
    #         self.y += dy

    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #     return False
      # collisions of walls for player      
    def collide_with_walls(self, dir):
        if self.material == True:
            if dir == 'x':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    if self.vx > 0:
                        self.x = hits[0].rect.left - self.rect.width
                    if self.vx < 0:
                        self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
            if dir == 'y':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    if self.vy > 0:
                        self.y = hits[0].rect.top - self.rect.height
                    if self.vy < 0:
                        self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    
    # made possible by Aayush's question!
    # collisons with mob and the effects it does; -5 hitpoints
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            for hit in hits: 
                if isinstance(hit, Mob):  
                    if self.status == "Invincible": 
                        print ("You can't hurt me")
                else: 
                    self.hitpoints -= 10  
                    print("Player health:", self.hitpoints)
                    if self.hitpoints <= 0: 
                        print("Game Over")
                        self.game.quit()
            if str(hits[0].__class__.__name__) == "Coin":
                self.hitpoints += 100
            if str(hits[0].__class__.__name__) == "PowerUp":
                print(hits[0].__class__.__name__)
                # powerup voids collisions and lets player goes through walls
                effect = choice(POWER_UP_EFFECTS)
                print(effect)
                if effect == "Invincible":
                    self.status = "Invincible"
            if str(hits[0].__class__.__name__) == "Mob":
                # print(hits[0].__class__.__name__)
                # print("Collided with mob")
                # collisions with mob -5, damage with enemy interaction
                self.hitpoints -= 5
                if self.status == "Invincible":
                    print("you can't hurt me")
            if str(hits[0].__class__.__name__) == "PowerUp":
                self.material = False
          
# collisions with coins, mobs, and powerups
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # added collisions
        self.collide_with_walls('x')
        self.rect.y = self.y
        # added collisions
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.mobs, False)
        
                                                                        
        # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        # if coin_hits:
        #     print("I got a coin")

        # makes game over once health reaches 0
        if self.hitpoints <= 0:             
            print("Game Over")             
            self.game.quit()

        
     
# wall class with collisions to restrict the player    
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
# coin class heals player
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
# powerup class lets player go through walls
class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
# mob class with damage from interactions with players     
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y, target):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(game.mob_img, (TILESIZE*2, TILESIZE*2))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 75
        self.target = target
# collides enemy with walls, so it doesn't go off the map x axis 
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
            self.vx = 0
            self.rect.x = self.x
            # collides enemy with walls, so it doesn't go off the map y axis 
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
            self.vy = 0
            self.rect.y = self.y
    def update(self):
        # self.rect.x += 1
        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt
        
        # if self.rect.x < self.game.player.rect.x:
        #     self.vx = 100
        # if self.rect.x > self.game.player.rect.x:
        #     self.vx = -100    
        # if self.rect.y < self.game.player.rect.y:
        #     self.vy = 100
        # if self.rect.y > self.game.player.rect.y:
        #     self.vy = -100

        # make enemy follow player around as a part of the game
        self.vx, self.vy = (Vector2(self.target.rect.center) - Vector2(self.x, self.y)) / TILESIZE * self.speed
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

