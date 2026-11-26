#Requires -Version 5.1
<#
.SYNOPSIS
  Prints how to open a project folder the right way, then optionally opens VS Code there.
.PARAMETER Path
  Folder to open. Defaults to the current directory.
.PARAMETER NoLaunch
  Only print the commands; do not start VS Code.
#>
[CmdletBinding()]
param(
    [string]$Path = (Get-Location).Path,
    [switch]$NoLaunch
)

$ErrorActionPreference = 'Stop'

$rootMarkers = @('.git', 'AGENTS.md', 'package.json', 'pyproject.toml', 'main.py', '.claude')
$resolved = Resolve-Path -LiteralPath $Path -ErrorAction SilentlyContinue

if (-not $resolved) {
    Write-Host ("Folder not found: {0}" -f $Path) -ForegroundColor Red
    exit 1
}

$fullPath = $resolved.Path

$found = @()
foreach ($marker in $rootMarkers) {
    if (Test-Path -LiteralPath (Join-Path $fullPath $marker)) { $found += $marker }
}

Write-Host ("folder: {0}" -f $fullPath) -ForegroundColor Cyan

if ($found.Count -eq 0) {
    Write-Host '  [WARN] No project root marker found here.' -ForegroundColor Yellow
    Write-Host '         You are probably inside a subfolder. Project skills load only from the real root.'
} else {
    Write-Host ("  root markers: {0}" -f ($found -join ', ')) -ForegroundColor Green
}

$skillsDir = Join-Path $fullPath '.claude\skills'
if (Test-Path -LiteralPath $skillsDir -PathType Container) {
    $names = @(Get-ChildItem -LiteralPath $skillsDir -Directory -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name)
    if ($names.Count -gt 0) {
        Write-Host ("  project skills: {0}" -f ($names -join ', ')) -ForegroundColor Green
    } else {
        Write-Host '  project skills: folder exists but is empty' -ForegroundColor DarkGray
    }
} else {
    Write-Host '  project skills: none (personal skills still apply)' -ForegroundColor DarkGray
}

Write-Host ''
Write-Host 'open it with:' -ForegroundColor Cyan
Write-Host ("  cd /d `"{0}`"" -f $fullPath)

if ($NoLaunch) { exit 0 }

$code = Get-Command code -ErrorAction SilentlyContinue
if ($code) {
    Write-Host '  code -r .'
    Write-Host ''
    Write-Host 'launching VS Code at that root...' -ForegroundColor Cyan
    & $code.Source -r $fullPath
} else {
    Write-Host '  (the "code" command is not on PATH, so VS Code was not launched)' -ForegroundColor Yellow
    Write-Host '  Use File > Open Folder... with the path above.'
}

exit 0
