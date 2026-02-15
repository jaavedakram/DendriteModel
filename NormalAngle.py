"""
Normal Angle Calculation Module

Computes interface normal angles using finite difference method.
"""
import numpy as np
import math


def FD(i, j, Fs, GvN):
    """Calculate normal angle using finite difference method.

    Computes the angle between the interface normal vector and the x-axis
    using central finite differences on the fraction solid field.

    Args:
        i, j: Grid coordinates
        Fs: Fraction solid array
        GvN: Growth vector normal array (modified in-place)

    Note:
        - Angle is calculated in degrees
        - Range: [-180°, 180°]
        - Returns without modification if gradient magnitude is zero
    """
    # Calculate gradients using central finite differences
    # Weighted average of three finite difference stencils
    Nx = ((Fs[i-1, j-1] - Fs[i-1, j+1]) +
          (Fs[i, j-1] - Fs[i, j+1]) +
          (Fs[i+1, j-1] - Fs[i+1, j+1])) / 6

    Ny = ((Fs[i-1, j-1] - Fs[i+1, j-1]) +
          (Fs[i-1, j] - Fs[i+1, j]) +
          (Fs[i-1, j+1] - Fs[i+1, j+1])) / 6

    # Calculate magnitude using math.sqrt (original for numerical consistency)
    magnitude = math.sqrt(Nx*Nx + Ny*Ny)

    # Safety check: avoid division by zero
    if magnitude == 0:
        return

    # Normalize gradient vector
    VecNx = Nx / magnitude
    VecNy = Ny / magnitude

    # Calculate angle using original logic for exact numerical consistency
    if VecNx > 0:
        GvN[i, j] = math.acos(VecNy) * (180 / np.pi)
    elif VecNx < 0:
        GvN[i, j] = -math.acos(VecNy) * (180 / np.pi)
