# Examples & Tutorials

## Quick Start Example

### Basic Simulation

```python
from simulation_config import DefaultConfig
from simulation_engine import run_dendrite_simulation, print_simulation_summary, save_results

# Use default configuration
config = DefaultConfig()

# Run simulation
results = run_dendrite_simulation(config, verbose=True)

# Print statistics
print_simulation_summary(results)

# Save visualization
save_results(results, 'my_dendrite.png')
```

**Output:**
```
Nucleation site: (38, 38), angle: 0°
  Step 1/400: Solid fraction = 0.0%, Max velocity = 2.150e-03 m/s
  Step 50/400: Solid fraction = 3.2%, Max velocity = 1.890e-03 m/s
  ...
  Step 400/400: Solid fraction = 15.3%, Max velocity = 1.234e-03 m/s

SIMULATION COMPLETE
Final Statistics:
  Total solid cells: 861 / 5625 (15.3%)
  Average fraction solid: 0.171
```

---

## Example 1: Crystal Orientation Study

Compare dendrite patterns at different angles.

```python
from simulation_config import DefaultConfig
from simulation_engine import run_dendrite_simulation, save_results

angles = [0, 15, 30, 45, 60, 75, 90]

for angle in angles:
    config = DefaultConfig()
    config.nucleation.crystal_angle = angle
    config.output.output_filename = f'dendrite_{angle}deg.png'

    results = run_dendrite_simulation(config, verbose=False)
    save_results(results, config.output.output_filename,
                 title_suffix=f'Crystal angle: {angle}°')

    print(f"{angle}°: Solid fraction = {results['final_solid_fraction']:.3f}")
```

**Key Observation:**
- Four-fold symmetry: 0° ≡ 90°, 45° shows rotated pattern
- Arms align with <100> crystal directions

---

## Example 2: Undercooling Effect

Study growth rate dependence on driving force.

```python
from simulation_config import DefaultConfig

undercoolings = [5, 10, 15, 20, 30]

for U_C in undercoolings:
    config = DefaultConfig()
    config.physical.undercooling = U_C
    config.output.output_filename = f'undercooling_{U_C}K.png'

    results = run_dendrite_simulation(config, verbose=False)

    print(f"ΔT = {U_C} K:")
    print(f"  Solid fraction: {results['final_solid_fraction']:.3f}")
    print(f"  Simulation time: {results['simulation_time']:.2e} s")
```

**Expected Results:**
- Higher ΔT → Faster growth, more dendrite arms
- Lower ΔT → Slower, more compact structure

---

## Example 3: Anisotropy Strength

Effect of crystallographic preference.

```python
from simulation_config import DefaultConfig

anisotropies = [0.0, 0.1, 0.2, 0.3, 0.4, 0.6]

for d_k in anisotropies:
    config = DefaultConfig()
    config.physical.anisotropy = d_k
    config.output.output_filename = f'anisotropy_{d_k:.1f}.png'

    results = run_dendrite_simulation(config, verbose=False)
    save_results(results, config.output.output_filename,
                 title_suffix=f'Anisotropy: δk = {d_k}')
```

**Observations:**
- `δk = 0.0`: Isotropic (circular) growth
- `δk = 0.3`: Moderate four-fold pattern
- `δk = 0.6`: Sharp dendrite tips, strong directional preference

---

## Example 4: Grid Resolution Study

Impact of grid spacing on dendrite tip resolution.

```python
from simulation_config import DefaultConfig

grid_spacings = [0.5e-6, 0.25e-6, 0.1e-6]

for Lc in grid_spacings:
    config = DefaultConfig()
    config.domain.Lc = Lc

    # Adjust timestep for stability
    config.time.initial_dt = (Lc**2) / (4 * 3e-9)

    results = run_dendrite_simulation(config, verbose=False)

    print(f"Lc = {Lc*1e6:.2f} μm:")
    print(f"  Tip radius: ~{Lc*5*1e6:.2f} μm (estimated)")
```

**Trade-off:**
- Finer grid → Better tip resolution, longer runtime
- Coarser grid → Faster, less detail

---

## Example 5: Domain Size Effect

Study boundary effects.

```python
from simulation_config import DefaultConfig

sizes = [50, 75, 100, 150]

for size in sizes:
    config = DefaultConfig()
    config.domain.sizex = size
    config.domain.sizey = size

    results = run_dendrite_simulation(config, verbose=False)

    print(f"{size}×{size} grid:")
    print(f"  Solid cells: {np.sum(results['Map']):.0f}")
    print(f"  Physical size: {size*config.domain.Lc*1e6:.1f} μm")
```

**Guideline:**
- Domain should be 3-5× larger than final dendrite size
- Smaller domains may constrain growth artificially

---

## Example 6: Time Evolution (Snapshots)

Save intermediate results to visualize growth.

```python
from simulation_config import DefaultConfig
from simulation_engine import run_dendrite_simulation
import matplotlib.pyplot as plt
import numpy as np

config = DefaultConfig()
config.time.num_steps = 500

# Modify simulation_engine to save snapshots, or run multiple shorter simulations
snapshot_steps = [50, 100, 200, 300, 500]

# Run until each snapshot
for i, steps in enumerate(snapshot_steps):
    config.time.num_steps = steps
    results = run_dendrite_simulation(config, verbose=False)

    plt.subplot(2, 3, i+1)
    plt.pcolor(results['CN_Equ'], cmap='coolwarm', vmin=0.5, vmax=7.5)
    plt.title(f't = {steps} steps')
    plt.axis('equal')

plt.tight_layout()
plt.savefig('time_evolution.png', dpi=150)
```

---

## Example 7: Parameter Sweep Script

Automated exploration using `run_examples.py`:

```bash
python run_examples.py
```

**Generates:**
1. **Crystal orientation study**: 0°, 15°, 30°, 45° (4 images)
2. **Undercooling study**: 10, 15, 20, 30 K (4 images)
3. **Anisotropy study**: δk = 0.0, 0.2, 0.4, 0.6 (4 images)
4. **Domain size study**: 50, 75, 100 cells (3 images)

**Total:** 15 parameter combinations in one run

---

## Example 8: Comparison Plotting

Compare three cases side-by-side:

```python
import matplotlib.pyplot as plt
from simulation_config import DefaultConfig
from simulation_engine import run_dendrite_simulation

configs = {
    'Low ΔT (10K)': lambda: setattr(DefaultConfig(), 'physical.undercooling', 10),
    'Medium ΔT (15K)': DefaultConfig(),
    'High ΔT (30K)': lambda: setattr(DefaultConfig(), 'physical.undercooling', 30),
}

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, (title, config) in zip(axes, configs.items()):
    results = run_dendrite_simulation(config, verbose=False)

    im = ax.pcolor(results['CN_Equ'], cmap='coolwarm')
    ax.set_title(title)
    ax.axis('equal')

plt.colorbar(im, ax=axes, label='Concentration (wt%)')
plt.tight_layout()
plt.savefig('comparison.png', dpi=150)
```

---

## Example 9: Extract Quantitative Data

Analyze results programmatically:

```python
from simulation_config import DefaultConfig
from simulation_engine import run_dendrite_simulation
import numpy as np

config = DefaultConfig()
results = run_dendrite_simulation(config, verbose=False)

# Extract data
CN_Equ = results['CN_Equ']
Map = results['Map']
Fs = results['Fs']

# Analyze microsegregation
C_solid = CN_Equ[Map == 1]
C_liquid = CN_Equ[Map == 0]

print("Microsegregation Analysis:")
print(f"  Solid phase:")
print(f"    Mean: {np.mean(C_solid):.3f} wt%")
print(f"    Range: {np.min(C_solid):.3f} - {np.max(C_solid):.3f}")
print(f"  Liquid phase:")
print(f"    Mean: {np.mean(C_liquid):.3f} wt%")
print(f"    Range: {np.min(C_liquid):.3f} - {np.max(C_liquid):.3f}")
print(f"  Enrichment ratio: {np.mean(C_liquid)/np.mean(C_solid):.2f}")
```

---

## Tips for Custom Examples

1. **Start with presets**: Modify existing configurations
2. **Change one parameter**: Isolate effects
3. **Use verbose=False**: For batch runs
4. **Save data**: Use `np.save()` for post-processing
5. **Consistent colormaps**: Use same vmin/vmax for comparisons

## Related Topics

- [Configuration Guide](Configuration) - Parameter details
- [Theory](Theory) - Physical interpretation
- [API Reference](API-Reference) - Function documentation
