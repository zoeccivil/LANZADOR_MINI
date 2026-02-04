#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZOEC Launcher - Diseño Moderno Profesional
Launcher rediseñado con interfaz minimalista y moderna.
"""

import sys
import os
import subprocess
from PyQt6 import QtCore, QtGui, QtWidgets

# Configuración de aplicaciones
APPS_CONFIG = [
    {"name": "Equipos", "exe": "equipos.exe", "icon": "motorcycle"},
    {"name": "Contabilidad", "exe": "contabilidad.exe", "icon": "account_balance"},
    {"name": "RRHH", "exe": "rrhh.exe", "icon": "groups"},
    {"name": "Taller", "exe": "taller.exe", "icon": "build"},
    {"name": "Inventario", "exe": "inventario.exe", "icon": "inventory_2"},
    {"name": "GPS", "exe": "gps.exe", "icon": "location_on"},
    {"name": "Archivos", "exe": "archivos.exe", "icon": "monitor"},
    {"name": "Ajustes", "exe": "ajustes.exe", "icon": "settings"},
    {"name": "Salir", "exe": None, "icon": "power_settings_new"}
]

# Paleta de colores
COLORS = {
    "background": "#F3F4F6",
    "button_bg": "#FFFFFF",
    "header": "#1F2937",
    "text_primary": "#1E40AF",
    "text_secondary": "#6B7280",
    "accent_hover": "#3B82F6",
    "footer_bg": "#F9FAFB",
    "exit_button": "#EF4444"
}


class LauncherBtn(QtWidgets.QPushButton):
    """Botón del launcher con diseño moderno."""
    
    def __init__(self, app_config, parent=None):
        super().__init__(parent)
        self.app_config = app_config
        self.is_exit_btn = app_config["name"] == "Salir"
        
        self._setup_ui()
        self._setup_style()
    
    def _setup_ui(self):
        """Configura la interfaz del botón."""
        self.setFixedSize(110, 110)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        
        # Layout vertical
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(8)
        
        # Icono
        icon_label = QtWidgets.QLabel()
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # Crear icono usando Material Icons (simulado con texto/forma)
        icon_pixmap = self._create_icon(self.app_config["icon"])
        icon_label.setPixmap(icon_pixmap)
        
        # Texto
        text_label = QtWidgets.QLabel(self.app_config["name"])
        text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        text_label.setWordWrap(True)
        
        # Estilo del texto
        text_color = COLORS["exit_button"] if self.is_exit_btn else COLORS["text_primary"]
        text_label.setStyleSheet(f"""
            QLabel {{
                color: {text_color};
                font-family: 'Segoe UI';
                font-size: 11px;
                font-weight: 600;
                background: transparent;
            }}
        """)
        
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
    
    def _create_icon(self, icon_name):
        """Crea un icono simple basado en el nombre."""
        pixmap = QtGui.QPixmap(40, 40)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        # Color del icono
        icon_color = COLORS["exit_button"] if self.is_exit_btn else COLORS["text_secondary"]
        painter.setPen(QtGui.QPen(QtGui.QColor(icon_color), 2.5))
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        # Dibujar diferentes formas según el tipo de icono
        if icon_name == "motorcycle":
            # Vehículo/Moto - círculos para ruedas
            painter.drawEllipse(5, 20, 10, 10)
            painter.drawEllipse(25, 20, 10, 10)
            painter.drawLine(10, 25, 30, 25)
            painter.drawLine(20, 10, 20, 25)
        elif icon_name == "account_balance":
            # Edificio/Banco
            painter.drawRect(10, 8, 20, 25)
            painter.drawLine(8, 8, 32, 8)
            painter.drawLine(12, 12, 12, 28)
            painter.drawLine(18, 12, 18, 28)
            painter.drawLine(24, 12, 24, 28)
            painter.drawLine(8, 33, 32, 33)
        elif icon_name == "groups":
            # Grupo de personas
            painter.drawEllipse(8, 8, 8, 8)
            painter.drawEllipse(24, 8, 8, 8)
            painter.drawArc(6, 16, 12, 12, 0, 180 * 16)
            painter.drawArc(22, 16, 12, 12, 0, 180 * 16)
        elif icon_name == "build":
            # Llave inglesa
            painter.drawLine(15, 8, 25, 18)
            painter.drawLine(15, 8, 12, 11)
            painter.drawLine(25, 18, 28, 15)
            painter.drawRect(20, 22, 8, 10)
        elif icon_name == "inventory_2":
            # Caja/Contenedor
            painter.drawRect(8, 12, 24, 20)
            painter.drawLine(8, 12, 20, 5)
            painter.drawLine(32, 12, 20, 5)
            painter.drawLine(20, 5, 20, 32)
        elif icon_name == "location_on":
            # Pin de ubicación
            painter.drawEllipse(15, 8, 10, 10)
            painter.drawLine(20, 18, 20, 32)
            painter.drawLine(20, 32, 16, 28)
            painter.drawLine(20, 32, 24, 28)
        elif icon_name == "monitor":
            # Monitor/Pantalla
            painter.drawRect(8, 8, 24, 18)
            painter.drawLine(20, 26, 20, 30)
            painter.drawLine(12, 30, 28, 30)
        elif icon_name == "settings":
            # Engranaje
            painter.drawEllipse(14, 14, 12, 12)
            for i in range(8):
                angle = i * 45
                painter.save()
                painter.translate(20, 20)
                painter.rotate(angle)
                painter.drawRect(-2, -12, 4, 5)
                painter.restore()
        elif icon_name == "power_settings_new":
            # Botón de power
            painter.setPen(QtGui.QPen(QtGui.QColor(COLORS["exit_button"]), 3))
            painter.drawArc(10, 12, 20, 20, 30 * 16, 300 * 16)
            painter.drawLine(20, 8, 20, 20)
        
        painter.end()
        return pixmap
    
    def _setup_style(self):
        """Configura el estilo del botón."""
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS["button_bg"]};
                border: 2px solid transparent;
                border-radius: 8px;
                padding: 8px;
            }}
            QPushButton:hover {{
                border: 2px solid {COLORS["accent_hover"]};
            }}
            QPushButton:pressed {{
                background-color: #F9FAFB;
            }}
        """)
        
        # Sombra suave
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QtGui.QColor(0, 0, 0, 25))
        self.setGraphicsEffect(shadow)


class LauncherWindow(QtWidgets.QWidget):
    """Ventana principal del launcher con diseño moderno."""
    
    def __init__(self, firebase_manager=None):
        super().__init__()
        self.firebase_manager = firebase_manager
        self.drag_position = None
        self._setup_window()
        self._setup_ui()
    
    def _setup_window(self):
        """Configura las propiedades de la ventana."""
        self.setWindowTitle("ZOEC Launcher")
        self.setFixedSize(380, 450)
        
        # Ventana sin bordes del sistema
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        
        # Centrar en pantalla
        self._center_on_screen()
        
        # Color de fondo
        self.setStyleSheet(f"background-color: {COLORS['background']};")
    
    def _center_on_screen(self):
        """Centra la ventana en la pantalla."""
        screen = QtWidgets.QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.geometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)
    
    def _setup_ui(self):
        """Configura la interfaz del launcher."""
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Grid de botones
        grid_container = QtWidgets.QWidget()
        grid_container.setStyleSheet(f"background-color: {COLORS['background']};")
        grid_layout = QtWidgets.QGridLayout(grid_container)
        grid_layout.setContentsMargins(15, 15, 15, 15)
        grid_layout.setSpacing(12)
        
        # Agregar botones en grid 3x3
        row = 0
        col = 0
        for app_config in APPS_CONFIG:
            btn = LauncherBtn(app_config, self)
            btn.clicked.connect(lambda checked, ac=app_config: self._on_app_clicked(ac))
            grid_layout.addWidget(btn, row, col)
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        main_layout.addWidget(grid_container, 1)
        
        # Footer
        footer = self._create_footer()
        main_layout.addWidget(footer)
    
    def _create_header(self):
        """Crea el header minimalista."""
        header = QtWidgets.QWidget()
        header.setFixedHeight(45)
        header.setStyleSheet(f"background-color: {COLORS['header']};")
        
        layout = QtWidgets.QHBoxLayout(header)
        layout.setContentsMargins(15, 0, 10, 0)
        
        # Título
        title = QtWidgets.QLabel("● ZOEC LAUNCHER")
        title.setStyleSheet(f"""
            QLabel {{
                color: #FFFFFF;
                font-family: 'Segoe UI';
                font-size: 13px;
                font-weight: 600;
            }}
        """)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Botón de cerrar
        close_btn = QtWidgets.QPushButton("✕")
        close_btn.setFixedSize(35, 35)
        close_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #9CA3AF;
                border: none;
                border-radius: 4px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #EF4444;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        return header
    
    def _create_footer(self):
        """Crea el footer minimalista."""
        footer = QtWidgets.QWidget()
        footer.setFixedHeight(30)
        footer.setStyleSheet(f"background-color: {COLORS['footer_bg']};")
        
        layout = QtWidgets.QHBoxLayout(footer)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # Estado
        status = QtWidgets.QLabel("Sistema listo")
        status.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_secondary']};
                font-family: 'Segoe UI';
                font-size: 9px;
            }}
        """)
        layout.addWidget(status)
        
        layout.addStretch()
        
        # Versión
        version = QtWidgets.QLabel("v2.0")
        version.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_secondary']};
                font-family: 'Segoe UI';
                font-size: 9px;
            }}
        """)
        layout.addWidget(version)
        
        return footer
    
    def _on_app_clicked(self, app_config):
        """Maneja el clic en un botón de aplicación."""
        if app_config["name"] == "Salir":
            self.close()
            return
        
        exe_name = app_config["exe"]
        if exe_name:
            self._launch_program(exe_name)
    
    def _launch_program(self, exe_name):
        """Lanza un programa externo."""
        try:
            # Asegurar la ruta
            if not os.path.isabs(exe_name):
                path = os.path.join(os.getcwd(), exe_name)
            else:
                path = exe_name
            
            # Intentar lanzar el programa
            subprocess.Popen([path], shell=False)
            
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(
                self,
                "No encontrado",
                f"No se encontró: {exe_name}"
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Error",
                f"Error al lanzar {exe_name}:\n{e}"
            )
    
    def mousePressEvent(self, event):
        """Permite mover la ventana arrastrando."""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Mueve la ventana cuando se arrastra."""
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
