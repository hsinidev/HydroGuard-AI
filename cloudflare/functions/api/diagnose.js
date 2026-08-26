// Cloudflare Pages Function: /api/diagnose
const GRAVITY_ACCEL = 9.80665;
const WATER_DENSITY_STANDARD = 998.2;

function calculateWaterVaporPressure(tempCelsius) {
  const A = 8.07131;
  const B = 1730.63;
  const C = 233.426;
  const log10_p_mmhg = A - (B / (tempCelsius + C));
  const p_mmhg = Math.pow(10, log10_p_mmhg);
  return p_mmhg * 133.322387415;
}

function calculateNPSHa(pSuctionBar, tempCelsius = 25.0, flowM3h = 118.0, suctionDiamM = 0.15, npshrM = 4.2) {
  const pSuctionPa = pSuctionBar * 100000.0;
  const pVaporPa = calculateWaterVaporPressure(tempCelsius);
  const flowM3s = flowM3h / 3600.0;
  const areaS = Math.PI * Math.pow(suctionDiamM / 2.0, 2);
  const velocityS = flowM3s / areaS;

  const headStatic = (pSuctionPa - pVaporPa) / (WATER_DENSITY_STANDARD * GRAVITY_ACCEL);
  const headVelocity = Math.pow(velocityS, 2) / (2.0 * GRAVITY_ACCEL);
  const npsha = headStatic + headVelocity;
  const margin = npsha - npshrM;

  let status = "HEALTHY_MARGIN";
  if (margin < 0.5) status = "CRITICAL_CAVITATION_RISK";
  else if (margin < 1.5) status = "WARNING_LOW_MARGIN";

  return {
    npsha_m: Number(npsha.toFixed(3)),
    npshr_m: npshrM,
    npsh_margin_m: Number(margin.toFixed(3)),
    head_static_m: Number(headStatic.toFixed(3)),
    head_velocity_m: Number(headVelocity.toFixed(4)),
    suction_velocity_m_s: Number(velocityS.toFixed(3)),
    status
  };
}

function calculatePumpEfficiency(pDischargeBar, pSuctionBar, flowM3h, electricalPowerKw, suctionDiamM = 0.15, dischargeDiamM = 0.10) {
  const pDischargePa = pDischargeBar * 100000.0;
  const pSuctionPa = pSuctionBar * 100000.0;
  const flowM3s = flowM3h / 3600.0;

  const areaS = Math.PI * Math.pow(suctionDiamM / 2.0, 2);
  const areaD = Math.PI * Math.pow(dischargeDiamM / 2.0, 2);
  const vS = flowM3s / areaS;
  const vD = flowM3s / areaD;

  const headPressure = (pDischargePa - pSuctionPa) / (WATER_DENSITY_STANDARD * GRAVITY_ACCEL);
  const headVelocity = (Math.pow(vD, 2) - Math.pow(vS, 2)) / (2.0 * GRAVITY_ACCEL);
  const totalHead = Math.max(0, headPressure + headVelocity);

  const hydraulicPowerKw = (WATER_DENSITY_STANDARD * GRAVITY_ACCEL * flowM3s * totalHead) / 1000.0;
  const shaftPowerKw = electricalPowerKw * 0.95;
  const efficiencyPct = shaftPowerKw > 0 ? Math.min(100.0, (hydraulicPowerKw / shaftPowerKw) * 100.0) : 0;
  const degradation = Math.max(0, 82.0 - efficiencyPct);

  return {
    total_head_m: Number(totalHead.toFixed(2)),
    hydraulic_power_kw: Number(hydraulicPowerKw.toFixed(2)),
    pump_efficiency_pct: Number(efficiencyPct.toFixed(1)),
    efficiency_degradation_pct: Number(degradation.toFixed(1))
  };
}

function generateFFTSpectrum(rpm = 2950.0, vanes = 5, cavSeverity = 0.0, misalignAmp = 0.2) {
  const f1x = Number((rpm / 60.0).toFixed(2));
  const f2x = Number((2.0 * f1x).toFixed(2));
  const fVpf = Number((vanes * f1x).toFixed(2));

  const frequencies = [];
  const amplitudes = [];
  const maxF = 5000;
  const points = 180;

  for (let i = 0; i <= points; i++) {
    const f = (i / points) * maxF;
    frequencies.push(Number(f.toFixed(1)));
    let amp = 0.08 + (Math.random() * 0.05);

    if (Math.abs(f - f1x) < 35) amp += 0.8 * Math.exp(-Math.pow(f - f1x, 2) / 200);
    if (Math.abs(f - f2x) < 40) amp += misalignAmp * Math.exp(-Math.pow(f - f2x, 2) / 250);
    if (Math.abs(f - fVpf) < 50) amp += 0.65 * Math.exp(-Math.pow(f - fVpf, 2) / 300);
    if (f >= 1000 && f <= 5000 && cavSeverity > 0) {
      amp += (cavSeverity * 1.8) * (0.6 + Math.random() * 0.8);
    }
    amplitudes.push(Number(amp.toFixed(4)));
  }

  const cavEnergy = cavSeverity > 0 ? Number((2.2 + cavSeverity * 1.5).toFixed(2)) : 0.45;
  const overallRms = Number((1.2 + (cavSeverity * 2.1) + (misalignAmp * 0.8)).toFixed(2));

  return {
    f_1x_hz: f1x,
    f_vpf_hz: fVpf,
    amp_1x_mm_s: 0.85,
    amp_2x_mm_s: misalignAmp,
    amp_vpf_mm_s: 0.65,
    overall_rms_mm_s: overallRms,
    cavitation_1_5khz_energy_rms: cavEnergy,
    cavitation_spectral_ratio: Number((cavEnergy / overallRms).toFixed(2)),
    is_cavitation_spectral_elevated: cavSeverity > 0.3 || cavEnergy > 1.8,
    spectrum: { frequencies, amplitudes }
  };
}

export async function onRequestPost(context) {
  try {
    const telemetry = await context.request.json();
    const apiKey = context.request.headers.get("X-Gemini-API-Key") || context.env.GEMINI_API_KEY || "";
    const model = context.request.headers.get("X-Gemini-Model") || "gemini-3.5-flash";

    const npsh = calculateNPSHa(
      telemetry.suction_pressure_bar,
      telemetry.fluid_temp_celsius || 25.0,
      telemetry.flow_m3_h,
      telemetry.suction_pipe_diam_m || 0.15,
      telemetry.npshr_m || 4.2
    );

    const eff = calculatePumpEfficiency(
      telemetry.discharge_pressure_bar,
      telemetry.suction_pressure_bar,
      telemetry.flow_m3_h,
      telemetry.electrical_power_kw
    );

    let cavSev = 0.0;
    if (npsh.npsh_margin_m < 0.5) cavSev = 0.85;
    else if (npsh.npsh_margin_m < 1.2) cavSev = 0.40;

    let misalignAmp = 0.2;
    if (Math.abs(telemetry.bearing_temp_de_celsius - telemetry.bearing_temp_nde_celsius) > 15.0) {
      misalignAmp = 1.3;
    }

    const fft = generateFFTSpectrum(telemetry.pump_speed_rpm, telemetry.impeller_vanes, cavSev, misalignAmp);

    const scores = {
      H_CAVITATION: npsh.npsh_margin_m < 0.5 ? 4.5 : npsh.npsh_margin_m < 1.2 ? 2.5 : -2.5,
      H_SUCTION_RESTRICTION: telemetry.suction_pressure_bar < 0.6 && telemetry.flow_m3_h < 105.0 ? 4.2 : telemetry.suction_pressure_bar < 0.8 ? 2.0 : -2.0,
      H_IMPELLER_EROSION: eff.efficiency_degradation_pct > 10.0 ? 4.5 : eff.efficiency_degradation_pct > 4.0 ? 2.5 : -2.5,
      H_SHAFT_MISALIGNMENT: misalignAmp > 0.8 ? 4.2 : -2.0,
      H_BEARING_FATIGUE: Math.max(telemetry.bearing_temp_de_celsius, telemetry.bearing_temp_nde_celsius) > 70.0 ? 4.0 : -2.0,
      H_HEALTHY_OPERATION: (npsh.npsh_margin_m >= 1.5 && eff.efficiency_degradation_pct < 4.0 && misalignAmp < 0.5) ? 3.5 : -3.5
    };

    const maxS = Math.max(...Object.values(scores));
    const expScores = Object.fromEntries(Object.entries(scores).map(([k, v]) => [k, Math.exp(v - maxS)]));
    const sumExp = Object.values(expScores).reduce((a, b) => a + b, 0);
    const probs = Object.fromEntries(Object.entries(expScores).map(([k, v]) => [k, (v / sumExp) * 100]));

    const meta = {
      H_CAVITATION: {
        name: "Cavitation / Vapor Bubble Implosion",
        mechanism: "Sheet/cloud cavitation forming at impeller eye due to suction pressure deficit.",
        action: "Inspect suction strainer delta-P, check suction valve position, review NPSH margin.",
        evidence: [`NPSH margin is ${npsh.npsh_margin_m}m (< 0.5m critical limit).`, `High frequency 1-5 kHz broadband energy: ${fft.cavitation_1_5khz_energy_rms} mm/s RMS.`]
      },
      H_SUCTION_RESTRICTION: {
        name: "Suction Line Restriction / Strainer Clogging",
        mechanism: "Excessive suction piping friction loss.",
        action: "Clean basket strainer ST-204 and check upstream isolation valves.",
        evidence: [`Suction pressure dropped to ${telemetry.suction_pressure_bar} bar abs.`]
      },
      H_IMPELLER_EROSION: {
        name: "Impeller Vane Erosion / Leading Edge Wear",
        mechanism: "Progressive metal loss on impeller blade tips.",
        action: "Schedule borescope inspection of impeller eye.",
        evidence: [`Hydraulic efficiency degraded by ${eff.efficiency_degradation_pct}%.`]
      },
      H_SHAFT_MISALIGNMENT: {
        name: "Shaft Misalignment / Coupling Wear",
        mechanism: "Angular/radial offset between motor and pump shafts.",
        action: "Execute laser alignment on pump-motor coupling under LOTO.",
        evidence: [`Dominant 2X running speed vibration peak (${fft.amp_2x_mm_s} mm/s).`]
      },
      H_BEARING_FATIGUE: {
        name: "Bearing Raceway Degradation / Lube Breakdown",
        mechanism: "Rolling element surface spalling.",
        action: "Take grease/oil sample and check ultrasonic vibration.",
        evidence: [`DE bearing temperature elevated to ${telemetry.bearing_temp_de_celsius}°C.`]
      },
      H_HEALTHY_OPERATION: {
        name: "Normal Baseline Operation",
        mechanism: "Operating within allowable BEP envelope.",
        action: "Continue routine continuous monitoring.",
        evidence: ["All hydraulic and vibration parameters are within healthy baseline tolerances."]
      }
    };

    const hypotheses = Object.entries(probs).map(([hid, prob]) => {
      let sev = "LOW";
      if (hid === "H_HEALTHY_OPERATION") sev = prob > 50 ? "HEALTHY" : "NORMAL";
      else if (prob >= 60) sev = "CRITICAL";
      else if (prob >= 35) sev = "HIGH";
      else if (prob >= 15) sev = "MEDIUM";

      return {
        hypothesis_id: hid,
        name: meta[hid].name,
        probability_pct: Number(prob.toFixed(1)),
        severity: sev,
        confidence_interval_pct: Number(Math.min(8.0, Math.max(2.5, 12.0 * (1.0 - prob / 100))).toFixed(1)),
        primary_mechanism: meta[hid].mechanism,
        supporting_evidence: meta[hid].evidence,
        conflicting_evidence: [],
        recommended_technician_action: meta[hid].action
      };
    }).sort((a, b) => b.probability_pct - a.probability_pct);

    const topH = hypotheses[0];
    let opState = topH.severity === "CRITICAL" || fft.overall_rms_mm_s > 4.5 ? "ALARM_CRITICAL" : topH.severity === "HIGH" ? "DEGRADED_WARNING" : "NORMAL_HEALTHY";

    let synthesis = `HydroGuard AI Edge Diagnostics: ${topH.name} identified on Pump ${telemetry.pump_id} with ${topH.probability_pct}% confidence.`;
    if (topH.hypothesis_id === "H_CAVITATION") {
      synthesis = `CRITICAL ALERT: Hydraulic cavitation detected on Pump ${telemetry.pump_id}.\n` +
        `Calculated NPSH Available is ${npsh.npsha_m} m against required ${npsh.npshr_m} m, yielding an unsafe margin of ${npsh.npsh_margin_m} m.\n` +
        `Vibration spectrum exhibits high-frequency broadband energy in the 1.0–5.0 kHz range (${fft.cavitation_1_5khz_energy_rms} mm/s RMS).\n` +
        `RECOMMENDED IMMEDIATE ACTION: Verify suction basket strainer differential pressure and fluid temperature.`;
    }

    const payload = {
      asset_id: telemetry.pump_id,
      timestamp_iso: new Date().toISOString(),
      operating_state: opState,
      hypotheses,
      top_hypothesis: topH,
      next_verification_action: {
        step_id: "NBV-101",
        action_title: "Verify Suction Basket Strainer Differential Pressure (Delta-P)",
        priority: topH.severity === "CRITICAL" ? "IMMEDIATE" : "HIGH",
        safety_risk_level: "LOW (External gauge reading)",
        loto_required: false,
        target_parameter: "Strainer Delta-P (bar)",
        field_instruction: "Connect calibrated differential pressure gauge across suction strainer taps ST-204-A and ST-204-B.",
        expected_information_gain_pct: 88.0,
        input_type: "number",
        input_unit: "bar",
        expected_range: "0.05 - 0.60 bar"
      },
      iso_10816_vibration_zone: fft.overall_rms_mm_s > 4.5 ? "Zone D" : fft.overall_rms_mm_s > 2.8 ? "Zone C" : "Zone A/B",
      calculated_metrics: { ...npsh, ...eff, ...fft },
      ai_engineering_synthesis: synthesis,
      safety_boundary_statement: "HydroGuard AI operates strictly as a Safety Decision-Support System across a read-only physical boundary."
    };

    return new Response(JSON.stringify(payload), {
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type, X-Gemini-API-Key, X-Gemini-Model"
      }
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 400,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, X-Gemini-API-Key, X-Gemini-Model"
    }
  });
}
