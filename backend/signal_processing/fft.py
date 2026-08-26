"""
HydroGuard AI — Vibration Signal Processing & Spectral Engine
Module: fft.py
Description: FFT spectral analysis, running speed harmonics, VPF, and 1-5 kHz cavitation energy band detection.
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from scipy import signal

def generate_synthetic_vibration_stream(
    duration_s: float = 1.0,
    sampling_rate_hz: int = 12000,
    pump_rpm: float = 2950.0,
    impeller_vanes: int = 5,
    baseline_noise_rms: float = 0.8,
    unbalance_1x_amp: float = 0.5,
    misalignment_2x_amp: float = 0.2,
    vpf_pulsation_amp: float = 0.3,
    cavitation_severity: float = 0.0,  # 0.0 (none) to 1.0 (severe)
    random_seed: Optional[int] = 42
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate realistic pump vibration acceleration signal (m/s^2 or mm/s RMS)
    with configurable mechanical and hydraulic fault signatures.
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    num_samples = int(duration_s * sampling_rate_hz)
    t = np.linspace(0, duration_s, num_samples, endpoint=False)

    f_1x = pump_rpm / 60.0  # 1X Running speed frequency (e.g. 49.17 Hz for 2950 RPM)
    f_2x = 2.0 * f_1x
    f_3x = 3.0 * f_1x
    f_vpf = impeller_vanes * f_1x  # Vane Pass Frequency (e.g. 245.8 Hz)

    # 1. Base mechanical rotation & harmonics
    signal_out = (
        unbalance_1x_amp * np.sin(2 * np.pi * f_1x * t) +
        misalignment_2x_amp * np.sin(2 * np.pi * f_2x * t + 0.5) +
        (misalignment_2x_amp * 0.3) * np.sin(2 * np.pi * f_3x * t + 1.2) +
        vpf_pulsation_amp * np.sin(2 * np.pi * f_vpf * t + 0.2)
    )

    # 2. Add Gaussian baseline sensor noise
    noise = np.random.normal(0, baseline_noise_rms, num_samples)
    signal_out += noise

    # 3. Cavitation signature: high-frequency random shock impacts (1000 - 5000 Hz)
    # Cavitation bubble collapse creates broad high-frequency burst impacts
    if cavitation_severity > 0.0:
        # High frequency bandpass noise burst (1 kHz to 5 kHz)
        nyq = sampling_rate_hz / 2.0
        low = 1000.0 / nyq
        high = min(4900.0 / nyq, 0.95)
        b, a = signal.butter(4, [low, high], btype='band')
        
        # High density random shock impulses
        cavitation_raw = np.random.standard_t(df=3, size=num_samples) * (cavitation_severity * 6.5)
        cavitation_filtered = signal.lfilter(b, a, cavitation_raw)
        
        # Amplitude modulation by low frequency turbulence (0.1X - 0.3X)
        modulator = 1.0 + 0.35 * np.sin(2 * np.pi * (f_1x * 0.25) * t)
        signal_out += cavitation_filtered * modulator

    return t, signal_out

def compute_vibration_fft(
    vibration_signal: np.ndarray,
    sampling_rate_hz: int = 12000,
    pump_rpm: float = 2950.0,
    impeller_vanes: int = 5,
    max_display_freq_hz: float = 6000.0
) -> Dict[str, Any]:
    """
    Perform discrete Fourier transform on vibration signal and compute key spectral indicators.
    Returns:
      - frequencies: List of frequency bins (Hz)
      - amplitudes: Magnitude spectrum (mm/s or g RMS)
      - vpf_hz: Vane Pass Frequency
      - f_1x_hz: Running speed fundamental
      - cavitation_band_energy: Integrated power in 1000-5000 Hz band
      - vpf_amplitude: Amplitude at VPF
      - harmonic_amplitudes: 1X, 2X, 3X, 4X amplitudes
      - overall_rms: Overall RMS vibration
      - cavitation_spectral_ratio: Ratio of (1-5kHz band power) to total power
    """
    if len(vibration_signal) == 0:
        raise ValueError("Vibration signal buffer cannot be empty")
    if sampling_rate_hz <= 0:
        raise ValueError("Sampling rate must be positive")

    n = len(vibration_signal)
    
    # Apply Hanning window to suppress spectral leakage
    window = np.hanning(n)
    windowed_signal = vibration_signal * window
    window_correction_factor = 1.0 / np.mean(window)

    # Real FFT with coherent gain amplitude correction
    fft_vals = np.fft.rfft(windowed_signal)
    freqs = np.fft.rfftfreq(n, d=1.0 / sampling_rate_hz)
    coherent_gain = np.mean(window)

    # For display: peak amplitude in mm/s
    amplitudes = (np.abs(fft_vals) / (n * coherent_gain)) * 2.0
    amplitudes[0] = amplitudes[0] / 2.0  # DC component

    # Characteristic frequencies
    f_1x = pump_rpm / 60.0
    f_2x = 2.0 * f_1x
    f_3x = 3.0 * f_1x
    f_4x = 4.0 * f_1x
    f_vpf = impeller_vanes * f_1x

    def get_peak_in_band(center_f: float, tolerance_hz: float = 3.5) -> Tuple[float, float]:
        idx = np.where((freqs >= center_f - tolerance_hz) & (freqs <= center_f + tolerance_hz))[0]
        if len(idx) > 0:
            max_i = idx[np.argmax(amplitudes[idx])]
            return float(freqs[max_i]), float(amplitudes[max_i])
        return center_f, 0.0

    peak_1x_f, amp_1x = get_peak_in_band(f_1x)
    peak_2x_f, amp_2x = get_peak_in_band(f_2x)
    peak_3x_f, amp_3x = get_peak_in_band(f_3x)
    peak_4x_f, amp_4x = get_peak_in_band(f_4x)
    peak_vpf_f, amp_vpf = get_peak_in_band(f_vpf)

    # 1 kHz - 5 kHz Cavitation Energy Band RMS
    cav_mask = (freqs >= 1000.0) & (freqs <= 5000.0)
    # Band RMS power via Parseval
    cav_band_power = np.sum((np.abs(fft_vals[cav_mask]) / n) ** 2) * 2.0
    cav_band_energy = float(np.sqrt(cav_band_power))
    
    # Total overall RMS
    overall_rms = float(np.sqrt(np.mean(vibration_signal ** 2)))

    # Cavitation spectral ratio (relative energy in 1-5kHz band vs total)
    cavitation_spectral_ratio = float(cav_band_energy / (overall_rms + 1e-6))

    # Cavitation anomaly detection rule:
    # Baseline nominal pump 1-5 kHz band energy is usually < 0.6 mm/s RMS (< 30% of total)
    # During cavitation, broad bubble collapses drive 1-5 kHz energy > 1.8 mm/s RMS and ratio > 0.55
    is_cavitation_spectral_elevated = cav_band_energy > 1.5 and cavitation_spectral_ratio > 0.50

    # Filter down points for UI visualization (e.g. 200 points max up to max_display_freq_hz)
    disp_mask = freqs <= max_display_freq_hz
    disp_freqs = freqs[disp_mask]
    disp_amps = amplitudes[disp_mask]

    # Subsample for lightweight SCADA telemetry transmission
    step = max(1, len(disp_freqs) // 250)
    sampled_freqs = [round(float(f), 1) for f in disp_freqs[::step]]
    sampled_amps = [round(float(a), 4) for a in disp_amps[::step]]

    return {
        "overall_rms_mm_s": round(overall_rms, 3),
        "f_1x_hz": round(f_1x, 2),
        "f_vpf_hz": round(f_vpf, 2),
        "amp_1x_mm_s": round(amp_1x, 3),
        "amp_2x_mm_s": round(amp_2x, 3),
        "amp_3x_mm_s": round(amp_3x, 3),
        "amp_vpf_mm_s": round(amp_vpf, 3),
        "cavitation_1_5khz_energy_rms": round(cav_band_energy, 3),
        "cavitation_spectral_ratio": round(cavitation_spectral_ratio, 3),
        "is_cavitation_spectral_elevated": is_cavitation_spectral_elevated,
        "spectrum": {
            "frequencies": sampled_freqs,
            "amplitudes": sampled_amps
        }
    }
