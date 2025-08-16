<#
Genera checksums SHA256 para todos los archivos en un directorio dado.
Uso: .\scripts\gen_checksums.ps1 -Path .\dist
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$Path
)

if (-not (Test-Path $Path)) {
    Write-Error "Directorio no existe: $Path"
    exit 1
}

$Out = Join-Path $Path "checksums.sha256"
Get-ChildItem -Recurse -File -Path $Path | ForEach-Object {
    $hash = Get-FileHash -Algorithm SHA256 -Path $_.FullName
    "{0}  {1}" -f $hash.Hash, $_.FullName
} | Out-File -Encoding utf8 $Out

Write-Host "Checksums guardados en: $Out"
