# Configuration Guide

## Overview

The simulation uses a modular configuration system in `simulation_config.py`. All parameters are organized into logical groups for easy customization.

## Configuration Structure

### Main Configuration Classes

```python
from simulation_config import DefaultConfig

config = DefaultConfig()
config.domain      # Domain and grid settings
config.time        # Time stepping parameters
config.nucleation  # Nucleation site and orientation
config.physical    # Physical properties
config.output      # Output and visualization
```

## Configuration Categories

### 1. Domain Configuration (`DomainConfig`)

Controls the computational domain and grid resolution.

```python
class DomainConfig:
    sizex = 75           # Grid cells in x-direction
    sizey = 75           # Grid cells in y-direction
    Lc = 0.25e-6         # Grid spacing (m)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sizex` | int | 75 | Number of grid cells in x |
| `sizey` | int | 75 | Number of grid cells in y |
| `Lc` | float | 0.25e-6 | Cell size in meters |

**Guidelines:**
- Larger grid = more detail, slower simulation
- Typical range: 50-200 cells per direction
- Finer grid (smaller Lc) = better tip resolution
- Physical domain size = sizex × Lc meters

### 2. Time Configuration (`TimeConfig`)

Controls simulation duration and time stepping.

```python
class TimeConfig:
    num_steps = 400      # Total iterations
    initial_dt = 1e-5    # Starting timestep (s)
    cfl_factor = 5       # CFL stability factor
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `num_steps` | int | 400 | Number of time steps |
| `initial_dt` | float | 1e-5 | Initial Δt (seconds) |
| `cfl_factor` | float | 5 | Stability factor for adaptive stepping |

**Adaptive Time Stepping:**
```python
Δt = Lc / (cfl_factor × V_max)
```
- Lower `cfl_factor` = more stable, slower
- Higher `cfl_factor` = faster, may be unstable
- Recommended: 3-10

### 3. Nucleation Configuration (`NucleationConfig`)

Sets the initial seed crystal location and orientation.

```python
class NucleationConfig:
    nucleation_location = 'center'    # or (x, y) tuple
    crystal_angle = 0.0               # degrees [0, 360]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `nucleation_location` | str or tuple | 'center' | Seed position |
| `crystal_angle` | float | 0.0 | Crystal orientation (°) |

**Location Options:**
- `'center'`: Automatic centering
- `(x, y)`: Specific grid coordinates

**Angle Effects:**
- 0°: Arms aligned with grid axes
- 45°: Arms rotated 45° from axes
- Four-fold symmetry: 0° ≡ 90° ≡ 180° ≡ 270°

### 4. Physical Configuration (`PhysicalConfig`)

Controls physical parameters affecting growth.

```python
class PhysicalConfig:
    undercooling = 15.0       # ΔT (K)
    geometric_factor = 0.4    # b0 (interface mobility)
    anisotropy = 0.3          # δk (directional preference)
```

**Parameters:**

| Parameter | Type | Default | Range | Effect |
|-----------|------|---------|-------|--------|
| `undercooling` (U_C) | float | 15.0 | 5-50 K | Driving force |
| `geometric_factor` (b0) | float | 0.4 | 0.3-0.8 | Interface mobility |
| `anisotropy` (d_k) | float | 0.3 | 0.0-0.6 | Four-fold strength |

**Effect on Growth:**
- **Higher undercooling** → Faster growth, more branching
- **Higher b0** → Thicker dendrite arms
- **Higher δk** → Stronger <100> preference, sharper tips

### 5. Output Configuration (`OutputConfig`)

Controls visualization and file output.

```python
class OutputConfig:
    output_filename = 'dendrite_result.png'
    figure_dpi = 150
    colormap = 'coolwarm'
    progress_interval = 50
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `output_filename` | str | 'dendrite_result.png' | Output file name |
| `figure_dpi` | int | 150 | Image resolution |
| `colormap` | str | 'coolwarm' | Matplotlib colormap |
| `progress_interval` | int | 50 | Print every N steps |

**Available Colormaps:**
- `'coolwarm'`: Blue (solid) to red (liquid)
- `'viridis'`: Perceptually uniform
- `'jet'`: Traditional rainbow
- `'gray'`: Grayscale

## Preset Configurations

### Quick Test (Fast)
```python
from simulation_config import QuickTestConfig
config = QuickTestConfig()
# 50×50 grid, 100 steps (~5 seconds)
```

### High Resolution
```python
from simulation_config import HighResolutionConfig
config = HighResolutionConfig()
# 100×100 grid, finer spacing (~60 seconds)
```

### Fast Growth
```python
from simulation_config import FastGrowthConfig
config = FastGrowthConfig()
# High undercooling (30 K)
```

### Rotated Crystal
```python
from simulation_config import RotatedCrystalConfig
config = RotatedCrystalConfig()
# 45° crystal orientation
```

### Strong Anisotropy
```python
from simulation_config import StrongAnisotropyConfig
config = StrongAnisotropyConfig()
# δk = 0.6 (sharp dendrite tips)
```

## Material Properties

Edit `Materials_Constants.json` for alloy-specific parameters:

```json
{
    "T_b": 1.7E-7,      // Gibbs-Thomson coefficient (K·m)
    "mu_k": 0.002,      // Kinetic coefficient (m/(s·K))
    "C0": 3,            // Initial concentration (wt%)
    "ml": -3.36,        // Liquidus slope (K/wt%)
    "P_C": 0.17,        // Partition coefficient
    "D_l": 3E-9,        // Liquid diffusivity (m²/s)
    "D_s": 1E-13        // Solid diffusivity (m²/s)
}
```

## Custom Configuration Example

```python
from simulation_config import (
    DomainConfig, TimeConfig, NucleationConfig,
    PhysicalConfig, OutputConfig
)

class MyCustomConfig:
    # Large domain, high resolution
    domain = DomainConfig()
    domain.sizex = 150
    domain.sizey = 150
    domain.Lc = 0.1e-6  # Finer grid

    # Longer simulation
    time = TimeConfig()
    time.num_steps = 1000

    # Off-center nucleation, rotated
    nucleation = NucleationConfig()
    nucleation.nucleation_location = (60, 60)
    nucleation.crystal_angle = 30.0

    # High undercooling, weak anisotropy
    physical = PhysicalConfig()
    physical.undercooling = 25.0
    physical.anisotropy = 0.1

    # Custom output
    output = OutputConfig()
    output.output_filename = 'my_dendrite.png'
    output.colormap = 'viridis'

# Use it
from simulation_engine import run_dendrite_simulation
config = MyCustomConfig()
results = run_dendrite_simulation(config)
```

## Performance Considerations

### Runtime Scaling

**Computational cost:**
```
Runtime ∝ (sizex × sizey) × num_steps
```

**Typical runtimes** (on standard laptop):
- 50×50, 100 steps: ~5 seconds
- 75×75, 400 steps: ~25 seconds
- 100×100, 1000 steps: ~5 minutes
- 150×150, 1000 steps: ~15 minutes

### Memory Usage

**Memory per array:**
```
Memory = sizex × sizey × 8 bytes (float64)
```

**Total arrays:** 11 fields
**Example:** 100×100 grid ≈ 1 MB total

### Optimization Tips

1. **Start small**: Test with QuickTestConfig first
2. **Adaptive timestep**: Reduces total steps needed
3. **Progress interval**: Set to 1000 for quiet mode
4. **Grid size**: Balance resolution vs speed

## Related Topics

- [Theory](Theory) - Understanding the physics
- [Examples](Examples) - Parameter effect studies
- [API Reference](API-Reference) - Programming interface
