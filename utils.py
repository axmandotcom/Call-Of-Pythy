# -*- coding: utf-8 -*-
"""
Created on Fri May  3 21:16:16 2024

@author: Axman
"""
import pygame, math, sys, os, random
pygame.init()
#from settings import*
#from entities import *
#from Call_Of_Pythy import Enemy, Character
def rotate(center, angle, hypotenuse):
    angle = math.radians(angle)
    pos_x = center[0] + math.sin(angle)*hypotenuse
    pos_y = center[1] - math.cos(angle)*hypotenuse
    direction = (pos_x, pos_y)
    return direction

def move(point, movement, angle):
    turn = math.radians(angle)
    horizontal = point[0]+(movement*math.sin(turn))
    vertical = point[1]-(movement*math.cos(turn))
    return (horizontal, vertical)

def chase(target, entity, movement):
    distance_to_target = math.sqrt((target.position[0] - entity.position[0])**2 + (target.position[1] - entity.position[1])**2)
    points_angle_x = (target.position[0] - entity.position[0]) / distance_to_target
    points_angle_y = (target.position[1] - entity.position[1]) / distance_to_target
    
    entity_x = entity.position[0] + points_angle_x * movement
    entity_y = entity.position[1] + points_angle_y * movement
    return (entity_x, entity_y)
"""
#This function was AI written:    
def prosecute(target, entity, movement):
    #Move the entity towards the target.
    # Calculate vector from entity to target
    vector_to_target = pygame.Vector2(target.position) - pygame.Vector2(entity.position)

    # If the distance is greater than movement, move directly towards target
    if vector_to_target.length() > movement:
        # Scale the vector to the desired movement
        movement_vector = vector_to_target.normalize() * movement
    
        # Move the zombie
        new_position = pygame.Vector2(entity.position) + movement_vector
    
        return new_position.x, new_position.y
    else:
        #If the distance is less than movement, move directly to target's position
        return target.position"""
    
def two_points_distance(point1, point2):
    distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    return distance

def distance_trigger(target, entity, trigger_distance):
    distance_to_target = two_points_distance(target.position, entity.position)
    if distance_to_target < trigger_distance:
        return True
    else:
        return False

#This functions is supposed to change the angle of a bullet when they're homming bullets
def angle_changed(entity, target):
    angle_x = (target[0] - entity[0])/two_points_distance(entity, target)
    angle_y = (target[1] - entity[1])/two_points_distance(entity, target)
    total_angle = math.degrees(angle_x)
    return total_angle

def rotate_point(center, point, angle):
    #Rotate a point counterclockwise by a given angle around a given origin.
    angle = math.radians(angle)
    ox, oy = center
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

#Function to call resources the right way (AI generated function)
def resource_path(relative_path):
    try:
        # PyInstaller creates a normal tmp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, 'assets', relative_path)

#Chase_trigger:
def chase_trigger(enemies, player, frame, WIDTH, HEIGHT):
    for zombie in enemies:
        original = two_points_distance((800,800), (0,0))
        adjustment = two_points_distance((WIDTH, HEIGHT), (0,0))
        if distance_trigger(player, zombie, 200):
            zombie.position = chase(player, zombie, 150*(frame/1000)*(original/adjustment))

#Random_sprite_selection:
def random_sprite():
    number = random.randint(0,(len(sprites_list)-1))
    return number
#Sounds:
#Weapons:
auto_fire = pygame.mixer.Sound(resource_path('Game_machine_gun.ogg'))
auto_fire_playing = False
auto_fire.set_volume(0.6)

single_shot = pygame.mixer.Sound(resource_path('Gun_shot.ogg'))
single_shot_playing = False
single_shot.set_volume(0.5)

shotgun = pygame.mixer.Sound(resource_path('shotgun_echo.ogg'))
shotgun.set_volume(0.6)
#Music soundtracks
BGM_music = pygame.mixer.Sound(resource_path('Graveyard_Shift.ogg'))

#Environmental sound effects:
zombie_death = pygame.mixer.Sound(resource_path('Zombie_killed.ogg'))
zombie_death.set_volume(0.7)
#Textures:
#Enemies:
zombie_sprite = pygame.image.load(resource_path("zombie_face_male.png"))
zombie_sprite2 = pygame.image.load(resource_path("zombie_face_female.png"))
sprites_list = [zombie_sprite, zombie_sprite2]
#Player
player_sprite = pygame.image.load(resource_path("player.png"))
#Weapons:
Gun = pygame.image.load(resource_path("Gun.png"))