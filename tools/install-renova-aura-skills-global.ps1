[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "High")]
param(
    [ValidateSet("Core", "AgentOs", "Pdf", "All")]
    [string[]]$Group = @("Core"),

    [string]$Destination = (Join-Path $env:USERPROFILE ".agents\skills"),

    [string]$BackupRoot,

    [switch]$Replace
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot

$CoreSkills = @(
    "renova-aura-router",
    "renova-aura-project-bootstrap",
    "renova-aura-product-spec",
    "renova-aura-saas-architect",
    "renova-aura-engineering-guardian",
    "renova-aura-security-data-guardian",
    "renova-aura-ux-design-system",
    "renova-aura-premium-frontend",
    "renova-aura-ai-integration-guardian",
    "renova-aura-quality-release",
    "renova-aura-observability-incident",
    "renova-aura-prompt-source-designer",
    "renova-aura-project-handoff",
    "renova-aura-skill-library-curator"
)

$AgentOsSkills = @(
    "renova-aura-agent-orchestrator",
    "renova-aura-backend-api-engineer",
    "renova-aura-database-reliability",
    "renova-aura-python-engineering",
    "renova-aura-performance-engineering",
    "renova-aura-independent-reviewer"
)

$PdfSkills = @(
    "renova-aura-pdf-forms-router",
    "renova-aura-fillable-pdf-architect",
    "renova-aura-pdf-compatibility-auditor",
    "renova-aura-pdf-viewer-validation-runbook",
    "renova-aura-pdf-delivery-guardian"
)

function Get-TreeHashMap {
    param([Parameter(Mandatory = $true)][string]$Path)

    $resolved = [System.IO.Path]::GetFullPath($Path)
    $map = [ordered]@{}
    foreach ($file in (Get-ChildItem -LiteralPath $resolved -File -Recurse -Force | Sort-Object FullName)) {
        $relative = $file.FullName.Substring($resolved.Length).TrimStart('\', '/') -replace '\\', '/'
        $map[$relative] = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash
    }
    return $map
}

function Test-TreeEqual {
    param(
        [Parameter(Mandatory = $true)][string]$Left,
        [Parameter(Mandatory = $true)][string]$Right
    )

    $leftMap = Get-TreeHashMap -Path $Left
    $rightMap = Get-TreeHashMap -Path $Right
    if ($leftMap.Count -ne $rightMap.Count) { return $false }
    foreach ($key in $leftMap.Keys) {
        if (-not $rightMap.Contains($key) -or $leftMap[$key] -ne $rightMap[$key]) { return $false }
    }
    return $true
}

function Test-SkillSource {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Path
    )

    $skillFile = Join-Path $Path "SKILL.md"
    if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
        throw "SKILL.md ausente: $skillFile"
    }

    $content = Get-Content -LiteralPath $skillFile -Raw -Encoding UTF8
    if ($content -notmatch "(?m)^name:\s*$([regex]::Escape($Name))\s*$") {
        throw "Nome declarado nao corresponde a pasta: $Name"
    }
    $todoMarker = '\[' + 'TO' + 'DO'
    if ($content -match $todoMarker) {
        throw "Placeholder TODO encontrado: $skillFile"
    }
}

$selectedGroups = if ($Group -contains "All") { @("Core", "AgentOs", "Pdf") } else { @($Group | Select-Object -Unique) }
$SkillNames = @()
if ($selectedGroups -contains "Core") { $SkillNames += $CoreSkills }
if ($selectedGroups -contains "AgentOs") { $SkillNames += $AgentOsSkills }
if ($selectedGroups -contains "Pdf") { $SkillNames += $PdfSkills }
$SkillNames = @($SkillNames | Select-Object -Unique)

$destinationFull = [System.IO.Path]::GetFullPath($Destination)
if ([System.IO.Path]::GetPathRoot($destinationFull) -eq $destinationFull) {
    throw "Destino amplo ou invalido: $destinationFull"
}

if (-not $BackupRoot) {
    $destinationParent = Split-Path -Parent $destinationFull
    $BackupRoot = Join-Path $destinationParent ("skills-backup-" + (Get-Date -Format "yyyyMMdd-HHmmssfff"))
}
$backupFull = [System.IO.Path]::GetFullPath($BackupRoot)

$plan = foreach ($name in $SkillNames) {
    $source = [System.IO.Path]::GetFullPath((Join-Path $RepoRoot "skills\$name"))
    $target = [System.IO.Path]::GetFullPath((Join-Path $destinationFull $name))
    Test-SkillSource -Name $name -Path $source

    if (-not $target.StartsWith($destinationFull + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Destino da skill escapou da raiz aprovada: $target"
    }

    $state = if (-not (Test-Path -LiteralPath $target)) {
        "NEW"
    }
    elseif (Test-TreeEqual -Left $source -Right $target) {
        "IDENTICAL"
    }
    else {
        "DIFFERENT"
    }

    [pscustomobject]@{ Name = $name; Source = $source; Target = $target; State = $state }
}

$conflicts = @($plan | Where-Object State -eq "DIFFERENT")
if ($conflicts.Count -gt 0 -and -not $Replace) {
    $names = ($conflicts.Name -join ", ")
    throw "Destinos divergentes encontrados: $names. Rode novamente com -Replace apos revisar o dry-run; cada destino sera salvo em backup."
}

foreach ($item in $plan) {
    if ($item.State -eq "IDENTICAL") {
        [pscustomobject]@{ Skill = $item.Name; Result = "UNCHANGED"; Destination = $item.Target; Backup = $null }
        continue
    }

    $action = if ($item.State -eq "NEW") { "instalar" } else { "substituir com backup" }
    if (-not $PSCmdlet.ShouldProcess($item.Target, "$action $($item.Name)")) {
        [pscustomobject]@{ Skill = $item.Name; Result = "PLANNED"; Destination = $item.Target; Backup = if ($item.State -eq "DIFFERENT") { Join-Path $backupFull $item.Name } else { $null } }
        continue
    }

    New-Item -ItemType Directory -Force -Path $destinationFull | Out-Null
    $tempRoot = Join-Path (Split-Path -Parent $destinationFull) ("skills-install-tmp-" + [guid]::NewGuid().ToString("N"))
    $staged = Join-Path $tempRoot $item.Name
    $backupTarget = Join-Path $backupFull $item.Name
    $oldMoved = $false

    try {
        New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null
        Copy-Item -LiteralPath $item.Source -Destination $staged -Recurse
        if (-not (Test-TreeEqual -Left $item.Source -Right $staged)) {
            throw "Copia temporaria divergiu da origem: $($item.Name)"
        }

        if ($item.State -eq "DIFFERENT") {
            New-Item -ItemType Directory -Force -Path $backupFull | Out-Null
            Move-Item -LiteralPath $item.Target -Destination $backupTarget
            $oldMoved = $true
        }

        Move-Item -LiteralPath $staged -Destination $item.Target
        if (-not (Test-TreeEqual -Left $item.Source -Right $item.Target)) {
            throw "Instalacao divergiu da origem: $($item.Name)"
        }

        [pscustomobject]@{ Skill = $item.Name; Result = if ($oldMoved) { "REPLACED" } else { "INSTALLED" }; Destination = $item.Target; Backup = if ($oldMoved) { $backupTarget } else { $null } }
    }
    catch {
        if (Test-Path -LiteralPath $item.Target) {
            New-Item -ItemType Directory -Force -Path $backupFull | Out-Null
            $failedTarget = Join-Path $backupFull ($item.Name + "-failed-" + [guid]::NewGuid().ToString("N"))
            Move-Item -LiteralPath $item.Target -Destination $failedTarget
        }
        if ($oldMoved -and (Test-Path -LiteralPath $backupTarget)) {
            Move-Item -LiteralPath $backupTarget -Destination $item.Target
        }
        throw
    }
    finally {
        $tempFull = [System.IO.Path]::GetFullPath($tempRoot)
        $parentFull = [System.IO.Path]::GetFullPath((Split-Path -Parent $destinationFull))
        if ((Test-Path -LiteralPath $tempFull) -and $tempFull.StartsWith($parentFull + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
            Remove-Item -LiteralPath $tempFull -Recurse -Force
        }
    }
}

Write-Host "Destino verificado: $destinationFull"
if ($plan.State -contains "DIFFERENT") { Write-Host "Backup: $backupFull" }
Write-Host "Abra uma nova sessao para recarregar as skills."
