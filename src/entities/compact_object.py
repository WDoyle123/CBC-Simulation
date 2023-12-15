class CompactObject:
    def __init__(self, x: float, y: float, z: float, velocity_x: float, velocity_y: float, velocity_z: float, mass: float, radius: float, object_type: str):
        """
        Initialise a  new compact object
        
        :param x: x-coordinate in 3D space
        :type x: float or int
        :param y: y-coordinate in 3D space
        :type y: float or int
        :param z: z-coordinate in 3D space
        :type z: float or int
        :param velocity_x: Velocity in the x direction
        :type velocity_x: float or int
        :param velocity_y: Velocity in the y direction
        :type velocity_y: float or int
        :param velocity_z: Velocity in the z direction
        :type velocity_z: float or int
        :param mass: Mass of the object
        :type mass: float
        :param radius: Radius of the object
        :type radius: float
        :param object_type: Type of the object (e.g., 'Black Hole', 'Neutron Star')
        :type object_type: str
        """
        self.x = x
        self.y = y
        self.z = z
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.velocity_z = velocity_z
        self.trajectory = [(self.x, self.y, self.z)]
        self.mass = mass
        self.radius = radius
        self.object_type = object_type

    def update_position(self, time_step: float):
        """
        Updates the position of the object based on its velocity and the given time step.
        """
        self.x += self.velocity_x * time_step
        self.y += self.velocity_y * time_step
        self.z += self.velocity_z * time_step
        self.trajectory.append((self.x, self.y, self.z))

    def update_velocity(self, acceleration: tuple[float, float, float], time_step: float):
        """
        Updates the velocity of the object based on the given acceleration and time step.
        """
        self.velocity_x += acceleration[0] * time_step
        self.velocity_y += acceleration[1] * time_step
        self.velocity_z += acceleration[2] * time_step

    def __str__(self):
        """
        Returns a string representation of the CompactObject, including its type,
        position, mass, and radius.
        """
        return f"Type: {self.object_type}, Position: ({self.x}, {self.y}, {self.z}), Velocity: ({self.velocity_x}, {self.velocity_y}, {self.velocity_z}), Mass: {self.mass}, Radius: {self.radius}"
