# ⛅ Cloudflare Pages Deployment Package — HydroGuard AI

This directory contains the production-ready configuration, SPA routing manifests, security headers, edge serverless functions, and automated build scripts to deploy **HydroGuard AI** to **Cloudflare Pages**.

> **Live Production URL:** [https://hydroguard-ai.pages.dev](https://hydroguard-ai.pages.dev)  
> **GitHub Repository:** [https://github.com/hsinidev/HydroGuard-AI](https://github.com/hsinidev/HydroGuard-AI)  
> **Lead Architect:** **Mohamed Hsini** ([https://hsini.dev](https://hsini.dev) | [contact@hsini.dev](mailto:contact@hsini.dev))

---

## 📁 Directory Structure

```
cloudflare/
├── wrangler.toml              # Cloudflare Pages / Workers configuration
├── _headers                   # Security headers (CSP, FrameGuard, Cache-Control)
├── _routes.json               # SPA routing rule definitions (excludes static assets)
├── build.ps1 / build.sh       # Automated build & dist assembly scripts
├── deploy.ps1 / deploy.sh     # One-click Wrangler deployment scripts
├── functions/                 # Cloudflare Pages Functions (V8 Edge API)
│   └── api/
│       ├── health.js          # Edge GET /api/health
│       ├── diagnose.js        # Edge POST /api/diagnose (Hydraulic Math & FFT)
│       └── work-order.js      # Edge POST /api/work-order (ISO 55000 / LOTO)
└── dist/                      # Compiled production distribution directory
```

---

## 🚀 Option 1: One-Click CLI Deployment (Wrangler)

### Windows (PowerShell):
```powershell
# 1. Log in to Cloudflare (one-time)
npx wrangler login

# 2. Run automated build and deploy
.\cloudflare\deploy.ps1
```

### Linux / macOS (Bash):
```bash
# 1. Log in to Cloudflare (one-time)
npx wrangler login

# 2. Run automated build and deploy
chmod +x cloudflare/deploy.sh
./cloudflare/deploy.sh
```

---

## 🌐 Option 2: Cloudflare Dashboard Git Integration (Recommended)

1. Open the [Cloudflare Dashboard](https://dash.cloudflare.com/) and navigate to **Workers & Pages** > **Create application** > **Pages** > **Connect to Git**.
2. Select repository: `hsinidev/HydroGuard-AI`
3. Configure the Build Settings:
   - **Framework preset:** `Vite`
   - **Build command:** `npm run build`
   - **Build output directory:** `frontend/dist`
   - **Root directory:** `frontend`
4. Click **Save and Deploy**. Cloudflare Pages will automatically rebuild and deploy on every push to `main`.

---

## 🛡️ Edge Features Included
- **Client & Edge Physical Math:** Pure deterministic equations ($NPSH_a$, Total Dynamic Head, Pump Efficiency, FFT Cavitation Energy band extraction) run natively in the browser and across 300+ Cloudflare edge data centers.
- **Edge API Functions:** Edge handlers in `functions/api/` handle real-time `/api/health`, `/api/diagnose`, and `/api/work-order` requests.
- **Strict Read-Only Boundary:** Zero physical actuation risk; conforms to ISO 10816-3, ISO 55000, and OSHA 1910.147.
