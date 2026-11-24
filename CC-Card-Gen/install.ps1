# Install the anki-deck skill as a personal Claude Code skill, plus its Python dependencies.
#
#   powershell -ExecutionPolicy Bypass -File install.ps1             # skill + deps
#   powershell -ExecutionPolicy Bypass -File install.ps1 -SkipDeps   # skill only
#   ... -Target D:\somewhere\skills                                  # custom skills folder
param(
    [string]$Target = (Join-Path $HOME ".claude\skills"),
    [switch]$SkipDeps
)
$ErrorActionPreference = "Stop"

$src = Join-Path $PSScriptRoot "skills\anki-deck"
$dest = Join-Path $Target "anki-deck"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Get-ChildItem -Path $src -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($src.Length).TrimStart('\', '/')
    $out = Join-Path $dest $rel
    New-Item -ItemType Directory -Force -Path (Split-Path $out -Parent) | Out-Null
    Copy-Item -Path $_.FullName -Destination $out -Force
}
Write-Host "Installed skill -> $dest"

if ($SkipDeps) { return }

$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $py) {
    Write-Error "Python 3.9+ was not found. Install it, then rerun this script (or run the pip commands in README.md)."
}
Write-Host "Installing Python dependencies with $($py.Source) ..."
& $py.Source -m pip install --upgrade pymupdf chevron frozendict cached-property
# genanki's pyyaml dependency often fails to build on new Python versions and isn't needed
# here (build_deck.py stubs it), so install genanki without dependencies.
& $py.Source -m pip install --upgrade --no-deps genanki
Write-Host "Done. In Claude Code, run: /anki-deck <path-to-lecture-folder> depth=exam"
