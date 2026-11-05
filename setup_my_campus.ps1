[CmdletBinding()]
param([switch]$PrepareOnly)
$ErrorActionPreference = 'Stop'
try {
    $projectRoot = $PSScriptRoot
    $pythonExe = $null
    $pythonPrefix = @()
    # Prefer the repository's environment; do not install into an unrelated
    # activated environment or depend on a developer's absolute Python path.
    $localPython = Join-Path $projectRoot '.venv\Scripts\python.exe'
    $registeredPython = @()
    foreach ($registryRoot in @('HKCU:\Software\Python\PythonCore', 'HKLM:\Software\Python\PythonCore')) {
        foreach ($version in (Get-ChildItem -LiteralPath $registryRoot -ErrorAction SilentlyContinue)) {
            $install = Get-ItemProperty -LiteralPath ($version.PSPath + '\InstallPath') -ErrorAction SilentlyContinue
            if ($install -and $install.ExecutablePath) { $registeredPython += $install.ExecutablePath }
        }
    }
    $candidates = @($localPython, 'py.exe') + $registeredPython + @('python.exe', 'python3.exe')
    foreach ($candidate in $candidates) {
        if ([IO.Path]::IsPathRooted($candidate)) {
            if (-not (Test-Path -LiteralPath $candidate)) { continue }
            $commandPath = $candidate
        } else {
            $command = Get-Command $candidate -ErrorAction SilentlyContinue
            if (-not $command) { continue }
            $commandPath = $command.Source
        }
        $prefix = @()
        if ($candidate -eq 'py.exe') { $prefix = @('-3') }
        & $commandPath @prefix -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)" 2>$null
        if ($LASTEXITCODE -eq 0) {
            $pythonExe = $commandPath
            $pythonPrefix = $prefix
            break
        }
    }
    if (-not $pythonExe) { throw 'Python 3.10+ was not found. Install Python with its launcher or PATH option, then rerun setup.' }
    $setupArgs = @((Join-Path $projectRoot 'setup_my_campus.py'))
    if ($PrepareOnly) { $setupArgs += '--prepare-only' }
    & $pythonExe @pythonPrefix @setupArgs
    if ($LASTEXITCODE -ne 0) { throw 'Project setup failed. See the Python/dependency error above.' }
} catch {
    Write-Error "MY CAMPUS setup failed: $($_.Exception.Message)" -ErrorAction Continue
    exit 1
}
