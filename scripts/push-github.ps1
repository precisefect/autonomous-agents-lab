# Push to an existing GitHub repo (after gh auth login as the repo owner).
# Usage:
#   .\scripts\push-github.ps1
#   .\scripts\push-github.ps1 -RemoteUrl https://github.com/precisefect/autonomous-agents-lab.git

param(
    [string]$RemoteUrl = "https://github.com/precisefect/autonomous-agents-lab.git"
)

$ErrorActionPreference = "Stop"
$LabRoot = Split-Path -Parent $PSScriptRoot
$Gh = "C:\Program Files\GitHub CLI\gh.exe"
if (-not (Test-Path $Gh)) { $Gh = (Get-Command gh).Source }

Push-Location $LabRoot

Write-Host "Checking GitHub login..." -ForegroundColor Cyan
$user = & $Gh api user --jq .login 2>$null
if (-not $user) {
    Write-Host "Not logged in. Run: gh auth login" -ForegroundColor Yellow
    & $Gh auth login -h github.com -p https -w
    & $Gh auth setup-git
    $user = & $Gh api user --jq .login
}
Write-Host "GitHub user: $user" -ForegroundColor Green

git remote remove origin 2>$null
git remote add origin $RemoteUrl
git branch -M main

Write-Host "Pushing to $RemoteUrl ..." -ForegroundColor Cyan
git push -u origin main

Pop-Location
Write-Host "Done: $RemoteUrl" -ForegroundColor Green
