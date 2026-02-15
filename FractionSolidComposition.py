"""
Fraction Solid and Composition Evolution Module

Calculates the evolution of fraction solid and solute concentration
at the solid-liquid interface using kinetic growth equations.
"""
import numpy as np
import math

# Module constants
DEG_TO_RAD = np.pi / 180  # Degree to radian conversion
FOUR_FOLD = 4  # Four-fold crystallographic symmetry


def Calculator(G, Fs, GvN, GB, Map, TCur, CN, CN_old, CN_S, D, C0, ml, Tinc, Lc,
               Fhi, d_k, mu_k, U_C, P_C, D_s, Vel):
    """Calculate fraction solid and composition evolution.

    Computes:
    1. Interface velocity from kinetic equation
    2. Fraction solid increment based on interface motion
    3. Solute rejection during solidification
    4. Solid composition accounting for partitioning

    Args:
        G: Geometric factor array
        Fs: Fraction solid array (modified in-place)
        GvN: Growth vector normal array
        GB: Grain boundary array
        Map: Phase map array (modified in-place)
        TCur: Temperature curvature array
        CN: Current concentration array (modified in-place)
        CN_old: Previous concentration array
        CN_S: Solid concentration array (modified in-place)
        D: Diffusion coefficient array (modified in-place)
        C0: Initial concentration (wt%)
        ml: Liquidus slope (K/wt%)
        Tinc: Time increment (s)
        Lc: Characteristic length (m)
        Fhi: Crystal orientation array
        d_k: Anisotropy coefficient (dimensionless)
        mu_k: Kinetic coefficient (m/(s·K))
        U_C: Undercooling (K)
        P_C: Partition coefficient (dimensionless)
        D_s: Solid diffusion coefficient (m²/s)
        Vel: Velocity array (modified in-place)

    Note:
        - Only processes interface cells (GB[i,j] == 1.0)
        - Enforces 0 ≤ Fs ≤ 1 bounds
        - Updates diffusion coefficient when fully solidified
    """
    (x, y) = np.shape(Map)

    for i in range(1, x):
        for j in range(1, y):
            if GB[i, j] == 1.0:
                # Interface Velocity Calculation
                # V = μk · [ΔT + ml(C - C0) - ΔT_curv] · [1 + δk·cos(4θ)]
                #
                # Components:
                # - ΔT: Applied undercooling
                # - ml(C - C0): Constitutional undercooling
                # - ΔT_curv: Curvature undercooling
                # - [1 + δk·cos(4θ)]: Anisotropic growth modifier

                angle_diff = (Fhi[i, j] - GvN[i, j]) * DEG_TO_RAD
                angle_factor = 1 + d_k * math.cos(FOUR_FOLD * angle_diff)

                driving_force = U_C + (ml * (CN[i, j] - C0)) - TCur[i, j]
                Vel[i, j] = mu_k * driving_force * angle_factor

                # Fraction Solid Increment
                # ΔFs = min(G · V · Δt / Lc, 1 - Fs)
                # Ensures: Fs never exceeds 1.0
                DelFs = min((G[i, j] * Vel[i, j] * Tinc / Lc), (1 - Fs[i, j]))
                Fs[i, j] = Fs[i, j] + DelFs

                # Solute Rejection
                # Mass balance: Rejected solute = C_old · (1 - k) · ΔFs
                # where k is the partition coefficient
                Rej = CN_old[i, j] * (1 - P_C) * DelFs
                CN[i, j] = CN[i, j] + Rej

                # Solid Concentration
                # C_solid = k · C_liquid (equilibrium partitioning)
                CN_S[i, j] = CN[i, j] * P_C

                # Complete Solidification Check
                if Fs[i, j] >= 1.0:
                    Fs[i, j] = 1.0  # Enforce upper bound
                    Map[i, j] = 1.0  # Mark as fully solid
                    D[i, j] = D_s    # Switch to solid diffusivity
