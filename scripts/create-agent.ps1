# Create a new agent from agent-template (Windows PowerShell).
# Usage: .\scripts\create-agent.ps1 -AgentName quality-inspector

param(
    [Parameter(Mandatory = $true)]
    [string]$AgentName
)

$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent $PSScriptRoot
$TemplateDir = Join-Path $RootDir "agent-template"
$AgentsDir = Join-Path $RootDir "agents"
$AgentName = $AgentName.ToLower() -replace '[\s_]+', '-'
$TargetDir = Join-Path $AgentsDir $AgentName

if (-not (Test-Path $TemplateDir)) {
    throw "agent-template not found at $TemplateDir"
}
if (Test-Path $TargetDir) {
    throw "Agent already exists at $TargetDir"
}

New-Item -ItemType Directory -Force -Path $AgentsDir | Out-Null
Copy-Item -Path $TemplateDir -Destination $TargetDir -Recurse

# Bundle shared-core for standalone runs and Docker builds
$SharedCoreSrc = Join-Path $RootDir "shared-core"
$SharedCoreDst = Join-Path $TargetDir "shared-core"
if (Test-Path $SharedCoreSrc) {
    Copy-Item -Path $SharedCoreSrc -Destination $SharedCoreDst -Recurse -Force
}

# Use standalone Dockerfile for per-agent builds
$DockerAgent = Join-Path $TemplateDir "Dockerfile.agent"
if (Test-Path $DockerAgent) {
    Copy-Item $DockerAgent (Join-Path $TargetDir "Dockerfile") -Force
}

$envFile = Join-Path $TargetDir ".env"
$envExample = Join-Path $TargetDir ".env.example"
if (Test-Path $envExample) {
    Copy-Item $envExample $envFile -Force
    (Get-Content $envFile) -replace 'APP_NAME=agent-template', "APP_NAME=$AgentName" | Set-Content $envFile
}

Write-Host "Agent '$AgentName' created at: $TargetDir"
Write-Host "Commit from lab root: git add agents/$AgentName && git commit -m 'Add $AgentName agent'"
Write-Host "Next: cd $TargetDir; python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt"
