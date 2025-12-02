# INFRARED SPECTROSCOPY PROTOCOL
## For Detection of Predicted Energy Peaks at 0.203, 0.406, 0.609 eV

**Theory Reference:** Unified Theory of Fundamental Interactions (Zenodo: https://doi.org/10.5281/zenodo.17400620)

**Predicted Values:**
• E₁ = 0.203 ± 0.010 eV
• E₂ = 0.406 ± 0.020 eV  
• E₃ = 0.609 ± 0.030 eV

---

## 1. EQUIPMENT REQUIREMENTS

### 1.1 Core Instrumentation
```
SPECTROMETER:
• Type: Fourier-transform infrared (FTIR) with step-scan capability
• Required resolution: < 10⁻¹⁴ eV (0.1 μeV)
• Spectral range: 0.1 - 0.8 eV (1240 - 15500 nm)
• Detector: Liquid helium cooled bolometer or photoconductive detector
• Beamsplitter: KBr or CsI for far-infrared range
```

```
CRYOGENIC SYSTEM:
• Type: Dilution refrigerator with optical access
• Base temperature: 0.05 K (50 mK)
• Temperature stability: ±0.005 K over 24 hours
• Optical windows: Diamond or polyethylene, anti-reflection coated
• Vibration isolation: Active damping system
```

```
SAMPLE ENVIRONMENT:
• Sample holder: OFHC copper, gold-plated
• Thermal coupling: Apiezon N grease or indium foil
• Pressure: < 10⁻⁷ mbar (UHV compatible)
• Magnetic shielding: μ-metal or superconducting shield
```

### 1.2 Optional but Recommended
• Lock-in amplifier for phase-sensitive detection
• White light source with intensity stabilizer
• Polarization control: Wire grid polarizer + quarter-wave plate
• In-situ temperature calibration: RuO₂ or Cernox sensor

---

## 2. SAMPLE PREPARATION

### 2.1 Material Selection
**Primary candidates:**
1. **Ultrapure silicon** (float-zone, >10 kΩ·cm)
   • Advantages: Low impurity, well-characterized phonons
   • Sample size: 10×10×1 mm, double-side polished

2. **Gallium arsenide** (semi-insulating)
   • Advantages: High electron mobility
   • Sample size: 10×10×0.5 mm

3. **Diamond** (type IIa)
   • Advantages: Excellent thermal conductivity
   • Sample size: 5×5×0.3 mm

### 2.2 Surface Preparation
```
CLEANING PROCEDURE:
1. Sonicate in acetone for 10 minutes
2. Rinse in isopropanol (IPA)
3. Oxygen plasma cleaning (100 W, 5 minutes)
4. Immediate transfer to UHV chamber
```

### 2.3 Mounting Protocol
```
MOUNTING STEPS:
1. Apply thin layer of Apiezon N grease to sample holder
2. Place sample using ceramic tweezers
3. Apply gentle pressure for 30 seconds
4. Attach thermal sensor with GE varnish
5. Install radiation shield at 4K stage
```

---

## 3. MEASUREMENT PROCEDURE

### 3.1 System Calibration

**Day 1: Baseline establishment**
```
CALIBRATION SEQUENCE:
1. Cool system to 4K (4 hours)
2. Cool to base temperature 0.05K (8-12 hours)
3. Stabilization period: 3 hours at 0.05K
4. Measure empty chamber spectrum (background)
5. Calibrate with reference samples:
   • Polyethylene film (known absorption at 0.117 eV)
   • Water vapor lines (0.205 eV, 0.414 eV)
```

### 3.2 Main Measurement

**Phase 1: High-resolution scan**
```
SCAN PARAMETERS:
• Spectral range: 0.15 - 0.65 eV
• Resolution: 5×10⁻¹⁵ eV
• Number of scans: 2000
• Scan speed: 0.5 cm⁻¹/s (step-scan mode)
• Apodization: Blackman-Harris 3-term
• Phase correction: Mertz method
```

**Phase 2: Signal optimization**
```
OPTIMIZATION STEPS:
1. Adjust beam alignment for maximum throughput
2. Optimize detector bias voltage
3. Set lock-in time constant to 30 seconds
4. Verify linearity with neutral density filters
5. Measure with different polarizations (0°, 45°, 90°)
```

### 3.3 Control Measurements

**At room temperature:**
• Quick scan to verify sample transparency
• Check for atmospheric absorption lines

**With different samples:**
• Repeat with Si, GaAs, diamond
• Compare with theoretical phonon densities

**Background verification:**
• Measure with sample rotated 90°
• Block beam to check detector dark noise

---

## 4. DATA ANALYSIS

### 4.1 Peak Identification Protocol

**Step 1: Background subtraction**
```
BACKGROUND MODEL:
I_corrected(ν) = I_raw(ν) - [A + B·ν + C·ν²]
• Fit polynomial to regions away from predicted peaks
• Use 0.12-0.18 eV and 0.62-0.68 eV for background determination
```

**Step 2: Peak fitting**
```
FITTING FUNCTION (each peak):
I(ν) = I₀ + A·[γ²/((ν-ν₀)² + γ²)] + Gaussian_term
• Voigt profile preferred (Lorentzian + Gaussian)
• Initial guesses: ν₀ from predictions, γ = 0.01 eV
• Fit constraints: 0.18 < ν₀ < 0.22 eV for E₁, etc.
```

**Step 3: Significance calculation**
```
SIGNAL-TO-NOISE CALCULATION:
S/N = (peak_height - background)/σ_noise
σ_noise = std_dev(0.12-0.18 eV region)
Minimum requirement: S/N > 7 for claim of detection
```

### 4.2 Expected Results

**For successful detection:**
```
EXPECTED PARAMETERS:
• E₁ position: 0.203 ± 0.006 eV
• E₂ position: 0.406 ± 0.012 eV
• E₃ position: 0.609 ± 0.018 eV
• Peak ratios: I₂/I₁ = 0.9-1.1, I₃/I₁ = 0.7-1.0
• Widths: Γ₁ ≈ 0.01 eV, Γ₂ ≈ 0.02 eV, Γ₃ ≈ 0.03 eV
```

**Consistency checks:**
• Temperature dependence: Should disappear above 10K
• Sample dependence: Similar peaks in different materials
• Polarization: Should be isotropic for scalar modes

---

## 5. TROUBLESHOOTING

### 5.1 Common Problems

**Problem: No peaks detected**
```
SOLUTIONS:
1. Verify temperature: Must be < 0.1K
2. Check sample thermalization: ΔT < 0.01K across sample
3. Increase integration time: Up to 5000 scans
4. Verify beam alignment: Use visible laser for alignment
5. Check window cleanliness: May need re-cleaning
```

**Problem: Excessive noise**
```
SOLUTIONS:
1. Improve vibration isolation
2. Check detector temperature stability
3. Verify lock-in settings (time constant > 10s)
4. Reduce source intensity fluctuations
5. Check for electromagnetic interference
```

### 5.2 Quality Control Metrics

**Must achieve before claiming detection:**
1. Temperature stability: ±0.005K over measurement period
2. Spectral resolution: Δν/ν < 5×10⁻⁵
3. Noise floor: < 10⁻⁴ in absorbance units
4. Reproducibility: Same peaks in 3 independent cool-downs

---

## 6. INTERPRETATION AND PUBLICATION

### 6.1 Criteria for Success

**Detection criteria (all must be met):**
1. ≥2 peaks detected within 3% of predicted energies
2. S/N > 7 for main peak (0.203 eV)
3. Consistent peak ratios (I₂/I₁, I₃/I₁ within 30% of predicted)
4. Temperature dependence consistent with theory
5. Reproducible across different samples

### 6.2 Publication Guidelines

**Data to include in publication:**
• Raw spectra and background-subtracted data
• Fitting parameters with uncertainties
• Temperature dependence plots
• Sample characterization data
• Calibration spectra

**Theory comparison:**
• Include comparison with predicted values
• Discuss implications for κ_q parameter
• Address alternative explanations

---

## 7. SAFETY PROCEDURES

### 7.1 Cryogenic Safety
• Always wear face shield when handling cryogens
• Ensure adequate ventilation for helium gas
• Check pressure relief valves weekly
• Never work alone with cryogenic systems

### 7.2 Laser Safety
• Use appropriate eyewear for alignment lasers
• Install beam blocks and shutters
• Post warning signs when laser is active
• Limit optical power to eye-safe levels

---

**Protocol Version:** 1.0  
**Last Updated:** December 2025  
**Contact:** adonaidabagyan@gmail.com  
**GitHub Repository:** https://github.com/UnifiedTheoryPredictions/unified-theory-experimental