import math
from utils.constants import *
from calculations.distance_metrics import distance_3d

def update_classical(compact_object_1, compact_object_2, time_step, initial_distance):

    # Calculate distance and direction
    dx, dy, dz, distance_between_objects = distance_3d(compact_object_1, compact_object_2)

    # Check if distance is greater than initial distance or if a collision happens
    if distance_between_objects > (initial_distance):
        return ('separation')
    
    if distance_between_objects <= (compact_object_1.radius + compact_object_2.radius):
        return('collision')

    direction = (dx / distance_between_objects, dy / distance_between_objects, dz / distance_between_objects)

    # Newton's Universal Law of Gravitation
    force_magnitude = (G * compact_object_1.mass * compact_object_2.mass) / (distance_between_objects ** 2)

    # Acceleration
    acceleration_scalar_1 = force_magnitude / compact_object_1.mass
    acceleration_scalar_2 = force_magnitude / compact_object_2.mass

    acceleration_1 = tuple(acceleration_scalar_1 * component for component in direction)
    acceleration_2 = tuple(acceleration_scalar_2 * component for component in direction)

    # Update velocities and positions
    compact_object_1.update_velocity(acceleration_1, time_step)
    compact_object_2.update_velocity((-acceleration_2[0], -acceleration_2[1], -acceleration_2[2]), time_step)

    compact_object_1.update_position(time_step)
    compact_object_2.update_position(time_step)

    return None
