class CompactObject:
    def __init__(self, x, y, z, mass, radius, object_type):
        """
        Initialise a  new compact object
        
        :param x: x-coordinate in 3D space
        :type x: float or int
        :param y: y-coordinate in 3D space
        :type y: float or int
        :param z: z-coordinate in 3D space
        :type z: float or int
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
        self.mass = mass
        self.radius = radius
        self.object_type = object_type

    def __str__(self):
        """
        Returns a string representation of the CompactObject, including its type,
        position, mass, and radius.
        """
        return f"Type: {self.object_type}, Position: ({self.x}, {self.y}, {self.z}), Mass: {self.mass}, Radius: {self.radius}"
