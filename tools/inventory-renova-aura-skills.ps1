[CmdletBinding()]
param(
    [string]$GlobalSkillsRoot = (Join-Path $env:USERPROFILE ".agents\skills"),
    [string[]]$PrivateRoots = @(),
    [Parameter(Mandatory = $true)][string]$OutputDirectory
)

$ErrorActionPreference = "Stop"
$outputFull = [System.IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Force -Path $outputFull | Out-Null

$globalRows = foreach ($dir in (Get-ChildItem -LiteralPath $GlobalSkillsRoot -Directory | Sort-Object Name)) {
    $skillFile = Join-Path $dir.FullName "SKILL.md"
    $files = @(Get-ChildItem -LiteralPath $dir.FullName -File -Recurse -Force | Sort-Object FullName)
    $content = if (Test-Path -LiteralPath $skillFile) { Get-Content -LiteralPath $skillFile -Raw -Encoding UTF8 } else { "" }
    $declaredName = if ($content -match '(?m)^name:\s*(.+?)\s*$') { $Matches[1].Trim('"'' ') } else { $null }
    $description = if ($content -match '(?m)^description:\s*(.+?)\s*$') { $Matches[1].Trim('"'' ') } else { $null }
    [pscustomobject]@{
        folder = $dir.Name
        declared_name = $declaredName
        description = $description
        file_count = $files.Count
        auxiliary_files = (@($files | Where-Object Name -ne "SKILL.md" | ForEach-Object { $_.FullName.Substring($dir.FullName.Length + 1) }) -join ";")
        bytes = ($files | Measure-Object Length -Sum).Sum
        created = $dir.CreationTime.ToString("o")
        modified = $dir.LastWriteTime.ToString("o")
        skill_sha256 = if (Test-Path -LiteralPath $skillFile) { (Get-FileHash -LiteralPath $skillFile -Algorithm SHA256).Hash } else { $null }
    }
}
$globalRows | Export-Csv -LiteralPath (Join-Path $outputFull "global-skills.csv") -NoTypeInformation -Encoding UTF8

$backupRows = foreach ($dir in (Get-ChildItem -LiteralPath (Split-Path -Parent $GlobalSkillsRoot) -Directory -Force | Where-Object { $_.Name -like "skills-backup-*" -or $_.Name -like "skills-backup-pdf-*" } | Sort-Object Name)) {
    $files = @(Get-ChildItem -LiteralPath $dir.FullName -File -Recurse -Force)
    [pscustomobject]@{ path = $dir.FullName; files = $files.Count; bytes = ($files | Measure-Object Length -Sum).Sum; modified = $dir.LastWriteTime.ToString("o") }
}
$backupRows | Export-Csv -LiteralPath (Join-Path $outputFull "skill-backups.csv") -NoTypeInformation -Encoding UTF8

$sourceRows = foreach ($root in $PrivateRoots) {
    if (-not (Test-Path -LiteralPath $root -PathType Container)) { continue }
    Push-Location -LiteralPath $root
    try {
        $paths = @(rg --files --hidden -g '!**/.git/**' -g '!**/node_modules/**' -g '!**/.next/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/coverage/**' 2>$null)
        foreach ($relative in $paths) {
            if ($relative -notmatch '(?i)(^|[\\/])(AGENTS(\.override)?\.md|SKILL\.md)$|prompt|agent|workflow|instruction|handoff|architecture|security|design|audit') { continue }
            $full = Join-Path $root $relative
            $item = Get-Item -LiteralPath $full
            [pscustomobject]@{
                source_root = $root
                relative_path = $relative
                bytes = $item.Length
                modified = $item.LastWriteTime.ToString("o")
                sha256 = (Get-FileHash -LiteralPath $full -Algorithm SHA256).Hash
            }
        }
    }
    finally { Pop-Location }
}
$sourceRows | Export-Csv -LiteralPath (Join-Path $outputFull "private-source-paths.csv") -NoTypeInformation -Encoding UTF8

[pscustomobject]@{ GlobalSkills = @($globalRows).Count; Backups = @($backupRows).Count; PrivateCandidates = @($sourceRows).Count; OutputDirectory = $outputFull }
