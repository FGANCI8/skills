[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "High")]
param([switch]$Replace)

$installer = Join-Path $PSScriptRoot "install-renova-aura-skills-global.ps1"
$parameters = @{ Group = "Pdf"; Replace = $Replace }
if ($WhatIfPreference) { $parameters.WhatIf = $true }
& $installer @parameters
