#!/usr/bin/env python3
"""
Comprehensive UBP Noise Theory Validation Across Multiple Noise Types

This script tests the UBP Noise theory across different types of noise:
1. Thermal (Johnson-Nyquist) noise
2. 1/f (pink) noise
3. White Gaussian noise
4. Shot noise
5. Brownian motion noise

The goal is to determine which types of noise show characteristics consistent
with the UBP theory of incoherent OffBit toggles.
"""

import numpy as np
import matplotlib.pyplot as plt
from noise_theory_validator import UBPNoiseValidator
import scipy.signal
from scipy.stats import norm
import warnings
warnings.filterwarnings('ignore')

class ComprehensiveNoiseAnalyzer:
    """Extended analyzer for multiple noise types."""
    
    def __init__(self):
        self.validator = UBPNoiseValidator()
        self.results = {}
        
    def generate_white_noise(self, duration=0.1, sampling_rate=1e6, amplitude=1.0):
        """Generate white Gaussian noise."""
        n_samples = int(duration * sampling_rate)
        noise = np.random.normal(0, amplitude, n_samples)
        time = np.linspace(0, duration, n_samples)
        return time, noise
    
    def generate_pink_noise(self, duration=0.1, sampling_rate=1e6, amplitude=1.0):
        """Generate 1/f (pink) noise."""
        n_samples = int(duration * sampling_rate)
        
        # Generate white noise
        white = np.random.normal(0, 1, n_samples)
        
        # Apply 1/f filter in frequency domain
        fft_white = np.fft.fft(white)
        freqs = np.fft.fftfreq(n_samples, 1/sampling_rate)
        
        # Avoid division by zero
        freqs[0] = 1e-10
        
        # Apply 1/f scaling
        fft_pink = fft_white / np.sqrt(np.abs(freqs))
        
        # Convert back to time domain
        pink = np.real(np.fft.ifft(fft_pink))
        pink = pink * amplitude / np.std(pink)
        
        time = np.linspace(0, duration, n_samples)
        return time, pink
    
    def generate_shot_noise(self, duration=0.1, sampling_rate=1e6, rate=1000, amplitude=1.0):
        """Generate shot noise (Poisson process)."""
        n_samples = int(duration * sampling_rate)
        dt = 1/sampling_rate
        
        # Generate Poisson events
        events = np.random.poisson(rate * dt, n_samples)
        
        # Convert to voltage-like signal
        noise = events * amplitude
        
        time = np.linspace(0, duration, n_samples)
        return time, noise
    
    def generate_brownian_noise(self, duration=0.1, sampling_rate=1e6, diffusion=1.0):
        """Generate Brownian motion (random walk) noise."""
        n_samples = int(duration * sampling_rate)
        dt = 1/sampling_rate
        
        # Generate random walk
        steps = np.random.normal(0, np.sqrt(diffusion * dt), n_samples)
        noise = np.cumsum(steps)
        
        time = np.linspace(0, duration, n_samples)
        return time, noise
    
    def analyze_all_noise_types(self):
        """Analyze all noise types for UBP compatibility."""
        print("=== Comprehensive UBP Noise Theory Analysis ===")
        print("Testing multiple noise types for UBP compatibility\n")
        
        # Parameters
        duration = 0.1  # 100 ms
        sampling_rate = 1e6  # 1 MHz
        
        # 1. Thermal noise (Johnson-Nyquist)
        print("1. Analyzing Thermal Noise...")
        time, thermal = self.validator.generate_thermal_noise(
            resistance=1000, temperature=300, 
            sampling_rate=sampling_rate, duration=duration
        )
        thermal_results = self.validator.validate_noise_hypothesis(
            thermal, sampling_rate, "Thermal Noise (1kΩ, 300K)"
        )
        self.results['thermal'] = thermal_results
        
        # 2. White Gaussian noise
        print("\n2. Analyzing White Gaussian Noise...")
        time, white = self.generate_white_noise(duration, sampling_rate, amplitude=1e-6)
        white_results = self.validator.validate_noise_hypothesis(
            white, sampling_rate, "White Gaussian Noise"
        )
        self.results['white'] = white_results
        
        # 3. Pink (1/f) noise
        print("\n3. Analyzing Pink (1/f) Noise...")
        time, pink = self.generate_pink_noise(duration, sampling_rate, amplitude=1e-6)
        pink_results = self.validator.validate_noise_hypothesis(
            pink, sampling_rate, "Pink (1/f) Noise"
        )
        self.results['pink'] = pink_results
        
        # 4. Shot noise
        print("\n4. Analyzing Shot Noise...")
        time, shot = self.generate_shot_noise(duration, sampling_rate, rate=1000, amplitude=1e-6)
        shot_results = self.validator.validate_noise_hypothesis(
            shot, sampling_rate, "Shot Noise (Poisson)"
        )
        self.results['shot'] = shot_results
        
        # 5. Brownian motion noise
        print("\n5. Analyzing Brownian Motion Noise...")
        time, brownian = self.generate_brownian_noise(duration, sampling_rate, diffusion=1e-12)
        brownian_results = self.validator.validate_noise_hypothesis(
            brownian, sampling_rate, "Brownian Motion Noise"
        )
        self.results['brownian'] = brownian_results
        
        return self.results
    
    def create_comparative_analysis(self):
        """Create comprehensive comparative analysis plots."""
        fig, axes = plt.subplots(3, 2, figsize=(20, 15))
        fig.suptitle('Comprehensive UBP Noise Theory Analysis - Multiple Noise Types', fontsize=16)
        
        noise_types = list(self.results.keys())
        colors = ['blue', 'red', 'green', 'orange', 'purple']
        
        # Plot 1: NRCI Comparison
        ax1 = axes[0, 0]
        nrci_values = [self.results[nt]['nrci'] for nt in noise_types]
        bars = ax1.bar(noise_types, nrci_values, color=colors[:len(noise_types)], alpha=0.7)
        ax1.axhline(y=self.validator.nrci_threshold, color='red', linestyle='--', 
                   label=f'UBP Threshold ({self.validator.nrci_threshold})')
        ax1.set_title('NRCI Comparison Across Noise Types')
        ax1.set_ylabel('NRCI Value')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        plt.setp(ax1.get_xticklabels(), rotation=45)
        
        # Add values on bars
        for bar, value in zip(bars, nrci_values):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.0001, 
                    f'{value:.4f}', ha='center', va='bottom', fontsize=10)
        
        # Plot 2: Mean Coherence Comparison
        ax2 = axes[0, 1]
        coherence_values = [self.results[nt]['coherence_analysis']['mean_coherence'] for nt in noise_types]
        bars = ax2.bar(noise_types, coherence_values, color=colors[:len(noise_types)], alpha=0.7)
        ax2.axhline(y=self.validator.coherence_threshold, color='red', linestyle='--', 
                   label=f'Coherence Threshold ({self.validator.coherence_threshold})')
        ax2.axhline(y=self.validator.sub_coherent_threshold, color='orange', linestyle='--', 
                   label=f'Sub-coherent Threshold ({self.validator.sub_coherent_threshold})')
        ax2.set_title('Mean Coherence Comparison')
        ax2.set_ylabel('Mean Coherence')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        plt.setp(ax2.get_xticklabels(), rotation=45)
        
        # Add values on bars
        for bar, value in zip(bars, coherence_values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{value:.3f}', ha='center', va='bottom', fontsize=10)
        
        # Plot 3: UBP Compatibility Scores
        ax3 = axes[1, 0]
        ubp_scores = [self.results[nt]['ubp_assessment']['overall_score'] for nt in noise_types]
        bars = ax3.bar(noise_types, ubp_scores, color=colors[:len(noise_types)], alpha=0.7)
        ax3.set_title('UBP Compatibility Scores')
        ax3.set_ylabel('UBP Score')
        ax3.set_ylim(0, max(ubp_scores) + 1)
        ax3.grid(True, alpha=0.3)
        plt.setp(ax3.get_xticklabels(), rotation=45)
        
        # Add values on bars
        for bar, value in zip(bars, ubp_scores):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
                    f'{value}', ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Plot 4: Toggle Rates
        ax4 = axes[1, 1]
        toggle_rates = [self.results[nt]['toggle_analysis']['toggle_rate'] for nt in noise_types]
        bars = ax4.bar(noise_types, toggle_rates, color=colors[:len(noise_types)], alpha=0.7)
        ax4.set_title('Toggle Rates')
        ax4.set_ylabel('Toggle Rate')
        ax4.grid(True, alpha=0.3)
        plt.setp(ax4.get_xticklabels(), rotation=45)
        
        # Plot 5: Statistical Test Results (KS p-values)
        ax5 = axes[2, 0]
        ks_pvalues = [self.results[nt]['statistical_tests']['ks_pvalue'] for nt in noise_types]
        bars = ax5.bar(noise_types, ks_pvalues, color=colors[:len(noise_types)], alpha=0.7)
        ax5.axhline(y=0.05, color='red', linestyle='--', label='p=0.05 significance')
        ax5.set_title('Kolmogorov-Smirnov Test p-values')
        ax5.set_ylabel('p-value')
        ax5.set_yscale('log')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        plt.setp(ax5.get_xticklabels(), rotation=45)
        
        # Plot 6: Summary Table
        ax6 = axes[2, 1]
        ax6.axis('off')
        
        # Create summary table
        table_data = []
        headers = ['Noise Type', 'NRCI', 'Mean Coh.', 'UBP Score', 'UBP Compatible']
        
        for nt in noise_types:
            nrci = self.results[nt]['nrci']
            coh = self.results[nt]['coherence_analysis']['mean_coherence']
            score = self.results[nt]['ubp_assessment']['overall_score']
            compatible = "✓" if (nrci < self.validator.nrci_threshold and 
                               coh < self.validator.coherence_threshold) else "✗"
            
            table_data.append([
                nt.capitalize(),
                f"{nrci:.4f}",
                f"{coh:.3f}",
                f"{score}",
                compatible
            ])
        
        table = ax6.table(cellText=table_data, colLabels=headers, 
                         cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.5)
        
        # Color code the compatibility column
        for i, row in enumerate(table_data):
            if row[4] == "✓":
                table[(i+1, 4)].set_facecolor('#90EE90')  # Light green
            else:
                table[(i+1, 4)].set_facecolor('#FFB6C1')  # Light red
        
        ax6.set_title('UBP Compatibility Summary', pad=20)
        
        plt.tight_layout()
        plt.savefig('/home/ubuntu/comprehensive_noise_analysis.png', dpi=300, bbox_inches='tight')
        print("Comprehensive analysis plot saved to: /home/ubuntu/comprehensive_noise_analysis.png")
        
        return fig
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report."""
        report = []
        report.append("# Comprehensive UBP Noise Theory Validation Report")
        report.append("=" * 60)
        report.append("")
        
        # Overall statistics
        noise_types = list(self.results.keys())
        compatible_count = 0
        
        for nt in noise_types:
            nrci = self.results[nt]['nrci']
            coh = self.results[nt]['coherence_analysis']['mean_coherence']
            if nrci < self.validator.nrci_threshold and coh < self.validator.coherence_threshold:
                compatible_count += 1
        
        compatibility_rate = compatible_count / len(noise_types)
        
        report.append(f"## Executive Summary")
        report.append(f"- **Noise types analyzed**: {len(noise_types)}")
        report.append(f"- **UBP compatible**: {compatible_count}/{len(noise_types)} ({compatibility_rate:.1%})")
        report.append(f"- **Overall conclusion**: {'Strong' if compatibility_rate > 0.7 else 'Moderate' if compatibility_rate > 0.4 else 'Limited'} support for UBP Noise theory")
        report.append("")
        
        # Detailed results for each noise type
        report.append("## Detailed Results by Noise Type")
        report.append("")
        
        for nt in noise_types:
            result = self.results[nt]
            nrci = result['nrci']
            coh = result['coherence_analysis']['mean_coherence']
            score = result['ubp_assessment']['overall_score']
            confidence = result['ubp_assessment']['confidence']
            
            compatible = nrci < self.validator.nrci_threshold and coh < self.validator.coherence_threshold
            
            report.append(f"### {nt.capitalize()} Noise")
            report.append(f"- **NRCI**: {nrci:.6f} ({'✓' if nrci < self.validator.nrci_threshold else '✗'} < {self.validator.nrci_threshold})")
            report.append(f"- **Mean Coherence**: {coh:.3f} ({'✓' if coh < self.validator.coherence_threshold else '✗'} < {self.validator.coherence_threshold})")
            report.append(f"- **UBP Score**: {score}")
            report.append(f"- **Confidence**: {confidence}")
            report.append(f"- **UBP Compatible**: {'✓ YES' if compatible else '✗ NO'}")
            
            # Key indicators
            indicators = result['ubp_assessment']['compatible_indicators']
            if indicators:
                report.append(f"- **Supporting evidence**: {indicators[0]}")
            
            report.append("")
        
        # Theoretical implications
        report.append("## Theoretical Implications")
        report.append("")
        
        if compatibility_rate > 0.7:
            report.append("The high compatibility rate across multiple noise types provides **strong evidence** for the UBP Noise theory. This suggests that the toggle mechanism may be a fundamental property of noise across different physical processes.")
        elif compatibility_rate > 0.4:
            report.append("The moderate compatibility rate suggests **partial support** for the UBP Noise theory. Some noise types show clear toggle signatures while others may arise from different mechanisms.")
        else:
            report.append("The low compatibility rate indicates **limited support** for the universal applicability of the UBP Noise theory. The toggle mechanism may be specific to certain types of noise.")
        
        report.append("")
        report.append("## Key Findings")
        report.append("")
        
        # Find best and worst performers
        nrci_values = [(nt, self.results[nt]['nrci']) for nt in noise_types]
        best_nrci = min(nrci_values, key=lambda x: x[1])
        worst_nrci = max(nrci_values, key=lambda x: x[1])
        
        report.append(f"- **Most UBP-compatible (lowest NRCI)**: {best_nrci[0].capitalize()} noise (NRCI = {best_nrci[1]:.6f})")
        report.append(f"- **Least UBP-compatible (highest NRCI)**: {worst_nrci[0].capitalize()} noise (NRCI = {worst_nrci[1]:.6f})")
        
        # Coherence analysis
        coh_values = [(nt, self.results[nt]['coherence_analysis']['mean_coherence']) for nt in noise_types]
        best_coh = min(coh_values, key=lambda x: x[1])
        worst_coh = max(coh_values, key=lambda x: x[1])
        
        report.append(f"- **Most sub-coherent**: {best_coh[0].capitalize()} noise (coherence = {best_coh[1]:.3f})")
        report.append(f"- **Most coherent**: {worst_coh[0].capitalize()} noise (coherence = {worst_coh[1]:.3f})")
        
        return "\n".join(report)

def main():
    """Main analysis function."""
    analyzer = ComprehensiveNoiseAnalyzer()
    
    # Run comprehensive analysis
    results = analyzer.analyze_all_noise_types()
    
    # Create comparative plots
    fig = analyzer.create_comparative_analysis()
    
    # Generate summary report
    report = analyzer.generate_summary_report()
    
    # Save report
    with open('/home/ubuntu/comprehensive_noise_report.md', 'w') as f:
        f.write(report)
    
    print("\n" + "="*60)
    print("COMPREHENSIVE ANALYSIS COMPLETE")
    print("="*60)
    print(f"Results saved to:")
    print(f"- Plot: /home/ubuntu/comprehensive_noise_analysis.png")
    print(f"- Report: /home/ubuntu/comprehensive_noise_report.md")
    print("\nSummary:")
    
    # Quick summary
    noise_types = list(results.keys())
    compatible_count = 0
    
    for nt in noise_types:
        nrci = results[nt]['nrci']
        coh = results[nt]['coherence_analysis']['mean_coherence']
        if nrci < analyzer.validator.nrci_threshold and coh < analyzer.validator.coherence_threshold:
            compatible_count += 1
            print(f"✓ {nt.capitalize()} noise: UBP compatible")
        else:
            print(f"✗ {nt.capitalize()} noise: Not UBP compatible")
    
    compatibility_rate = compatible_count / len(noise_types)
    print(f"\nOverall UBP compatibility: {compatible_count}/{len(noise_types)} ({compatibility_rate:.1%})")

if __name__ == "__main__":
    main()

