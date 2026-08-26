// Cloudflare Pages Function: /api/work-order
export async function onRequestPost(context) {
  try {
    const body = await context.request.json();
    const telem = body.telemetry || {};

    const workOrder = {
      work_order_id: `WO-${Date.now().toString().slice(-6)}`,
      asset_id: telem.pump_id || "P-204",
      asset_tag: "BOOSTER-FEED-01",
      title: "Corrective Hydraulic Inspection: Suction Strainer & Impeller Cavitation Mitigation",
      priority: "EMERGENCY_HIGH",
      failure_mode_diagnosed: "Active Cavitation / Suction Starvation",
      failure_mechanism: "NPSH Available (3.65m) has breached minimum required threshold (4.20m), causing vapor pocket generation.",
      scope_of_work: [
        "1. Execute Lockout/Tagout (LOTO) isolation on motor feeder circuit breaker CB-204.",
        "2. Depressurize and vent suction spool; isolate manual gate valve V-SUC-01.",
        "3. Remove suction basket strainer ST-204; inspect mesh for scale, particulate blinding, or marine fouling.",
        "4. Perform borescope examination of 1st-stage impeller suction eye for pitting or material loss.",
        "5. Reassemble with new spiral wound gaskets and record differential pressure baseline."
      ],
      required_parts_bom: [
        { part_number: "GSK-SPW-316-6", description: "Spiral Wound Gasket 6\" ANSI 300# 316SS/PTFE", quantity: 2, stock_status: "IN_STOCK", location: "Warehouse Bay 4-B" },
        { part_number: "STR-BKT-SS-100", description: "Suction Basket Strainer Screen 100 Mesh 316SS", quantity: 1, stock_status: "IN_STOCK", location: "Warehouse Bay 2-A" },
        { part_number: "LUB-ISO-VG-46", description: "Synthetic Turbine Bearing Oil ISO VG 46 (5L)", quantity: 1, stock_status: "IN_STOCK", location: "Lube Room C-1" }
      ],
      loto_isolation_protocol: {
        loto_id: "LOTO-P204-HYD-01",
        equipment_name: "Booster Pump P-204 & 37kW Drive",
        osha_standard: "OSHA 1910.147",
        steps: [
          { step_number: 1, action: "Notify unit shift supervisor and control room operators of Pump P-204 isolation." },
          { step_number: 2, action: "Open and lockout main 400V Motor Circuit Breaker CB-204 in MCC Room 2 with padlocks." },
          { step_number: 3, action: "Close and lock Suction Isolation Valve V-SUC-01." },
          { step_number: 4, action: "Close and lock Discharge Isolation Valve V-DIS-01." },
          { step_number: 5, action: "Open Casing Drain Valve V-DRN-01 to vent trapped pressure into oily water drainage." },
          { step_number: 6, action: "Perform Zero Energy State Verification on local start pushbutton." }
        ]
      },
      safety_sign_off_status: "PENDING_ENGINEER_APPROVAL",
      created_at_iso: new Date().toISOString()
    };

    return new Response(JSON.stringify(workOrder), {
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type"
      }
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 400,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  }
}
