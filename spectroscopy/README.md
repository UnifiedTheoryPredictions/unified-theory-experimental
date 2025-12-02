# Spectroscopy Simulations

Scripts for simulating infrared and femtosecond measurements to test predictions:
- **Infrared peaks** at 0.203, 0.406, 0.609 eV
- **Temporal correlation** at τ = 20.4 fs

## Files

- `ir_simulation.py` - Infrared spectrum simulation
- `femtosecond_simulation.py` - Femtosecond correlation simulation  
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Infrared Simulation
```bash
python ir_simulation.py
```

### Femtosecond Simulation
```bash
python femtosecond_simulation.py
```

## Output Files

### Infrared Simulation generates:
1. `ir_spectrum_results.png` - Spectrum plots with peak detection
2. `ir_spectrum_data.txt` - Simulated spectrum data
3. `ir_analysis_results.txt` - Peak parameters and comparisons

### Femtosecond Simulation generates:
1. `femtosecond_correlation_results.png` - Correlation plots
2. `femtosecond_data.txt` - Correlation data
3. `femtosecond_analysis_results.txt` - Time constant measurements

## Theory Context

These simulations demonstrate the expected signals for experimental testing of predictions from heterotic string compactification on a Calabi-Yau manifold.

### Infrared Peaks:
Derived from compactification radius R_c = 1.619 nm and quantum consistency parameter κ_q = 1.000000. The energies are:
- E₁ = ħc/(2πR_c) × √g_s × C_top × corrections = 0.203 ± 0.010 eV
- E₂ = 2 × E₁ = 0.406 ± 0.020 eV
- E₃ = 3 × E₁ = 0.609 ± 0.030 eV

### Temporal Correlation:
- τ = ħ/E₁ + τ_consensus = (2.04 ± 0.02) × 10⁻¹⁴ s
- Corresponds to the inverse of the fundamental energy scale plus consensus time

## Experimental Parameters

### For Infrared Measurements:
- Temperature: 0.05 K
- Resolution: < 10⁻¹⁴ eV
- Number of scans: 2000
- Expected S/N: > 7
- Sample: Ultrapure silicon or GaAs

### For Femtosecond Measurements:
- Laser: 50 fs, 800 nm, 1 kHz, 1 mJ/pulse
- Temperature: 0.05 K
- Number of pulses: 2×10⁶
- Time resolution: 0.05 fs
- Expected S/N: > 7

## Repository

Main repository: https://github.com/UnifiedTheoryPredictions/unified-theory-experimental