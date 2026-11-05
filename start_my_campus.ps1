[CmdletBinding()]
param([switch]$NoBrowser, [switch]$ValidateOnly)
$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$backendRoot = Join-Path $projectRoot 'backend'
$frontendRoot = Join-Path $projectRoot 'frontend'
$runRoot = Join-Path $projectRoot '.run'
$startedProcesses = @()

function Get-CampusService([int]$Port, [string]$Kind) {
    # Probe HTTP first: Windows CIM port inventory can omit existing listeners.
    try {
        if ($Kind -eq 'backend') {
            $response = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/" -TimeoutSec 3
            if ($response.application -ne 'My Campus') { throw 'Unexpected API' }
        } else {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/index.html" -UseBasicParsing -TimeoutSec 3
            if ($response.Content -notmatch '(?i)my\s*campus') { throw 'Unexpected frontend' }
        }
    } catch {
        $probe = New-Object System.Net.Sockets.TcpClient
        try {
            $pending = $probe.BeginConnect('127.0.0.1', $Port, $null, $null)
            if (-not $pending.AsyncWaitHandle.WaitOne(500)) { return $false }
            $probe.EndConnect($pending)
        } catch { return $false } finally { $probe.Dispose() }
        throw "Port $Port is occupied by another service. Stop it or use the existing project's server."
    }
    return $true
}

function Wait-CampusService([int]$Port, [string]$Kind, $Process) {
    $deadline = (Get-Date).AddSeconds(60)
    do {
        $Process.Refresh()
        if ($Process.HasExited) { throw "$Kind exited. See $runRoot\$Kind.err.log" }
        try { if (Get-CampusService $Port $Kind) { return } } catch { }
        Start-Sleep -Milliseconds 300
    } while ((Get-Date) -lt $deadline)
    throw "$Kind did not become ready within 60 seconds. See $runRoot\$Kind.err.log"
}

try {
    $candidates = @()
    if ($env:VIRTUAL_ENV) { $candidates += (Join-Path $env:VIRTUAL_ENV 'Scripts\python.exe') }
    $candidates += (Join-Path $projectRoot '.venv\Scripts\python.exe')
    $candidates += (Join-Path (Split-Path $projectRoot -Parent) '.venv\Scripts\python.exe')
    $pythonExe = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if (-not $pythonExe) { throw 'No virtual environment found. Create .venv and install requirements.txt first.' }
    & $pythonExe -c "import fastapi,uvicorn,sqlalchemy,httpx,passlib,bcrypt,email_validator,multipart; assert int(bcrypt.__version__.split('.')[0]) < 5, 'Install bcrypt==4.0.1 for passlib compatibility'"
    if ($LASTEXITCODE -ne 0) { throw "Dependency validation failed. Run: & '$pythonExe' -m pip install -r '$projectRoot\requirements.txt'" }
    Write-Host "Python: $pythonExe"
    $backendRunning = Get-CampusService 8000 'backend'
    $frontendRunning = Get-CampusService 5500 'frontend'
    if ($ValidateOnly) { Write-Host 'Launcher prerequisites validated.'; exit 0 }
    & $pythonExe (Join-Path $projectRoot 'setup_demo.py')
    if ($LASTEXITCODE -ne 0) { throw 'Safe initialization failed. Servers have not been started.' }
    New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
    if (-not $backendRunning) {
        $backendArgs = @('-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8000')
        $proc = Start-Process -FilePath $pythonExe -ArgumentList $backendArgs -WorkingDirectory $backendRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $runRoot 'backend.out.log') -RedirectStandardError (Join-Path $runRoot 'backend.err.log')
        $startedProcesses += $proc
        Wait-CampusService 8000 'backend' $proc
    } else { Write-Host 'Reusing MY CAMPUS backend on port 8000. Restart it after source updates.' }
    if (-not $frontendRunning) {
        $proc = Start-Process -FilePath $pythonExe -ArgumentList @('-m','http.server','5500','--bind','127.0.0.1') -WorkingDirectory $frontendRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $runRoot 'frontend.out.log') -RedirectStandardError (Join-Path $runRoot 'frontend.err.log')
        $startedProcesses += $proc
        Wait-CampusService 5500 'frontend' $proc
    } else { Write-Host 'Reusing MY CAMPUS frontend on port 5500.' }
    Write-Host 'Frontend: http://127.0.0.1:5500/index.html'
    Write-Host 'Backend:  http://127.0.0.1:8000/docs'
    if (-not $NoBrowser) { Start-Process 'http://127.0.0.1:5500/index.html' }
} catch {
    foreach ($proc in $startedProcesses) {
        if (-not $proc.HasExited) { Stop-Process -Id $proc.Id -ErrorAction SilentlyContinue }
    }
    Write-Error "MY CAMPUS startup failed: $($_.Exception.Message)" -ErrorAction Continue
    exit 1
}
