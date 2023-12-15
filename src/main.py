from calculations.orbital_mechanics import update_classical
from calculations.parameters import schwarzschild_radius
from entities.compact_object import CompactObject

def main():

    # Example initialisation of two compact objects
    mass1 = 80
    mass2 = 60
    radius1 = schwarzschild_radius(mass1)
    radius2 = schwarzschild_radius(mass2)

    object1 = CompactObject(x=0., y=0., z=0., mass=mass1, radius=radius1, object_type="Black Hole", velocity_x=0., velocity_y=0., velocity_z=0.)
    object2 = CompactObject(x=1e+4, y=1e+4, z=1e+4, mass=mass2, radius=radius2, object_type="Black Hole", velocity_x=0., velocity_y=0., velocity_z=0.)

    # Simulation parameters
    time_step = 1 # Time step in seconds
    num_steps = 1000000 # Number of steps in the simulation

    for step in range(num_steps):
        collision = update_classical(object1, object2, time_step)

        if collision:
            print(f"\nCollision detected at step {step}")
            break

        print(f"\rStep {step}: Object 1 Position: ({object1.x}, {object1.y}, {object1.z}), Object 2 Position: ({object2.x}, {object2.y}, {object2.z})", end="", flush=True)


if __name__ == '__main__':
    main()
