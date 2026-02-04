import PyInstaller.__main__
import os
import sys

# --- CONFIGURACIÓN ---
APP_NAME = "lanzador_programas"
MAIN_SCRIPT = "main.py"  # Usamos main.py como entrada ya que tu código usa un loader previo
ICONS_DIR = "icons"
# Ruta específica del icono del ejecutable
EXE_ICON_PATH = r"D:\Dropbox\PROGAIN\icons\icon_programa-00.ico"

def build_exe():
    print(f"🚀 Generando: {APP_NAME}.exe")
    
    # Validaciones básicas
    if not os.path.exists(MAIN_SCRIPT):
        print(f"❌ Error: No se encuentra {MAIN_SCRIPT}")
        return
        
    sep = ';' if sys.platform == 'win32' else ':'

    # Argumentos PyInstaller
    args = [
        MAIN_SCRIPT,
        f'--name={APP_NAME}',
        '--noconsole',
        '--onefile',
        '--clean',
        
        # Incluir carpeta de iconos SVG dentro del exe
        f'--add-data={ICONS_DIR}{sep}{ICONS_DIR}',
        
        # Imports necesarios para SVG y Firebase
        '--hidden-import=PyQt6.QtSvg',
        '--hidden-import=firebase_admin',
        
        # Icono del .exe
        f'--icon={EXE_ICON_PATH}'
    ]
    
    try:
        PyInstaller.__main__.run(args)
        print(f"\n✅ ¡ÉXITO! Ejecutable creado en la carpeta /dist")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    build_exe()