import sys
import os
sys.path.append(os.path.abspath('../'))

import math

from calculations.classical_mechanics import update_classical, kinetic_energy, update_classical_no_gw
from calculations.distance_metrics import distance_3d
from calculations.parameters import schwarzschild_radius
from entities.compact_object import CompactObject
from visualisation.plotter import plot_3d_scatter_animation, mp4_to_gif

def main():

    # Example initialisation of two compact objects
    mass_1 = 80
    mass_2 = 60
    radius_1 = schwarzschild_radius(mass_1)
    radius_2 = schwarzschild_radius(mass_2)

    separation = 500

    compact_object_1 = CompactObject(x=0.,
                                     y=0.,
                                     z=0.,
                                     mass=mass_1,
                                     radius=radius_1, 
                                     object_type="Black Hole", 
                                     velocity_x=0.01, 
                                     velocity_y=0.05, 
                                     velocity_z=0.05)

    compact_object_2 = CompactObject(x=separation,
                                     y=separation, 
                                     z=separation, 
                                     mass=mass_2, 
                                     radius=radius_2, 
                                     object_type="Black Hole", 
                                     velocity_x=-0.00, 
                                     velocity_y=-0.00, 
                                     velocity_z=-0.00)

    # Simulation parameters
    time_step = 8 # Time step in seconds
    current_step = 0
    max_step = 5e+6

    _, _, _, initial_distance = distance_3d(compact_object_1, compact_object_2)
    compact_object_1.kinetic_energy = kinetic_energy(compact_object_1)
    compact_object_2.kinetic_energy = kinetic_energy(compact_object_2)

    while True:
        current_step += time_step
        simulation = update_classical(compact_object_1, compact_object_2, time_step, initial_distance)
        if simulation == 'separation' or simulation == 'collision':
            file = '../../figures/test/energy_loss/simulation_gw'
            plot_3d_scatter_animation(compact_object_1, compact_object_2, file, separation=separation, trail=120, fps=240)
            mp4_to_gif(f'{file}.mp4', f'{file}.gif')
            break
        if current_step >= max_step:
            break

    separation = 5e+3
    time_step = 1000
    current_step = 0 

    # No gravitational wave energy loss
    compact_object_3 = CompactObject(x=0., 
                                     y=0., 
                                     z=0., 
                                     mass=mass_1, 
                                     radius=radius_1, 
                                     object_type="Black Hole", 
                                     velocity_x=0.01, 
                                     velocity_y=0.05, 
                                     velocity_z=0.05)
    
    compact_object_4 = CompactObject(x=separation, 
                                     y=separation, 
                                     z=separation, 
                                     mass=mass_2, 
                                     radius=radius_2, 
                                     object_type="Black Hole", 
                                     velocity_x=-0.00, 
                                     velocity_y=-0.00, 
                                     velocity_z=-0.00
                                     )

    _, _, _, initial_distance = distance_3d(compact_object_3, compact_object_4)
    compact_object_3.kinetic_energy = kinetic_energy(compact_object_3)
    compact_object_4.kinetic_energy = kinetic_energy(compact_object_4)

    while True:
        simulation = update_classical_no_gw(compact_object_3, compact_object_4, time_step, initial_distance)
        if simulation == 'separation' or simulation == 'collision':
            file = '../../figures/test/energy_loss/simulation_no_gw'
            plot_3d_scatter_animation(compact_object_3, compact_object_4, file, separation, trail=30, fps=60)
            mp4_to_gif(f'{file}.mp4', f'{file}.gif')
            break
        if current_step >= max_step:
            break

if __name__ == '__main__':
    main()
