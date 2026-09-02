#!/usr/bin/env bash
# HydroGuard AI — Cloudflare Pages Automated Deployment Script (Bash)
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Run build
bash "$SCRIPT_DIR/build.sh"

# 2. Deploy via Wrangler
echo ""
echo "3. Uploading to Cloudflare Pages (Project: hydroguard-ai)..."
cd "$SCRIPT_DIR"
npx wrangler pages deploy dist --project-name hydroguard-ai --commit-dirty=true

echo ""
echo "DEPLOYMENT SUCCESS: HydroGuard AI is live on Cloudflare Pages!"
echo "Live URL: https://hydroguardai.pages.dev/"
