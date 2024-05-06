# -*- coding: utf-8 -*-
"""
Created on Fri May  3 21:16:16 2024

@author: Axman
"""
import pygame, math, sys, os
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

def prosecute(target, entity, movement, trigger):
    distance_to_target = math.sqrt((target.position[0] - entity.position[0])**2 + (target.position[1] - entity.position[1])**2)
    points_angle_x = (target.position[0] - entity.position[0]) / distance_to_target
    points_angle_y = (target.position[1] - entity.position[1]) / distance_to_target
    
    entity_x = entity.position[0] + points_angle_x * 0
    entity_y = entity.position[1] + points_angle_y * 0
    if distance_to_target < trigger:
        entity_x = entity.position[0] + points_angle_x * movement
        entity_y = entity.position[1] + points_angle_y * movement
    return (entity_x, entity_y)
"""
def prosecute(target, entity, movement):
    #Move the zombie towards the player.
    # Calculate vector from zombie to player
    vector_to_player = pygame.Vector2(target.position) - pygame.Vector2(entity.position)

    # If the distance is greater than movement, move directly towards player
    if vector_to_player.length() > movement:
        # Scale the vector to the desired movement
        movement_vector = vector_to_player.normalize() * movement

        # Move the zombie
        new_position = pygame.Vector2(entity.position) + movement_vector

        return new_position.x, new_position.y
    else:
        # If the distance is less than movement, move directly to player's position
        return target.position"""
def rotate_point(center, point, angle):
    #Rotate a point counterclockwise by a given angle around a given origin.
    angle = math.radians(angle)
    ox, oy = center
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

#Function to call resources the right way
def resource_path(relative_path):
    try:
        # PyInstaller creates a normal tmp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)