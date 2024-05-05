# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 07:04:07 2024

@author: Axman
"""

import pygame, math, random
from settings import *
from utils import *
#from entities import Character, Enemy
#pygame variables/initializations
pygame.init()
WIDTH, HEIGHT = 800, 800
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
title = pygame.display.set_caption("Call of Pythy")
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
        self.distance_to_player = round(self.distance_to_player, 3)

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

#Geometric points
position = (WIDTH/2, HEIGHT/2)
nose = (position[0], position[1] - size)
TRIANGLE = [position, (WIDTH/2 - size, HEIGHT/2 - 3*size), (WIDTH/2 + size, HEIGHT/2 - 3*size)]

#Geometric params
head_size_hypotenuse = math.sqrt((nose[0] - position[0])**2 + (nose[1] - position[1])**2)
sight_length_hypotenuse = math.sqrt((TRIANGLE[0][0] - TRIANGLE[1][0])**2 + (TRIANGLE[0][1] - TRIANGLE[1][1])**2)

#Initial angles
nose_angle_radians = (nose[0] - position[0]) / head_size_hypotenuse
left_sightpoint_angle = math.degrees((TRIANGLE[1][0] - TRIANGLE[0][0]) / sight_length_hypotenuse)
right_sightpoint_angle = math.degrees((TRIANGLE[2][0] - TRIANGLE[0][0]) / sight_length_hypotenuse)
#print(left_sightpoint_angle)
#print(right_sightpoint_angle)
#print(sight_length_hypotenuse)

#Sounds:
#Weapons:
auto_fire = pygame.mixer.Sound('Game_machine_gun.ogg')
auto_fire_playing = False
auto_fire.set_volume(0.6)

single_shot = pygame.mixer.Sound('Gun_shot.ogg')
single_shot_playing = False
single_shot.set_volume(0.5)

shotgun = pygame.mixer.Sound('shotgun_echo.ogg')
shotgun.set_volume(0.6)
#Music soundtracks
BGM_music = pygame.mixer.music.load('Graveyard_Shift.ogg') #('Graveyard_Shift.mp3')

#Environmental sound effects:
zombie_death = pygame.mixer.Sound('Zombie_killed.ogg')
zombie_death.set_volume(0.7)
#Initializing Entities:
bullets_fired = []
enemies = []    
sight = rotate(position, angle, size)
player = Character(sight, size, position)
enemies.append(Enemy(enemy_pos, size, player, starting_life))
enemies.append(Enemy(((random.randint(0, WIDTH)),(random.randint(0, HEIGHT))), size, player, starting_life))
#sight_vertices = [zombie.position, ((zombie.position[0] - size),(zombie.position[1] - 3*size)), ((zombie.position[0] + size),(zombie.position[1] - 3*size))]
#BGM_music.play()
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play()
initial_position = player.position
#Main game loop
while not game_over:
    frame = clock.tick_busy_loop(FPS)
    
    #Timers:
    movement_timer += frame
    shotgun_timer += frame
    rifle_timer += frame
    general_timer += frame
    #Debugging timers:
    #print(movement_timer)
    #print(shotgun_timer)
    #print(rifle_timer)
    print(f"This frame took {frame} miliseconds")
    
    WIN.fill(RED)
    font = pygame.font.SysFont('comicsans', fontsize)
    text = font.render("P", True, BLACK)
    #radius_point = (position[0], position[1]-size*5)
    keys = pygame.key.get_pressed()
    #Controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    #Close game:
    if keys[pygame.K_q]:
        game_over = True
    #Directions and moving:
    if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and movement_timer >= frame:
        angle -= angle_offset*(frame/1000)
        TRIANGLE[1:3] = [rotate_point(position, vertex, -angle_offset*(frame/1000)) for vertex in TRIANGLE[1:3]]          
    if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and movement_timer >= frame:
        angle += angle_offset*(frame/1000)
        TRIANGLE[1:3] = [rotate_point(position, vertex, angle_offset*(frame/1000)) for vertex in TRIANGLE[1:3]]
    if keys[pygame.K_UP] and movement_timer >= frame:
        position = move(position, movement*(frame/1000), angle)
        TRIANGLE = [move(vertex, movement*(frame/1000), angle) for vertex in TRIANGLE]
    if keys[pygame.K_DOWN] and movement_timer >= frame:
        position = move(position, -movement*(frame/1000), angle)
        TRIANGLE = [move(vertex, -movement*(frame/1000), angle) for vertex in TRIANGLE]
    
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
    #Sound effects:
    if auto_fire_playing and (1000/rifle_fire_rate) < 200 and general_timer > 99:
        general_timer = 0
        auto_fire.play(loops = 0, maxtime = 100)
        auto_fire_playing = False
    if single_shot_playing and (1000/rifle_fire_rate) >= 200:
        single_shot.play(loops = 0)
        single_shot_playing = False
    
    #Multiple bullets firing:
    if keys[pygame.K_s] and not keys[pygame.K_f] and not shotgun_fired:
        shotgun_fired = True
        shotgun_timer = 0
        for n in range(5):
            bullets_fired.append(Ammo(sight, angle + (random.randint(-3*shotgun_accuracy, 3*shotgun_accuracy))))
        print("Miliseconds since last shell:" + str(shotgun_timer))
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
        enemies.append(Enemy(((WIDTH*(3/4)),(HEIGHT*(3/4))), size, player, starting_life))
        enemies.append(Enemy(((random.randint(0, WIDTH)),(random.randint(0, HEIGHT))), size, player, starting_life))
    
    #Positions Calculations
    angle = angle % 360
    sight = rotate(position, angle, size)
    laser_sight = rotate(position, angle, size*100)
    player = Character(laser_sight, size, position)

    #Drawing zombies
    if len(enemies) > 0:
        for zombie in enemies:
            zombie = Enemy(zombie.position, size, player, zombie.life)
            current_life = font.render(str(zombie.life), True, YELLOW)
            WIN.blit(current_life, (zombie.position[0] - current_life.get_width()//2, zombie.position[1] - current_life.get_height()//2))

    #Drawing/firing bullets:
    if len(bullets_fired) > 0:
        for bullet in bullets_fired:
            bullet.velocity = bullet_speed*(frame)
            bullet.draw(bullet.position, bullet.angle, bullet.velocity)
            #Destroying bullets out of out of the screen
            if bullet.position[0] < 0 or bullet.position[0] > WIDTH or bullet.position[1] < 0 or bullet.position[1] > HEIGHT:
                bullets_fired.remove(bullet)
                continue
            #Destroying enemies
            if len(enemies) > 0:
                for zombie in enemies:
                    if bullet.box.colliderect(zombie.box):
                        zombie.life -= bullet.damage
                        bullets_fired.remove(bullet)
                    if zombie.life <= 0:
                        zombie_death.play()
                        enemies.remove(zombie)
            if len(enemies) == 0:
                enemies.append(Enemy(((random.randint(0, WIDTH)),(random.randint(0, HEIGHT))), size, player, starting_life))
  
    WIN.blit(text, (position[0] - text.get_width()//2, position[1] - text.get_height()//2))
    closest_zombie = 0   
    
    #Prosecution Trigger
    if len(enemies) > 0:
        for zombie in enemies:
            #if zombie.distance_to_player < 200 and movement_timer >= (1000/movement_speed):
            if movement_timer >= frame and zombie.detection_sight.colliderect(player.face):
                zombie.position = prosecute(player, zombie, 200*(frame/1000))
    closest_zombie = min([zombie.distance_to_player for zombie in enemies])
    distance = "Stay away!, distance to zombie is: " + str(closest_zombie)
    stay_away = font.render(distance, True, YELLOW)
    WIN.blit(stay_away, (WIDTH//2 - stay_away.get_width()//2 , HEIGHT//2 - stay_away.get_height()//2))

    if general_timer >= 1000:
        general_timer = 0
        moved = math.sqrt((initial_position[0] - player.position[0])**2 + (initial_position[1]-player.position[1])**2)
        initial_position = player.position
        print(f"You have moved {moved} units since the last second")
    if movement_timer >= frame:
        movement_timer = 0
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
print("There were: " + str(len(bullets_fired)) + " bullets")