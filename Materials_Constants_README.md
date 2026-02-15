# Materials Constants Guide

This guide explains the material properties used in the dendrite growth simulation.

## File Format

The `Materials_Constants.json` file contains alloy-specific parameters used in the solidification model.

## Parameters

### `T_b` - Gibbs-Thomson Coefficient

**Symbol**: Γ
**Units**: K·m
**Typical Range**: 1e-7 to 1e-6
**Current Value**: 1.7e-7

**Physical Meaning**: Relates interface curvature to equilibrium temperature depression.

**Effect on Simulation**:
- Higher values → Stronger curvature effects
- Lower values → Sharper dendrite tips

**Equation**: ΔT_curv = Γ · κ
where κ is the interface curvature (1/m)

---

### `mu_k` - Kinetic Coefficient

**Symbol**: μ
**Units**: m/(s·K)
**Typical Range**: 1e-4 to 1e-2
**Current Value**: 0.002

**Physical Meaning**: Relates interfaceundercooling to growth velocity.

**Effect on Simulation**:
- Higher values → Faster growth at same undercooling
- Lower values → Slower, more stable growth

**Equation**: V = μ · ΔT
where V is velocity (m/s) and ΔT is undercooling (K)

---

### `C0` - Initial Concentration

**Symbol**: C₀
**Units**: wt% (weight percent)
**Typical Range**: 0.1 to 10
**Current Value**: 3.0

**Physical Meaning**: Nominal alloy composition.

**Effect on Simulation**:
- Sets the baseline solute concentration
- Affects equilibrium temperatures via liquidus slope
- Determines extent of microsegregation

**Example**: 3.0 wt% = Al-3wt%Cu alloy

---

### `ml` - Liquidus Slope

**Symbol**: m
**Units**: K/wt%
**Typical Range**: -10 to -1 (usually negative)
**Current Value**: -3.36

**Physical Meaning**: Rate of change of liquidus temperature with composition.

**Effect on Simulation**:
- More negative → Larger freezing range
- Determines constitutional undercooling
- Affects solute redistribution intensity

**Equation**: T_liquidus = T_melt + m · C

**Example**: For Al-Cu, m ≈ -3.36 K/wt%

---

### `P_C` - Partition Coefficient

**Symbol**: k
**Units**: Dimensionless
**Typical Range**: 0.1 to 1.0
**Current Value**: 0.17

**Physical Meaning**: Ratio of solute concentration in solid to liquid at equilibrium.

**Effect on Simulation**:
- k < 1: Solute rejected into liquid (most alloys)
- k = 1: No partitioning (pure substance)
- Lower k → Stronger microsegregation

**Equation**: C_solid = k · C_liquid

**Example**: For Al-Cu, k ≈ 0.17 (Cu enriches in liquid)

---

### `D_l` - Liquid Diffusion Coefficient

**Symbol**: D_L
**Units**: m²/s
**Typical Range**: 1e-9 to 1e-8
**Current Value**: 3e-9

**Physical Meaning**: Rate of solute diffusion in liquid phase.

**Effect on Simulation**:
- Higher D_L → Faster solute redistribution
- Lower D_L → Sharper concentration gradients
- Affects dendrite spacing and morphology

**Typical Values**:
- Metallic liquids: ~1e-9 m²/s
- Aqueous solutions: ~1e-9 m²/s
- Organic liquids: ~1e-10 m²/s

---

### `D_s` - Solid Diffusion Coefficient

**Symbol**: D_S
**Units**: m²/s
**Typical Range**: 1e-15 to 1e-12
**Current Value**: 1e-13

**Physical Meaning**: Rate of solute diffusion in solid phase.

**Effect on Simulation**:
- Usually D_S << D_L (several orders of magnitude)
- Controls back-diffusion in solid
- Affects microsegregation pattern

**Note**: Often negligible at solidification temperatures, but included for completeness.

---

## Example Configurations

### Aluminum-Copper (Al-Cu)

Current default configuration:
```json
{
    "T_b": 1.7e-7,
    "mu_k": 0.002,
    "C0": 3.0,
    "ml": -3.36,
    "P_C": 0.17,
    "D_l": 3e-9,
    "D_s": 1e-13
}
```

### Steel (Fe-C)

```json
{
    "T_b": 2.4e-7,
    "mu_k": 0.001,
    "C0": 0.4,
    "ml": -78.0,
    "P_C": 0.34,
    "D_l": 5e-9,
    "D_s": 5e-11
}
```

### Nickel-Copper (Ni-Cu)

```json
{
    "T_b": 1.8e-7,
    "mu_k": 0.003,
    "C0": 30.0,
    "ml": -2.5,
    "P_C": 0.85,
    "D_l": 4e-9,
    "D_s": 2e-13
}
```

## Parameter Relationships

### Solidification Time Scale

```
t_solid ~ L² / (D_l · m · C0 / T_melt)
```

### Characteristic Length Scale

```
l_diff ~ D_l · t_solid / V
```

### Dendrite Tip Radius

```
R_tip ~ Γ / (ΔT · ζ)
```
where ζ is a geometric factor

## Dimensionless Numbers

### Solutal Péclet Number

```
Pe = V · R_tip / D_l
```

**Interpretation**:
- Pe << 1: Diffusion-controlled
- Pe >> 1: Kinetically-controlled

### Lewis Number

```
Le = α / D_l
```
where α is thermal diffusivity

## Sources of Data

1. **Thermodynamic Databases**:
   - Thermo-Calc
   - FactSage
   - CALPHAD assessments

2. **Experimental Measurements**:
   - Differential scanning calorimetry (DSC)
   - Directional solidification experiments
   - Diffusion couple studies

3. **Literature Values**:
   - ASM Handbooks
   - Materials science textbooks
   - Journal publications

## Validation

To validate material parameters:

1. **Liquidus Slope**: Compare T-C phase diagram
2. **Partition Coefficient**: Measure segregation profiles
3. **Diffusivity**: Compare to literature values
4. **Kinetic Coefficient**: Fit to measured velocities

## Troubleshooting

### Simulation Too Fast

- Reduce `mu_k`
- Increase `T_b`
- Decrease undercooling `U_C`

### Simulation Too Slow

- Increase `mu_k`
- Decrease `T_b`
- Increase undercooling `U_C`

### Numerical Instability

- Ensure `D_l` not too large relative to grid spacing
- Check CFL condition is satisfied
- Reduce time step if needed

### Unrealistic Morphology

- Check `P_C` is reasonable (0.1 to 1.0)
- Verify `ml` sign (usually negative)
- Ensure `T_b` in typical range

## References

1. Kurz, W., & Fisher, D. J. (1998). *Fundamentals of Solidification*. Trans Tech Publications.
2. Dantzig, J. A., & Rappaz, M. (2009). *Solidification*. EPFL Press.
3. Porter, D. A., & Easterling, K. E. (2009). *Phase Transformations in Metals and Alloys*. CRC Press.

---

**Last Updated**: February 2026
