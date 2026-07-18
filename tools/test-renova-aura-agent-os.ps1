[CmdletBinding()]
param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$ValidationPython = "python",
    [string]$ReferencePython = "python"
)

$ErrorActionPreference = "Stop"
$repoFull = [System.IO.Path]::GetFullPath($RepoRoot)
$validator = Join-Path $repoFull "tools\validate-renova-aura-agent-os.py"
$testRunner = Join-Path $repoFull "tools\run-renova-aura-reference-tests.py"
$reference = Join-Path $repoFull "reference\renova-aura-agent-os-python"

& $ValidationPython $validator --repo-root $repoFull
if ($LASTEXITCODE -ne 0) { throw "Agent OS schema/catalog validation failed." }

$compileCache = Join-Path ([System.IO.Path]::GetTempPath()) ("renova-aura-agent-os-pycache-" + [guid]::NewGuid().ToString("N"))
$previousCachePrefix = $env:PYTHONPYCACHEPREFIX
New-Item -ItemType Directory -Path $compileCache -ErrorAction Stop | Out-Null
try {
    $env:PYTHONPYCACHEPREFIX = $compileCache
    & $ReferencePython -m compileall -q (Join-Path $reference "src") (Join-Path $reference "tests")
    if ($LASTEXITCODE -ne 0) { throw "Reference Python compileall failed." }
}
finally {
    $env:PYTHONPYCACHEPREFIX = $previousCachePrefix
    if (Test-Path -LiteralPath $compileCache) {
        Remove-Item -LiteralPath $compileCache -Recurse -Force
    }
}

$previousPythonPath = $env:PYTHONPATH
$previousDontWriteBytecode = $env:PYTHONDONTWRITEBYTECODE
$testSummary = $null
try {
    $env:PYTHONPATH = Join-Path $reference "src"
    $env:PYTHONDONTWRITEBYTECODE = "1"
    Push-Location -LiteralPath $reference
    try {
        $testOutput = @(& $ReferencePython $testRunner --tests-dir (Join-Path $reference "tests"))
        $testExitCode = $LASTEXITCODE
        $summaryLine = @($testOutput | Where-Object { $_ -like 'RENOVA_AURA_TEST_SUMMARY=*' })
        if ($summaryLine.Count -ne 1) { throw "Reference Python test summary is missing." }
        $testSummary = $summaryLine[0].Substring('RENOVA_AURA_TEST_SUMMARY='.Length) | ConvertFrom-Json
        $testOutput | ForEach-Object { Write-Output $_ }
        if ($testExitCode -ne 0) { throw "Reference Python tests failed." }
    }
    finally { Pop-Location }
}
finally {
    $env:PYTHONPATH = $previousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $previousDontWriteBytecode
}

$ruffStatus = "NOT RUN (dependency unavailable)"
& $ReferencePython -c "import importlib.util; raise SystemExit(0 if importlib.util.find_spec('ruff') else 1)"
if ($LASTEXITCODE -eq 0) {
    & $ReferencePython -m ruff check --no-cache $reference
    if ($LASTEXITCODE -ne 0) { throw "Reference Python Ruff check failed." }
    $ruffStatus = "PASS"
}
elseif ($LASTEXITCODE -ne 1) {
    throw "Unable to determine whether Ruff is available."
}

[pscustomobject]@{
    Status = "PASS"
    AgentOsSchema = "PASS"
    ReferenceCompile = "PASS"
    ReferenceTests = "PASS ($($testSummary.passed)/$($testSummary.tests_run))"
    TestFailures = $testSummary.failures
    TestErrors = $testSummary.errors
    InternalLint = "PASS (tests/test_code_quality.py)"
    Ruff = $ruffStatus
    Skipped = $testSummary.skipped
    Warnings = $testSummary.warnings
    Network = "NOT RUN"
    RealProvider = "NOT RUN"
}
