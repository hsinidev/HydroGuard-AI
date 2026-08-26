# HydroGuard AI - Cloudflare Pages Build Script (PowerShell)
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " HydroGuard AI - Building Cloudflare Pages Distribution   " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$FrontendDir = Join-Path $ProjectRoot "frontend"
$DistDir = Join-Path $ScriptDir "dist"

Write-Host "1. Compiling React and Vite Frontend Bundle..." -ForegroundColor Yellow
Set-Location $FrontendDir
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Frontend build failed!" -ForegroundColor Red
    Set-Location $ProjectRoot
    exit 1
}

Write-Host "2. Assembling Cloudflare Distribution in: $DistDir..." -ForegroundColor Yellow
if (Test-Path $DistDir) {
    Remove-Item -Recurse -Force $DistDir
}
New-Item -ItemType Directory -Force -Path $DistDir | Out-Null

Copy-Item -Recurse -Force (Join-Path $FrontendDir "dist\*") $DistDir
Copy-Item -Force (Join-Path $ScriptDir "_headers") $DistDir
Copy-Item -Force (Join-Path $ScriptDir "_routes.json") $DistDir

Write-Host "SUCCESS: Cloudflare Pages distribution bundle is ready!" -ForegroundColor Green
Write-Host "Target Directory: $DistDir" -ForegroundColor Green
Set-Location $ProjectRoot
