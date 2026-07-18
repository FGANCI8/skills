[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "High")]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectPath,
    [switch]$Replace
)

$ErrorActionPreference = "Stop"
$projectFull = [System.IO.Path]::GetFullPath($ProjectPath)
if (-not (Test-Path -LiteralPath $projectFull -PathType Container)) {
    throw "Projeto nao encontrado: $projectFull"
}

$destination = Join-Path $projectFull ".agents\skills"
$backup = Join-Path $projectFull (".agents\skills-backup-" + (Get-Date -Format "yyyyMMdd-HHmmssfff"))
$installer = Join-Path $PSScriptRoot "install-renova-aura-skills-global.ps1"
$parameters = @{ Group = "Pdf"; Destination = $destination; BackupRoot = $backup; Replace = $Replace }
if ($WhatIfPreference) { $parameters.WhatIf = $true }
& $installer @parameters
