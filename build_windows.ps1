# PowerShell script para construir tetrix.exe usando PyInstaller
# Ejecutar en PowerShell (no en el ISE) con permisos suficientes.

python -m pip install --upgrade pip
python -m pip install --user -r .\requirements.txt
python -m pip install --upgrade pyinstaller

# Limpiar builds previos
if (Test-Path .\build) { Remove-Item -Recurse -Force .\build }
if (Test-Path .\dist) { Remove-Item -Recurse -Force .\dist }
if (Test-Path .\tetrix.spec) { Remove-Item -Force .\tetrix.spec }

# Construir ejecutable en modo ventana (--noconsole)
pyinstaller --noconsole --onefile --name tetrix tetrix.py

Write-Host "Build terminado. Revisa la carpeta dist\tetrix.exe"
