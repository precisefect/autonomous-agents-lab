# Create a new GitHub repo on your account and push this lab.
# Usage:
#   .\scripts\setup-github.ps1
#   .\scripts\setup-github.ps1 -RepoName autonomous-agents-lab -Visibility private
#   .\scripts\setup-github.ps1 -GitHubUser YOUR_USERNAME

param(
    [string]$RepoName = "autonomous-agents-lab",
    [ValidateSet("public", "private")]
    [string]$Visibility = "private",
    [string]$GitHubUser = ""
)

$ErrorActionPreference = "Stop"
$LabRoot = Split-Path -Parent $PSScriptRoot
$Gh = "C:\Program Files\GitHub CLI\gh.exe"

if (-not (Test-Path $Gh)) {
    $Gh = (Get-Command gh -ErrorAction SilentlyContinue).Source
}
if (-not $Gh) {
    throw "GitHub CLI (gh) not found. Install: winget install GitHub.cli"
}

Write-Host "=== Step 1: Sign in to your NEW GitHub account ===" -ForegroundColor Cyan
Write-Host "A browser window will open. Log in with the account where you want this repo."
& $Gh auth status 2>$null
if ($LASTEXITCODE -ne 0) {
    & $Gh auth login -h github.com -p https -w
}

$status = & $Gh api user --jq .login 2>$null
if (-not $status) {
    throw "GitHub authentication failed. Run: gh auth login"
}
Write-Host "Authenticated as: $status" -ForegroundColor Green

if ($GitHubUser -and $GitHubUser -ne $status) {
    Write-Warning "Logged in as '$status' but -GitHubUser was '$GitHubUser'. Continuing with $status."
}

Push-Location $LabRoot

Write-Host "`n=== Step 2: Create repository '$RepoName' ($Visibility) ===" -ForegroundColor Cyan
$createArgs = @(
    "repo", "create", $RepoName,
    "--source=.", "--remote=origin",
    "--$Visibility", "--push"
)
& $Gh @createArgs

if ($LASTEXITCODE -ne 0) {
    Write-Host "If the repo already exists, adding remote and pushing instead..." -ForegroundColor Yellow
    $remoteUrl = "https://github.com/$status/$RepoName.git"
    git remote remove origin 2>$null
    git remote add origin $remoteUrl
    git push -u origin main
}

Pop-Location

Write-Host "`nDone. Repository:" -ForegroundColor Green
Write-Host "  https://github.com/$status/$RepoName"
