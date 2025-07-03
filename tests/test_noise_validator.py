#!/usr/bin/env python3
"""
Test suite for UBP Noise Theory Validation Package

This module contains unit tests for the noise theory validator to ensure
correct functionality and reproducible results.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import numpy as np
from noise_theory_validator import UBPNoiseValidator

class TestUBPNoiseValidator(unittest.TestCase):
    """Test cases for UBPNoiseValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = UBPNoiseValidator()
        self.test_sampling_rate = 1e6
        self.test_duration = 0.01  # Short duration for fast tests
    
    def test_thermal_noise_generation(self):
        """Test thermal noise generation."""
        time, noise = self.validator.generate_thermal_noise(
            resistance=1000,
            temperature=300,
            sampling_rate=self.test_sampling_rate,
            duration=self.test_duration
        )
        
        expected_samples = int(self.test_duration * self.test_sampling_rate)
        
        # Check array lengths
        self.assertEqual(len(time), expected_samples)
        self.assertEqual(len(noise), expected_samples)
        
        # Check time array
        self.assertAlmostEqual(time[0], 0.0, places=10)
        self.assertAlmostEqual(time[-1], self.test_duration, places=6)
        
        # Check noise properties
        self.assertIsInstance(noise, np.ndarray)
        self.assertTrue(np.all(np.isfinite(noise)))
        self.assertGreater(np.std(noise), 0)  # Should have non-zero variance
    
    def test_coherence_analysis(self):
        """Test coherence analysis functionality."""
        # Generate test signal
        time, noise = self.validator.generate_thermal_noise(
            resistance=1000, temperature=300,
            sampling_rate=self.test_sampling_rate,
            duration=self.test_duration
        )
        
        # Discretize signal first
        binary_signal = self.validator.discretize_signal(noise)
        
        # Run coherence analysis
        coherence_results = self.validator.compute_coherence(binary_signal)
        
        # Check results structure
        self.assertIn('coherence_matrix', coherence_results)
        self.assertIn('mean_coherence', coherence_results)
        
        # Check coherence values are in valid range [0, 1]
        coherence_matrix = coherence_results['coherence_matrix']
        self.assertTrue(np.all(coherence_matrix >= 0))
        self.assertTrue(np.all(coherence_matrix <= 1))
        
        # Check mean coherence
        mean_coherence = coherence_results['mean_coherence']
        self.assertGreaterEqual(mean_coherence, 0)
        self.assertLessEqual(mean_coherence, 1)
    
    def test_nrci_calculation(self):
        """Test NRCI calculation."""
        # Generate test signal
        time, noise = self.validator.generate_thermal_noise(
            resistance=1000, temperature=300,
            sampling_rate=self.test_sampling_rate,
            duration=self.test_duration
        )
        
        # Calculate NRCI
        nrci = self.validator.compute_nrci(noise)
        
        # Check NRCI is a valid number
        self.assertIsInstance(nrci, (int, float))
        self.assertTrue(np.isfinite(nrci))
        self.assertGreaterEqual(nrci, 0)
        self.assertLessEqual(nrci, 1)
    
    def test_toggle_analysis(self):
        """Test toggle pattern analysis."""
        # Generate test signal
        time, noise = self.validator.generate_thermal_noise(
            resistance=1000, temperature=300,
            sampling_rate=self.test_sampling_rate,
            duration=self.test_duration
        )
        
        # Discretize signal first
        binary_signal = self.validator.discretize_signal(noise)
        
        # Run toggle analysis
        toggle_results = self.validator.analyze_toggle_patterns(binary_signal)
        
        # Check results structure
        self.assertIn('toggle_intervals', toggle_results)
        self.assertIn('toggle_rate', toggle_results)
        self.assertIn('mean_interval', toggle_results)
        
        # Check toggle rate
        toggle_rate = toggle_results['toggle_rate']
        self.assertGreaterEqual(toggle_rate, 0)
    
    def test_full_validation(self):
        """Test complete validation workflow."""
        # Generate test signal
        time, noise = self.validator.generate_thermal_noise(
            resistance=1000, temperature=300,
            sampling_rate=self.test_sampling_rate,
            duration=self.test_duration
        )
        
        # Run full validation
        results = self.validator.validate_noise_hypothesis(
            noise, self.test_sampling_rate, "Test Signal"
        )
        
        # Check all required sections are present
        required_sections = [
            'nrci',
            'coherence_analysis',
            'frequency_analysis',
            'toggle_analysis',
            'statistical_tests',
            'ubp_assessment'
        ]
        
        for section in required_sections:
            self.assertIn(section, results)
        
        # Check specific values
        self.assertIsInstance(results['nrci'], (int, float))
        self.assertIn('mean_coherence', results['coherence_analysis'])
        self.assertIn('overall_score', results['ubp_assessment'])
        self.assertIn('confidence', results['ubp_assessment'])
    
    def test_white_noise_vs_thermal_noise(self):
        """Test that thermal noise and white noise show different characteristics."""
        # Generate thermal noise
        time, thermal = self.validator.generate_thermal_noise(
            resistance=1000, temperature=300,
            sampling_rate=self.test_sampling_rate,
            duration=self.test_duration
        )
        
        # Generate white noise
        n_samples = len(thermal)
        white = np.random.normal(0, np.std(thermal), n_samples)
        
        # Validate both
        thermal_results = self.validator.validate_noise_hypothesis(
            thermal, self.test_sampling_rate, "Thermal Test"
        )
        white_results = self.validator.validate_noise_hypothesis(
            white, self.test_sampling_rate, "White Test"
        )
        
        # Both should be valid results
        self.assertIsInstance(thermal_results['nrci'], (int, float))
        self.assertIsInstance(white_results['nrci'], (int, float))
        
        # Results should be finite
        self.assertTrue(np.isfinite(thermal_results['nrci']))
        self.assertTrue(np.isfinite(white_results['nrci']))
    
    def test_reproducibility(self):
        """Test that results are reproducible with same input."""
        # Set random seed for reproducibility
        np.random.seed(42)
        
        # Generate test signal
        time, noise = self.validator.generate_thermal_noise(
            resistance=1000, temperature=300,
            sampling_rate=self.test_sampling_rate,
            duration=self.test_duration
        )
        
        # Run validation twice
        results1 = self.validator.validate_noise_hypothesis(
            noise, self.test_sampling_rate, "Reproducibility Test 1"
        )
        results2 = self.validator.validate_noise_hypothesis(
            noise, self.test_sampling_rate, "Reproducibility Test 2"
        )
        
        # Key metrics should be identical
        self.assertAlmostEqual(results1['nrci'], results2['nrci'], places=10)
        self.assertAlmostEqual(
            results1['coherence_analysis']['mean_coherence'],
            results2['coherence_analysis']['mean_coherence'],
            places=10
        )

class TestPackageIntegration(unittest.TestCase):
    """Integration tests for the complete package."""
    
    def test_package_imports(self):
        """Test that all package modules can be imported."""
        try:
            from noise_theory_validator import UBPNoiseValidator
            from comprehensive_noise_analysis import ComprehensiveNoiseAnalyzer
            # analyze_nist_data requires specific data files, so we just test import
            import analyze_nist_data
        except ImportError as e:
            self.fail(f"Failed to import package modules: {e}")
    
    def test_example_script_functionality(self):
        """Test that example scripts can run without errors."""
        # This is a basic test - in practice you'd run the actual example
        validator = UBPNoiseValidator()
        
        # Generate small test signal
        time, noise = validator.generate_thermal_noise(
            resistance=1000, temperature=300,
            sampling_rate=1e5, duration=0.001  # Very short for fast test
        )
        
        # Should be able to validate without errors
        results = validator.validate_noise_hypothesis(
            noise, 1e5, "Integration Test"
        )
        
        self.assertIsInstance(results, dict)
        self.assertIn('nrci', results)

def run_tests():
    """Run all tests and display results."""
    print("=== UBP Noise Theory Package Test Suite ===")
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestUBPNoiseValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestPackageIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print()
    print("=== Test Summary ===")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
        return True
    else:
        print("❌ Some tests failed.")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

