#!/usr/bin/env bash
# Genera checksums SHA256 recursivamente para todos los archivos dentro del directorio indicado
# Uso: ./scripts/gen_checksums.sh dist
set -e
if [ -z "$1" ]; then
  echo "Uso: $0 <directorio>"
  exit 1
fi
TARGET_DIR="$1"
OUT_FILE="$TARGET_DIR/checksums.sha256"

if [ ! -d "$TARGET_DIR" ]; then
  echo "Directorio no existe: $TARGET_DIR"
  exit 2
fi

# Generar checksums
find "$TARGET_DIR" -type f -exec sha256sum {} \; > "$OUT_FILE"
echo "Checksums guardados en: $OUT_FILE"
