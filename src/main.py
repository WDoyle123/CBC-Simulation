from calculations.orbital_mechanics import update_classical
from entities.compact_object import CompactObject

def main():

    # Example initialization of two compact objects
    object1 = CompactObject(x=0., y=0., z=0., mass=10., radius=2., object_type="Neutron Star", velocity_x=0., velocity_y=0., velocity_z=0.)
    object2 = CompactObject(x=1000., y=1000., z=1000., mass=10., radius=2., object_type="Black Hole", velocity_x=0., velocity_y=0., velocity_z=0.)

    # Simulation parameters
    time_step = 86400 # Time step in seconds
    num_steps = 100000 # Number of steps in the simulation

    for step in range(num_steps):
        collision = update_classical(object1, object2, time_step)

        if collision:
            print(f"\nCollision detected at step {step}")
            break

        print(f"\rStep {step}: Object 1 Position: ({object1.x}, {object1.y}, {object1.z}), Object 2 Position: ({object2.x}, {object2.y}, {object2.z})", end="", flush=True)



if __name__ == '__main__':
    main()
