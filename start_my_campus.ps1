[CmdletBinding()]
param([switch]$NoBrowser, [switch]$ValidateOnly)
$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$backendRoot = Join-Path $projectRoot 'backend'
$frontendRoot = Join-Path $projectRoot 'frontend'
$runRoot = Join-Path $projectRoot '.run'
$startedProcesses = @()
$expectedInstance = $null

function Get-CampusService([int]$Port, [string]$Kind) {
    # Probe HTTP first: Windows CIM port inventory can omit existing listeners.
    try {
        if ($Kind -eq 'backend') {
            $response = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/health" -TimeoutSec 3
            if ($response.instance_id -ne $expectedInstance) { throw 'A different checkout/database or outdated MY CAMPUS backend is using this port. Stop that backend and restart from this repository.' }
            if ($response.status -ne 'healthy' -or -not $response.content.ready) { throw 'Learning content is incomplete. Run setup_my_campus.bat and check DATABASE_URL.' }
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
        throw "Port $Port cannot be reused: $($_.Exception.Message)"
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
    $localPython = Join-Path $projectRoot '.venv\Scripts\python.exe'
    $candidates = @($localPython, (Join-Path (Split-Path $projectRoot -Parent) '.venv\Scripts\python.exe'))
    $pythonExe = $null
    foreach ($candidate in $candidates) {
        if (-not (Test-Path -LiteralPath $candidate)) { continue }
        & $candidate -c "import importlib.util; raise SystemExit(0 if all(importlib.util.find_spec(m) for m in ['fastapi','uvicorn','sqlalchemy','httpx','passlib','bcrypt','email_validator','multipart']) else 1)"
        if ($LASTEXITCODE -eq 0) { $pythonExe = $candidate; break }
    }
    if (-not $pythonExe) {
        if ($ValidateOnly) { throw 'Run setup_my_campus.bat to prepare the project environment first.' }
        & (Join-Path $projectRoot 'setup_my_campus.ps1') -PrepareOnly
        if ($LASTEXITCODE -ne 0) { throw 'Automatic first-time environment setup failed.' }
        $pythonExe = $localPython
    } elseif ($pythonExe -eq $localPython -and -not $ValidateOnly) {
        & $pythonExe (Join-Path $projectRoot 'setup_my_campus.py') --prepare-only
        if ($LASTEXITCODE -ne 0) { throw 'Project dependency preparation failed.' }
    }
    & $pythonExe -c "import fastapi,uvicorn,sqlalchemy,httpx,passlib,bcrypt,email_validator,multipart; assert bcrypt.__version__ == '4.0.1', 'Run setup_my_campus.bat to install compatible dependencies'"
    if ($LASTEXITCODE -ne 0) { throw 'Dependency validation failed. Run setup_my_campus.bat.' }
    Write-Host "Python: $pythonExe"
    Push-Location $backendRoot
    try {
        $expectedInstance = & $pythonExe -c 'from app.services.runtime_info import INSTANCE_ID; print(INSTANCE_ID)'
        if ($LASTEXITCODE -ne 0) { throw 'Could not determine project/database identity.' }
        $expectedInstance = $expectedInstance.Trim()
    } finally { Pop-Location }
    if (-not $ValidateOnly) {
        & $pythonExe -X utf8 (Join-Path $projectRoot 'setup_demo.py')
        if ($LASTEXITCODE -ne 0) { throw 'Safe initialization failed. Servers have not been started.' }
    }
    $backendRunning = Get-CampusService 8000 'backend'
    $frontendRunning = Get-CampusService 5500 'frontend'
    if ($ValidateOnly) { Write-Host 'Launcher prerequisites and existing service content validated.'; exit 0 }
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
