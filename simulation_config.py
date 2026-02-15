"""
Simulation Configuration File

Edit this file to change simulation parameters without modifying the main code.
All parameters are clearly documented with typical ranges and effects.
"""

# ============================================================================
# DOMAIN CONFIGURATION
# ============================================================================

class DomainConfig:
    """Grid domain parameters."""

    # Grid dimensions (cells)
    # Typical range: 50-200
    # Effect: Larger = more detail but slower computation
    # Runtime scales as: O(sizex * sizey)
    sizex = 75
    sizey = 75

    # Grid spacing (meters)
    # Typical range: 1e-7 to 1e-6 m
    # Effect: Smaller = finer resolution, more dendrite detail
    # Must match characteristic microstructure length scale
    grid_spacing = 0.25e-6  # 0.25 microns

    def __init__(self):
        self.Lc = self.grid_spacing

    def __str__(self):
        return (f"Domain: {self.sizex}×{self.sizey} grid, "
                f"spacing: {self.grid_spacing*1e6:.3f} μm")


# ============================================================================
# TIME STEPPING CONFIGURATION
# ============================================================================

class TimeConfig:
    """Time integration parameters."""

    # Number of time steps
    # Typical range: 100-1000
    # Effect: More steps = longer growth evolution
    # Adjust based on desired dendrite size
    num_steps = 400

    # Initial time increment (seconds)
    # Typical range: 1e-6 to 1e-4 s
    # Effect: Smaller = more stable but slower
    # Note: Will adapt automatically during simulation (CFL condition)
    initial_dt = 1e-5

    # CFL safety factor for adaptive time stepping
    # Typical range: 3-10
    # Effect: Smaller = more stable but slower
    cfl_factor = 5.0

    def __init__(self):
        self.Tinc = self.initial_dt

    def __str__(self):
        return (f"Time steps: {self.num_steps}, "
                f"initial Δt: {self.initial_dt*1e6:.3f} μs")


# ============================================================================
# NUCLEATION CONFIGURATION
# ============================================================================

class NucleationConfig:
    """Initial nucleation parameters."""

    # Nucleation location (grid coordinates)
    # Options:
    #   'center' - nucleate at domain center
    #   (x, y)   - nucleate at specific coordinates
    #   'random' - random location (for future implementation)
    nucleation_location = 'center'

    # Crystal orientation angle (degrees)
    # Typical range: 0-90 (due to four-fold symmetry)
    # Effect: Changes dendrite orientation
    # 0° = dendrite arms align with grid axes
    # 45° = dendrite arms at 45° to grid axes
    crystal_angle = 0.0

    # Multiple nucleation sites (for future multi-grain simulations)
    # Format: [(x1, y1, angle1), (x2, y2, angle2), ...]
    # Example: [(30, 30, 0), (45, 45, 30)]
    multi_nucleation = None  # Set to list for multiple grains

    def __str__(self):
        return (f"Nucleation: {self.nucleation_location}, "
                f"angle: {self.crystal_angle}°")


# ============================================================================
# PHYSICAL PARAMETERS
# ============================================================================

class PhysicalConfig:
    """Physical parameters for solidification."""

    # Undercooling (Kelvin)
    # Typical range: 5-50 K
    # Effect: Higher = faster growth, more branching
    # This is the driving force for solidification
    undercooling = 15.0

    # Base geometric factor (dimensionless)
    # Typical range: 0.3-0.8
    # Effect: Controls interface mobility
    # Lower = slower growth
    geometric_factor = 0.4

    # Anisotropy strength (dimensionless)
    # Typical range: 0.0-0.3
    # Effect: Controls dendrite morphology
    # 0.0 = isotropic (no preferred direction)
    # 0.3 = strong anisotropy (four-fold symmetry)
    anisotropy = 0.3

    def __init__(self):
        self.U_C = self.undercooling
        self.b0 = self.geometric_factor
        self.d_k = self.anisotropy

    def __str__(self):
        return (f"ΔT: {self.undercooling} K, "
                f"b0: {self.geometric_factor}, "
                f"δk: {self.anisotropy}")


# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================

class OutputConfig:
    """Output and visualization parameters."""

    # Progress reporting interval
    # Print progress every N steps
    progress_interval = 100

    # Output filename for visualization
    output_filename = 'dendrite_result.png'

    # Figure resolution (DPI)
    # Typical range: 100-300
    # Effect: Higher = better quality but larger file
    figure_dpi = 150

    # Colormap for visualization
    # Options: 'coolwarm', 'viridis', 'plasma', 'jet', 'RdBu'
    colormap = 'coolwarm'

    # Save intermediate results
    # If True, saves snapshots during simulation
    save_intermediate = False
    intermediate_interval = 100  # Save every N steps

    def __str__(self):
        return f"Output: {self.output_filename}, DPI: {self.figure_dpi}"


# ============================================================================
# EXAMPLE CONFIGURATIONS
# ============================================================================

class QuickTestConfig:
    """Quick test configuration - small domain, few steps."""
    domain = DomainConfig()
    domain.sizex = 50
    domain.sizey = 50

    time = TimeConfig()
    time.num_steps = 200

    nucleation = NucleationConfig()
    physical = PhysicalConfig()
    output = OutputConfig()


class HighResolutionConfig:
    """High resolution configuration - large domain, fine grid."""
    domain = DomainConfig()
    domain.sizex = 150
    domain.sizey = 150
    domain.grid_spacing = 0.1e-6  # Finer spacing

    time = TimeConfig()
    time.num_steps = 600
    time.initial_dt = 5e-6  # Smaller time step

    nucleation = NucleationConfig()
    physical = PhysicalConfig()
    output = OutputConfig()
    output.figure_dpi = 200


class FastGrowthConfig:
    """Fast growth configuration - high undercooling."""
    domain = DomainConfig()
    time = TimeConfig()
    time.num_steps = 300

    nucleation = NucleationConfig()

    physical = PhysicalConfig()
    physical.undercooling = 30.0  # Higher undercooling

    output = OutputConfig()


class RotatedCrystalConfig:
    """Rotated crystal configuration - 45° orientation."""
    domain = DomainConfig()
    time = TimeConfig()

    nucleation = NucleationConfig()
    nucleation.crystal_angle = 45.0  # Rotate dendrite arms

    physical = PhysicalConfig()
    output = OutputConfig()


class StrongAnisotropyConfig:
    """Strong anisotropy configuration - pronounced dendrite structure."""
    domain = DomainConfig()
    time = TimeConfig()

    nucleation = NucleationConfig()

    physical = PhysicalConfig()
    physical.anisotropy = 0.5  # Stronger four-fold symmetry

    output = OutputConfig()


# ============================================================================
# DEFAULT CONFIGURATION
# ============================================================================

class DefaultConfig:
    """Default configuration - standard simulation parameters."""
    domain = DomainConfig()
    time = TimeConfig()
    nucleation = NucleationConfig()
    physical = PhysicalConfig()
    output = OutputConfig()

    def print_summary(self):
        """Print configuration summary."""
        print("="*70)
        print("SIMULATION CONFIGURATION")
        print("="*70)
        print(f"Domain:     {self.domain}")
        print(f"Time:       {self.time}")
        print(f"Nucleation: {self.nucleation}")
        print(f"Physical:   {self.physical}")
        print(f"Output:     {self.output}")
        print("="*70)


# ============================================================================
# USAGE INSTRUCTIONS
# ============================================================================

"""
HOW TO USE THIS CONFIGURATION FILE:

1. BASIC USAGE (modify default parameters):
   - Edit the values in the class definitions above
   - Run: python Terminal2DCompositionModel.py

2. USE A PRESET CONFIGURATION:
   In Terminal2DCompositionModel.py, change:
       config = DefaultConfig()
   to:
       config = QuickTestConfig()
   or any other preset configuration

3. CREATE CUSTOM CONFIGURATION:

   class MyConfig:
       domain = DomainConfig()
       domain.sizex = 100  # Custom size

       time = TimeConfig()
       time.num_steps = 500

       nucleation = NucleationConfig()
       nucleation.crystal_angle = 30  # Custom angle

       physical = PhysicalConfig()
       output = OutputConfig()

4. PARAMETER SWEEP (for advanced users):

   for angle in [0, 15, 30, 45]:
       config = DefaultConfig()
       config.nucleation.crystal_angle = angle
       config.output.output_filename = f'dendrite_angle_{angle}.png'
       # Run simulation with this config

EXAMPLES:

- Quick test run:
  config = QuickTestConfig()

- High detail simulation:
  config = HighResolutionConfig()

- Study effect of crystal orientation:
  config = RotatedCrystalConfig()

- Study effect of undercooling:
  config = FastGrowthConfig()

- Study anisotropy effect:
  config = StrongAnisotropyConfig()
"""
