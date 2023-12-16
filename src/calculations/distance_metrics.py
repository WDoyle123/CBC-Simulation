import math

def distance(compact_object_1, compact_object_2, axis):
    return getattr(compact_object_2, axis) - getattr(compact_object_1, axis)

def distance_3d(compact_object_1, compact_object_2):
    dx = distance(compact_object_1, compact_object_2, 'x')
    dy = distance(compact_object_1, compact_object_2, 'y')
    dz = distance(compact_object_1, compact_object_2, 'z')
    distance_between_objects = math.sqrt(dx**2 + dy**2 + dz**2)
    return dx, dy, dz, distance_between_objects
