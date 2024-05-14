# -*- coding: utf-8 -*-
"""
Created on Fri May  3 19:42:46 2024

@author: Axman
"""
import pygame
pygame.init()
#Environment variables
WIDTH, HEIGHT = 800, 800
# clock = pygame.time.Clock()
# flags = pygame.RESIZABLE | pygame.HWACCEL | pygame.HWSURFACE
# WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags)
# title = pygame.display.set_caption("Call of Pythy")
# Define the colors palette
WHITE = (255, 255, 255)
PINK = (255,150,255)
GREEN = (0,150,0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 220, 0)
BLUE = (0,0,255)
PURPLE = (255,0,255)
RANDOM_COLORS = [PURPLE, PINK, GREEN, YELLOW, BLUE]
SKINS = [[141, 85, 36], [198, 134, 66], [224, 172, 105], [241, 194, 125], [255, 219, 172]]
SKIN_COLORS = [tuple(SKIN) for SKIN in SKINS]
#print(SKIN_COLORS)

#Other environment variables
fontsize = 20

#Geometric distances
angle = 0
angle2 = 0
size = 25
movement = 300

#Enemy
# #Geometric points
# enemy_pos = ((WIDTH*(3/4)), (HEIGHT*(3/4)))
# position = (WIDTH//2, HEIGHT//2)
# TRIANGLE = [position, (position[0]+size, position[1]-3*size), (position[0]-size, position[1]-3*size)]
# nose = (position[0], position[1] - size)
starting_life = 200

#Weapon parameters:
rifle_fire_rate = 5 #How many shots every 1 second
rifle_accuracy = 2
rifle_timer = 0

shotgun_accuracy = 6
shotgun_fired = False
shotgun_timer = 0
shotgun_fire_rate = 10 #How many shots every 10 seconds
shotgun_bullets_per_shot = 5
seeking_bullets = True

#Initialization:
bullet_speed = 80/100
angle_offset = 270
game_over = False
movement_speed = 60
movement_timer = 0
general_timer = 0
FPS = 0 #0 means unlimited
FULL_DISPLAY = False
bullets_fired = []
enemies = []