"""
Infrared Spectroscopy Simulation for Predicted Peaks at 0.203, 0.406, 0.609 eV

This script simulates high-resolution FTIR spectra to demonstrate
the predicted infrared peaks from Calabi-Yau compactification.

Predicted peaks:
- E1 = 0.203 ± 0.010 eV
- E2 = 0.406 ± 0.020 eV
- E3 = 0.609 ± 0.030 eV

Author: UnifiedTheoryPredictions
Repository: https://github.com/UnifiedTheoryPredictions/unified-theory-experimental
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# THEORETICAL PREDICTIONS
# ============================================================================

PREDICTIONS = {
    "E1": {"energy": 0.203, "uncertainty": 0.010, "amplitude": 1.0, "width": 0.010},
    "E2": {"energy": 0.406, "uncertainty": 0.020, "amplitude": 0.5, "width": 0.020},
    "E3": {"energy": 0.609, "uncertainty": 0.030, "amplitude": 0.3, "width": 0.030}
}

# ============================================================================
# SPECTRAL MODELS
# ============================================================================

def gaussian(x, amplitude, center, sigma):
    """Gaussian peak shape."""
    return amplitude * np.exp(-((x - center) / sigma)**2 / 2)

def lorentzian(x, amplitude, center, gamma):
    """Lorentzian peak shape."""
    return amplitude * (gamma**2) / ((x - center)**2 + gamma**2)

def voigt(x, amplitude, center, sigma, gamma):
    """Voigt profile (convolution of Gaussian and Lorentzian)."""
    # Simplified approximation
    g = gaussian(x, 1.0, center, sigma)
    l = lorentzian(x, 1.0, center, gamma)
    return amplitude * (g + l) / 2

def background(x, a, b, c):
    """Polynomial background."""
    return a + b*x + c*x**2

def full_spectrum(x, a, b, c, 
                  amp1, cen1, sig1, gam1,
                  amp2, cen2, sig2, gam2,
                  amp3, cen3, sig3, gam3):
    """Full spectrum model: background + three peaks."""
    bg = background(x, a, b, c)
    peak1 = voigt(x, amp1, cen1, sig1, gam1)
    peak2 = voigt(x, amp2, cen2, sig2, gam2)
    peak3 = voigt(x, amp3, cen3, sig3, gam3)
    return bg + peak1 + peak2 + peak3

# ============================================================================
# SPECTRUM GENERATION
# ============================================================================

def generate_ftir_spectrum(num_points=2000, temperature=0.05, resolution=5e-6):
    """
    Generate simulated FTIR spectrum with predicted peaks.
    
    Parameters:
    -----------
    num_points : int
        Number of spectral points
    temperature : float
        Sample temperature in Kelvin (0.05 K for proposed experiment)
    resolution : float
        Spectral resolution in eV (5e-6 eV = 5 μeV for high-resolution FTIR)
        
    Returns:
    --------
    energy : array
        Energy axis in eV
    spectrum : array
        Simulated intensity
    noise : array
        Estimated noise level
    """
    # Energy range: 0.1 to 0.8 eV (infrared)
    energy = np.linspace(0.1, 0.8, num_points)
    
    # Background (typical for semiconductors at low temperature)
    bg_params = [0.1, -0.05, 0.02]  # [a, b, c]
    background_signal = background(energy, *bg_params)
    
    # Add predicted peaks
    spectrum = background_signal.copy()
    
    for name, pred in PREDICTIONS.items():
        peak = voigt(energy,
                    pred["amplitude"],
                    pred["energy"],
                    pred["width"] / 2.355,  # Convert FWHM to sigma
                    pred["width"] / 2)      # Convert FWHM to gamma
        spectrum += peak
    
    # Add temperature-dependent effects
    if temperature > 0:
        # Boltzmann factor for temperature broadening
        kT = 8.617333262e-5 * temperature  # eV
        broadening = np.exp(-energy / kT)
        spectrum *= broadening
    
    # Add noise (typical for high-resolution FTIR)
    # Signal-to-noise improves with sqrt(scan_number)
    scan_number = 2000  # As proposed in protocol
    base_noise = 0.005 * np.sqrt(np.abs(spectrum) + 0.001)
    noise = base_noise / np.sqrt(scan_number)
    
    # Add statistical fluctuations
    spectrum_with_noise = spectrum + np.random.normal(0, noise)
    
    # Apply instrumental resolution
    if resolution > 0:
        from scipy.ndimage import gaussian_filter1d
        # Convert resolution from eV to pixels
        sigma_pixels = resolution / (energy[1] - energy[0])
        spectrum_with_noise = gaussian_filter1d(spectrum_with_noise, sigma_pixels)
    
    return energy, spectrum_with_noise, noise

# ============================================================================
# PEAK DETECTION AND ANALYSIS
# ============================================================================

def detect_peaks(energy, spectrum, height_threshold=0.05, distance=50):
    """
    Detect peaks in spectrum and compare with predictions.
    
    Returns:
    --------
    detected_peaks : list of tuples (energy, amplitude)
    matches : dict of matched predictions
    """
    # Find peaks
    peak_indices, properties = find_peaks(spectrum, 
                                         height=height_threshold,
                                         distance=distance,
                                         prominence=0.02)
    
    detected_peaks = []
    for idx in peak_indices:
        detected_peaks.append({
            "energy": energy[idx],
            "amplitude": spectrum[idx],
            "index": idx
        })
    
    # Match with predictions
    matches = {}
    tolerance = 0.05  # 50 meV tolerance for matching
    
    for name, pred in PREDICTIONS.items():
        best_match = None
        best_diff = tolerance
        
        for peak in detected_peaks:
            diff = abs(peak["energy"] - pred["energy"])
            if diff < best_diff:
                best_diff = diff
                best_match = peak
        
        if best_match:
            matches[name] = {
                "predicted": pred["energy"],
                "measured": best_match["energy"],
                "difference": best_match["energy"] - pred["energy"],
                "relative_error": abs(best_match["energy"] - pred["energy"]) / pred["energy"],
                "amplitude": best_match["amplitude"]
            }
    
    return detected_peaks, matches

def fit_spectrum(energy, spectrum, noise):
    """
    Fit spectrum to extract precise peak parameters.
    """
    # Initial guesses based on predictions
    p0 = [
        # Background: [a, b, c]
        0.1, -0.05, 0.02,
        # Peak 1: [amp, center, sigma, gamma]
        1.0, 0.203, 0.004, 0.008,
        # Peak 2
        0.5, 0.406, 0.008, 0.016,
        # Peak 3
        0.3, 0.609, 0.012, 0.024
    ]
    
    # Parameter bounds
    lower_bounds = [0, -1, 0,
                   0, 0.18, 0.001, 0.001,
                   0, 0.38, 0.001, 0.001,
                   0, 0.58, 0.001, 0.001]
    
    upper_bounds = [1, 0, 1,
                   2, 0.22, 0.02, 0.02,
                   1, 0.42, 0.04, 0.04,
                   1, 0.62, 0.06, 0.06]
    
    try:
        popt, pcov = curve_fit(full_spectrum, energy, spectrum, p0=p0,
                              sigma=noise, bounds=(lower_bounds, upper_bounds),
                              maxfev=10000)
        
        perr = np.sqrt(np.diag(pcov))
        
        # Extract fitted parameters
        fit_results = {
            "background": popt[:3],
            "peaks": []
        }
        
        for i in range(3):
            idx = 3 + i*4
            fit_results["peaks"].append({
                "amplitude": popt[idx],
                "amplitude_error": perr[idx],
                "center": popt[idx+1],
                "center_error": perr[idx+1],
                "sigma": popt[idx+2],
                "sigma_error": perr[idx+2],
                "gamma": popt[idx+3],
                "gamma_error": perr[idx+3]
            })
        
        return {"success": True, "parameters": popt, "errors": perr, "results": fit_results}
    
    except Exception as e:
        print(f"Fit failed: {e}")
        return {"success": False, "error": str(e)}

# ============================================================================
# VISUALIZATION
# ============================================================================

def plot_spectrum(energy, spectrum, noise, detected_peaks=None, matches=None, fit_result=None):
    """
    Create comprehensive spectrum plot.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Full spectrum
    axes[0, 0].plot(energy, spectrum, 'b-', linewidth=1.5, label='Simulated Spectrum')
    axes[0, 0].fill_between(energy, spectrum - noise, spectrum + noise,
                           alpha=0.3, color='blue', label='Noise level')
    
    # Mark predicted peak positions
    colors = ['red', 'green', 'purple']
    pred_names = ["E1", "E2", "E3"]
    
    for i, name in enumerate(pred_names):
        pred = PREDICTIONS[name]
        axes[0, 0].axvline(x=pred["energy"], color=colors[i], linestyle='--',
                          alpha=0.7, label=f'Pred {name}: {pred["energy"]} eV')
        # Uncertainty bands
        axes[0, 0].axvspan(pred["energy"] - pred["uncertainty"],
                          pred["energy"] + pred["uncertainty"],
                          alpha=0.1, color=colors[i])
    
    axes[0, 0].set_xlabel('Energy (eV)', fontsize=12)
    axes[0, 0].set_ylabel('Intensity (arb. units)', fontsize=12)
    axes[0, 0].set_title('Simulated FTIR Spectrum with Predicted Peaks', fontsize=14)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend(loc='upper right', fontsize=9)
    
    # Plot 2: Background subtracted
    if fit_result and fit_result["success"]:
        bg = background(energy, *fit_result["parameters"][:3])
        bg_subtracted = spectrum - bg
        axes[0, 1].plot(energy, bg_subtracted, 'g-', linewidth=1.5, label='BG subtracted')
    else:
        # Simple baseline subtraction
        bg_subtracted = spectrum - np.percentile(spectrum, 10)
        axes[0, 1].plot(energy, bg_subtracted, 'g-', linewidth=1.5, label='Baseline subtracted')
    
    # Mark detected peaks
    if detected_peaks:
        for peak in detected_peaks:
            axes[0, 1].plot(peak["energy"], peak["amplitude"], 'ro', markersize=8)
    
    axes[0, 1].set_xlabel('Energy (eV)', fontsize=12)
    axes[0, 1].set_ylabel('Intensity (arb. units)', fontsize=12)
    axes[0, 1].set_title('Peak Detection', fontsize=14)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].legend()
    
    # Plot 3: Zoom on predicted region
    zoom_min, zoom_max = 0.15, 0.65
    zoom_mask = (energy > zoom_min) & (energy < zoom_max)
    
    axes[1, 0].plot(energy[zoom_mask], spectrum[zoom_mask], 'b-', linewidth=2)
    
    # Add theoretical peak shapes with corrected formatting
    for i, name in enumerate(pred_names):
        pred = PREDICTIONS[name]
        peak_shape = voigt(energy[zoom_mask],
                          pred["amplitude"],
                          pred["energy"],
                          pred["width"] / 2.355,
                          pred["width"] / 2)
        axes[1, 0].plot(energy[zoom_mask], peak_shape, color=colors[i], linestyle='--',
                       linewidth=1.5, alpha=0.7, label=f'Theory {name}')
    
    axes[1, 0].set_xlabel('Energy (eV)', fontsize=12)
    axes[1, 0].set_ylabel('Intensity (arb. units)', fontsize=12)
    axes[1, 0].set_title('Zoom: 0.15 - 0.65 eV Region', fontsize=14)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()
    
    # Plot 4: Analysis results
    axes[1, 1].axis('off')
    
    text = "ANALYSIS RESULTS\n"
    text += "================\n\n"
    
    text += "Theory Predictions:\n"
    for name, pred in PREDICTIONS.items():
        text += f"  {name}: {pred['energy']} ± {pred['uncertainty']} eV\n"
    
    if matches:
        text += "\nDetected Peaks:\n"
        for name, match in matches.items():
            text += f"  {name}: {match['measured']:.3f} eV "
            text += f"(diff = {match['difference']*1000:.1f} meV)\n"
    
    if fit_result and fit_result["success"]:
        text += "\nFitted Parameters:\n"
        for i, peak in enumerate(fit_result["results"]["peaks"]):
            text += f"  Peak {i+1}: {peak['center']:.3f} ± {peak['center_error']:.3f} eV\n"
    
    # Calculate expected S/N
    expected_sn = 7.0  # As predicted in theory
    text += f"\nExpected S/N: > {expected_sn:.1f}\n"
    text += f"Required resolution: < 10e-14 eV\n"
    text += f"Temperature: 0.05 K\n"
    text += f"Scans: 2000\n"
    
    axes[1, 1].text(0.05, 0.95, text, transform=axes[1, 1].transAxes,
                   fontsize=10, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    return fig

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main infrared spectroscopy simulation pipeline.
    """
    print("=" * 70)
    print("INFRARED SPECTROSCOPY SIMULATION")
    print("For Predicted Peaks from Calabi-Yau Compactification")
    print("=" * 70)
    
    # Step 1: Generate spectrum
    print("\n1. Generating simulated FTIR spectrum...")
    energy, spectrum, noise = generate_ftir_spectrum(
        temperature=0.05,  # 0.05 K as in protocol
        resolution=5e-6    # 5 μeV resolution
    )
    print(f"   • Energy range: {energy[0]:.3f} - {energy[-1]:.3f} eV")
    print(f"   • Resolution: {energy[1]-energy[0]:.1e} eV/point")
    print(f"   • Average noise: {np.mean(noise):.2e}")
    
    # Step 2: Detect peaks
    print("\n2. Detecting peaks...")
    detected_peaks, matches = detect_peaks(energy, spectrum)
    print(f"   • Detected {len(detected_peaks)} peaks")
    
    for name, match in matches.items():
        diff_meV = match["difference"] * 1000
        print(f"   • {name}: {match['measured']:.3f} eV (diff = {diff_meV:.1f} meV from prediction)")
    
    # Step 3: Fit spectrum
    print("\n3. Fitting spectrum...")
    fit_result = fit_spectrum(energy, spectrum, noise)
    
    if fit_result["success"]:
        print("   • Fit successful!")
        for i, peak in enumerate(fit_result["results"]["peaks"]):
            print(f"   • Peak {i+1}: {peak['center']:.3f} ± {peak['center_error']:.3f} eV")
    else:
        print(f"   • Fit failed: {fit_result.get('error', 'Unknown error')}")
    
    # Step 4: Create visualization
    print("\n4. Generating plots...")
    fig = plot_spectrum(energy, spectrum, noise, detected_peaks, matches, fit_result)
    
    # Save results
    output_files = []
    
    # Save figure
    fig.savefig('ir_spectrum_results.png', dpi=300, bbox_inches='tight')
    output_files.append('ir_spectrum_results.png')
    print(f"   • Saved plot: ir_spectrum_results.png")
    
    # Save spectrum data
    np.savetxt('ir_spectrum_data.txt',
              np.column_stack([energy, spectrum, noise]),
              header='energy[eV] intensity noise',
              fmt='%.6f %.6f %.6f')
    output_files.append('ir_spectrum_data.txt')
    print(f"   • Saved data: ir_spectrum_data.txt")
    
    # Save analysis results
    with open('ir_analysis_results.txt', 'w') as f:
        f.write("INFRARED SPECTROSCOPY ANALYSIS RESULTS\n")
        f.write("=======================================\n\n")
        
        f.write("THEORY PREDICTIONS:\n")
        for name, pred in PREDICTIONS.items():
            f.write(f"{name}: {pred['energy']} ± {pred['uncertainty']} eV\n")
        
        f.write("\nDETECTED PEAKS:\n")
        for peak in detected_peaks:
            f.write(f"Peak at {peak['energy']:.3f} eV, amplitude {peak['amplitude']:.3f}\n")
        
        f.write("\nMATCHES WITH PREDICTIONS:\n")
        for name, match in matches.items():
            f.write(f"{name}: predicted {match['predicted']:.3f} eV, "
                   f"measured {match['measured']:.3f} eV, "
                   f"diff = {match['difference']*1000:.1f} meV\n")
        
        if fit_result["success"]:
            f.write("\nFITTED PARAMETERS:\n")
            for i, peak in enumerate(fit_result["results"]["peaks"]):
                f.write(f"Peak {i+1}: center = {peak['center']:.3f} ± {peak['center_error']:.3f} eV, "
                       f"amplitude = {peak['amplitude']:.3f} ± {peak['amplitude_error']:.3f}\n")
    
    output_files.append('ir_analysis_results.txt')
    print(f"   • Saved analysis: ir_analysis_results.txt")
    
    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print(f"Generated files: {', '.join(output_files)}")
    print("=" * 70)
    
    # Show plot (optional)
    try:
        plt.show()
    except:
        pass  # Non-interactive mode
    
    return fit_result

# ============================================================================
# EXECUTE IF RUN AS SCRIPT
# ============================================================================

if __name__ == "__main__":
    main()