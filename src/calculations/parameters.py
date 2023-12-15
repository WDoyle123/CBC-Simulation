from utils.constants import *

def schwarzschild_radius(solar_mass):
    """
    This function computes the Schwarzschild radius based on the provided mass in solar masses. The Schwarzschild radius is calculated using the formula R = 2GM/c^2, where G is the gravitational constant, M is the mass of the black hole, and c is the speed of light.

    :param solar_mass: The mass of the black hole in solar masses.
    :type solar_mass: float
    :return: Schwarzschild radius in solar radii.
    :rtype: float

    Example:
    >>> schwarzschild_radius(8)
    (16)
    """

    # Schwarzchild radius R = 2GM/c^2 in metres
    return ((2 * G * solar_mass) / (c ** 2))


