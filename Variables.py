"""
Variable Initialization Module

Initializes all field variables (NumPy arrays) for the dendrite growth simulation.
"""
import numpy as np


def Initiate(sizex, sizey):
    """Initialize simulation variables for dendrite growth model.

    Creates and initializes all field arrays needed for the phase-field
    solidification simulation with composition (solutal) fields.

    Args:
        sizex (int): Grid size in x direction (number of cells)
        sizey (int): Grid size in y direction (number of cells)

    Returns:
        tuple: (Fs, Map, GB, G, GvN, TCur, Fhi, CN, CN_S, D, Vel)

    Field Descriptions:
        - Fs: Fraction solid [0,1]
        - Map: Phase map (0=liquid, 1=solid)
        - GB: Grain boundary marker (1=interface, 0=interior)
        - G: Geometric factor (interface area)
        - GvN: Growth vector normal angle (degrees)
        - TCur: Temperature curvature undercooling (K)
        - Fhi: Crystal orientation angle (degrees)
        - CN: Concentration field (wt%)
        - CN_S: Solid concentration (wt%)
        - D: Diffusion coefficient (m²/s)
        - Vel: Interface velocity (m/s)

    Note:
        - All arrays are initialized as float64 (NumPy default)
        - Most fields start at zero, except CN and D which start at 1.0
        - Memory usage: ~sizex × sizey × 8 bytes per array
    """
    # Input validation
    if sizex <= 0 or sizey <= 0:
        raise ValueError(f"Grid size must be positive. Got sizex={sizex}, sizey={sizey}")

    # Phase field and thermal arrays
    Fs = np.zeros((sizex, sizey))    # Fraction solid
    Map = np.zeros((sizex, sizey))   # Phase map
    GB = np.zeros((sizex, sizey))    # Grain boundary
    G = np.zeros((sizex, sizey))     # Geometric factor
    GvN = np.zeros((sizex, sizey))   # Growth vector normal
    TCur = np.zeros((sizex, sizey))  # Temperature curvature
    Fhi = np.zeros((sizex, sizey))   # Crystal orientation

    # Composition (solutal) field arrays
    CN = np.ones((sizex, sizey))     # Concentration (initialized to 1.0)
    CN_S = np.zeros((sizex, sizey))  # Solid concentration
    D = np.ones((sizex, sizey))      # Diffusion coefficient (initialized to 1.0)
    Vel = np.ones((sizex, sizey))    # Velocity (initialized to 1.0)

    return (Fs, Map, GB, G, GvN, TCur, Fhi, CN, CN_S, D, Vel)
