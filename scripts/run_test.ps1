param(
    [Parameter(Mandatory = $true)][ValidateSet("no-lb", "lb-2-api")][string]$Mode,
    [Parameter(Mandatory = $true)][ValidateSet(100, 1000, 10000)][int]$Users,
    [Parameter(Mandatory = $true)][ValidateSet("1kb", "10kb", "1mb", "10mb", "100mb")][string]$FileSize,
    [int]$SpawnRate = 100,
    [int]$DurationSeconds = 300,
    [string]$ResultsRoot = "results"
)
$ErrorActionPreference = "Stop"
$target = if ($Mode -eq "no-lb") { "http://127.0.0.1:8001" } else { "http://127.0.0.1:8081" }
$ports = if ($Mode -eq "no-lb") { "8001" } else { "8001,8002,8081" }
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$runDir = Join-Path $ResultsRoot "$Mode-$FileSize-$Users-$stamp"
New-Item -ItemType Directory -Path $runDir -Force | Out-Null
$metadata = [ordered]@{ mode = $Mode; target = $target; users = $Users; spawn_rate = $SpawnRate; file_size = $FileSize; duration_seconds = $DurationSeconds; started_at = (Get-Date).ToString("o") }
$metadata | ConvertTo-Json | Set-Content -Path (Join-Path $runDir "metadata.json") -Encoding utf8
Invoke-WebRequest -Uri "$target/" -UseBasicParsing | Out-Null
$env:FILE_SIZE = $FileSize
$collector = Start-Process -FilePath "python" -ArgumentList @("scripts/collect_resources.py", "--ports", $ports, "--duration", $DurationSeconds, "--output", (Join-Path $runDir "resources.csv")) -PassThru -NoNewWindow
try { locust --headless --host $target --users $Users --spawn-rate $SpawnRate --run-time "$DurationSeconds`s" --csv (Join-Path $runDir "locust") --html (Join-Path $runDir "locust-report.html") }
finally { if (-not $collector.HasExited) { $collector.WaitForExit(15000) | Out-Null } }
python scripts/summarize_result.py --stats (Join-Path $runDir "locust_stats.csv") --resources (Join-Path $runDir "resources.csv") --metadata (Join-Path $runDir "metadata.json") --output (Join-Path $runDir "summary.csv")
Write-Host "Completed. Summary: $runDir\summary.csv"