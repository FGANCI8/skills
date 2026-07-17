[CmdletBinding()]
param([string]$RepoRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = "Stop"
$errors = [System.Collections.Generic.List[string]]::new()
$skillRoot = Join-Path $RepoRoot "skills"
$skills = Get-ChildItem -LiteralPath $skillRoot -Directory | Where-Object Name -like "renova-aura-*" | Sort-Object Name

foreach ($skill in $skills) {
    $skillFile = Join-Path $skill.FullName "SKILL.md"
    $interfaceFile = Join-Path $skill.FullName "agents\openai.yaml"
    if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
        $errors.Add("$($skill.Name): SKILL.md ausente")
        continue
    }

    $content = Get-Content -LiteralPath $skillFile -Raw -Encoding UTF8
    if ($content -notmatch '(?s)^---\s*\r?\n(.*?)\r?\n---') {
        $errors.Add("$($skill.Name): frontmatter invalido")
        continue
    }

    $frontmatter = $Matches[1]
    $keys = @([regex]::Matches($frontmatter, '(?m)^([a-zA-Z0-9_-]+):') | ForEach-Object { $_.Groups[1].Value })
    $unexpected = @($keys | Where-Object { $_ -notin @('name', 'description') })
    if ($unexpected.Count -gt 0) { $errors.Add("$($skill.Name): chaves inesperadas no frontmatter: $($unexpected -join ', ')") }

    $declaredName = if ($frontmatter -match '(?m)^name:\s*(.+?)\s*$') { $Matches[1].Trim('"'' ') } else { $null }
    $description = if ($frontmatter -match '(?m)^description:\s*(.+?)\s*$') { $Matches[1].Trim('"'' ') } else { $null }
    if ($declaredName -ne $skill.Name) { $errors.Add("$($skill.Name): name divergente: $declaredName") }
    if (-not $description -or $description.Length -gt 1024) { $errors.Add("$($skill.Name): description ausente ou longa demais") }
    if ($content -match '\[TODO|TODO:') { $errors.Add("$($skill.Name): TODO nao resolvido") }

    if (-not (Test-Path -LiteralPath $interfaceFile -PathType Leaf)) {
        $errors.Add("$($skill.Name): agents/openai.yaml ausente")
    }
    else {
        $interface = Get-Content -LiteralPath $interfaceFile -Raw -Encoding UTF8
        if ($interface -notmatch [regex]::Escape("`$$($skill.Name)")) {
            $errors.Add("$($skill.Name): default_prompt nao menciona `$$($skill.Name)")
        }
        if ($interface -notmatch '(?m)^\s*short_description:\s*"([^"]+)"') {
            $errors.Add("$($skill.Name): short_description ausente")
        }
        elseif ($Matches[1].Length -lt 25 -or $Matches[1].Length -gt 64) {
            $errors.Add("$($skill.Name): short_description deve ter 25-64 caracteres")
        }
        if ($interface.Contains([char]0xFFFD)) {
            $errors.Add("$($skill.Name): caractere de substituicao Unicode em openai.yaml")
        }
    }

    foreach ($match in [regex]::Matches($content, '\]\((references/[^)#]+)\)')) {
        $reference = Join-Path $skill.FullName ($match.Groups[1].Value -replace '/', '\')
        if (-not (Test-Path -LiteralPath $reference -PathType Leaf)) {
            $errors.Add("$($skill.Name): referencia ausente: $($match.Groups[1].Value)")
        }
    }
}

$publicFiles = @(
    Get-ChildItem -LiteralPath $RepoRoot -File | Where-Object { $_.Name -like 'RENOVA_AURA_*' -or $_.Name -eq 'README.md' }
    Get-ChildItem -LiteralPath (Join-Path $RepoRoot 'prompts') -File -Recurse -Force
    Get-ChildItem -LiteralPath (Join-Path $RepoRoot 'tools') -File -Force | Where-Object Name -like '*renova-aura*'
    foreach ($skill in $skills) { Get-ChildItem -LiteralPath $skill.FullName -File -Recurse -Force }
) | Sort-Object FullName -Unique
$secretPattern = '(?i)(gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----)'
foreach ($file in $publicFiles) {
    if ($file.Extension -notin @('.md', '.yaml', '.yml', '.json', '.ps1', '.txt')) { continue }
    $text = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if ($text.Contains([char]0xFFFD)) { $errors.Add("Encoding UTF-8 invalido em $($file.FullName.Substring($RepoRoot.Length + 1))") }
    if ($text -match $secretPattern) { $errors.Add("Possivel segredo em $($file.FullName.Substring($RepoRoot.Length + 1))") }
    if ($text -match '(?i)C:\\Users\\[^\\\s]+|C:\\(Aura|Zuno|PetShop|Negocia)') {
        $errors.Add("Possivel caminho privado em $($file.FullName.Substring($RepoRoot.Length + 1))")
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    throw "Validacao falhou com $($errors.Count) erro(s)."
}

[pscustomobject]@{ Status = "PASS"; Skills = $skills.Count; PublicFilesScanned = $publicFiles.Count }
