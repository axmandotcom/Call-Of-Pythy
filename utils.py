# -*- coding: utf-8 -*-
"""
Created on Fri May  3 21:16:16 2024

@author: Axman
"""
import pygame, math     
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
"""
def prosecute(player, zombie, movement):
    points_angle_x = (player.position[0] - zombie.position[0]) / zombie.distance_to_player
    points_angle_y = (player.position[1] - zombie.position[1]) / zombie.distance_to_player
    if player.position != zombie.position:
        zombie_x = zombie.position[0] + points_angle_x * movement
        zombie_y = zombie.position[1] + points_angle_y * movement
    return (zombie_x, zombie_y)"""

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
        return target.position
def rotate_point(center, point, angle):
    #Rotate a point counterclockwise by a given angle around a given origin.
    angle = math.radians(angle)
    ox, oy = center
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy