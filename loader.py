#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loader Window - Splash Screen con barra de progreso
Ventana de carga profesional que se muestra al iniciar el launcher.
"""

from PyQt6 import QtCore, QtGui, QtWidgets
from firebase_config import FirebaseManager


class LoaderWindow(QtWidgets.QWidget):
    """
    Ventana splash (loader) con barra de progreso animada.
    Simula la carga de datos y conexión a Firebase.
    """
    
    # Señal emitida cuando la carga está completa
    loading_complete = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.firebase_manager = FirebaseManager()
        self.progress = 0
        self._setup_ui()
        self._setup_timer()
    
    def _setup_ui(self):
        """Configura la interfaz del loader."""
        # Ventana sin bordes
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint | 
            QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Tamaño fijo
        self.setFixedSize(400, 250)
        
        # Centrar en pantalla
        self._center_on_screen()
        
        # Layout principal
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Container con fondo degradado
        self.container = QtWidgets.QFrame()
        self.container.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F3F4F6, stop:1 #E5E7EB
                );
                border-radius: 12px;
            }
        """)
        
        container_layout = QtWidgets.QVBoxLayout(self.container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(20)
        
        # Logo/Título
        title = QtWidgets.QLabel("ZOEC LAUNCHER")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #1F2937;
                font-family: 'Segoe UI';
                font-size: 28px;
                font-weight: 700;
                background: transparent;
            }
        """)
        container_layout.addWidget(title)
        
        # Espacio
        container_layout.addSpacing(10)
        
        # Barra de progreso
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setFixedWidth(300)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #E5E7EB;
            }
            QProgressBar::chunk {
                border-radius: 4px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #F59E0B, stop:1 #EF4444
                );
            }
        """)
        
        progress_container = QtWidgets.QWidget()
        progress_layout = QtWidgets.QHBoxLayout(progress_container)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.addStretch()
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addStretch()
        container_layout.addWidget(progress_container)
        
        # Etiqueta de estado
        self.status_label = QtWidgets.QLabel("Inicializando...")
        self.status_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #6B7280;
                font-family: 'Segoe UI';
                font-size: 10pt;
                background: transparent;
            }
        """)
        container_layout.addWidget(self.status_label)
        
        # Espacio flexible
        container_layout.addStretch()
        
        # Versión
        version_label = QtWidgets.QLabel("v2.0")
        version_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("""
            QLabel {
                color: #9CA3AF;
                font-family: 'Segoe UI';
                font-size: 9pt;
                background: transparent;
            }
        """)
        container_layout.addWidget(version_label)
        
        main_layout.addWidget(self.container)
    
    def _center_on_screen(self):
        """Centra la ventana en la pantalla."""
        screen = QtWidgets.QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.geometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)
    
    def _setup_timer(self):
        """Configura el timer para la animación de progreso."""
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_progress)
        self.timer.setInterval(50)  # 50ms para animación suave (20 FPS mínimo)
    
    def start_loading(self):
        """Inicia la animación de carga."""
        self.progress = 0
        self.timer.start()
    
    def _update_progress(self):
        """Actualiza el progreso de la barra."""
        # Incremento más rápido al principio, más lento al final
        if self.progress < 25:
            increment = 2
            self.status_label.setText("Inicializando sistema...")
        elif self.progress < 50:
            increment = 1.5
            self.status_label.setText("Conectando a Firebase...")
            # Simular conexión a Firebase
            if self.progress == 25:
                QtCore.QTimer.singleShot(100, self._connect_firebase)
        elif self.progress < 75:
            increment = 1.5
            self.status_label.setText("Cargando configuración de usuario...")
            # Simular carga de datos
            if self.progress == 50:
                QtCore.QTimer.singleShot(100, self._load_user_data)
        else:
            increment = 1
            self.status_label.setText("Preparando interfaz...")
        
        self.progress += increment
        self.progress_bar.setValue(int(self.progress))
        
        # Cuando llega al 100%, espera un poco y emite señal
        if self.progress >= 100:
            self.timer.stop()
            QtCore.QTimer.singleShot(300, self._finish_loading)
    
    def _connect_firebase(self):
        """Conecta a Firebase en segundo plano."""
        try:
            self.firebase_manager.connect()
        except Exception as e:
            print(f"Error en conexión Firebase: {e}")
    
    def _load_user_data(self):
        """Carga datos del usuario en segundo plano."""
        try:
            self.firebase_manager.load_user_data()
        except Exception as e:
            print(f"Error al cargar datos: {e}")
    
    def _finish_loading(self):
        """Finaliza la carga y emite señal."""
        self.loading_complete.emit()
    
    def get_firebase_manager(self):
        """Retorna el FirebaseManager para usarlo en el launcher."""
        return self.firebase_manager
