#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Entry Point - ZOEC Launcher
Punto de entrada principal que muestra primero el loader y luego el launcher.
"""

import sys
from PyQt6 import QtWidgets
from loader import LoaderWindow
from launcher import LauncherWindow


def main():
    """Función principal de la aplicación."""
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Crear ventana de carga
    loader = LoaderWindow()
    
    # Variable para almacenar el launcher
    launcher = None
    
    def on_loading_complete():
        """Callback cuando la carga se completa."""
        nonlocal launcher
        
        # Obtener el FirebaseManager del loader
        firebase_manager = loader.get_firebase_manager()
        
        # Crear y mostrar el launcher
        launcher = LauncherWindow(firebase_manager)
        launcher.show()
        
        # Cerrar el loader
        loader.close()
    
    # Conectar señal de carga completa
    loader.loading_complete.connect(on_loading_complete)
    
    # Mostrar loader e iniciar carga
    loader.show()
    loader.start_loading()
    
    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
