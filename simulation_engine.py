"""
Simulation Engine Module

Core simulation logic extracted to avoid code duplication.
All simulation scripts import and use this engine.
"""
import numpy as np
import json

# Import simulation modules
import Variables
import GrainBoundary
import GeometricFactor
import SoluteTransport
import FractionSolidComposition


def run_dendrite_simulation(config, verbose=True):
    """
    Run dendrite growth simulation with given configuration.

    Args:
        config: Configuration object (from simulation_config)
        verbose: If True, print progress messages

    Returns:
        dict: Results dictionary containing:
            - CN_Equ: Equilibrium concentration field
            - Fs: Fraction solid field
            - Map: Phase map (0=liquid, 1=solid)
            - CN: Concentration field
            - Fhi: Crystal orientation field
            - simulation_time: Total simulation time
    """

    # Extract parameters from configuration
    sizex = config.domain.sizex
    sizey = config.domain.sizey
    Lc = config.domain.Lc
    Tinc = config.time.Tinc
    num_steps = config.time.num_steps
    U_C = config.physical.U_C
    b0 = config.physical.b0
    d_k = config.physical.d_k
    crystal_angle = config.nucleation.crystal_angle

    # Load material properties from JSON
    with open('Materials_Constants.json') as M_inputs:
        M_data = json.load(M_inputs)

    T_b = M_data['T_b']
    mu_k = M_data['mu_k']
    C0 = M_data['C0']
    ml = M_data['ml']
    P_C = M_data['P_C']
    D_l = M_data['D_l']
    D_s = M_data['D_s']

    # Initialize all field variables
    (Fs, Map, GB, G, GvN, TCur, Fhi, CN, CN_S, D, Vel) = Variables.Initiate(sizex, sizey)

    # Set initial conditions
    CN = CN * C0
    CN_old = CN.copy()
    D = D * D_l

    # Place seed crystal
    if config.nucleation.nucleation_location == 'center':
        center_x = round(sizex / 2)
        center_y = round(sizey / 2)
    elif isinstance(config.nucleation.nucleation_location, tuple):
        center_x, center_y = config.nucleation.nucleation_location
    else:
        center_x = round(sizex / 2)
        center_y = round(sizey / 2)

    Map[center_x, center_y] = 1
    Fs[center_x, center_y] = 1
    Fhi[center_x, center_y] = crystal_angle

    if verbose:
        print(f"Nucleation site: ({center_x}, {center_y}), angle: {crystal_angle}°")

    # Track total simulation time
    total_time = 0.0

    # Main solidification loop
    for Loop in range(1, num_steps + 1):
        # Step 1: Identify solid-liquid interface
        GrainBoundary.SL(GB, Map)

        # Step 2: Calculate geometric factors and curvature
        GeometricFactor.Calculator(G, Fs, GvN, GB, Map, TCur, Fhi, Lc, b0, d_k, T_b)

        # Step 3: Solve solute diffusion
        SoluteTransport.FDExplicit(CN, CN_old, D, Tinc, Lc)

        # Step 4: Update fraction solid and composition
        FractionSolidComposition.Calculator(G, Fs, GvN, GB, Map, TCur, CN, CN_old, CN_S,
                                            D, C0, ml, Tinc, Lc, Fhi, d_k, mu_k, U_C,
                                            P_C, D_s, Vel)

        # Step 5: Adaptive time stepping (CFL condition)
        Max_Vel = np.max(Vel)
        if Max_Vel > 0:
            Tinc = Lc / (config.time.cfl_factor * Max_Vel)

        total_time += Tinc

        # Step 6: Prepare for next iteration
        Vel = np.zeros((sizex, sizey))
        CN_old = CN.copy()

        # Progress output
        if verbose and (Loop % config.output.progress_interval == 0 or Loop == 1 or Loop == num_steps):
            solid_fraction = np.sum(Fs) / (sizex * sizey)
            print(f"  Step {Loop}/{num_steps}: Solid fraction = {solid_fraction:.1%}, "
                  f"Max velocity = {Max_Vel:.3e} m/s, Δt = {Tinc:.3e} s")

        # Save intermediate results if requested
        if config.output.save_intermediate and Loop % config.output.intermediate_interval == 0:
            # This is handled by the calling script for custom visualization
            pass

    # Calculate equilibrium concentration
    CN_Equ = (P_C * CN * Map) + ((1 - Map) * CN)

    # Return results dictionary
    results = {
        'CN_Equ': CN_Equ,
        'Fs': Fs,
        'Map': Map,
        'CN': CN,
        'Fhi': Fhi,
        'simulation_time': total_time,
        'final_solid_fraction': np.sum(Map) / (sizex * sizey),
        'config': config
    }

    return results


def print_simulation_summary(results):
    """
    Print summary statistics for simulation results.

    Args:
        results: Dictionary returned by run_dendrite_simulation
    """
    CN_Equ = results['CN_Equ']
    Map = results['Map']
    Fs = results['Fs']
    config = results['config']

    sizex, sizey = CN_Equ.shape
    C0 = 3.0  # From Materials_Constants.json
    P_C = 0.17

    print(f"\n{'='*60}")
    print(f"SIMULATION COMPLETE")
    print(f"{'='*60}")
    print(f"\nFinal Statistics:")
    print(f"  Total solid cells: {np.sum(Map):.0f} / {sizex*sizey} ({np.sum(Map)/(sizex*sizey)*100:.1f}%)")
    print(f"  Average fraction solid: {np.mean(Fs):.3f}")
    print(f"  Simulation time: {results['simulation_time']:.6e} s")
    print(f"  Equilibrium concentration:")
    print(f"    Sum:  {np.sum(CN_Equ):.6e} wt%")
    print(f"    Mean: {np.mean(CN_Equ):.6e} wt%")
    print(f"    Std:  {np.std(CN_Equ):.6e} wt%")
    print(f"    Min:  {np.min(CN_Equ):.3f} wt%")
    print(f"    Max:  {np.max(CN_Equ):.3f} wt%")

    if np.sum(Map) > 0 and np.sum(Map == 0) > 0:
        print(f"\nMicrosegregation:")
        print(f"  Solid enrichment ratio: {np.mean(CN_Equ[Map==1])/C0:.3f}")
        print(f"  Liquid enrichment ratio: {np.mean(CN_Equ[Map==0])/C0:.3f}")


def save_results(results, filename, dpi=150, colormap='coolwarm', title_suffix=''):
    """
    Save simulation results as an image.

    Args:
        results: Dictionary returned by run_dendrite_simulation
        filename: Output filename
        dpi: Image resolution
        colormap: Matplotlib colormap name
        title_suffix: Additional text for title
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    CN_Equ = results['CN_Equ']
    config = results['config']

    C0 = 3.0  # From Materials_Constants.json
    P_C = 0.17
    U_C = config.physical.U_C
    crystal_angle = config.nucleation.crystal_angle

    plt.figure(figsize=(10, 8))
    plt.pcolor(CN_Equ, cmap=colormap)
    plt.colorbar(label='Equilibrium Concentration (wt%)')

    title = f'2D Dendrite Composition Distribution\n' \
            f'(C₀={C0} wt%, k={P_C:.2f}, ΔT={U_C} K, θ={crystal_angle}°)'
    if title_suffix:
        title += f'\n{title_suffix}'

    plt.title(title)
    plt.xlabel('X Position (grid cells)')
    plt.ylabel('Y Position (grid cells)')
    plt.axis('equal')
    plt.tight_layout()

    plt.savefig(filename, dpi=dpi, bbox_inches='tight')
    plt.close()

    return filename
