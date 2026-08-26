#!/usr/bin/env bash
# HydroGuard AI — Cloudflare Pages Automated Build Script (Bash/Linux/macOS)
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
DIST_DIR="$SCRIPT_DIR/dist"

echo "=========================================================="
echo " HydroGuard AI — Building Cloudflare Pages Distribution   "
echo "=========================================================="

echo "1. Compiling React + Vite + Tailwind Frontend Bundle..."
cd "$FRONTEND_DIR"
npm run build

echo "2. Assembling Cloudflare Production Distribution in $DIST_DIR..."
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

cp -r "$FRONTEND_DIR/dist/"* "$DIST_DIR/"
cp "$SCRIPT_DIR/_headers" "$DIST_DIR/"
cp "$SCRIPT_DIR/_routes.json" "$DIST_DIR/"

echo "SUCCESS: Cloudflare Pages distribution bundle assembled successfully in $DIST_DIR"
