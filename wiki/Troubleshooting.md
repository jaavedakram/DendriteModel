# Troubleshooting Guide

## Installation Issues

### ModuleNotFoundError: No module named 'numpy'

**Problem:** Python can't find required packages.

**Solution:**
```bash
# Make sure virtual environment is activated
source mcenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import numpy; print(numpy.__version__)"
```

### Virtual Environment Not Activating

**Problem:** `source mcenv/bin/activate` doesn't work.

**Solutions:**

**Linux/Mac:**
```bash
source mcenv/bin/activate
```

**Windows (Command Prompt):**
```bash
mcenv\Scripts\activate.bat
```

**Windows (PowerShell):**
```bash
mcenv\Scripts\Activate.ps1
```

**Permission denied:**
```bash
chmod +x mcenv/bin/activate
source mcenv/bin/activate
```

---

## Runtime Errors

### Division by Zero Warning

**Problem:**
```
RuntimeWarning: invalid value encountered in scalar divide
```

**Status:** ✅ Already fixed in current version

**If you encounter it:**
- Update to latest version
- Check that `NormalAngle.py` has division-by-zero protection:
  ```python
  if magnitude == 0:
      return
  ```

### NaN or Inf in Results

**Problem:** Results contain `NaN` or `Inf` values.

**Possible causes:**

1. **Time step too large**
   ```python
   # Solution: Reduce CFL factor
   config.time.cfl_factor = 3  # Lower is more stable
   ```

2. **Extreme parameters**
   ```python
   # Avoid very high undercooling
   config.physical.undercooling = 50  # Too high, try ≤ 30 K
   ```

3. **Check stability warning**
   ```
   UserWarning: Time step exceeds stability limit
   ```
   - Reduce `initial_dt` or increase `cfl_factor`

### Simulation Doesn't Grow

**Problem:** Solid fraction stays at ~0%, no dendrite growth.

**Checklist:**

1. **Check undercooling** is positive:
   ```python
   config.physical.undercooling = 15  # Must be > 0
   ```

2. **Check nucleation** was successful:
   ```python
   print(f"Map sum: {np.sum(Map)}")  # Should be > 0
   ```

3. **Run longer**:
   ```python
   config.time.num_steps = 1000  # Increase if growth is slow
   ```

4. **Check kinetic coefficient** in `Materials_Constants.json`:
   ```json
   "mu_k": 0.002  // Should be > 0
   ```

---

## Visualization Issues

### No Image Generated

**Problem:** Script runs but no PNG file appears.

**Checklist:**

1. **Check filename**:
   ```python
   print(config.output.output_filename)
   ```

2. **Check current directory**:
   ```bash
   ls -la *.png
   pwd  # Verify you're in the right directory
   ```

3. **Permission error**:
   ```bash
   # Check write permissions
   touch test.png && rm test.png
   ```

4. **Matplotlib backend** (should use 'Agg'):
   ```python
   import matplotlib
   print(matplotlib.get_backend())  # Should show 'agg'
   ```

### Qt Platform Plugin Error

**Problem:**
```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb"
```

**Status:** ✅ Fixed - Code uses 'Agg' backend (no display needed)

**If you still see it:**
```python
# Add to top of script
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
```

### Poor Image Quality

**Problem:** Dendrite details not visible.

**Solutions:**

1. **Increase DPI**:
   ```python
   config.output.figure_dpi = 300  # Higher resolution
   ```

2. **Try different colormap**:
   ```python
   config.output.colormap = 'viridis'  # Better contrast
   ```

3. **Increase grid resolution**:
   ```python
   config.domain.sizex = 150
   config.domain.sizey = 150
   ```

---

## Performance Issues

### Simulation Too Slow

**Problem:** Taking too long to complete.

**Solutions:**

**1. Reduce grid size:**
```python
config.domain.sizex = 50  # From 75 or 100
config.domain.sizey = 50
```

**2. Fewer steps:**
```python
config.time.num_steps = 200  # From 400
```

**3. Use QuickTestConfig:**
```python
from simulation_config import QuickTestConfig
config = QuickTestConfig()  # Optimized for speed
```

**4. Disable verbose output:**
```python
results = run_dendrite_simulation(config, verbose=False)
```

**5. Increase progress interval:**
```python
config.output.progress_interval = 1000  # Less frequent printing
```

### Out of Memory

**Problem:**
```
MemoryError: Unable to allocate array
```

**Solutions:**

1. **Reduce grid size:**
   ```python
   # Memory ∝ (sizex × sizey)
   config.domain.sizex = 75  # Instead of 200
   ```

2. **Check available RAM:**
   ```bash
   free -h  # Linux
   # Ensure several GB available
   ```

3. **Close other applications**

---

## Numerical Issues

### Results Don't Match Literature

**Problem:** Growth velocity or morphology differs from expected.

**Check:**

1. **Material properties** in `Materials_Constants.json`
2. **Physical parameters** match your reference:
   - Undercooling
   - Partition coefficient
   - Diffusion coefficients

3. **Grid resolution** adequate:
   - Need Lc << dendrite tip radius
   - Typically Lc = 0.1-0.5 μm

4. **Boundary effects**:
   - Domain large enough (3-5× dendrite size)

### Asymmetric Growth (Should Be Symmetric)

**Problem:** 0° and 90° orientations give different results.

**Status:** ✅ Should be identical (four-fold symmetry verified)

**If you see asymmetry:**

1. **Check random initialization** - none should exist
2. **Verify constants** are not accidentally modified
3. **Run validation**:
   ```bash
   python final_validation.py
   ```

### Mass Not Conserved

**Problem:** Total concentration changes during simulation.

**Expected:** ~10-15% change due to boundary effects and numerical diffusion

**If > 20%:**

1. **Check CFL stability**:
   ```python
   config.time.cfl_factor = 3  # More conservative
   ```

2. **Reduce time step**:
   ```python
   config.time.initial_dt = 1e-6  # Smaller
   ```

3. **Check for NaN/Inf** in results

---

## Git/GitHub Issues

### Push Rejected

**Problem:** `git push` fails.

**Solutions:**

1. **Pull first** if remote has changes:
   ```bash
   git pull origin main
   git push origin main
   ```

2. **Force push** (use with caution):
   ```bash
   git push -f origin main  # Only if you're sure
   ```

3. **Check remote**:
   ```bash
   git remote -v
   ```

### SSH Permission Denied

**Problem:**
```
Permission denied (publickey)
```

**Solution:** Add SSH key to GitHub:
```bash
# Display your public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
```

---

## Getting Help

### Before Asking

1. **Check error message** carefully
2. **Search this troubleshooting guide**
3. **Try QuickTestConfig** to isolate problem
4. **Run validation**:
   ```bash
   python final_validation.py
   ```

### How to Report Issues

Include:

1. **Error message** (full traceback)
2. **Configuration used**:
   ```python
   print(config.__dict__)
   ```
3. **Python version**:
   ```bash
   python --version
   ```
4. **Package versions**:
   ```bash
   pip list
   ```
5. **Operating system**

### Where to Ask

- 📧 Email: jaavedakram@gmail.com
- 🐛 GitHub Issues: https://github.com/jaavedakram/DendriteModel/issues
- 📖 Check [Examples](Examples) for working code

---

## Validation Checklist

**Run these to verify installation:**

```bash
# 1. Check Python version
python --version  # Should be ≥ 3.7

# 2. Check packages
python -c "import numpy, matplotlib; print('OK')"

# 3. Quick test run
python -c "
from simulation_config import QuickTestConfig
from simulation_engine import run_dendrite_simulation
config = QuickTestConfig()
results = run_dendrite_simulation(config, verbose=False)
print(f'Solid fraction: {results[\"final_solid_fraction\"]:.3f}')
"

# 4. Full validation
python final_validation.py
```

**Expected output:**
```
✓✓✓ ALL VALIDATION CHECKS PASSED ✓✓✓
```

---

## Performance Benchmarks

**Expected runtimes** (reference: Intel i5, 8GB RAM):

| Configuration | Grid | Steps | Time |
|---------------|------|-------|------|
| QuickTestConfig | 50×50 | 100 | ~5s |
| DefaultConfig | 75×75 | 400 | ~25s |
| HighResolutionConfig | 100×100 | 400 | ~60s |

**If significantly slower:**
- Close other programs
- Check CPU usage (`top` / Task Manager)
- Try smaller grid first

---

## Related Topics

- [Configuration Guide](Configuration) - Parameter tuning
- [Examples](Examples) - Working code
- [Theory](Theory) - Expected physical behavior
