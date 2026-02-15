"""
Crystal Orientation Comparison Script

Runs simulations with different crystal orientations and creates comparison
figures to demonstrate the effect of crystallographic orientation on dendrite
growth morphology.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import sys

sys.path.append('..')

from simulation_config import DefaultConfig
from simulation_engine import run_dendrite_simulation


def main():
    """Run simulations for three orientations and create comparison."""

    print("\n" + "="*60)
    print("CRYSTAL ORIENTATION COMPARISON")
    print("Running simulations for 0°, 45°, and 90° orientations")
    print("="*60)

    angles = [0, 45, 90]
    results = []

    # Run simulations for each orientation
    for angle in angles:
        print(f"\nRunning simulation with crystal angle: {angle}°")
        print("="*60)

        # Create configuration for this angle
        config = DefaultConfig()
        config.nucleation.crystal_angle = angle
        config.time.num_steps = 400

        # Run simulation
        result = run_dendrite_simulation(config, verbose=True)
        results.append((angle, result))

        print(f"✓ Completed: {angle}° orientation")

    # Create comparison figure
    print("\n" + "="*60)
    print("Creating comparison figure...")
    print("="*60)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Get consistent color scale across all plots
    all_values = [r['CN_Equ'] for _, r in results]
    vmin = min(np.min(v) for v in all_values)
    vmax = max(np.max(v) for v in all_values)

    for idx, (angle, result) in enumerate(results):
        CN_Equ = result['CN_Equ']
        solid_fraction = result['final_solid_fraction']

        # Plot concentration field
        im = axes[idx].pcolor(CN_Equ, cmap='coolwarm', vmin=vmin, vmax=vmax)
        axes[idx].set_title(f'Crystal Orientation: {angle}°\n'
                           f'(Solid fraction: {solid_fraction:.1%})',
                           fontsize=14, fontweight='bold')
        axes[idx].set_xlabel('X Position (grid cells)', fontsize=12)
        axes[idx].set_ylabel('Y Position (grid cells)', fontsize=12)
        axes[idx].axis('equal')
        axes[idx].set_aspect('equal', adjustable='box')

    # Add colorbar
    fig.colorbar(im, ax=axes, orientation='horizontal',
                 label='Equilibrium Concentration (wt%)',
                 pad=0.1, fraction=0.05)

    plt.suptitle('Effect of Crystal Orientation on Dendrite Growth',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()

    # Save comparison figure
    output_file = 'crystal_orientation_comparison.png'
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f"\n✓ Comparison figure saved: {output_file}")
    plt.close()

    # Save individual figures
    print("\nSaving individual figures...")
    for angle, result in results:
        CN_Equ = result['CN_Equ']

        plt.figure(figsize=(8, 8))
        plt.pcolor(CN_Equ, cmap='coolwarm')
        plt.colorbar(label='Equilibrium Concentration (wt%)')
        plt.title(f'Crystal Orientation: {angle}°', fontsize=14, fontweight='bold')
        plt.xlabel('X Position (grid cells)')
        plt.ylabel('Y Position (grid cells)')
        plt.axis('equal')

        filename = f'dendrite_{angle}deg.png'
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"  ✓ Saved: {filename}")
        plt.close()

    # Print summary
    print("\n" + "="*60)
    print("COMPLETED!")
    print("="*60)
    print("\nGenerated files:")
    print("  - crystal_orientation_comparison.png (comparison)")
    print("  - dendrite_0deg.png (0° orientation)")
    print("  - dendrite_45deg.png (45° orientation)")
    print("  - dendrite_90deg.png (90° orientation)")
    print("\n")


if __name__ == "__main__":
    main()
