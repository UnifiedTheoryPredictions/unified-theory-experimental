"""
LHC Dijet Analysis for Predicted Resonances at 2.3 TeV and 3.1 TeV

This script provides tools for analyzing LHC dijet data to search for
predicted resonances from Calabi-Yau compactification theory.

Predicted resonances:
- M_coh = 2.3 ± 0.2 TeV (scalar coherent resonance)
- M_κ   = 3.1 ± 0.3 TeV (tensor coherent resonance)

Author: UnifiedTheoryPredictions
Repository: https://github.com/UnifiedTheoryPredictions/unified-theory-experimental
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import poisson, norm
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# IMPORTANT NOTE FOR EXPERIMENTAL COLLABORATORS
# ============================================================================
"""
This script currently uses SIMULATED data to demonstrate the analysis method.

TO USE REAL LHC DATA:

1. Replace simulate_lhc_data() function with data loading from:
   - CMS Open Data: https://opendata.cern.ch
   - ATLAS Open Data: https://atlasopendata.web.cern.ch
   - Or internal collaboration data

2. Required data format:
   - Dijet invariant mass spectrum (GeV)
   - Event weights and uncertainties
   - Trigger efficiency corrections

3. Contact for data access:
   - CMS: cms-dijet-conveners@cern.ch
   - ATLAS: atlas-exotics-conveners@cern.ch

4. Expected with real data:
   - ~100 fb⁻¹ integrated luminosity (Run 2 + Run 3)
   - Statistical sensitivity to ~5σ for predicted resonances
   - Systematic uncertainties dominated by jet energy scale
"""

# ============================================================================
# PHYSICAL CONSTANTS AND PREDICTIONS
# ============================================================================

PREDICTIONS = {
    "M_coh": {"center": 2300.0, "uncertainty": 200.0, "type": "scalar"},  # GeV
    "M_kappa": {"center": 3100.0, "uncertainty": 300.0, "type": "tensor"}  # GeV
}

# ============================================================================
# MATHEMATICAL MODELS
# ============================================================================

def background_model(mass, a, b, c):
    """
    Smooth background model for dijet mass spectrum.
    
    Parameters:
    -----------
    mass : array_like
        Dijet invariant mass in GeV
    a, b, c : float
        Background parameters
        
    Returns:
    --------
    background : array_like
    """
    return a * np.exp(-b * mass) + c * mass**(-3.5)

def resonance_model(mass, amplitude, center, width):
    """
    Relativistic Breit-Wigner resonance shape.
    
    Parameters:
    -----------
    mass : array_like
        Dijet invariant mass in GeV
    amplitude : float
        Resonance amplitude
    center : float
        Resonance mass in GeV
    width : float
        Resonance width in GeV
        
    Returns:
    --------
    resonance : array_like
    """
    return amplitude * (width**2) / ((mass**2 - center**2)**2 + (center * width)**2)

def full_model(mass, a, b, c, amp1, center1, width1, amp2, center2, width2):
    """
    Full model: background + two resonances.
    """
    bg = background_model(mass, a, b, c)
    res1 = resonance_model(mass, amp1, center1, width1)
    res2 = resonance_model(mass, amp2, center2, width2)
    return bg + res1 + res2

# ============================================================================
# DATA SIMULATION (REPLACE WITH REAL LHC DATA)
# ============================================================================

def simulate_lhc_data(num_points=1000, seed=42):
    """
    Simulate LHC dijet data with predicted resonances.
    
    In real analysis, replace this with CMS/ATLAS Open Data.
    """
    np.random.seed(seed)
    
    # Mass range: 1.5 TeV to 4.0 TeV
    mass = np.linspace(1500, 4000, num_points)
    
    # Background parameters (typical for dijet spectra)
    a, b, c = 1e6, 0.0015, 1e8
    
    # Generate smooth background
    bg = background_model(mass, a, b, c)
    
    # Add predicted resonances
    signal = np.zeros_like(mass)
    
    # Resonance 1: M_coh = 2.3 TeV
    res1 = resonance_model(mass, 
                          amplitude=0.05 * bg[np.abs(mass - 2300).argmin()],
                          center=2300.0,
                          width=50.0)
    
    # Resonance 2: M_κ = 3.1 TeV
    res2 = resonance_model(mass,
                          amplitude=0.03 * bg[np.abs(mass - 3100).argmin()],
                          center=3100.0,
                          width=60.0)
    
    # Total expected events
    expected = bg + res1 + res2
    
    # Poisson fluctuations
    data = np.random.poisson(expected)
    
    # Statistical uncertainties
    errors = np.sqrt(data)
    errors[errors == 0] = 1.0  # Avoid division by zero
    
    return mass, data, errors, bg, res1 + res2

# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def fit_resonances(mass, data, errors):
    """
    Fit the data to search for resonances.
    
    Returns:
    --------
    result : dict with fit parameters and significance
    """
    # Initial parameter guesses
    # [a, b, c, amp1, center1, width1, amp2, center2, width2]
    p0 = [1e6, 0.0015, 1e8,  # background
          5e3, 2300.0, 50.0,  # resonance 1
          3e3, 3100.0, 60.0]  # resonance 2
    
    # Parameter bounds
    bounds = ([1e5, 0.0005, 1e7, 0, 2200, 20, 0, 3000, 30],
              [1e7, 0.003, 1e9, 1e6, 2400, 100, 1e6, 3200, 100])
    
    try:
        # Perform fit
        popt, pcov = curve_fit(full_model, mass, data, p0=p0, 
                              sigma=errors, bounds=bounds, maxfev=5000)
        
        # Calculate uncertainties
        perr = np.sqrt(np.diag(pcov))
        
        # Calculate significance for each resonance
        significance = []
        for i, name in enumerate(["Resonance 1 (2.3 TeV)", "Resonance 2 (3.1 TeV)"]):
            amp_idx = 3 + i*3
            amp = popt[amp_idx]
            amp_err = perr[amp_idx]
            if amp_err > 0:
                sig = amp / amp_err
                significance.append((name, sig))
        
        return {
            "parameters": popt,
            "uncertainties": perr,
            "covariance": pcov,
            "significance": significance,
            "success": True
        }
    
    except Exception as e:
        print(f"Fit failed: {e}")
        return {"success": False, "error": str(e)}

def calculate_significance_local(data, bg, window=100):
    """
    Calculate local significance around predicted masses.
    """
    significances = {}
    
    for name, pred in PREDICTIONS.items():
        center = pred["center"]
        # Find mass bin closest to predicted center
        mass_bins = np.linspace(1500, 4000, len(data))
        idx = np.abs(mass_bins - center).argmin()
        
        # Define signal region (± window GeV around prediction)
        mask = (mass_bins > center - window) & (mass_bins < center + window)
        
        # Calculate signal and background in signal region
        signal_sum = np.sum(data[mask] - bg[mask])
        bg_sum = np.sum(bg[mask])
        
        if bg_sum > 0:
            significance = signal_sum / np.sqrt(bg_sum)
            significances[name] = significance
        else:
            significances[name] = 0.0
    
    return significances

# ============================================================================
# VISUALIZATION
# ============================================================================

def plot_analysis(mass, data, errors, bg, signal, fit_result=None):
    """
    Create comprehensive analysis plot.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Data with background
    axes[0, 0].errorbar(mass, data, yerr=errors, fmt='.', color='black', 
                       alpha=0.5, label='Simulated Data', markersize=2)
    axes[0, 0].plot(mass, bg, 'r-', linewidth=2, label='Background')
    axes[0, 0].set_xlabel('Dijet Mass (GeV)')
    axes[0, 0].set_ylabel('Events')
    axes[0, 0].set_title('LHC Dijet Spectrum with Background')
    axes[0, 0].set_yscale('log')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()
    
    # Plot 2: Background-subtracted data
    bg_subtracted = data - bg
    bg_subtracted_err = np.sqrt(data + bg)  # Approximate error
    
    axes[0, 1].errorbar(mass, bg_subtracted, yerr=bg_subtracted_err, 
                       fmt='.', color='blue', alpha=0.5, markersize=2)
    axes[0, 1].axhline(y=0, color='red', linestyle='--')
    
    # Mark predicted resonance positions
    for name, pred in PREDICTIONS.items():
        axes[0, 1].axvline(x=pred["center"], color='green', 
                          linestyle=':', alpha=0.7,
                          label=f'Predicted {name}: {pred["center"]/1000:.1f} TeV')
    
    axes[0, 1].set_xlabel('Dijet Mass (GeV)')
    axes[0, 1].set_ylabel('Events - Background')
    axes[0, 1].set_title('Background-Subtracted Spectrum')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].legend()
    
    # Plot 3: Signal region zoom
    zoom_min, zoom_max = 2200, 3400
    zoom_mask = (mass > zoom_min) & (mass < zoom_max)
    
    axes[1, 0].errorbar(mass[zoom_mask], bg_subtracted[zoom_mask], 
                       yerr=bg_subtracted_err[zoom_mask], 
                       fmt='.', color='blue', alpha=0.7, markersize=3)
    axes[1, 0].axhline(y=0, color='red', linestyle='--')
    
    # Add predicted resonance bands
    for name, pred in PREDICTIONS.items():
        axes[1, 0].axvspan(pred["center"] - pred["uncertainty"],
                          pred["center"] + pred["uncertainty"],
                          alpha=0.2, color='green',
                          label=f'{name} ± uncertainty')
    
    axes[1, 0].set_xlabel('Dijet Mass (GeV)')
    axes[1, 0].set_ylabel('Events - Background')
    axes[1, 0].set_title('Signal Region (2.2-3.4 TeV)')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()
    
    # Plot 4: Significance scan (if fit was successful)
    if fit_result and fit_result["success"]:
        axes[1, 1].axis('off')
        text = "Fit Results:\n\n"
        for i, (name, sig) in enumerate(fit_result["significance"]):
            text += f"{name}: {sig:.1f}σ\n"
        
        if fit_result["significance"]:
            max_sig = max([sig for _, sig in fit_result["significance"]])
            text += f"\nMaximum significance: {max_sig:.1f}σ\n"
        
        # Add theory predictions
        text += "\nTheory Predictions:\n"
        for name, pred in PREDICTIONS.items():
            text += f"{name}: {pred['center']/1000:.1f} ± {pred['uncertainty']/1000:.1f} TeV\n"
        
        axes[1, 1].text(0.1, 0.5, text, transform=axes[1, 1].transAxes,
                       fontsize=10, verticalalignment='center',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        axes[1, 1].set_title('Analysis Summary')
    else:
        axes[1, 1].axis('off')
        axes[1, 1].text(0.5, 0.5, 'Fit not available\nor unsuccessful',
                       transform=axes[1, 1].transAxes,
                       ha='center', va='center', fontsize=12)
    
    plt.tight_layout()
    return fig

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main analysis pipeline.
    """
    print("=" * 70)
    print("LHC DIJET ANALYSIS FOR PREDICTED RESONANCES")
    print("From Calabi-Yau Compactification Theory")
    print("=" * 70)
    
    # Step 1: Generate/simulate data
    print("\n1. Loading/Simulating LHC dijet data...")
    mass, data, errors, bg, signal = simulate_lhc_data()
    print(f"   • Mass range: {mass[0]:.0f} - {mass[-1]:.0f} GeV")
    print(f"   • Total events: {np.sum(data):.0f}")
    
    # Step 2: Calculate local significances
    print("\n2. Calculating local significances...")
    local_sigs = calculate_significance_local(data, bg)
    for name, sig in local_sigs.items():
        pred = PREDICTIONS[name]
        print(f"   • {name} ({pred['center']/1000:.1f} TeV): {sig:.1f}σ")
    
    # Step 3: Fit for resonances
    print("\n3. Fitting for resonances...")
    fit_result = fit_resonances(mass, data, errors)
    
    if fit_result["success"]:
        print("   • Fit successful!")
        for name, sig in fit_result["significance"]:
            print(f"   • {name}: {sig:.1f}σ")
    else:
        print(f"   • Fit failed: {fit_result.get('error', 'Unknown error')}")
    
    # Step 4: Create visualization
    print("\n4. Generating plots...")
    fig = plot_analysis(mass, data, errors, bg, signal, fit_result)
    
    # Save results
    output_files = []
    
    # Save figure
    fig.savefig('dijet_analysis_results.png', dpi=300, bbox_inches='tight')
    output_files.append('dijet_analysis_results.png')
    print(f"   • Saved plot: dijet_analysis_results.png")
    
    # Save data to text file
    np.savetxt('dijet_data.txt', 
              np.column_stack([mass, data, errors, bg]),
              header='mass[GeV] data errors background',
              fmt='%.1f %.1f %.1f %.1f')
    output_files.append('dijet_data.txt')
    print(f"   • Saved data: dijet_data.txt")
    
    # Save fit results
    if fit_result["success"]:
        with open('fit_results.txt', 'w') as f:
            f.write("FIT RESULTS\n")
            f.write("===========\n\n")
            f.write("Parameters:\n")
            params_names = ['a', 'b', 'c', 'amp1', 'center1', 'width1', 
                           'amp2', 'center2', 'width2']
            for name, val, err in zip(params_names, 
                                      fit_result["parameters"], 
                                      fit_result["uncertainties"]):
                f.write(f"{name:10s} = {val:12.3f} ± {err:8.3f}\n")
            
            f.write("\nSignificance:\n")
            for name, sig in fit_result["significance"]:
                f.write(f"{name}: {sig:.1f}σ\n")
        
        output_files.append('fit_results.txt')
        print(f"   • Saved fit results: fit_results.txt")
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print(f"Generated files: {', '.join(output_files)}")
    print("=" * 70)
    
    # Show plot (if running interactively)
    try:
        plt.show()
    except:
        pass  # Running in non-interactive mode
    
    return fit_result

# ============================================================================
# EXECUTE IF RUN AS SCRIPT
# ============================================================================

if __name__ == "__main__":
    main()