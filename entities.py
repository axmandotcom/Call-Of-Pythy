# -*- coding: utf-8 -*-
"""
Created on Fri May  3 20:27:44 2024

@author: Axman
"""
import pygame, math, random
from utils import *
from settings import *
#Entities
class Character:
    def __init__(self, direction, size, position):
        self.position = position
        self.face = pygame.draw.circle(WIN, SKIN_COLORS[2], self.position, radius = size)
        self.sight = pygame.draw.line(WIN, BLACK, self.position, direction, width = 2)
        self.detection_sight = pygame.draw.polygon(WIN, BLACK, TRIANGLE)

class Enemy:
    def __init__(self, enemy_pos, size, player, life):
        self.life = life
        self.position = enemy_pos
        self.size = size
        self.color = GREEN
        self.index = len(enemies)
        #self.face = pygame.draw.polygon(WIN, GREEN)
        self.box = pygame.draw.circle(WIN, self.color, self.position, radius = self.size)
        self.sight_vertices = [self.position, ((self.position[0] - size),(self.position[1] - 4*size)), ((self.position[0] + size),(self.position[1] - 4*size))]
        self.detection_sight = pygame.draw.polygon(WIN, BLACK, self.sight_vertices)
        self.distance_to_player = math.sqrt((self.position[0] - player.position[0])**2 + (self.position[1] - player.position[1])**2)
        #self.distance_to_player = round(self.distance_to_player, 3)

class Ammo:
    def __init__(self, position, angle):
        self.damage = 20
        self.position = position
        self.angle = angle
        self.velocity = 3
        self.index = len(bullets_fired)
        self.box = pygame.draw.circle(WIN, YELLOW, self.position, radius = 5)
    def draw(self, position, angle, velocity):
        if not seeking_bullets:
            self.position = move(position, velocity, angle)
        else:
            self.position = prosecute(zombie, self, velocity/2)
        self.box = pygame.draw.circle(WIN, YELLOW, self.position, radius = 5)