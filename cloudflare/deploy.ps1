# HydroGuard AI - Cloudflare Pages Deploy Script (PowerShell)
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " HydroGuard AI - Deploying to Cloudflare Pages via Wrangler" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Run build
& (Join-Path $ScriptDir "build.ps1")

# 2. Deploy via Wrangler
Write-Host "`n3. Uploading to Cloudflare Pages (Project: hydroguard-ai)..." -ForegroundColor Yellow
Set-Location $ScriptDir
npx wrangler pages deploy dist --project-name hydroguard-ai --commit-dirty=true

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nDEPLOYMENT SUCCESS: HydroGuard AI is live on Cloudflare Pages!" -ForegroundColor Green
    Write-Host "Live URL: https://hydroguard-ai.pages.dev" -ForegroundColor Cyan
} else {
    Write-Host "`nNOTE: If not logged in, please run 'npx wrangler login' or export CLOUDFLARE_API_TOKEN." -ForegroundColor Yellow
}
