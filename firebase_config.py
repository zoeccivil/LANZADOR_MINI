#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Firebase Configuration Manager
Estructura preparada para integración futura con Firebase.
Por ahora, simula la conexión y carga de datos.
"""

import time
from typing import Dict, List, Optional


class FirebaseManager:
    """
    Administrador de Firebase para el launcher.
    Actualmente simula la conexión y métodos de Firebase.
    """
    
    def __init__(self):
        self.connected = False
        self.user_data = None
        self.offline_mode = False
    
    def connect(self) -> bool:
        """
        Simula la conexión a Firebase.
        
        Returns:
            bool: True si la conexión fue exitosa, False en caso contrario
        """
        try:
            # Simular tiempo de conexión
            time.sleep(0.5)
            self.connected = True
            return True
        except Exception as e:
            print(f"Error al conectar con Firebase: {e}")
            self.offline_mode = True
            return False
    
    def load_user_data(self, user_id: Optional[str] = "default_user") -> Dict:
        """
        Simula la carga de datos del usuario desde Firebase.
        
        Args:
            user_id: ID del usuario (opcional, por defecto "default_user")
            
        Returns:
            Dict: Datos del usuario
        """
        try:
            # Simular tiempo de carga
            time.sleep(0.5)
            
            # Datos simulados del usuario
            self.user_data = {
                "user_id": user_id,
                "name": "Usuario Demo",
                "email": "demo@zoec.com",
                "permissions": {
                    "progain": True,
                    "equipos": True,
                    "facturas": True,
                    "facturas_emp": True,
                    "licitaciones": True,
                    "facot": True,
                    "documentos": True,
                    "ajustes": True
                },
                "theme": "modern",
                "last_login": time.time()
            }
            
            return self.user_data
        except Exception as e:
            print(f"Error al cargar datos del usuario: {e}")
            return {}
    
    def get_app_permissions(self, user_id: Optional[str] = None) -> Dict[str, bool]:
        """
        Obtiene los permisos de aplicaciones para un usuario.
        
        Args:
            user_id: ID del usuario (opcional)
            
        Returns:
            Dict[str, bool]: Diccionario con permisos de cada aplicación
        """
        if self.user_data and "permissions" in self.user_data:
            return self.user_data["permissions"]
        
        # Permisos por defecto si no hay datos cargados
        return {
            "progain": True,
            "equipos": True,
            "facturas": True,
            "facturas_emp": True,
            "licitaciones": True,
            "facot": True,
            "documentos": True,
            "ajustes": True
        }
    
    def is_offline(self) -> bool:
        """
        Verifica si está en modo offline.
        
        Returns:
            bool: True si está en modo offline
        """
        return self.offline_mode
    
    def disconnect(self):
        """Desconecta de Firebase."""
        self.connected = False
        self.user_data = None
