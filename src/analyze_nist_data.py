#!/usr/bin/env python3
"""
Analysis of Real NIST Thermal Noise Data for UBP Noise Theory Validation

This script loads and analyzes the real NIST thermal noise dataset to test
the UBP Noise theory hypothesis.
"""

import numpy as np
import h5py
import json
from noise_theory_validator import UBPNoiseValidator
import matplotlib.pyplot as plt

def load_nist_data(data_path):
    """Load NIST thermal noise data from HDF5 file."""
    try:
        with h5py.File(data_path, 'r') as h5f:
            print(f"Available datasets: {list(h5f.keys())}")
            
            # Try to load available dataset (could be 'test' or 'train')
            if 'test' in h5f:
                dataset = h5f['test'][:]
                dataset_name = 'test'
            elif 'train' in h5f:
                dataset = h5f['train'][:]
                dataset_name = 'train'
            else:
                print(f"No recognized dataset found. Available: {list(h5f.keys())}")
                return None, None
                
            print(f"Loaded NIST {dataset_name} data shape: {dataset.shape}")
            
            # Extract parameter values and data
            # According to README: targ_param_values = dataset[:, 0]
            # targ_data = dataset[:, 1:]
            param_values = dataset[:, 0]
            noise_data = dataset[:, 1:]
            
            return param_values, noise_data
    except Exception as e:
        print(f"Error loading NIST data: {e}")
        return None, None

def load_noise_params(params_path):
    """Load noise parameters from JSON file."""
    try:
        with open(params_path, 'r') as f:
            params = json.load(f)
        return params
    except Exception as e:
        print(f"Error loading parameters: {e}")
        return None

def analyze_nist_thermal_noise():
    """Comprehensive analysis of NIST thermal noise data."""
    print("=== NIST Thermal Noise Data Analysis ===")
    
    # Load data
    data_path = "/home/ubuntu/bandpass/band3/test.h5"
    params_path = "/home/ubuntu/bandpass/band3/noise_params.json"
    
    # Load parameters
    params = load_noise_params(params_path)
    if params:
        print(f"Noise parameters: {params}")
    
    # Load data
    param_values, noise_data = load_nist_data(data_path)
    
    if noise_data is None:
        print("Failed to load NIST data")
        return None
    
    print(f"Number of time series: {noise_data.shape[0]}")
    print(f"Time series length: {noise_data.shape[1]}")
    
    # Initialize validator
    validator = UBPNoiseValidator()
    
    # Analyze multiple time series
    results_summary = {
        'nrci_values': [],
        'mean_coherence_values': [],
        'ubp_scores': [],
        'detected_resonances': []
    }
    
    # Analyze first 10 time series (to save time)
    n_analyze = min(10, noise_data.shape[0])
    
    for i in range(n_analyze):
        print(f"\nAnalyzing time series {i+1}/{n_analyze}")
        
        # Get time series
        signal = noise_data[i, :]
        
        # Estimate sampling rate from parameters or use default
        # For bandpass filtered noise, we need to estimate
        sampling_rate = 1e6  # 1 MHz default, adjust based on actual data
        
        # Validate against UBP theory
        results = validator.validate_noise_hypothesis(
            signal, 
            sampling_rate, 
            f"NIST Thermal Noise Series {i+1}"
        )
        
        # Store summary statistics
        results_summary['nrci_values'].append(results['nrci'])
        results_summary['mean_coherence_values'].append(results['coherence_analysis']['mean_coherence'])
        results_summary['ubp_scores'].append(results['ubp_assessment']['overall_score'])
        results_summary['detected_resonances'].append(len(results['frequency_analysis']['detected_resonances']))
        
        # Save detailed results for first series
        if i == 0:
            detailed_results = results
            # Create detailed plot
            fig = validator.plot_analysis_results(results, f"/home/ubuntu/nist_thermal_analysis_series_{i+1}.png")
            plt.close(fig)
    
    # Create summary analysis
    create_summary_analysis(results_summary, validator)
    
    return detailed_results, results_summary

def create_summary_analysis(results_summary, validator):
    """Create summary plots and statistics for multiple time series."""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('NIST Thermal Noise Data - UBP Theory Analysis Summary', fontsize=16)
    
    # Plot 1: NRCI distribution
    ax1 = axes[0, 0]
    ax1.hist(results_summary['nrci_values'], bins=20, alpha=0.7, edgecolor='black')
    ax1.axvline(x=validator.nrci_threshold, color='red', linestyle='--', label=f'UBP Threshold ({validator.nrci_threshold})')
    ax1.set_title('NRCI Distribution')
    ax1.set_xlabel('NRCI Value')
    ax1.set_ylabel('Frequency')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Coherence distribution
    ax2 = axes[0, 1]
    ax2.hist(results_summary['mean_coherence_values'], bins=20, alpha=0.7, edgecolor='black')
    ax2.axvline(x=validator.coherence_threshold, color='red', linestyle='--', label=f'Coherence Threshold ({validator.coherence_threshold})')
    ax2.axvline(x=validator.sub_coherent_threshold, color='orange', linestyle='--', label=f'Sub-coherent Threshold ({validator.sub_coherent_threshold})')
    ax2.set_title('Mean Coherence Distribution')
    ax2.set_xlabel('Mean Coherence')
    ax2.set_ylabel('Frequency')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: UBP Compatibility Scores
    ax3 = axes[1, 0]
    score_counts = np.bincount(results_summary['ubp_scores'])
    ax3.bar(range(len(score_counts)), score_counts, alpha=0.7, edgecolor='black')
    ax3.set_title('UBP Compatibility Scores')
    ax3.set_xlabel('UBP Score')
    ax3.set_ylabel('Number of Time Series')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Detected Resonances
    ax4 = axes[1, 1]
    ax4.hist(results_summary['detected_resonances'], bins=range(max(results_summary['detected_resonances'])+2), 
             alpha=0.7, edgecolor='black')
    ax4.set_title('Detected UBP Resonances')
    ax4.set_xlabel('Number of Detected Resonances')
    ax4.set_ylabel('Frequency')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/nist_summary_analysis.png', dpi=300, bbox_inches='tight')
    print("Summary analysis saved to: /home/ubuntu/nist_summary_analysis.png")
    
    # Print summary statistics
    print("\n=== NIST Data Summary Statistics ===")
    print(f"Number of time series analyzed: {len(results_summary['nrci_values'])}")
    print(f"Mean NRCI: {np.mean(results_summary['nrci_values']):.6f} ± {np.std(results_summary['nrci_values']):.6f}")
    print(f"Mean Coherence: {np.mean(results_summary['mean_coherence_values']):.3f} ± {np.std(results_summary['mean_coherence_values']):.3f}")
    print(f"Mean UBP Score: {np.mean(results_summary['ubp_scores']):.2f} ± {np.std(results_summary['ubp_scores']):.2f}")
    print(f"Mean Detected Resonances: {np.mean(results_summary['detected_resonances']):.2f} ± {np.std(results_summary['detected_resonances']):.2f}")
    
    # UBP Theory Assessment
    sub_coherent_fraction = np.sum(np.array(results_summary['mean_coherence_values']) < validator.coherence_threshold) / len(results_summary['mean_coherence_values'])
    low_nrci_fraction = np.sum(np.array(results_summary['nrci_values']) < validator.nrci_threshold) / len(results_summary['nrci_values'])
    
    print(f"\n=== UBP Theory Compatibility ===")
    print(f"Fraction with sub-coherent mean: {sub_coherent_fraction:.2f}")
    print(f"Fraction with low NRCI: {low_nrci_fraction:.2f}")
    
    if sub_coherent_fraction > 0.7 and low_nrci_fraction > 0.7:
        print("CONCLUSION: Strong support for UBP Noise theory")
    elif sub_coherent_fraction > 0.5 and low_nrci_fraction > 0.5:
        print("CONCLUSION: Moderate support for UBP Noise theory")
    else:
        print("CONCLUSION: Limited support for UBP Noise theory")

def compare_synthetic_vs_nist():
    """Compare synthetic thermal noise with NIST data."""
    print("\n=== Synthetic vs NIST Comparison ===")
    
    # Generate synthetic data
    validator = UBPNoiseValidator()
    time, synthetic_noise = validator.generate_thermal_noise(
        resistance=1000, temperature=300, sampling_rate=1e6, duration=0.1
    )
    
    # Analyze synthetic
    synthetic_results = validator.validate_noise_hypothesis(
        synthetic_noise, 1e6, "Synthetic Thermal Noise"
    )
    
    # Load and analyze one NIST series
    param_values, noise_data = load_nist_data("/home/ubuntu/bandpass/band3/test.h5")
    if noise_data is not None:
        nist_results = validator.validate_noise_hypothesis(
            noise_data[0, :], 1e6, "NIST Thermal Noise"
        )
        
        # Compare key metrics
        print(f"Synthetic NRCI: {synthetic_results['nrci']:.6f}")
        print(f"NIST NRCI: {nist_results['nrci']:.6f}")
        print(f"Synthetic Mean Coherence: {synthetic_results['coherence_analysis']['mean_coherence']:.3f}")
        print(f"NIST Mean Coherence: {nist_results['coherence_analysis']['mean_coherence']:.3f}")
        print(f"Synthetic UBP Score: {synthetic_results['ubp_assessment']['overall_score']}")
        print(f"NIST UBP Score: {nist_results['ubp_assessment']['overall_score']}")

if __name__ == "__main__":
    # Analyze NIST data
    detailed_results, summary_results = analyze_nist_thermal_noise()
    
    # Compare with synthetic
    compare_synthetic_vs_nist()
    
    print("\nAnalysis complete!")

