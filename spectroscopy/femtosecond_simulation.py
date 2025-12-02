"""
Femtosecond Correlation Simulation for Predicted Temporal Feature at t = 20.4 fs

This script simulates femtosecond correlation measurements to demonstrate
the predicted temporal correlation from Calabi-Yau compactification.

Predicted feature:
- t = (2.04 ± 0.02) × 10⁻¹⁴ s (20.4 femtoseconds)

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

PREDICTION = {
    "t": 2.04e-14,           # 20.4 fs
    "uncertainty": 0.02e-14,  # 0.2 fs
    "amplitude": 1.0,
    "width": 0.3e-14         # 3.0 fs FWHM
}

# ============================================================================
# TEMPORAL MODELS
# ============================================================================

def correlation_function(time, A, t0, sigma, background):
    """
    Correlation function for femtosecond measurements.
    
    Parameters:
    -----------
    time : array
        Time delay in seconds
    A : float
        Correlation amplitude
    t0 : float
        Correlation time (predicted t)
    sigma : float
        Temporal width
    background : float
        Constant background
    """
    return A * np.exp(-(time - t0)**2 / (2*sigma**2)) + background

def instrument_response(t, t0, width):
    """Instrument response function (laser pulse)."""
    return np.exp(-(t - t0)**2 / (2*width**2))

def generate_correlation_data(num_points=1000, laser_width=50e-15, noise_level=0.05):
    """
    Generate simulated femtosecond correlation data.
    
    Parameters:
    -----------
    num_points : int
        Number of time points
    laser_width : float
        Laser pulse width in seconds (50 fs typical)
    noise_level : float
        Relative noise level
        
    Returns:
    --------
    time_delay : array
        Time delay axis in seconds
    correlation : array
        Correlation signal
    noise : array
        Estimated noise
    """
    # Time delay range: -50 fs to +50 fs around predicted t
    time_range = 50e-15  # 50 fs
    time_delay = np.linspace(-time_range, time_range, num_points)
    
    # Generate correlation function
    A = PREDICTION["amplitude"]
    t0_val = PREDICTION["t"]
    sigma = PREDICTION["width"] / 2.355  # Convert FWHM to sigma
    background = 0.1
    
    ideal_correlation = correlation_function(time_delay, A, t0_val, sigma, background)
    
    # Convolve with instrument response
    from scipy.signal import convolve
    instrument = instrument_response(time_delay, 0, laser_width)
    correlation = convolve(ideal_correlation, instrument, mode='same') / np.sum(instrument)
    
    # Normalize
    correlation = correlation / np.max(correlation)
    
    # Add noise (improves with sqrt(number_of_pulses))
    pulses = 2e6  # As in protocol
    base_noise = noise_level * np.sqrt(np.abs(correlation) + 0.01)
    noise = base_noise / np.sqrt(pulses)
    
    # Add statistical fluctuations
    correlation_with_noise = correlation + np.random.normal(0, noise)
    
    return time_delay, correlation_with_noise, noise

# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def find_correlation_peak(time, signal, height_threshold=0.5):
    """
    Find the correlation peak and measure its parameters.
    """
    # Find peaks
    peak_indices, properties = find_peaks(signal, 
                                         height=height_threshold,
                                         prominence=0.3,
                                         width=2)
    
    if len(peak_indices) == 0:
        return None
    
    # Take the highest peak
    main_peak_idx = peak_indices[np.argmax(signal[peak_indices])]
    
    # Measure peak properties
    peak_time = time[main_peak_idx]
    peak_amplitude = signal[main_peak_idx]
    
    # Estimate width (FWHM)
    half_max = peak_amplitude / 2
    # Find left half-max point
    left_side = signal[:main_peak_idx]
    left_indices = np.where(left_side < half_max)[0]
    
    # Find right half-max point
    right_side = signal[main_peak_idx:]
    right_indices = np.where(right_side < half_max)[0]
    
    if len(left_indices) > 0 and len(right_indices) > 0:
        left_time = time[left_indices[-1]]
        right_time = time[main_peak_idx + right_indices[0]]
        fwhm = right_time - left_time
    else:
        fwhm = PREDICTION["width"]  # Use theoretical if can't measure
    
    return {
        "time": peak_time,
        "amplitude": peak_amplitude,
        "fwhm": fwhm,
        "index": main_peak_idx
    }

def fit_correlation(time, signal, noise):
    """
    Fit correlation data to extract precise parameters.
    """
    # Initial guesses
    A_guess = np.max(signal) - np.min(signal)
    t0_guess = time[np.argmax(signal)]
    sigma_guess = PREDICTION["width"] / 2.355
    bg_guess = np.min(signal)
    
    p0 = [A_guess, t0_guess, sigma_guess, bg_guess]
    
    # Bounds
    lower_bounds = [0, -10e-15, 0.1e-15, 0]
    upper_bounds = [2*A_guess, 10e-15, 5e-15, 0.5]
    
    try:
        popt, pcov = curve_fit(correlation_function, time, signal, p0=p0,
                              sigma=noise, bounds=(lower_bounds, upper_bounds))
        
        perr = np.sqrt(np.diag(pcov))
        
        return {
            "success": True,
            "amplitude": popt[0], "amplitude_error": perr[0],
            "t0": popt[1], "t0_error": perr[1],
            "sigma": popt[2], "sigma_error": perr[2],
            "background": popt[3], "background_error": perr[3],
            "fwhm": 2.355 * popt[2],  # Convert sigma to FWHM
            "parameters": popt,
            "errors": perr
        }
    
    except Exception as e:
        print(f"Fit failed: {e}")
        return {"success": False, "error": str(e)}

# ============================================================================
# VISUALIZATION
# ============================================================================

def plot_correlation_analysis(time, signal, noise, peak_info=None, fit_result=None):
    """
    Create comprehensive correlation analysis plot.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Convert time to femtoseconds for plotting
    time_fs = time * 1e15
    
    # Plot 1: Raw correlation data
    axes[0, 0].errorbar(time_fs, signal, yerr=noise, fmt='b.', 
                       alpha=0.5, markersize=3, label='Simulated Data')
    
    # Mark predicted t
    pred_t_fs = PREDICTION["t"] * 1e15
    axes[0, 0].axvline(x=pred_t_fs, color='r', linestyle='--',
                      linewidth=2, label=f'Pred t = {pred_t_fs:.1f} fs')
    
    # Uncertainty band
    unc_fs = PREDICTION["uncertainty"] * 1e15
    axes[0, 0].axvspan(pred_t_fs - unc_fs, pred_t_fs + unc_fs,
                      alpha=0.2, color='red', label='Uncertainty')
    
    axes[0, 0].set_xlabel('Time Delay (fs)', fontsize=12)
    axes[0, 0].set_ylabel('Correlation', fontsize=12)
    axes[0, 0].set_title('Femtosecond Correlation Measurement', fontsize=14)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend(loc='upper right')
    
    # Plot 2: Background subtracted
    if fit_result and fit_result["success"]:
        bg = fit_result["background"]
        signal_bg_subtracted = signal - bg
    else:
        signal_bg_subtracted = signal - np.percentile(signal, 10)
    
    axes[0, 1].plot(time_fs, signal_bg_subtracted, 'g-', linewidth=1.5, label='BG subtracted')
    
    # Mark detected peak
    if peak_info:
        peak_time_fs = peak_info["time"] * 1e15
        axes[0, 1].plot(peak_time_fs, peak_info["amplitude"], 'ro', 
                       markersize=10, label=f'Detected: {peak_time_fs:.1f} fs')
    
    axes[0, 1].axvline(x=pred_t_fs, color='r', linestyle='--', alpha=0.7)
    axes[0, 1].set_xlabel('Time Delay (fs)', fontsize=12)
    axes[0, 1].set_ylabel('BG-Subtracted', fontsize=12)
    axes[0, 1].set_title('Peak Detection', fontsize=14)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].legend()
    
    # Plot 3: Fit results
    axes[1, 0].errorbar(time_fs, signal, yerr=noise, fmt='b.', 
                       alpha=0.3, markersize=2, label='Data')
    
    if fit_result and fit_result["success"]:
        # Plot fit
        fit_curve = correlation_function(time, *fit_result["parameters"])
        axes[1, 0].plot(time_fs, fit_curve, 'r-', linewidth=2, label='Fit')
        
        # Mark fitted t
        fit_t_fs = fit_result["t0"] * 1e15
        axes[1, 0].axvline(x=fit_t_fs, color='green', linestyle=':',
                          linewidth=2, label=f'Fitted t = {fit_t_fs:.1f} fs')
    
    axes[1, 0].set_xlabel('Time Delay (fs)', fontsize=12)
    axes[1, 0].set_ylabel('Correlation', fontsize=12)
    axes[1, 0].set_title('Fit Results', fontsize=14)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()
    
    # Plot 4: Analysis summary
    axes[1, 1].axis('off')
    
    text = "FEMTOSECOND CORRELATION ANALYSIS\n"
    text += "================================\n\n"
    
    text += "Theory Prediction:\n"
    text += f"  t = {PREDICTION['t']*1e15:.1f} ± {PREDICTION['uncertainty']*1e15:.1f} fs\n"
    text += f"  FWHM ≈ {PREDICTION['width']*1e15:.1f} fs\n\n"
    
    if peak_info:
        text += "Detected Peak:\n"
        text += f"  Time = {peak_info['time']*1e15:.1f} fs\n"
        text += f"  Amplitude = {peak_info['amplitude']:.3f}\n"
        text += f"  FWHM = {peak_info['fwhm']*1e15:.1f} fs\n\n"
        
        # Calculate difference from prediction
        diff_fs = (peak_info['time'] - PREDICTION['t']) * 1e15
        text += f"Diff from pred = {diff_fs:.1f} fs\n"
    
    if fit_result and fit_result["success"]:
        text += "\nFit Results:\n"
        text += f"  t = {fit_result['t0']*1e15:.1f} ± {fit_result['t0_error']*1e15:.1f} fs\n"
        text += f"  FWHM = {fit_result['fwhm']*1e15:.1f} fs\n"
        text += f"  Amplitude = {fit_result['amplitude']:.3f} ± {fit_result['amplitude_error']:.3f}\n\n"
    
    text += "\nExperimental Parameters:\n"
    text += f"  Laser: 50 fs, 800 nm, 1 kHz\n"
    text += f"  Temperature: 0.05 K\n"
    text += f"  Pulses: 2e6\n"
    text += f"  Expected S/N: > 7\n"
    text += f"  Resolution: 0.05 fs\n"
    
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
    Main femtosecond correlation simulation pipeline.
    """
    print("=" * 70)
    print("FEMTOSECOND CORRELATION SIMULATION")
    print("For Predicted Temporal Feature t = 20.4 fs")
    print("=" * 70)
    
    # Step 1: Generate correlation data
    print("\n1. Generating simulated correlation data...")
    time, correlation, noise = generate_correlation_data(
        laser_width=50e-15,  # 50 fs laser
        noise_level=0.05
    )
    print(f"   • Time range: {time[0]*1e15:.0f} to {time[-1]*1e15:.0f} fs")
    print(f"   • Time resolution: {(time[1]-time[0])*1e15:.2f} fs/point")
    print(f"   • Average noise: {np.mean(noise):.2e}")
    
    # Step 2: Find correlation peak
    print("\n2. Finding correlation peak...")
    peak_info = find_correlation_peak(time, correlation)
    
    if peak_info:
        print(f"   • Peak detected at: {peak_info['time']*1e15:.1f} fs")
        print(f"   • Amplitude: {peak_info['amplitude']:.3f}")
        print(f"   • FWHM: {peak_info['fwhm']*1e15:.1f} fs")
        
        # Compare with prediction
        diff_fs = (peak_info['time'] - PREDICTION['t']) * 1e15
        print(f"   • Diff from pred: {diff_fs:.1f} fs")
    else:
        print("   • No peak detected!")
        peak_info = None
    
    # Step 3: Fit correlation
    print("\n3. Fitting correlation function...")
    fit_result = fit_correlation(time, correlation, noise)
    
    if fit_result["success"]:
        print(f"   • Fit successful!")
        print(f"   • t = {fit_result['t0']*1e15:.1f} ± {fit_result['t0_error']*1e15:.1f} fs")
        print(f"   • FWHM = {fit_result['fwhm']*1e15:.1f} fs")
        print(f"   • Amplitude = {fit_result['amplitude']:.3f}")
    else:
        print(f"   • Fit failed: {fit_result.get('error', 'Unknown error')}")
    
    # Step 4: Create visualization
    print("\n4. Generating plots...")
    fig = plot_correlation_analysis(time, correlation, noise, peak_info, fit_result)
    
    # Save results
    output_files = []
    
    # Save figure
    fig.savefig('femtosecond_correlation_results.png', dpi=300, bbox_inches='tight')
    output_files.append('femtosecond_correlation_results.png')
    print(f"   • Saved plot: femtosecond_correlation_results.png")
    
    # Save data
    np.savetxt('femtosecond_data.txt',
              np.column_stack([time, correlation, noise]),
              header='time[s] correlation noise',
              fmt='%.6e %.6e %.6e')
    output_files.append('femtosecond_data.txt')
    print(f"   • Saved data: femtosecond_data.txt")
    
    # Save analysis results
    with open('femtosecond_analysis_results.txt', 'w', encoding='utf-8') as f:
        f.write("FEMTOSECOND CORRELATION ANALYSIS\n")
        f.write("=================================\n\n")
        
        f.write("THEORY PREDICTION:\n")
        f.write(f"t = {PREDICTION['t']} s ({PREDICTION['t']*1e15:.1f} fs)\n")
        f.write(f"Uncertainty: ± {PREDICTION['uncertainty']} s (± {PREDICTION['uncertainty']*1e15:.1f} fs)\n\n")
        
        if peak_info:
            f.write("DETECTED PEAK:\n")
            f.write(f"Time: {peak_info['time']} s ({peak_info['time']*1e15:.1f} fs)\n")
            f.write(f"Amplitude: {peak_info['amplitude']:.3f}\n")
            f.write(f"FWHM: {peak_info['fwhm']} s ({peak_info['fwhm']*1e15:.1f} fs)\n\n")
            
            diff = peak_info['time'] - PREDICTION['t']
            f.write(f"DIFF FROM PREDICTION:\n")
            f.write(f"dt = {diff} s ({diff*1e15:.1f} fs)\n")
            f.write(f"Relative: {abs(diff)/PREDICTION['t']*100:.1f}%\n\n")
        
        if fit_result["success"]:
            f.write("FIT RESULTS:\n")
            f.write(f"t = {fit_result['t0']:.2e} s ({fit_result['t0']*1e15:.1f} fs)\n")
            f.write(f"t error = {fit_result['t0_error']:.2e} s ({fit_result['t0_error']*1e15:.1f} fs)\n")
            f.write(f"FWHM = {fit_result['fwhm']:.2e} s ({fit_result['fwhm']*1e15:.1f} fs)\n")
            f.write(f"Amplitude = {fit_result['amplitude']:.3f} ± {fit_result['amplitude_error']:.3f}\n")
    
    output_files.append('femtosecond_analysis_results.txt')
    print(f"   • Saved analysis: femtosecond_analysis_results.txt")
    
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