# Comprehensive UBP Noise Theory Validation Report
============================================================

## Executive Summary
- **Noise types analyzed**: 5
- **UBP compatible**: 3/5 (60.0%)
- **Overall conclusion**: Moderate support for UBP Noise theory

## Detailed Results by Noise Type

### Thermal Noise
- **NRCI**: 0.995400 (✓ < 0.9999999)
- **Mean Coherence**: 0.248 (✓ < 0.5)
- **UBP Score**: 2
- **Confidence**: low
- **UBP Compatible**: ✓ YES
- **Supporting evidence**: Mean coherence (0.248) < threshold (0.5), consistent with sub-coherent toggles

### White Noise
- **NRCI**: 0.992980 (✓ < 0.9999999)
- **Mean Coherence**: 0.255 (✓ < 0.5)
- **UBP Score**: 2
- **Confidence**: low
- **UBP Compatible**: ✓ YES
- **Supporting evidence**: Mean coherence (0.255) < threshold (0.5), consistent with sub-coherent toggles

### Pink Noise
- **NRCI**: 0.000000 (✓ < 0.9999999)
- **Mean Coherence**: 1.000 (✗ < 0.5)
- **UBP Score**: 2
- **Confidence**: medium
- **UBP Compatible**: ✗ NO
- **Supporting evidence**: Toggle detectable fraction (1.000) suggests structured activity

### Shot Noise
- **NRCI**: 0.002400 (✓ < 0.9999999)
- **Mean Coherence**: 0.000 (✓ < 0.5)
- **UBP Score**: 2
- **Confidence**: low
- **UBP Compatible**: ✓ YES
- **Supporting evidence**: Mean coherence (0.000) < threshold (0.5), consistent with sub-coherent toggles

### Brownian Noise
- **NRCI**: 0.521920 (✓ < 0.9999999)
- **Mean Coherence**: 0.630 (✗ < 0.5)
- **UBP Score**: 2
- **Confidence**: medium
- **UBP Compatible**: ✗ NO
- **Supporting evidence**: Toggle detectable fraction (0.673) suggests structured activity

## Theoretical Implications

The moderate compatibility rate suggests **partial support** for the UBP Noise theory. Some noise types show clear toggle signatures while others may arise from different mechanisms.

## Key Findings

- **Most UBP-compatible (lowest NRCI)**: Pink noise (NRCI = 0.000000)
- **Least UBP-compatible (highest NRCI)**: Thermal noise (NRCI = 0.995400)
- **Most sub-coherent**: Shot noise (coherence = 0.000)
- **Most coherent**: Pink noise (coherence = 1.000)