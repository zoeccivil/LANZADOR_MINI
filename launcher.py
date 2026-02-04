#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher Window - Ventana principal del launcher moderno
Launcher minimalista con diseño profesional y grid 3x3.
"""

import sys
import os
import subprocess
import math
from PyQt6 import QtCore, QtGui, QtWidgets
from firebase_config import FirebaseManager


# Configuración de aplicaciones
APPS_CONFIG = [
    {"name": "PROGAIN", "exe": "progain_app.exe", "icon": "construction"},
    {"name": "EQUIPOS", "exe": "alquiler_equipos.exe", "icon": "truck"},
    {"name": "FACTURAS", "exe": "gestion_facturas.exe", "icon": "receipt"},
    {"name": "FACTURAS EMP", "exe": "facturacion_gui.exe", "icon": "business"},
    {"name": "LICITACIONES", "exe": "gestor_licitaciones_db.exe", "icon": "gavel"},
    {"name": "FA-COT", "exe": "facot.exe", "icon": "calculator"},
    {"name": "DOCUMENTOS", "exe": "explorer.exe", "icon": "folder"},
    {"name": "AJUSTES", "exe": "config.exe", "icon": "settings"},
    {"name": "SALIR", "exe": None, "icon": "power_settings_new"}
]


class AppButton(QtWidgets.QWidget):
    """Botón individual de aplicación con icono y etiqueta."""
    
    clicked = QtCore.pyqtSignal(str, str)  # name, exe
    
    def __init__(self, name, exe, icon_name, parent=None):
        super().__init__(parent)
        self.name = name
        self.exe = exe
        self.icon_name = icon_name
        self.is_exit_button = (exe is None)
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz del botón."""
        self.setFixedSize(110, 110)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        
        # Layout vertical
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Crear icono
        icon_label = QtWidgets.QLabel()
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        icon_pixmap = self._create_icon(self.icon_name)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setObjectName("icon_label")
        
        # Etiqueta de texto
        text_label = QtWidgets.QLabel(self.name)
        text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        text_label.setWordWrap(True)
        text_label.setObjectName("text_label")
        
        layout.addWidget(icon_label, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(text_label, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()
        
        # Estilo del botón
        if self.is_exit_button:
            # Botón de salir con estilo especial
            self.setStyleSheet("""
                AppButton {
                    background-color: #FFFFFF;
                    border-radius: 8px;
                    border: 1px solid #E5E7EB;
                }
                AppButton:hover {
                    background-color: #FEE2E2;
                    border: 1px solid #EF4444;
                }
                QLabel#text_label {
                    color: #EF4444;
                    font-family: 'Segoe UI';
                    font-size: 11px;
                    font-weight: 600;
                    background: transparent;
                }
            """)
        else:
            self.setStyleSheet("""
                AppButton {
                    background-color: #FFFFFF;
                    border-radius: 8px;
                    border: 1px solid #E5E7EB;
                }
                AppButton:hover {
                    background-color: #EFF6FF;
                    border: 1px solid #3B82F6;
                }
                QLabel#text_label {
                    color: #1F2937;
                    font-family: 'Segoe UI';
                    font-size: 11px;
                    font-weight: 600;
                    background: transparent;
                }
            """)
    
    def _create_icon(self, icon_name):
        """
        Crea un icono usando QPainter.
        
        Args:
            icon_name: Nombre del icono a dibujar
            
        Returns:
            QPixmap: Icono dibujado
        """
        pixmap = QtGui.QPixmap(40, 40)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        # Color del icono
        if self.is_exit_button:
            color = QtGui.QColor("#EF4444")  # Rojo para salir
        else:
            color = QtGui.QColor("#6B7280")  # Gris para otros
        
        pen = QtGui.QPen(color)
        pen.setWidth(2)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(QtCore.Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        
        # Dibujar icono según el nombre
        if icon_name == "construction":
            # Casco de construcción
            painter.drawArc(8, 10, 24, 20, 0, 180 * 16)  # Casco (arco superior)
            painter.drawLine(8, 20, 32, 20)  # Borde del casco
            painter.drawLine(20, 10, 20, 20)  # Línea vertical centro
            # Estructura/grúa
            painter.drawLine(28, 12, 35, 8)  # Brazo de grúa
            painter.drawLine(28, 12, 32, 16)  # Cable
            
        elif icon_name == "truck":
            # Camión/vehículo pesado
            # Cabina
            painter.drawRect(8, 15, 12, 12)
            # Compartimento de carga
            painter.drawRect(20, 12, 15, 15)
            # Ruedas
            painter.drawEllipse(11, 27, 6, 6)
            painter.drawEllipse(26, 27, 6, 6)
            # Ventana de cabina
            painter.drawLine(10, 17, 18, 17)
            
        elif icon_name == "receipt":
            # Documento tipo factura
            painter.drawRect(10, 6, 20, 28)  # Rectángulo del documento
            # Líneas horizontales (texto)
            painter.drawLine(13, 11, 27, 11)
            painter.drawLine(13, 15, 27, 15)
            painter.drawLine(13, 19, 27, 19)
            painter.drawLine(13, 23, 20, 23)
            # Símbolo de moneda
            painter.drawText(22, 28, "$")
            
        elif icon_name == "business":
            # Edificio de oficinas
            painter.drawRect(10, 8, 20, 28)  # Edificio principal
            # Ventanas en grid (3x4)
            for row in range(4):
                for col in range(3):
                    x = 13 + col * 6
                    y = 11 + row * 6
                    painter.drawRect(x, y, 3, 3)
            
        elif icon_name == "gavel":
            # Mazo de juez
            # Mango del mazo
            painter.drawLine(22, 15, 10, 27)
            # Cabeza del mazo
            painter.drawRect(20, 10, 10, 6)
            # Base/bloque
            painter.drawLine(8, 32, 25, 32)
            painter.drawLine(8, 34, 25, 34)
            
        elif icon_name == "calculator":
            # Calculadora
            painter.drawRect(10, 6, 20, 28)  # Cuerpo
            # Pantalla
            painter.drawRect(13, 9, 14, 5)
            # Botones en grid (3x4)
            for row in range(4):
                for col in range(3):
                    x = 13 + col * 5
                    y = 17 + row * 4
                    painter.drawRect(x, y, 3, 3)
            
        elif icon_name == "folder":
            # Carpeta abierta
            # Pestaña de carpeta
            painter.drawLine(8, 12, 18, 12)
            painter.drawLine(18, 12, 20, 14)
            # Cuerpo de la carpeta
            painter.drawRect(8, 14, 24, 16)
            # Papeles sobresaliendo
            painter.drawLine(15, 14, 15, 10)
            painter.drawLine(20, 14, 20, 11)
            painter.drawLine(25, 14, 25, 12)
            
        elif icon_name == "settings":
            # Engranaje
            # Círculo central
            painter.drawEllipse(15, 15, 10, 10)
            # Dientes del engranaje (8 dientes)
            for i in range(8):
                angle = i * 45
                rad = math.radians(angle)
                x1 = 20 + 10 * math.cos(rad)
                y1 = 20 + 10 * math.sin(rad)
                x2 = 20 + 13 * math.cos(rad)
                y2 = 20 + 13 * math.sin(rad)
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
            
        elif icon_name == "power_settings_new":
            # Botón de power
            # Círculo exterior
            painter.drawArc(10, 10, 20, 20, 45 * 16, 270 * 16)
            # Línea de power en el centro
            painter.drawLine(20, 8, 20, 20)
        
        painter.end()
        return pixmap
    
    def mousePressEvent(self, event):
        """Maneja el clic del botón."""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit(self.name, self.exe)


class LauncherWindow(QtWidgets.QWidget):
    """Ventana principal del launcher con grid 3x3."""
    
    def __init__(self, firebase_manager=None):
        super().__init__()
        self.firebase_manager = firebase_manager or FirebaseManager()
        self._setup_ui()
        self._create_buttons()
        self._dragging = False
        self._drag_position = QtCore.QPoint()
    
    def _setup_ui(self):
        """Configura la interfaz de la ventana."""
        # Ventana sin bordes
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Tamaño fijo
        self.setFixedSize(380, 450)
        
        # Centrar en pantalla
        self._center_on_screen()
        
        # Layout principal
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Container principal
        self.container = QtWidgets.QFrame()
        self.container.setStyleSheet("""
            QFrame {
                background-color: #F3F4F6;
                border-radius: 12px;
            }
        """)
        
        container_layout = QtWidgets.QVBoxLayout(self.container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)
        
        # Header
        header = self._create_header()
        container_layout.addWidget(header)
        
        # Grid de aplicaciones
        self.grid_widget = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(12)
        
        container_layout.addWidget(self.grid_widget)
        
        # Footer
        footer = self._create_footer()
        container_layout.addWidget(footer)
        
        main_layout.addWidget(self.container)
    
    def _create_header(self):
        """Crea el header de la ventana."""
        header = QtWidgets.QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                border-radius: 8px;
            }
        """)
        
        header_layout = QtWidgets.QHBoxLayout(header)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        # Título
        title = QtWidgets.QLabel("ZOEC LAUNCHER")
        title.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-family: 'Segoe UI';
                font-size: 18px;
                font-weight: 700;
                background: transparent;
            }
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Botón cerrar
        close_btn = QtWidgets.QPushButton("×")
        close_btn.setFixedSize(30, 30)
        close_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #FFFFFF;
                font-size: 24px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #EF4444;
            }
        """)
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn)
        
        return header
    
    def _create_footer(self):
        """Crea el footer de la ventana."""
        footer = QtWidgets.QLabel("© 2026 ZOEC Civil")
        footer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        footer.setFixedHeight(30)
        footer.setStyleSheet("""
            QLabel {
                color: #6B7280;
                font-family: 'Segoe UI';
                font-size: 10px;
                background: transparent;
            }
        """)
        return footer
    
    def _create_buttons(self):
        """Crea los botones de aplicaciones en el grid 3x3."""
        row = 0
        col = 0
        
        for app in APPS_CONFIG:
            button = AppButton(app["name"], app["exe"], app["icon"], self)
            button.clicked.connect(self._on_button_clicked)
            
            self.grid_layout.addWidget(
                button, row, col, 
                QtCore.Qt.AlignmentFlag.AlignCenter
            )
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
    
    def _on_button_clicked(self, name, exe):
        """
        Maneja el clic en un botón de aplicación.
        
        Args:
            name: Nombre de la aplicación
            exe: Ejecutable a lanzar
        """
        if exe is None:
            # Botón de salir
            self.close()
        else:
            # Lanzar programa
            self._launch_program(name, exe)
    
    def _find_executable(self, exe_name):
        """
        Busca un ejecutable en múltiples ubicaciones.
        
        Args:
            exe_name: Nombre del ejecutable a buscar
            
        Returns:
            str: Ruta absoluta del ejecutable o None
        """
        # Obtener directorio base
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Ubicaciones a buscar
        search_paths = [
            os.path.join(base_dir, exe_name),
            os.path.join(base_dir, "apps", exe_name),
            os.path.join(base_dir, "..", exe_name),
            os.path.join(base_dir, "..", "apps", exe_name),
            os.path.join(os.getcwd(), exe_name),
            os.path.join(os.getcwd(), "apps", exe_name)
        ]
        
        for path in search_paths:
            if os.path.exists(path) and os.path.isfile(path):
                return os.path.abspath(path)
        
        return None
    
    def _launch_program(self, name, exe_name):
        """
        Lanza un programa ejecutable.
        
        Args:
            name: Nombre de la aplicación
            exe_name: Nombre del ejecutable
        """
        # Buscar el ejecutable
        exe_path = self._find_executable(exe_name)
        
        if exe_path:
            try:
                # Lanzar el programa
                subprocess.Popen([exe_path])
                print(f"Lanzando: {name} ({exe_path})")
            except Exception as e:
                self._show_error(f"Error al lanzar {name}", str(e))
        else:
            self._show_error(
                f"No se encontró {name}",
                f"El ejecutable '{exe_name}' no está disponible."
            )
    
    def _show_error(self, title, message):
        """
        Muestra un diálogo de error.
        
        Args:
            title: Título del error
            message: Mensaje del error
        """
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg_box.exec()
    
    def _center_on_screen(self):
        """Centra la ventana en la pantalla."""
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def mousePressEvent(self, event):
        """Permite arrastrar la ventana."""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._dragging = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Mueve la ventana al arrastrar."""
        if self._dragging:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Termina el arrastre de la ventana."""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._dragging = False
            event.accept()
