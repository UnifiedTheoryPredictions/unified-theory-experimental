# LHC DIJET ANALYSIS PROTOCOL
## For Search of Predicted Resonances at 2.3 TeV and 3.1 TeV

**Theory Reference:** Unified Theory of Fundamental Interactions (Zenodo: https://doi.org/10.5281/zenodo.17400620)

**Predicted Resonances:**
• M_coh = 2.3 ± 0.2 TeV (scalar coherent resonance)
• M_κ = 3.1 ± 0.3 TeV (tensor coherent resonance)

---

## 1. DATA ACCESS AND PREPARATION

### 1.1 Data Sources

**Primary datasets:**
```
CMS OPEN DATA:
• Dataset: /JetHT/Run2018A-UL2018_MiniAODv2-v2/MINIAOD
• Integrated luminosity: ~60 fb⁻¹ (Run 2)
• Access: https://opendata.cern.ch/record/12350
```

```
ATLAS OPEN DATA:
• Dataset: mc16_13TeV.364701.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ7W.deriv.DAOD_JETM8
• Integrated luminosity: ~50 fb⁻¹
• Access: https://atlasopendata.web.cern.ch
```

**Simulated datasets (for background estimation):**
• QCD multijet events (Pythia8, Sherpa, MadGraph)
• Top quark pair production
• W/Z+jets production

### 1.2 Software Requirements
```
ANALYSIS FRAMEWORK:
• ROOT version: 6.26/10 or newer
• CMSSW release: CMSSW_10_6_X for Run 2 analysis
• Key packages: RooFit, RooStats, TRExFitter
• Python: 3.8+ with uproot, awkward, hist
```

```
COMPUTING RESOURCES:
• Minimum: 32 GB RAM, 8 cores
• Recommended: 64+ GB RAM, 16+ cores
• Storage: 1+ TB for local data caching
• Batch system: Access to HPC or GRID
```

---

## 2. EVENT SELECTION

### 2.1 Trigger Requirements
```
CMS TRIGGERS:
• HLT_PFHT1050_v* (high pT jet triggers)
• HLT_AK8PFJet400_TrimMass30_v*
• Prescale factors must be applied
```

```
ATLAS TRIGGERS:
• HLT_j460_a10_lcw_sub_L1J100
• HLT_4j100_a10t_lcw_L1J100
• Use trigger efficiency maps
```

### 2.2 Object Selection

**Jets:**
```
JET SELECTION CRITERIA:
• Anti-kT algorithm with R=0.4 or 0.8
• pT > 500 GeV (leading jet), > 400 GeV (subleading)
• |η| < 2.4 (CMS) or 2.5 (ATLAS)
• Jet energy corrections: L1FastJet, L2Relative, L3Absolute
• Pileup mitigation: Area-based subtraction
```

**Event cleaning:**
• Primary vertex: ≥4 tracks, |z| < 24 cm
• Jet cleaning: Remove events with noisy jets
• Pileup: ρ < 40 GeV (CMS), NPV < 60 (ATLAS)

### 2.3 Dijet Selection
```
DIJET SELECTION:
1. Select two highest pT jets
2. Require Δφ(j1, j2) > 2.0 radians
3. Require |η*| = |η1 - η2|/2 < 1.5
4. Calculate dijet mass: M_jj = √(2·pT1·pT2·cosh(Δη) - 2·pT1·pT2·cos(Δφ))
5. Mass range: 1.5-4.0 TeV for analysis
```

---

## 3. BACKGROUND MODELING

### 3.1 Smooth Background Parameterization
```
BACKGROUND FUNCTION:
dN/dM = p0·(1 - M/√s)^(p1)·M^(p2)
• p0: Normalization
• p1, p2: Shape parameters
• √s: Center-of-mass energy (13 TeV)
```

**Alternative functions to test:**
• Exponential: A·exp(-B·M)
• Power law: A·M^(-γ)
• Bernstein polynomials (for systematic studies)

### 3.2 Background Estimation Methods

**Method A: Sideband fitting**
```
SIDEBAND REGIONS:
• Low sideband: 1.5-2.0 TeV
• Signal region: 2.1-2.5 TeV (M_coh), 2.9-3.3 TeV (M_κ)
• High sideband: 3.6-4.0 TeV
• Fit background to sidebands, interpolate to signal region
```

**Method B: Smoothing techniques**
• Kernel density estimation
• Moving average with adaptive bandwidth
• Gaussian process regression

### 3.3 Systematic Uncertainties

**Dominant systematics:**
```
JET ENERGY SCALE (JES):
• Uncertainty: 1-3% depending on pT and η
• Propagate through mass calculation
• Use in-situ calibration (Z+jet, γ+jet balance)
```

```
JET ENERGY RESOLUTION (JER):
• Uncertainty: 10-15% at high pT
• Smearing correction applied
• Impact on mass resolution
```

**Other systematics:**
• Luminosity (1.7-2.5%)
• Pileup modeling
• Trigger efficiency
• PDF uncertainties

---

## 4. SIGNAL MODELING

### 4.1 Resonance Lineshape
```
RELAVISTIC BREIT-WIGNER:
dσ/dM ∝ (M·Γ)/[(M² - M₀²)² + (M₀·Γ)²]
• M₀: Resonance mass (2.3 or 3.1 TeV)
• Γ: Resonance width (expected: 50-100 GeV)
• Include detector resolution convolution
```

### 4.2 Detector Effects

**Mass resolution:**
```
RESOLUTION FUNCTION:
σ_M/M ≈ 10% at 2 TeV, scaling as 1/√M
• Parameterize as Gaussian smearing
• Determine from MC simulation
• Verify with Z'→jj simulated events
```

**Acceptance and efficiency:**
```
ACCEPTANCE CORRECTION:
A(M) = ∫ dη1 dη2 Θ(selection cuts)
• Calculate from MC for each mass point
• Typically 30-50% for central dijets
• Include trigger efficiency map
```

---

## 5. STATISTICAL ANALYSIS

### 5.1 Hypothesis Testing

**Test statistic:**
```
PROFILE LIKELIHOOD RATIO:
q(μ) = -2 ln[L(μ, θ̂̂)/L(μ̂, θ̂)]
• μ: Signal strength (0 for background-only)
• θ: Nuisance parameters (systematics)
• Use asymptotic approximation for p-values
```

### 5.2 Significance Calculation

**Local significance:**
```
Z_LOCAL = √(q(0)) for discovery test
• Convert to p-value: p = 1 - Φ(Z)
• Discovery threshold: Z > 5 (p < 2.87×10⁻⁷)
• Evidence threshold: Z > 3 (p < 1.35×10⁻³)
```

**Look-elsewhere effect:**
```
TRIAL FACTOR CORRECTION:
• Search window: 1.5-4.0 TeV
• Effective number of independent bins
• Use Gross-Vitells method for global p-value
```

### 5.3 Exclusion Limits

**95% CL upper limits:**
• Use CL_s method
• Include systematics via nuisance parameters
• Report expected and observed limits

---

## 6. ANALYSIS WORKFLOW

### 6.1 Step-by-Step Procedure

**Week 1-2: Data preparation**
```
DATA PROCESSING:
1. Download datasets from CERN Open Data
2. Apply basic event selection
3. Calculate dijet masses
4. Create histograms (100 GeV bins initially)
5. Produce quick-look plots
```

**Week 3-4: Background modeling**
```
BACKGROUND STUDIES:
1. Fit smooth function to data
2. Compare different functional forms
3. Estimate systematic uncertainties
4. Validate with MC simulation
5. Define signal regions
```

**Week 5-6: Signal search**
```
SIGNAL INJECTION:
1. Add simulated signals to background
2. Perform fits with floating signal strength
3. Calculate significances
4. Determine exclusion limits
5. Study angular distributions
```

**Week 7-8: Systematic studies**
```
SYSTEMATICS EVALUATION:
1. Vary JES within uncertainties
2. Test different background functions
3. Check pileup dependence
4. Study trigger efficiency impact
5. Combine all systematics
```

### 6.2 Cross-Checks

**Essential validation:**
1. **Closure test:** Fit MC without signal, recover μ=0
2. **Blinding:** Keep signal region blinded until analysis fixed
3. **Subsample consistency:** Split data, check stability
4. **Alternative methods:** Compare different statistical approaches

---

## 7. EXPECTED RESULTS

### 7.1 Sensitivity Projections

**With 100 fb⁻¹ (Run 2 + Run 3):**
```
EXPECTED SIGNIFICANCE:
• M_coh (2.3 TeV): 3-4σ with smooth background
• M_κ (3.1 TeV): 2-3σ with smooth background
• Combined: 4-5σ if both resonances present
```

**Exclusion limits (95% CL):**
• σ×BR < 0.1-1.0 fb depending on resonance width
• Convert to cross-section ratio to SM background

### 7.2 Angular Distributions

**Discriminating variables:**
```
ANGULAR OBSERVABLES:
• χ_dijet = exp(|y1 - y2|) ≈ (1 + |cos θ*|)/(1 - |cos θ*|)
• Centrality ratio: |y_boost| = |y1 + y2|/2
• Azimuthal correlation: Δφ(j1, j2)
• For tensor resonance: check spin-2 angular distributions
```

---

## 8. INTERPRETATION

### 8.1 Connection to Theory

**If resonances detected:**
• Confirm mass predictions from Calabi-Yau compactification
• Measure widths to extract coupling parameters
• Angular distributions test spin assignments
• Cross-sections relate to κ_q parameter

**If no signal:**
• Set limits on production cross-sections
• Constrain parameters of unified theory
• Guide theoretical refinements

### 8.2 Alternative Explanations

**Standard Model backgrounds:**
• QCD dijet continuum (smooth)
• Top quark pair production (threshold at ~0.7 TeV)
• W/Z+jets (peaks at W/Z masses)

**Other new physics:**
• Z' bosons (different angular distributions)
• Quantum black holes (different mass spectrum)
• Colorons or axigluons

---

## 9. PUBLICATION PREPARATION

### 9.1 Required Plots

**Main figures:**
1. Dijet mass spectrum with background fit
2. Background-subtracted spectrum
3. Significance scan vs mass
4. Exclusion limits (expected and observed)
5. Angular distributions

**Supplementary:**
• Systematic uncertainty breakdown
• Closure tests
• Alternative background functions
• MC validation plots

### 9.2 Data Release

**With publication:**
• Analysis code on GitHub
• Background models and fits
• Statistical analysis scripts
• Documentation for reproduction

---

## 10. COLLABORATION CONTACTS

### 10.1 CMS Collaboration
• Dijet conveners: cms-dijet-conveners@cern.ch
• Exotica group: cms-exotica-conveners@cern.ch
• Open Data support: cms-opendata-support@cern.ch

### 10.2 ATLAS Collaboration
• Exotics conveners: atlas-exotics-conveners@cern.ch
• Standard Model conveners: atlas-sm-conveners@cern.ch

**Protocol Version:** 1.0  
**Last Updated:** December 2025  
**Contact:** adonaidabagyan@gmail.com  
**GitHub Repository:** https://github.com/UnifiedTheoryPredictions/unified-theory-experimental  
**Data Sources:** https://opendata.cern.ch | https://atlasopendata.web.cern.ch