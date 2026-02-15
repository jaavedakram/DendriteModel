"""
Grain Boundary Detection Module

Identifies interface cells between different phases (solid-liquid)
and between different grains (solid-solid).
"""
import numpy as np


def SL(GB, Map):
    """Find grain boundaries in solid-liquid phase.

    Identifies interface cells where solid neighbors exist but the cell
    itself is liquid. Uses Moore neighborhood (8 neighbors).

    Args:
        GB: Grain boundary array (modified in-place)
        Map: Phase map array (0=liquid, 1=solid)

    Note:
        GB array is set to 1.0 at interface cells, unchanged elsewhere.
    """
    (x, y) = np.shape(Map)

    for i in range(1, x):
        for j in range(1, y):
            # Use np.sum for efficient NumPy array summation
            neighbor_sum = np.sum(Map[i-1:i+2, j-1:j+2])
            if neighbor_sum > 0 and Map[i, j] == 0.0:
                GB[i, j] = 1.0


def SS(GB, Map):
    """Find grain boundaries in solid-solid phase using von Neumann neighborhood.

    Identifies boundaries between grains with different IDs or orientations.
    Uses 4-neighbor (von Neumann) neighborhood.

    Args:
        GB: Grain boundary array (modified in-place)
        Map: Phase map array with grain IDs

    Note:
        This function is currently not used in the main simulation but
        is available for multi-grain solidification studies.
    """
    (x, y) = np.shape(Map)

    for i in range(2, x-1):
        for j in range(2, y-1):
            # Average of 4 neighbors (von Neumann neighborhood)
            neighbor_avg = (Map[i, j-1] + Map[i, j+1] + Map[i-1, j] + Map[i+1, j]) / 4

            if Map[i, j] != neighbor_avg and Map[i, j] == 0.0:
                GB[i, j] = 1.0
            else:
                GB[i, j] = 0
