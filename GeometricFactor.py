"""
Geometric Factor and Curvature Module

Calculates geometric factors for interface cells and curvature effects
on local equilibrium temperature (Gibbs-Thomson effect).
"""
import numpy as np
import math
import NormalAngle

# Module constants
SQRT_2 = math.sqrt(2)  # Diagonal neighbor distance factor
DEG_TO_RAD = np.pi / 180  # Degree to radian conversion


def Calculator(G, Fs, GvN, GB, Map, TCur, Fhi, Lc, b0, d_k, T_b):
    """Calculate geometric factor and curvature effects.

    Computes:
    1. Interface normal angles
    2. Geometric factor (proportional to interface area)
    3. Crystal orientation propagation
    4. Curvature undercooling (Gibbs-Thomson effect)

    Args:
        G: Geometric factor array (modified in-place)
        Fs: Fraction solid array
        GvN: Growth vector normal array (modified in-place)
        GB: Grain boundary array
        Map: Phase map array
        TCur: Temperature curvature array (modified in-place)
        Fhi: Angle array (modified in-place)
        Lc: Characteristic length (m)
        b0: Base geometric factor (dimensionless)
        d_k: Anisotropy coefficient (dimensionless)
        T_b: Gibbs-Thomson coefficient (K·m)

    Note:
        Only processes cells marked as grain boundaries (GB[i,j] == 1.0)
    """
    (x, y) = np.shape(G)

    for i in range(1, x):
        for j in range(1, y):
            if GB[i, j] == 1.0:
                # Normal Angle Calculation
                NormalAngle.FD(i, j, Fs, GvN)

                # Geometric Factor Calculation
                # Counts solid neighbors with distance weighting
                # Orthogonal neighbors: distance = 1
                # Diagonal neighbors: distance = sqrt(2)
                orthogonal = Map[i, j+1] + Map[i, j-1] + Map[i-1, j] + Map[i+1, j]
                diagonal = Map[i-1, j+1] + Map[i-1, j-1] + Map[i+1, j+1] + Map[i+1, j-1]
                G[i, j] = b0 * orthogonal + (b0 / SQRT_2) * diagonal

                # Crystal Orientation Propagation
                # Inherit maximum orientation from neighbors
                Fhi[i, j] = np.max(Fhi[i-1:i+2, j-1:j+2])

                # Curvature Calculation
                # Curvature is proportional to deviation from average fraction solid
                # κ ≈ (1 - 2·<fs>/9) / Lc
                fs_neighborhood = np.sum(Fs[i-1:i+2, j-1:j+2])
                Curvature = (1 - 2 * fs_neighborhood / 9) / Lc

                # Anisotropic Curvature Undercooling (Gibbs-Thomson)
                # ΔT_curv = [1 - δk·cos(4θ)] · κ · Γ
                # where θ is misorientation between crystal and growth direction
                angle_diff = (Fhi[i, j] - GvN[i, j]) * DEG_TO_RAD
                angle_factor = 1 - d_k * math.cos(4 * angle_diff)
                TCur[i, j] = angle_factor * Curvature * T_b
