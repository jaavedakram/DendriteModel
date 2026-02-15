# Theory & Governing Equations

## Physical Model

The dendrite growth model is based on cellular automaton methods coupled with solute diffusion. The simulation tracks the solid-liquid interface evolution driven by undercooling and crystallographic anisotropy.

## Governing Equations

### 1. Interface Evolution (Fraction Solid)

The fraction solid evolution is governed by:

```
∂fs/∂t = G(x,y) · V(x,y) / Lc
```

Where:
- `fs`: Fraction solid [0,1]
- `G`: Geometric factor (interface area per cell)
- `V`: Interface velocity (m/s)
- `Lc`: Cell size (m)

### 2. Solute Transport (Fick's Second Law)

Solute diffusion with partition coefficient:

```
∂C/∂t = ∇·(D∇C)
```

Where:
- `C`: Concentration field (wt%)
- `D`: Diffusion coefficient (m²/s)
  - `D_l` in liquid phase
  - `D_s` in solid phase (typically `D_s << D_l`)

### 3. Interface Velocity (Kinetic Equation)

The growth velocity depends on local undercooling and crystallographic direction:

```
V = μk [ΔT + ml(C - C0) - ΔTcurv] · [1 + δk·cos(4θ)]
```

**Terms:**
- `μk`: Kinetic coefficient (m/(s·K))
- `ΔT`: Constitutional undercooling (K)
- `ml`: Liquidus slope (K/wt%)
- `C`: Local concentration
- `C0`: Initial/bulk concentration
- `ΔTcurv`: Curvature undercooling (Gibbs-Thomson)
- `δk`: Anisotropy strength [0,1]
- `θ`: Angle between growth direction and crystal axis

### 4. Curvature Undercooling

Gibbs-Thomson effect at curved interfaces:

```
ΔTcurv = Γ · κ
```

Where:
- `Γ = T_b`: Gibbs-Thomson coefficient (K·m)
- `κ`: Interface curvature (1/m)

The curvature is approximated from the fraction solid field:

```
κ = (1 - 2·fs_neighborhood/9) / Lc
```

### 5. Four-Fold Anisotropy

Crystallographic preference for <100> directions:

```
δ(θ) = δk · cos(4θ)
```

This creates the characteristic four-arm dendrite pattern aligned with crystal axes.

## Numerical Method

### Spatial Discretization
- **Method**: Finite differences on uniform Cartesian grid
- **Stencil**: 9-point (3×3) neighborhood for gradients
- **Grid spacing**: Typically 0.1-0.5 μm

### Time Integration
- **Method**: Explicit Euler
- **Adaptive stepping**: Based on maximum interface velocity
- **CFL condition**:
  ```
  Δt ≤ Lc² / (4·D_max)  # Diffusion stability
  Δt ≤ Lc / (5·V_max)   # Interface motion stability
  ```

### Algorithm

1. **Identify interface**: Locate solid-liquid boundary cells
2. **Calculate curvature**: Compute geometric factors and undercooling
3. **Solve diffusion**: Update concentration field (explicit FD)
4. **Grow interface**: Calculate velocities and update fraction solid
5. **Adapt timestep**: Ensure numerical stability
6. **Repeat**: Until desired simulation time or solid fraction

## Boundary Conditions

- **Domain boundaries**: Zero-flux (∂C/∂n = 0)
- **Initial conditions**:
  - Uniform concentration C = C0
  - Single seed crystal at center
  - Zero fraction solid except at seed

## Physical Parameters

Typical values for Al-Cu alloys:

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Gibbs-Thomson coefficient | T_b | 1.7×10⁻⁷ | K·m |
| Kinetic coefficient | μk | 0.002 | m/(s·K) |
| Initial concentration | C0 | 3.0 | wt% |
| Liquidus slope | ml | -3.36 | K/wt% |
| Partition coefficient | P_C | 0.17 | - |
| Liquid diffusion | D_l | 3×10⁻⁹ | m²/s |
| Solid diffusion | D_s | 1×10⁻¹³ | m²/s |

## Assumptions

1. **2D simulation**: Assumes infinite extent in third dimension
2. **Isothermal**: Constant temperature (purely solutal dendrites)
3. **Dilute alloy**: Binary system with small solute concentration
4. **Local equilibrium**: At solid-liquid interface
5. **No convection**: Purely diffusive solute transport
6. **Cubic symmetry**: Four-fold anisotropy appropriate for FCC/BCC

## References

> M.F. Zhu, S.Y. Lee, C.P. Hong, "Modified cellular automaton model for the prediction of dendritic growth with melt convection," *Phys. Rev. E* **69** (2004) 061610. [doi:10.1103/PhysRevE.69.061610](https://doi.org/10.1103/PhysRevE.69.061610)

## Related Topics

- [Configuration Guide](Configuration) - How to set physical parameters
- [API Reference](API-Reference) - Module documentation
- [Examples](Examples) - Parameter effect studies
