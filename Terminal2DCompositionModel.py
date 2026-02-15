"""
2D Dendrite Growth Composition Model

Simulates solidification and dendrite growth with solute transport using a
phase-field approach. The model couples:
- Interface tracking via fraction solid field
- Solute diffusion via Fick's second law
- Crystallographic anisotropy via four-fold symmetry
- Curvature effects via Gibbs-Thomson relation

Author: Javed Akram
Version: 2.1.0
Date: February 2026

USAGE:
    python Terminal2DCompositionModel.py

CONFIGURATION:
    Edit simulation_config.py to change:
    - Domain size and grid spacing
    - Number of time steps
    - Crystal orientation angle
    - Physical parameters
    - Output settings

    Or use preset configurations (QuickTestConfig, HighResolutionConfig, etc.)
"""
import sys
sys.path.append('..')

# Import configuration
from simulation_config import DefaultConfig
# Alternative configurations (uncomment to use):
# from simulation_config import QuickTestConfig as DefaultConfig
# from simulation_config import HighResolutionConfig as DefaultConfig
# from simulation_config import FastGrowthConfig as DefaultConfig
# from simulation_config import RotatedCrystalConfig as DefaultConfig
# from simulation_config import StrongAnisotropyConfig as DefaultConfig

# Import simulation engine
from simulation_engine import run_dendrite_simulation, print_simulation_summary, save_results


def main():
    """Main simulation runner."""

    # Initialize configuration
    config = DefaultConfig()

    # Print configuration summary
    config.print_summary()

    # Print material properties info
    print(f"\nMaterial Properties (from Materials_Constants.json):")
    print(f"  Initial concentration (C0): 3.0 wt%")
    print(f"  Partition coefficient (k):  0.17")
    print(f"  Liquidus slope (ml):        -3.36 K/wt%")
    print(f"  Liquid diffusivity (D_l):   3.00e-09 m²/s")
    print(f"\nStarting simulation...\n")

    # Run simulation using shared engine
    results = run_dendrite_simulation(config, verbose=True)

    # Print summary statistics
    print_simulation_summary(results)

    # Save visualization
    output_file = save_results(
        results,
        filename=config.output.output_filename,
        dpi=config.output.figure_dpi,
        colormap=config.output.colormap
    )

    print(f"\n{'='*60}")
    print(f"Output saved to: {output_file}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
