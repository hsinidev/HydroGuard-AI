"""
HydroGuard AI — Unit Tests for Deterministic Hydraulic & Signal Processing Engines
File: test_hydraulic_math.py
"""

import pytest
import numpy as np
from backend.calculations.npsh import (
    calculate_npsha,
    evaluate_npsh_margin,
    water_vapor_pressure_antoine
)
from backend.calculations.efficiency import (
    calculate_total_dynamic_head,
    calculate_pump_efficiency
)
from backend.signal_processing.fft import (
    generate_synthetic_vibration_stream,
    compute_vibration_fft
)

class TestNPSHCalculations:
    def test_water_vapor_pressure(self):
        # Water at 20 C is approx 2.338 kPa (2338 Pa)
        p_vap_20 = water_vapor_pressure_antoine(20.0)
        assert 2300.0 < p_vap_20 < 2400.0

        # Water at 100 C is 101.325 kPa
        p_vap_100 = water_vapor_pressure_antoine(100.0)
        assert 100000.0 < p_vap_100 < 103000.0

        # Out of bounds temperature raises ValueError
        with pytest.raises(ValueError):
            water_vapor_pressure_antoine(-10.0)
        with pytest.raises(ValueError):
            water_vapor_pressure_antoine(180.0)

    def test_calculate_npsha_nominal(self):
        # Suction pressure = 1.5 bar abs (150,000 Pa), Temp = 20 C, Flow = 120 m3/h, Diam = 0.15 m
        res = calculate_npsha(
            p_suction_abs=150000.0,
            temp_celsius=20.0,
            flow_m3_h=120.0,
            suction_pipe_diam_m=0.15
        )
        assert res["npsha_m"] > 14.0
        assert res["head_static_m"] > 14.0
        assert res["head_velocity_m"] > 0.0
        assert res["is_flashing"] is False

    def test_calculate_npsha_low_pressure(self):
        # Low suction pressure = 0.5 bar abs (50,000 Pa), Temp = 20 C
        res = calculate_npsha(
            p_suction_abs=50000.0,
            temp_celsius=20.0,
            flow_m3_h=120.0,
            suction_pipe_diam_m=0.15
        )
        assert 4.5 < res["npsha_m"] < 5.2
        assert res["is_flashing"] is False

    def test_calculate_npsha_invalid_inputs(self):
        with pytest.raises(ValueError):
            calculate_npsha(p_suction_abs=-1000.0)  # Negative pressure
        with pytest.raises(ValueError):
            calculate_npsha(p_suction_abs=100000.0, density_kg_m3=-900)
        with pytest.raises(ValueError):
            calculate_npsha(p_suction_abs=100000.0, flow_m3_h=-50)

    def test_evaluate_npsh_margin_statuses(self):
        # Case 1: Healthy margin
        h_eval = evaluate_npsh_margin(npsha_m=7.5, npshr_m=4.2)
        assert h_eval["status"] == "HEALTHY_MARGIN"
        assert h_eval["severity"] == "NORMAL"
        assert h_eval["npsh_margin_m"] == 3.3

        # Case 2: Warning low margin
        w_eval = evaluate_npsh_margin(npsha_m=5.0, npshr_m=4.2)
        assert w_eval["status"] == "WARNING_LOW_MARGIN"
        assert w_eval["severity"] == "MEDIUM"

        # Case 3: Critical cavitation risk (P-204 scenario: NPSHa = 4.3m, NPSHr = 4.2m)
        c_eval = evaluate_npsh_margin(npsha_m=4.3, npshr_m=4.2)
        assert c_eval["status"] == "CRITICAL_CAVITATION_RISK"
        assert c_eval["severity"] == "HIGH"
        assert c_eval["cavitation_risk_index"] >= 0.7

class TestEfficiencyCalculations:
    def test_calculate_total_dynamic_head(self):
        # P_s = 100 kPa, P_d = 800 kPa, Flow = 120 m3/h
        res = calculate_total_dynamic_head(
            p_discharge_pa=800000.0,
            p_suction_pa=100000.0,
            flow_m3_h=120.0
        )
        assert 70.0 < res["total_head_m"] < 75.0
        assert res["differential_pressure_kpa"] == 700.0

    def test_calculate_pump_efficiency(self):
        # Total head ~72m, Flow = 120 m3/h, Electrical Power = 30 kW, motor eta = 0.95
        # Shaft Power = 28.5 kW. Hydraulic Power = 998.2 * 9.80665 * (120/3600) * 72 / 1000 = 23.5 kW
        # eta = 23.5 / 28.5 * 100 = ~82.4%
        res = calculate_pump_efficiency(
            p_discharge_pa=800000.0,
            p_suction_pa=100000.0,
            flow_m3_h=120.0,
            electrical_power_kw=30.0,
            motor_efficiency_factor=0.95
        )
        assert 78.0 <= res["efficiency_pct"] <= 86.0
        assert res["is_efficiency_anomaly"] is False

    def test_efficiency_bounds_and_anomalies(self):
        # Negative electrical power rejected
        with pytest.raises(ValueError):
            calculate_pump_efficiency(
                p_discharge_pa=800000.0,
                p_suction_pa=100000.0,
                flow_m3_h=120.0,
                electrical_power_kw=-10.0
            )

class TestVibrationSignalProcessing:
    def test_fft_frequency_harmonics_and_vpf(self):
        rpm = 2950.0  # 1X = 49.17 Hz
        vanes = 5     # VPF = 245.83 Hz
        t, sig = generate_synthetic_vibration_stream(
            duration_s=1.0,
            sampling_rate_hz=12000,
            pump_rpm=rpm,
            impeller_vanes=vanes,
            unbalance_1x_amp=1.2,
            misalignment_2x_amp=0.8,
            vpf_pulsation_amp=0.9,
            cavitation_severity=0.0,
            random_seed=123
        )
        fft_res = compute_vibration_fft(
            vibration_signal=sig,
            sampling_rate_hz=12000,
            pump_rpm=rpm,
            impeller_vanes=vanes
        )
        assert fft_res["f_1x_hz"] == 49.17
        assert fft_res["f_vpf_hz"] == 245.83
        assert fft_res["amp_1x_mm_s"] > 0.8
        assert fft_res["amp_2x_mm_s"] > 0.5
        assert fft_res["amp_vpf_mm_s"] > 0.6
        assert fft_res["is_cavitation_spectral_elevated"] is False

    def test_cavitation_high_frequency_band_detection(self):
        # Severe cavitation condition: elevated 1-5 kHz band energy
        t, sig_cav = generate_synthetic_vibration_stream(
            duration_s=1.0,
            sampling_rate_hz=12000,
            pump_rpm=2950.0,
            impeller_vanes=5,
            cavitation_severity=0.85,
            random_seed=999
        )
        fft_cav = compute_vibration_fft(
            vibration_signal=sig_cav,
            sampling_rate_hz=12000,
            pump_rpm=2950.0,
            impeller_vanes=5
        )
        assert fft_cav["cavitation_1_5khz_energy_rms"] > 2.5
        assert fft_cav["is_cavitation_spectral_elevated"] is True
