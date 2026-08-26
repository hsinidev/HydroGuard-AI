export async function onRequestGet(context) {
  return new Response(JSON.stringify({
    status: "ONLINE",
    service: "HydroGuard AI Cloudflare Edge Diagnostic Gateway",
    version: "2.4.0-PROD",
    edge_runtime: "Cloudflare Pages Functions (V8 Worker)",
    safety_mode: "READ_ONLY_DECISION_SUPPORT",
    lead_architect: "Mohamed Hsini",
    portfolio: "https://hsini.dev",
    contact: "contact@hsini.dev",
    supported_models: ["gemini-3.5-flash", "gemini-3.5-pro", "gemini-2.5-flash"]
  }), {
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Cache-Control": "no-cache"
    }
  });
}
