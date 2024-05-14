# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 07:04:07 2024

@author: Axman
"""

import pygame, math, random, sys, os
sys.dont_write_bytecode = True
pygame.init()
from settings import *
from utils import *
#from entities import Character, Enemy, Ammo
#pygame variables/initializations
clock = pygame.time.Clock()
flags = pygame.RESIZABLE | pygame.HWACCEL | pygame.HWSURFACE
WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags)
title = pygame.display.set_caption("Call of Pythy")
#Entities
class Character:
    def __init__(self, direction, size, position, TRIANGLE):
        self.position = position
        self.face = pygame.draw.circle(WIN, SKIN_COLORS[2], self.position, radius = size)
        self.sight = pygame.draw.line(WIN, BLACK, self.position, direction, width = 2)
        WIN.blit(player_sprite, ((self.position[0] - size),(self.position[1]-size)))
        #self.TRIANGLE = TRIANGLE
        #self.detection_sight = pygame.draw.polygon(WIN, BLACK, self.TRIANGLE)

class Enemy:
    def __init__(self, enemy_pos, size, player, life, sprite):
        self.life = life
        self.sprite = sprite
        self.position = enemy_pos
        self.size = size
        self.color = GREEN
        self.index = len(enemies)
        self.box = pygame.draw.circle(WIN, self.color, self.position, radius = self.size)
        WIN.blit(sprites_list[self.sprite], ((self.position[0] - size), (self.position[1]-size)))
        #self.sight_vertices = [self.position, ((self.position[0] - size),(self.position[1] - 4*size)), ((self.position[0] + size),(self.position[1] - 4*size))]
        #self.detection_sight = pygame.draw.polygon(WIN, BLACK, self.sight_vertices)

class Ammo:
    def __init__(self, position, angle):
        self.size = 5
        self.damage = 20
        self.position = position
        self.angle = angle
        self.velocity = 3
        self.index = len(bullets_fired)
        self.box = pygame.draw.circle(WIN, YELLOW, self.position, radius = self.size)
    def draw(self, position):
        self.box = pygame.draw.circle(WIN, YELLOW, position, radius = self.size)
#Geometric points
enemy_pos = ((WIDTH*(3/4)), (HEIGHT*(3/4)))
position = (WIDTH//2, HEIGHT//2)
TRIANGLE = [position, (position[0]+size, position[1]-3*size), (position[0]-size, position[1]-3*size)]
#Initializing Entities:
bullets_fired = []
enemies = []
sight = rotate(position, angle, size*2)
player = Character(sight, size, position, TRIANGLE)
enemies.append(Enemy(enemy_pos, size, player, starting_life, random_sprite()))
enemies.append(Enemy(((random.randint(0, WIDTH)),(random.randint(0, HEIGHT))), size, player, starting_life, random_sprite()))
#sight_vertices = [zombie.position, ((zombie.position[0] - size),(zombie.position[1] - 3*size)), ((zombie.position[0] + size),(zombie.position[1] - 3*size))]
BGM_music.set_volume(0.4)
BGM_music.play(loops = -1)
last_position = player.position
font = pygame.font.SysFont('comicsans', fontsize)
Gun.convert_alpha()
#Main game loop
while not game_over:
    HEIGHT = WIN.get_height()
    WIDTH = WIN.get_width()
    frame = clock.tick_busy_loop(FPS)
    
    #Timers:
    general_timer += frame
    shotgun_timer += frame
    rifle_timer += frame
    general_timer += frame
    #Debugging timers:
    #print(shotgun_timer)
    #print(rifle_timer)
    #print(f"This frame took {frame} miliseconds")
    
    WIN.fill(RED)
    #text = font.render("Player", True, BLACK)
    keys = pygame.key.get_pressed()
    #Close_alternative:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True        
    #Close game:
    if keys[pygame.K_q]:
        game_over = True
    if keys[pygame.K_F12] and general_timer >= 1000 and not FULL_DISPLAY:
        general_timer = 0
        FULL_DISPLAY = True
        WIDTH, HEIGHT = 1920, 1080
        flags = pygame.RESIZABLE | pygame.HWACCEL | pygame.HWSURFACE | pygame.FULLSCREEN
        WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        
        #Characters reallocation on the screen:
        new_player_x = player.position[0]*(WIDTH/800)
        new_player_y = player.position[1]*(HEIGHT/800)
        player.position = (new_player_x, new_player_y)
        for zombie in enemies:
            new_zombie_x = zombie.position[0]*(WIDTH/800)
            new_zombie_y = zombie.position[1]*(HEIGHT/800)
            zombie.position = (new_zombie_x, new_zombie_y)
    if keys[pygame.K_F12] and general_timer >= 1000 and FULL_DISPLAY:
        general_timer = 0
        FULL_DISPLAY = False
        WIDTH, HEIGHT = 800, 800
        flags = pygame.RESIZABLE | pygame.HWACCEL | pygame.HWSURFACE
        WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        #Characters reallocation on the screen:
        new_player_x = player.position[0]*(WIDTH/1920)
        new_player_y = player.position[1]*(HEIGHT/1080)
        player.position = (new_player_x, new_player_y)
        for zombie in enemies:
            new_zombie_x = zombie.position[0]*(WIDTH/1920)
            new_zombie_y = zombie.position[1]*(HEIGHT/1080)
            zombie.position = (new_zombie_x, new_zombie_y)
    Gun_copy = pygame.transform.rotate(Gun, -angle)
    #Directions and moving:
    if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        angle -= angle_offset*(frame/1000)
        angle = angle % 360
        TRIANGLE[1:3] = [rotate_point(position, vertex, -angle_offset*(frame/1000)) for vertex in TRIANGLE[1:3]] 
    if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
        angle += angle_offset*(frame/1000)
        angle = angle % 360
        TRIANGLE[1:3] = [rotate_point(position, vertex, angle_offset*(frame/1000)) for vertex in TRIANGLE[1:3]]
    if keys[pygame.K_UP]:
        position = move(position, movement*(frame/1000), angle)
        TRIANGLE = [move(vertex, movement*(frame/1000), angle) for vertex in TRIANGLE]
    if keys[pygame.K_DOWN]:
        position = move(position, -movement*(frame/1000), angle)
        TRIANGLE = [move(vertex, -movement*(frame/1000), angle) for vertex in TRIANGLE]
    if keys[pygame.K_a] and general_timer >= 1000:
        seeking_bullets = not seeking_bullets
    
    #Single bullets firing:
    if keys[pygame.K_f] and rifle_timer >= (1000/rifle_fire_rate):
        bullets_fired.append(Ammo(sight, angle + (random.randint(-3*rifle_accuracy, 3*rifle_accuracy))))
        print("There are: " + str(len(bullets_fired)) + " bullets on the screen")
        auto_fire_playing = True
        single_shot_playing = True
        if keys[pygame.K_PLUS] and not keys[pygame.K_MINUS]:
            if rifle_fire_rate >= 1:
                rifle_fire_rate += 1
        if keys[pygame.K_MINUS] and not keys[pygame.K_PLUS]:
            if rifle_fire_rate >= 2:
                rifle_fire_rate -= 1
    #Weapon sound effects:
    if auto_fire_playing and (1000/rifle_fire_rate) < 200 and general_timer > 50:
        general_timer = 0
        auto_fire.play(loops = 0, maxtime = 100)
        auto_fire_playing = False
    if single_shot_playing and (1000/rifle_fire_rate) >= 200:
        single_shot.play(loops = 0)
        single_shot_playing = False
    
    #Multiple bullets/shotgun firing:
    if keys[pygame.K_s] and not keys[pygame.K_f] and not shotgun_fired:
        shotgun_fired = True
        shotgun_timer = 0
        for n in range(shotgun_bullets_per_shot):
            bullets_fired.append(Ammo(sight, angle + (random.randint(-3*shotgun_accuracy, 3*shotgun_accuracy))))
        #print("Miliseconds since last shell:" + str(shotgun_timer))
        if 10000/shotgun_fire_rate >= 1000:
            shotgun.play(loops = 0)
        else:
            shotgun.play(loops = 0, maxtime = 10000//shotgun_fire_rate)
        if keys[pygame.K_PLUS] and not keys[pygame.K_MINUS]:
            if shotgun_fire_rate >= 1:
                shotgun_fire_rate += 1
        if keys[pygame.K_MINUS] and not keys[pygame.K_PLUS]:
            if shotgun_fire_rate >= 2:
                shotgun_fire_rate -= 1
    #print("There are: " + str(len(bullets_fired)) + " bullets on the screen")
    
    #Reset_Game_State
    if keys[pygame.K_r]:
        bullets_fired.clear()
        angle = 0
        position = (WIDTH/2, HEIGHT/2)
        TRIANGLE = [position, (WIDTH/2+size, HEIGHT/2-3*size), (WIDTH/2-size, HEIGHT/2-3*size)]
        enemies.clear()
        enemies.append(Enemy(((WIDTH*(3/4)),(HEIGHT*(3/4))), size, player, starting_life, random_sprite()))
        enemies.append(Enemy(((random.randint(0, WIDTH)),(random.randint(0, HEIGHT))), size, player, starting_life, random_sprite()))
    
    #Positions Calculations
    sight = rotate(position, angle, size*2)
    laser_sight = rotate(position, angle, size*100)
    #Draw Call
    player = Character(laser_sight, size, position, TRIANGLE)
    WIN.blit(Gun_copy, ((sight[0] - Gun_copy.get_width()/2),(sight[1] - Gun_copy.get_height()/2)))
    #Drawing zombies
    if len(enemies) > 0:
        for zombie in enemies:
            zombie = Enemy(zombie.position, size, player, zombie.life, zombie.sprite)
            current_life = font.render(str(zombie.life), True, YELLOW)
            WIN.blit(current_life, (zombie.position[0] - current_life.get_width()//2, zombie.position[1] + current_life.get_height()*0.25))
    #Drawing/firing bullets:
    if len(bullets_fired) > 0:
        original = two_points_distance((800,800), (0,0))
        adjustment = two_points_distance((WIDTH, HEIGHT), (0,0))
        for bullet in bullets_fired:
            bullet.velocity = bullet_speed*(frame)*(adjustment/original)
            if len(enemies) > 0:
                zombie_to_bullet_distances = [two_points_distance(bullet.position, zombie.position) for zombie in enemies]
                smallest_zombie_distance = min(zombie_to_bullet_distances)
                nearest_zombie_index = zombie_to_bullet_distances.index(smallest_zombie_distance)
            #Chasing Trigger:
            if not seeking_bullets:
                bullet.position = move(bullet.position, bullet.velocity, bullet.angle)
                bullet.draw(bullet.position)
                if len(enemies) > 0:
                    if distance_trigger(enemies[nearest_zombie_index], bullet, size):
                        enemies[nearest_zombie_index].life -= bullet.damage
                        bullets_fired.remove(bullet)
                    if enemies[nearest_zombie_index].life <= 0:
                        enemies.pop(nearest_zombie_index)
                        zombie_death.play()
                    if len(enemies) == 0:
                        for n in range(random.randint(1,5)):
                            enemies.append(Enemy(((random.randint(0, WIDTH)),(random.randint(0, HEIGHT))), size, player, starting_life, random_sprite()))
            else:
                bullet.draw(bullet.position)
                if len(enemies) > 0:
                    if smallest_zombie_distance < 200:
                        bullet.position = chase(enemies[nearest_zombie_index], bullet, bullet.velocity)
                        #bullet.angle = angle_changed(bullet.position, enemies[nearest_zombie_index].position)
                        if two_points_distance(bullet.position, enemies[nearest_zombie_index].position) < enemies[nearest_zombie_index].size:
                            enemies[nearest_zombie_index].life -= bullet.damage
                            bullets_fired.remove(bullet)
                            if enemies[nearest_zombie_index].life <= 0:
                                enemies.pop(nearest_zombie_index)
                                zombie_death.play()
                            if len(enemies) == 0:
                                for n in range(random.randint(1,5)):
                                    enemies.append(Enemy(((random.randint(0, WIDTH)),(random.randint(0, HEIGHT))), size, player, starting_life, random_sprite()))
                    else:
                        bullet.position = move(bullet.position, bullet.velocity, bullet.angle)
            if bullet.position[0] < 0 or bullet.position[0] > WIDTH or bullet.position[1] < 0 or bullet.position[1] > HEIGHT:
                bullets_fired.remove(bullet)
                
    #WIN.blit(text, (position[0] - text.get_width()//2, position[1] - text.get_height()//2))
    
    #Warning Message
    if len(enemies) > 0:
        chase_trigger(enemies, player, frame, WIDTH, HEIGHT)
        last_frame = f"Last frame took {frame} miliseconds, there are {len(bullets_fired)} on the screen"
        closest_zombie = min([two_points_distance(zombie.position, player.position) for zombie in enemies])
        distance = f"Stay away!, distance to closest zombie is: {round(closest_zombie, 3)}"
        stay_away = font.render(distance, True, YELLOW)
        game_stats = font.render(last_frame, True, YELLOW)
        WIN.blit(stay_away, (WIDTH//2 - stay_away.get_width()//2 , HEIGHT//2 - stay_away.get_height()//2))
        WIN.blit(game_stats, (WIDTH//2 - game_stats.get_width()//2, HEIGHT//2 + stay_away.get_height()))
    if general_timer >= 1000:
        general_timer = 0
        moved = two_points_distance(last_position, player.position)
        last_position = player.position
        #print(f"You have moved {moved} units since the last second")

    #Timing reset:
    if general_timer >= 1000:
        general_timer = 0
    if rifle_timer >= round(1000/rifle_fire_rate, 3):
        rifle_timer = 0
    if shotgun_timer >= round(10000/shotgun_fire_rate, 3) and shotgun_fired:
        shotgun_fired = False
    elif shotgun_timer >= round(10000/shotgun_fire_rate, 3):
        #print("Miliseconds since the last shell: " + str(shotgun_timer))
        shotgun_timer = round(10000/shotgun_fire_rate, 3)
    pygame.display.flip()
movement_timer = 0
shotgun_timer = 0
rifle_timer = 0
general_timer = 0
pygame.quit()
print(f"There were {len(bullets_fired)} on the screen")