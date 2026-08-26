"""
HydroGuard AI Signal Processing Package
Vibration FFT, spectrum analysis, and cavitation acoustic/vibration energy calculation.
"""
from backend.signal_processing.fft import (
    generate_synthetic_vibration_stream,
    compute_vibration_fft
)

__all__ = [
    "generate_synthetic_vibration_stream",
    "compute_vibration_fft"
]
