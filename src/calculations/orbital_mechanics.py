import math
from utils.constants import *

def update_classical(compact_object_1, compact_object_2, time_step):

    # Calculate distance and direction
    dx = distance(compact_object_1, compact_object_2, 'x')
    dy = distance(compact_object_1, compact_object_2, 'y')
    dz = distance(compact_object_1, compact_object_2, 'z')
    distance_3d = math.sqrt(dx**2 + dy**2 + dz**2)

    # Basic collision detection
    if distance_3d <= (compact_object_1.radius + compact_object_2.radius):
        return True

    direction = (dx / distance_3d, dy / distance_3d, dz / distance_3d)

    # Newton's Universal Law of Gravitation
    force_magnitude = (G * compact_object_1.mass * compact_object_2.mass) / (distance_3d ** 2)

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

    return False

def distance(compact_object_1, compact_object_2, axis):
    return getattr(compact_object_2, axis) - getattr(compact_object_1, axis)

