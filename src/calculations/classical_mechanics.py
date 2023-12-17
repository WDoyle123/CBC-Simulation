import math
from utils.constants import *
from calculations.distance_metrics import distance_3d

def update_classical(compact_object_1, compact_object_2, time_step, initial_distance):
    # Calculate distance and direction
    dx, dy, dz, distance_between_objects = distance_3d(compact_object_1, compact_object_2)

    # Check for separation or collision
    if distance_between_objects > initial_distance:
        return 'separation'
    if distance_between_objects <= (compact_object_1.radius + compact_object_2.radius):
        return 'collision'

    direction = (dx / distance_between_objects, dy / distance_between_objects, dz / distance_between_objects)

    # Newton's Universal Law of Gravitation
    force_magnitude = (G * compact_object_1.mass * compact_object_2.mass) / (distance_between_objects ** 2)

    # Acceleration
    acceleration_scalar_1 = force_magnitude / compact_object_1.mass
    acceleration_scalar_2 = force_magnitude / compact_object_2.mass

    acceleration_1 = tuple(acceleration_scalar_1 * component for component in direction)
    acceleration_2 = tuple(-acceleration_scalar_2 * component for component in direction)

    # Update velocities and positions
    compact_object_1.update_velocity(acceleration_1, time_step)
    compact_object_2.update_velocity(acceleration_2, time_step)

    compact_object_1.update_position(time_step)
    compact_object_2.update_position(time_step)

    # Energy lost to gravitational waves
    energy_lost_to_gravitational_waves = gw_energy_loss(compact_object_1, compact_object_2, distance_between_objects)
    compact_object_1.kinetic_energy -= energy_lost_to_gravitational_waves
    compact_object_2.kinetic_energy -= energy_lost_to_gravitational_waves
    
    update_velocity_from_kinetic_energy(compact_object_1)
    update_velocity_from_kinetic_energy(compact_object_2)

    return None

def update_orbital_energy(compact_object_1, compact_object_2, distance):
    potential_energy = (-G * compact_object_1.mass * compact_object_2.mass) / distance
    velocity_1 = math.sqrt(compact_object_1.velocity_x**2 + compact_object_1.velocity_y**2 + compact_object_1.velocity_z**2)
    velocity_2 = math.sqrt(compact_object_2.velocity_x**2 + compact_object_2.velocity_y**2 + compact_object_2.velocity_z**2)

    kinetic_energy_1 = (0.5 * compact_object_1.mass) * (velocity_1 ** 2)
    kinetic_energy_2 = (0.5 * compact_object_2.mass) * (velocity_2 ** 2)

    total_energy_1 = kinetic_energy_1 + (potential_energy / 2)
    total_energy_2 = kinetic_energy_2 + (potential_energy / 2)

    return total_energy_1, total_energy_2

def kinetic_energy(compact_object):
    velocity = math.sqrt(compact_object.velocity_x**2 + compact_object.velocity_y**2 + compact_object.velocity_z**2)
    return (0.5 * compact_object.mass * velocity**2)

def gw_energy_loss(compact_object_1, compact_object_2, distance_between_objects):
    mu = (compact_object_1.mass * compact_object_2.mass) / (compact_object_1.mass + compact_object_2.mass)
    orbital_energy_loss = (32/5) * (G**4 / c**5) * (mu**2 * (compact_object_1.mass + compact_object_2.mass)**2) / (distance_between_objects**5)

    return orbital_energy_loss

def update_velocity_from_kinetic_energy(compact_object):
    # Calculate the magnitude of the new velocity
    new_velocity_magnitude = math.sqrt(2 * compact_object.kinetic_energy / compact_object.mass)

    # Update velocity components proportionally
    total_velocity = math.sqrt(compact_object.velocity_x**2 + compact_object.velocity_y**2 + compact_object.velocity_z**2)
    if total_velocity > 0:
        compact_object.velocity_x *= new_velocity_magnitude / total_velocity
        compact_object.velocity_y *= new_velocity_magnitude / total_velocity
        compact_object.velocity_z *= new_velocity_magnitude / total_velocity

def update_classical_no_gw(compact_object_1, compact_object_2, time_step, initial_distance):

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
