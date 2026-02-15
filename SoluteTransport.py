"""
Solute Transport Module

Solves the diffusion equation for solute transport in liquid and solid phases
using explicit finite difference method.
"""
import numpy as np
import warnings


def FDExplicit(CN, CN_old, D, Tinc, Lc):
    """Calculate solute transport using explicit finite difference method.

    Solves the diffusion equation:
        ∂C/∂t = ∇·(D∇C)

    Using explicit (forward Euler) time integration:
        C[i,j]^(n+1) = C[i,j]^n + D[i,j] · Δt/Δx² · ∇²C[i,j]^n

    Args:
        CN: Current concentration array (modified in-place)
        CN_old: Previous concentration array
        D: Diffusion coefficient array (m²/s)
        Tinc: Time increment (s)
        Lc: Characteristic length (m)

    Note:
        - Uses 5-point stencil for Laplacian
        - Boundary cells (i=0, i=x-1, j=0, j=y-1) are not updated
        - Stability condition: Δt ≤ Δx²/(4D_max) should be satisfied

    Warnings:
        Issues a warning if time step exceeds stability limit.
    """
    (x, y) = np.shape(CN)

    # Stability check (optional, can be disabled for performance)
    # CFL condition for 2D explicit diffusion: Δt ≤ Δx²/(4D)
    max_D = np.max(D)
    dt_stability = (Lc * Lc) / (4 * max_D)

    if Tinc > dt_stability * 1.1:  # 10% tolerance
        warnings.warn(
            f"Time step ({Tinc:.2e} s) exceeds stability limit ({dt_stability:.2e} s). "
            f"Numerical instability may occur. Consider reducing time step.",
            UserWarning
        )

    # Explicit finite difference loop
    for i in range(1, x-1):
        for j in range(1, y-1):
            # Second derivatives using central differences
            # ∂²C/∂x² ≈ (C[i-1,j] - 2C[i,j] + C[i+1,j]) / Δx²
            Difx = (CN_old[i-1, j] - 2*CN_old[i, j] + CN_old[i+1, j]) * D[i, j]
            Dify = (CN_old[i, j-1] - 2*CN_old[i, j] + CN_old[i, j+1]) * D[i, j]

            # Update concentration
            CN[i, j] = CN_old[i, j] + (Difx + Dify) * (Tinc / (Lc * Lc))
