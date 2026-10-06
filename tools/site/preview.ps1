# Local preview of the alargov.com site (course/site) at http://localhost:8080
# Usage: powershell -File tools/site/preview.ps1 [-Port 8080] [-Staging]
#   -Staging  shows the site the way the staging service renders it (noindex + ribbon), without touching the files.
param([int]$Port = 8080, [switch]$Staging)

$ErrorActionPreference = 'Stop'
$root = Resolve-Path (Join-Path $PSScriptRoot '..\..\course\site')
$branch = (git -C $root rev-parse --abbrev-ref HEAD) 2>$null
Write-Host "Site: $root"
Write-Host "Branch: $branch"

$serveDir = $root
if ($Staging) {
  $serveDir = Join-Path $env:TEMP 'alargov-staging-preview'
  if (Test-Path $serveDir) { Remove-Item $serveDir -Recurse -Force }
  Copy-Item $root $serveDir -Recurse
  Get-ChildItem $serveDir -Recurse -Filter *.html | ForEach-Object {
    $c = Get-Content $_.FullName -Raw -Encoding UTF8
    $c = $c.Replace('<head>', '<head><meta name="robots" content="noindex,nofollow">')
    $c = $c.Replace('</body>', '<div style="position:fixed;bottom:12px;left:12px;z-index:9999;background:#f0a94a;color:#0a1428;font:600 12px/1 sans-serif;padding:6px 10px;border-radius:6px">STAGING · ' + $branch + '</div></body>')
    Set-Content $_.FullName $c -Encoding UTF8
  }
}

Start-Process "http://localhost:$Port/"
npx --yes http-server $serveDir -p $Port -c-1
