#!/usr/bin/env bash
# Script para Linux/macOS: construye un ejecutable onefile con PyInstaller
set -e
python3 -m pip install --user -r ./requirements.txt
python3 -m pip install --upgrade pyinstaller

# limpiar
rm -rf build dist tetrix.spec

# construir
pyinstaller --onefile --name tetrix tetrix.py

echo "Build terminado. Revisa dist/tetrix (o dist/tetrix.exe en Windows)"
