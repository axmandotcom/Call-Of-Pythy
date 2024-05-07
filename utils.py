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

def prosecute(target, entity, movement):
    distance_to_target = math.sqrt((target.position[0] - entity.position[0])**2 + (target.position[1] - entity.position[1])**2)
    points_angle_x = (target.position[0] - entity.position[0]) / distance_to_target
    points_angle_y = (target.position[1] - entity.position[1]) / distance_to_target
    #points_angle_x = (entity.position[0] - target.position[0]) / distance_to_target
    #points_angle_y = (entity.position[1] - target.position[1]) / distance_to_target
    
    entity_x = entity.position[0] + points_angle_x * movement
    entity_y = entity.position[1] + points_angle_y * movement
    return (entity_x, entity_y)

def distance_trigger(target, entity, trigger_distance):
    distance_to_target = math.sqrt((target.position[0] - entity.position[0])**2 + (target.position[1] - entity.position[1])**2)
    if distance_to_target < trigger_distance:
        return True
    else:
        return False
"""    
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

#This functions is supposed to change the angle of a bullet when they're homming bullets
def angle_changed(reference, origin):
    angle_x = (reference[0] - origin[0])/two_points_distance(reference, origin)
    angle_y = (reference[1] - origin[1])/two_points_distance(reference, origin)
    total_angle = math.degrees(angle_x + angle_y)
    return total_angle

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