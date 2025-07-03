#!/usr/bin/env python3
"""
Basic UBP Noise Theory Validation Example

This script demonstrates how to use the UBP Noise Theory validation framework
to analyze thermal noise and test for UBP compatibility.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from noise_theory_validator import UBPNoiseValidator
import matplotlib.pyplot as plt

def main():
    """Run basic UBP noise validation example."""
    print("=== UBP Noise Theory - Basic Validation Example ===")
    print()
    
    # Initialize the validator
    validator = UBPNoiseValidator()
    
    # Generate thermal noise (Johnson-Nyquist)
    print("1. Generating thermal noise...")
    resistance = 1000  # 1 kΩ
    temperature = 300  # 300 K (room temperature)
    sampling_rate = 1e6  # 1 MHz
    duration = 0.1  # 100 ms
    
    time, thermal_noise = validator.generate_thermal_noise(
        resistance=resistance,
        temperature=temperature,
        sampling_rate=sampling_rate,
        duration=duration
    )
    
    print(f"Generated {len(thermal_noise)} samples of thermal noise")
    print(f"Resistance: {resistance} Ω")
    print(f"Temperature: {temperature} K")
    print(f"Sampling rate: {sampling_rate/1e6:.1f} MHz")
    print(f"Duration: {duration*1000:.1f} ms")
    print()
    
    # Validate against UBP theory
    print("2. Validating against UBP Noise Theory...")
    results = validator.validate_noise_hypothesis(
        thermal_noise, 
        sampling_rate, 
        "Basic Thermal Noise Example"
    )
    
    # Display key results
    print("=== Validation Results ===")
    print(f"NRCI: {results['nrci']:.6f}")
    print(f"Mean Coherence: {results['coherence_analysis']['mean_coherence']:.3f}")
    print(f"UBP Compatibility Score: {results['ubp_assessment']['overall_score']}")
    print(f"Confidence Level: {results['ubp_assessment']['confidence']}")
    print()
    
    # Interpret results
    nrci_threshold = validator.nrci_threshold
    coherence_threshold = validator.coherence_threshold
    
    nrci_compatible = results['nrci'] < nrci_threshold
    coherence_compatible = results['coherence_analysis']['mean_coherence'] < coherence_threshold
    
    print("=== UBP Theory Compatibility ===")
    print(f"NRCI < {nrci_threshold}: {'✓ YES' if nrci_compatible else '✗ NO'}")
    print(f"Mean Coherence < {coherence_threshold}: {'✓ YES' if coherence_compatible else '✗ NO'}")
    
    if nrci_compatible and coherence_compatible:
        print("🎉 CONCLUSION: Thermal noise shows STRONG UBP compatibility!")
        print("   This supports the theory that noise represents incoherent OffBit toggles.")
    elif nrci_compatible or coherence_compatible:
        print("⚠️  CONCLUSION: Thermal noise shows PARTIAL UBP compatibility.")
        print("   Some evidence for toggle patterns, but not all criteria met.")
    else:
        print("❌ CONCLUSION: Thermal noise does NOT show UBP compatibility.")
        print("   No evidence for structured toggle patterns.")
    
    print()
    print("=== Supporting Evidence ===")
    for evidence in results['ubp_assessment']['compatible_indicators']:
        print(f"• {evidence}")
    
    print()
    print("Analysis plot saved to: thermal_noise_basic_example.png")
    print("For more detailed analysis, see the comprehensive_noise_analysis.py script.")

if __name__ == "__main__":
    main()

