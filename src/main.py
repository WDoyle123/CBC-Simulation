from calculations.orbital_mechanics import update_classical
from calculations.parameters import schwarzschild_radius
from entities.compact_object import CompactObject
from visualisation.plotter import plot_3d_scatter_animation

def main():

    # Example initialisation of two compact objects
    mass_1 = 80
    mass_2 = 60
    radius_1 = schwarzschild_radius(mass_1)
    radius_2 = schwarzschild_radius(mass_2)

    object_1 = CompactObject(x=0., y=0., z=0., mass=mass_1, radius=radius_1, object_type="Black Hole", velocity_x=0.01, velocity_y=0.05, velocity_z=0.05)
    object_2 = CompactObject(x=5e+3, y=5e+3, z=5e+3, mass=mass_2, radius=radius_2, object_type="Black Hole", velocity_x=-0.00, velocity_y=-0.00, velocity_z=-0.00)

    # Simulation parameters
    time_step = 1000 # Time step in seconds
    num_steps = 500 # Number of steps in the simulation

    for step in range(num_steps):
        collision = update_classical(object_1, object_2, time_step)

        if collision:
            print(f"\nCollision detected at step {step}")
            break

        print(f"\rStep {step}: Object 1 Position: ({object_1.x}, {object_1.y}, {object_1.z}), Object 2 Position: ({object_2.x}, {object_2.y}, {object_2.z})", end="", flush=True)

    plot_3d_scatter_animation(object_1, object_2)


if __name__ == '__main__':
    main()
