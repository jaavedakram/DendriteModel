"""
Example Script - Running Multiple Simulations

This script demonstrates how to run multiple simulations with different
configurations to study the effects of various parameters.

Run this script to generate a series of dendrite growth simulations exploring:
- Different crystal orientations
- Different undercooling values
- Different domain sizes
- Different anisotropy strengths
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import sys

sys.path.append('..')

# Import configuration and simulation engine
from simulation_config import DefaultConfig
from simulation_engine import run_dendrite_simulation


def example_1_crystal_orientation():
    """Study effect of crystal orientation."""

    print("\n" + "="*70)
    print("EXAMPLE 1: Effect of Crystal Orientation")
    print("="*70)

    angles = [0, 15, 30, 45]
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    axes = axes.flatten()

    for idx, angle in enumerate(angles):
        config = DefaultConfig()
        config.nucleation.crystal_angle = angle
        config.time.num_steps = 300
        config.output.progress_interval = 1000  # Reduce output

        print(f"\nRunning: Crystal angle {angle}°")
        result = run_dendrite_simulation(config, verbose=False)
        print(f"  Completed: Solid fraction = {result['final_solid_fraction']:.1%}")

        axes[idx].pcolor(result['CN_Equ'], cmap='coolwarm')
        axes[idx].set_title(f'Crystal Orientation: {angle}°')
        axes[idx].set_xlabel('X Position')
        axes[idx].set_ylabel('Y Position')
        axes[idx].axis('equal')

    plt.tight_layout()
    plt.savefig('example_1_crystal_orientation.png', dpi=150)
    print(f"\n✓ Saved: example_1_crystal_orientation.png")


def example_2_undercooling():
    """Study effect of undercooling."""

    print("\n" + "="*70)
    print("EXAMPLE 2: Effect of Undercooling")
    print("="*70)

    undercoolings = [10, 15, 20, 30]
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    axes = axes.flatten()

    for idx, uc in enumerate(undercoolings):
        config = DefaultConfig()
        config.physical.undercooling = uc
        config.time.num_steps = 300
        config.output.progress_interval = 1000

        print(f"\nRunning: Undercooling {uc} K")
        result = run_dendrite_simulation(config, verbose=False)
        print(f"  Completed: Solid fraction = {result['final_solid_fraction']:.1%}")

        axes[idx].pcolor(result['CN_Equ'], cmap='coolwarm')
        axes[idx].set_title(f'Undercooling: {uc} K')
        axes[idx].set_xlabel('X Position')
        axes[idx].set_ylabel('Y Position')
        axes[idx].axis('equal')

    plt.tight_layout()
    plt.savefig('example_2_undercooling.png', dpi=150)
    print(f"\n✓ Saved: example_2_undercooling.png")


def example_3_anisotropy():
    """Study effect of anisotropy strength."""

    print("\n" + "="*70)
    print("EXAMPLE 3: Effect of Anisotropy Strength")
    print("="*70)

    anisotropies = [0.0, 0.2, 0.4, 0.6]
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    axes = axes.flatten()

    for idx, dk in enumerate(anisotropies):
        config = DefaultConfig()
        config.physical.anisotropy = dk
        config.time.num_steps = 300
        config.output.progress_interval = 1000

        print(f"\nRunning: Anisotropy δk={dk}")
        result = run_dendrite_simulation(config, verbose=False)
        print(f"  Completed: Solid fraction = {result['final_solid_fraction']:.1%}")

        axes[idx].pcolor(result['CN_Equ'], cmap='coolwarm')
        axes[idx].set_title(f'Anisotropy: δk={dk:.1f}')
        axes[idx].set_xlabel('X Position')
        axes[idx].set_ylabel('Y Position')
        axes[idx].axis('equal')

    plt.tight_layout()
    plt.savefig('example_3_anisotropy.png', dpi=150)
    print(f"\n✓ Saved: example_3_anisotropy.png")


def example_4_domain_size():
    """Study effect of domain size and resolution."""

    print("\n" + "="*70)
    print("EXAMPLE 4: Effect of Domain Size")
    print("="*70)

    sizes = [50, 75, 100]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for idx, size in enumerate(sizes):
        config = DefaultConfig()
        config.domain.sizex = size
        config.domain.sizey = size
        config.time.num_steps = 300
        config.output.progress_interval = 1000

        print(f"\nRunning: Domain {size}×{size}")
        result = run_dendrite_simulation(config, verbose=False)
        print(f"  Completed: Solid fraction = {result['final_solid_fraction']:.1%}")

        axes[idx].pcolor(result['CN_Equ'], cmap='coolwarm')
        axes[idx].set_title(f'Domain: {size}×{size}')
        axes[idx].set_xlabel('X Position')
        axes[idx].set_ylabel('Y Position')
        axes[idx].axis('equal')

    plt.tight_layout()
    plt.savefig('example_4_domain_size.png', dpi=150)
    print(f"\n✓ Saved: example_4_domain_size.png")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("DENDRITE MODEL - EXAMPLE SIMULATIONS")
    print("="*70)
    print("\nThis script will run 4 example studies:")
    print("  1. Effect of crystal orientation (4 simulations)")
    print("  2. Effect of undercooling (4 simulations)")
    print("  3. Effect of anisotropy (4 simulations)")
    print("  4. Effect of domain size (3 simulations)")
    print("\nTotal: 15 simulations")
    print("\nEstimated time: 3-5 minutes")

    response = input("\nProceed? [y/N]: ")

    if response.lower() == 'y':
        example_1_crystal_orientation()
        example_2_undercooling()
        example_3_anisotropy()
        example_4_domain_size()

        print("\n" + "="*70)
        print("ALL EXAMPLES COMPLETED!")
        print("="*70)
        print("\nGenerated files:")
        print("  - example_1_crystal_orientation.png")
        print("  - example_2_undercooling.png")
        print("  - example_3_anisotropy.png")
        print("  - example_4_domain_size.png")
        print("\n")
    else:
        print("\nCancelled.")
