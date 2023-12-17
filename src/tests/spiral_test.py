import sys
import os
sys.path.append(os.path.abspath('../'))

import math

from calculations.classical_mechanics import update_classical, kinetic_energy, update_classical_no_gw, orbital_velocity
from calculations.distance_metrics import distance_3d
from calculations.parameters import schwarzschild_radius
from entities.compact_object import CompactObject
from visualisation.plotter import plot_3d_scatter_animation, mp4_to_gif
from utils.constants import *

def main():

    mass_1 = 9
    mass_2 = 12
    radius_1 = schwarzschild_radius(mass_1)
    radius_2 = schwarzschild_radius(mass_2)

    # Calculate the center of mass position
    total_mass = mass_1 + mass_2
    separation = 300
    center_of_mass_x = (mass_1 * 0 + mass_2 * separation) / total_mass

    velocity_y_1, velocity_y_2 = orbital_velocity(separation, center_of_mass_x, mass_1, mass_2)

    # Create the compact objects with these velocities
    compact_object_1 = CompactObject(
            x=0,
            y=0.,
            z=0.,
            mass=mass_1,
            radius=radius_1,
            object_type="Black Hole",
            velocity_x=0,
            velocity_y=velocity_y_1,
            velocity_z=0)

    compact_object_2 = CompactObject(
            x=separation,
            y=0.,
            z=0,
            mass=mass_2,
            radius=radius_2,
            object_type="Black Hole",
            velocity_x=0,
            velocity_y=velocity_y_2,
            velocity_z=0)

    # Simulation parameters
    time_step = 2 # Time step in seconds
    current_step = 0
    max_step = 3e+7
    
    _, _, _, initial_distance = distance_3d(compact_object_1, compact_object_2)
    compact_object_1.kinetic_energy = kinetic_energy(compact_object_1)
    compact_object_2.kinetic_energy = kinetic_energy(compact_object_2)

    while True:
        current_step += time_step
        simulation = update_classical(compact_object_1, compact_object_2, time_step, initial_distance)
        if simulation == 'collision' or current_step >= max_step:
            file = '../../figures/test/spirals/simulation_spiral_gw'
            plot_3d_scatter_animation(compact_object_1, compact_object_2, file, separation=separation, trail=160, fps=700)
            mp4_to_gif(f'{file}.mp4', f'{file}.gif')
            break
        if current_step >= max_step:
            break

if __name__ == '__main__':
    main()

