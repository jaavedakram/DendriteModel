"""
Nucleation Module

Provides functions for initializing nucleation sites in the simulation domain.
Supports static nucleation with specified crystal orientations.
"""
import numpy as np


def Static(loc_x, loc_y, loc_z, phi1, Phi, phi2, Map, Fs, Cry_ort):
    """Initialize static nucleation at specified location with crystal orientation.

    Args:
        loc_x: X-coordinate of nucleation site
        loc_y: Y-coordinate of nucleation site
        loc_z: Z-coordinate of nucleation site (for 3D extension)
        phi1: Euler angle φ₁ (degrees)
        Phi: Euler angle Φ (degrees)
        phi2: Euler angle φ₂ (degrees)
        Map: Phase map array (modified in-place)
        Fs: Fraction solid array (modified in-place)
        Cry_ort: Crystal orientation array (modified in-place)

    Note:
        Currently designed for 3D but used in 2D simulations by setting loc_z=0.
    """
    Map[loc_x, loc_y, loc_z] = 1
    Fs[loc_x, loc_y, loc_z] = 1
    Cry_ort[loc_x, loc_y, loc_z, 0] = phi1
    Cry_ort[loc_x, loc_y, loc_z, 1] = Phi
    Cry_ort[loc_x, loc_y, loc_z, 2] = phi2
