param()

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Destination = Join-Path $env:USERPROFILE ".agents\skills"
$SkillNames = @(
    "renova-aura-pdf-forms-router",
    "renova-aura-fillable-pdf-architect",
    "renova-aura-pdf-compatibility-auditor",
    "renova-aura-pdf-viewer-validation-runbook",
    "renova-aura-pdf-delivery-guardian"
)

New-Item -ItemType Directory -Force -Path $Destination | Out-Null

foreach ($Name in $SkillNames) {
    $Source = Join-Path $RepoRoot "skills\$Name"
    if (-not (Test-Path $Source)) {
        throw "Skill nao encontrada: $Source"
    }
    $Target = Join-Path $Destination $Name
    New-Item -ItemType Directory -Force -Path $Target | Out-Null
    Copy-Item -Path (Join-Path $Source "*") -Destination $Target -Recurse -Force
    Write-Host "Instalada: $Name"
}

Write-Host ""
Write-Host "Destino: $Destination"
Write-Host "Abra uma nova sessao do Codex."