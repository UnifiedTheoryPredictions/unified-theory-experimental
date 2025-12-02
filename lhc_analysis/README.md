# LHC Dijet Analysis

Scripts for analyzing LHC data to search for predicted resonances at:
- **M_coh** = 2.3 ± 0.2 TeV (scalar coherent resonance)
- **M_κ** = 3.1 ± 0.3 TeV (tensor coherent resonance)

## Files

- `dijet_analysis.py` - Main analysis script
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the analysis
python dijet_analysis.py
```

## Output

The script generates:
1. `dijet_analysis_results.png` - Analysis plots
2. `dijet_data.txt` - Simulated/analyzed data
3. `fit_results.txt` - Fit parameters and significances

## Theory Context

These resonances are predicted from heterotic string compactification on a Calabi-Yau manifold with Hodge numbers h¹¹=6, h²¹=251. The predictions come with full error analysis and are testable with existing LHC data.

## Notes

- This simulation uses artificial data. Replace with CMS/ATLAS Open Data for real analysis.
- For actual LHC data analysis, use official CMS/ATLAS software frameworks.
- See the comments in `dijet_analysis.py` for instructions on using real LHC data.

## Repository

Main repository: https://github.com/UnifiedTheoryPredictions/unified-theory-experimental