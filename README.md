# Tetrix — Juego clásico recreado en Python

## Presentación

Tetrix es una implementación sencilla y entretenida del clásico juego de piezas (Tetris) creada como ejercicio práctico en Python usando Tkinter. Está pensada para ser fácil de jugar, fácil de construir y para demostrar buenas prácticas básicas: manejo de eventos, lógica de juego, GUI y empaquetado con PyInstaller.

Este repositorio contiene el código fuente en `tetrix.py`, scripts de construcción y un ejecutable Windows ya generado (`dist/tetrix.exe`).

## Breve historia

Tetris fue inventado por Alexey Pajitnov en 1984 en la Unión Soviética. Desde entonces ha sido uno de los videojuegos más populares y ha inspirado infinidad de variantes y clones. "Tetrix" en este repositorio es una versión didáctica que respeta la mecánica clásica: piezas (tetrominos), rotaciones, limpieza de líneas y progresión por niveles.

## Por qué este proyecto

Trabajar en un juego simple como Tetrix es una forma divertida y práctica de mejorar habilidades en Python. Permite practicar estructuras de datos, temporización, entradas de usuario (teclado y mouse), y despliegue multiplataforma. Además es un buen ejemplo para aprender a crear binarios con PyInstaller y preparar builds automáticos.

## Estado actual del repositorio

- Código fuente: `tetrix.py` (juego completo en Tkinter).
- Ejecutable Windows (ya generado): `dist/tetrix.exe` (prueba local disponible).
- Scripts de build:
  - `build_windows.ps1` — PowerShell helper para construir `tetrix.exe` con PyInstaller en Windows.
  - `build_unix.sh` — Bash helper para construir con PyInstaller en Linux/macOS (ejecutar en el sistema objetivo).
- Dependencias para build: `requirements.txt` (incluye PyInstaller).

## Licencia y distribución

Este repositorio se mantiene público para facilitar la descarga del juego y la revisión, pero el código NO está disponible para reutilización sin permiso explícito. Es decir:

- Puedes descargar y ejecutar los binarios disponibles (o construidos por ti) para uso personal.
- No se permite reutilizar, copiar o redistribuir el código fuente sin contactar y obtener permiso del autor.

Esta nota no reemplaza asesoría legal; si necesitas un texto de licencia formal, contacta al autor.

## Ejecutar el juego (usuarios finales)

Si sólo quieres jugar, puedes usar los binarios precompilados o ejecutar el script directamente si tienes Python.

### Windows (ejecutable descargado)

```powershell
# Ejecuta el binario precompilado en dist\tetrix.exe
.\dist\tetrix.exe
```

### Windows (ejecutar desde fuente)

```powershell
# Crear y activar un entorno virtual recomendado
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependencias (opcional, sólo para desarrollo)
python -m pip install --upgrade pip
pip install -r requirements.txt

# Ejecutar el juego desde el código fuente
python .\tetrix.py
```

### Linux (ejecutable)

```bash
# Si tienes un ejecutable proporcionado (por ejemplo dist/tetrix)
./dist/tetrix
# Si no, y quieres ejecutar desde fuente:
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python3 tetrix.py
```

### macOS (ejecutable)

```bash
# Si existe un binario nativo generado en macOS, normalmente será un bundle .app o un binario en dist/
# Ejecuta desde Finder o la terminal:
open dist/tetrix.app || ./dist/tetrix

# Ejecutar desde fuente (desarrollo)
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python3 tetrix.py
```

## Cómo construir los ejecutables (para desarrolladores)

Recomendación: crear un entorno virtual antes de instalar dependencias para aislar el build.

### Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
# Ejecutar el helper incluido
.\build_windows.ps1
# Resultado: dist\tetrix.exe
```

### Linux / macOS (bash):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
# Ejecutar el helper incluido
./build_unix.sh
# Resultado: dist/tetrix (o dist/tetrix on linux, en mac puede crear dist/tetrix o un bundle)
```

## Notas sobre builds multiplataforma

- PyInstaller debe ejecutarse en la plataforma de destino para generar binarios nativos confiables: usa `windows-latest`, `ubuntu-latest` y `macos-latest` en CI para builds automáticos.
- El script `build_unix.sh` es el helper para sistemas Unix-like; si lo ejecutas en Windows bajo WSL puede funcionar, pero para macOS preferible usar runner macOS o un mac real.
- Para publicar los binarios públicamente y que los usuarios los descarguen fácilmente, recomendamos usar GitHub Releases. En CI puedes generar los artefactos y adjuntarlos automáticamente a un Release cuando crees una etiqueta (`v1.0.0`, por ejemplo).

## Checksums y verificación

Es buena práctica publicar una suma SHA256 junto al binario para que los usuarios verifiquen la descarga. Ejemplo de cómo generar una suma:

```bash
# Linux/macOS
sha256sum dist/tetrix > dist/tetrix.sha256
# Windows (PowerShell)
Get-FileHash .\dist\tetrix.exe -Algorithm SHA256 | Format-List
```

## Firma y notarización

- Windows: la firma de código reduce advertencias SmartScreen; requiere un certificado (pfx) y `signtool`. Se puede integrar en CI usando secretos.
- macOS: notarización y firma requieren cuenta de desarrollador Apple; la notarización es necesaria para evitar advertencias de Gatekeeper.

## Distribución y canales recomendados

- GitHub Releases: centraliza assets por versión y es gratuito. Recomendado como primer canal.
- itch.io: buena opción para juegos — permite página con imágenes, descripciones, y descarga para usuarios menos técnicos.

## Siguientes pasos sugeridos

1. Si quieres, adapto un workflow de GitHub Actions para generar binarios automáticamente en las 3 plataformas y publicar un Release draft con los assets.
2. Si necesitas firmado/notarización, prepara los certificados y los secretos de repo (no puedo generarlos por ti).
3. Si quieres una página de itch.io, puedo preparar instrucciones para subir manualmente o con la API.

## Contacto y créditos

Desarrollado por: Daniel Mardones
Si necesitas permiso para usar el código o distribuirlo de forma distinta, contacta al autor.

-----
Archivo actualizado automáticamente para incluir instrucciones de uso, build y distribución.

