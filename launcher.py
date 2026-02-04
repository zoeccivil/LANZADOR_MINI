import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, 
    QFrame, QToolButton, QApplication, QGraphicsDropShadowEffect, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QIcon, QCursor, QColor, QPixmap, QAction, QPainter
from PyQt6.QtSvg import QSvgRenderer  # Necesario para renderizar SVGs en el loader

# --- CONFIGURACIÓN DE APLICACIONES ---
APPS_CONFIG = [
    {"name": "PROGRAIN", "exe": "progain_app.exe", "icon": "construction"},
    {"name": "EQUIPOS", "exe": "alquiler_equipos.exe", "icon": "truck"},
    {"name": "FACTURAS", "exe": "gestion_facturas.exe", "icon": "receipt"},
    {"name": "FACTURAS EMP", "exe": "facturacion_gui.exe", "icon": "business"},
    {"name": "LICITACIONES", "exe": "gestor_licitaciones_db.exe", "icon": "gavel"},
    {"name": "FA-COT", "exe": "facot.exe", "icon": "calculator"},
    {"name": "DOCUMENTOS", "exe": "explorer.exe", "icon": "folder"},
    {"name": "AJUSTES", "exe": "config.exe", "icon": "settings"},
    {"name": "SALIR", "exe": None, "icon": "power_settings_new"}
]

# --- UTILIDADES ---
def resource_path(relative_path):
    """Obtiene ruta absoluta compatible con PyInstaller y entorno dev."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_icon_path(icon_name):
    """Resuelve la ruta del archivo SVG basado en el nombre clave."""
    icon_map = {
        "construction": "construction.svg",
        "truck": "agriculture.svg",        
        "receipt": "receipt_long.svg",
        "business": "inventory.svg",       
        "gavel": "gavel.svg",
        "calculator": "request_quote.svg", 
        "folder": "folder_open.svg",
        "settings": "settings.svg",
        "power_settings_new": "power_settings_new.svg"
    }
    filename = icon_map.get(icon_name, f"{icon_name}.svg")
    return resource_path(os.path.join("icons", filename))

# --- VENTANA DE CARGA (LOADER) ---
class AppLoader(QDialog):
    """
    Ventana flotante modal que muestra el icono del programa mientras carga.
    Estilo 'Industrial Light' (Blanco/Gris/Amarillo).
    """
    def __init__(self, app_config, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(260, 280)

        # Layout Principal (transparente para la sombra)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Tarjeta contenedora
        self.card = QFrame()
        self.card.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 16px;
                border: 1px solid #F59E0B; /* Borde Amarillo sutil */
            }
        """)
        
        # Sombra profunda
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.card.setGraphicsEffect(shadow)

        # Contenido de la tarjeta
        card_layout = QVBoxLayout(self.card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.setSpacing(20)

        # 1. Icono Grande
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(80, 80)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Renderizar SVG manualmente para tamaño grande en QLabel
        icon_path = get_icon_path(app_config["icon"])
        if os.path.exists(icon_path):
            pixmap = QPixmap(80, 80)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            renderer = QSvgRenderer(icon_path)
            renderer.render(painter)
            painter.end()
            self.icon_label.setPixmap(pixmap)

        # 2. Texto "Abriendo..."
        self.title_label = QLabel(f"Iniciando\n{app_config['name']}")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            color: #111827; 
            font-family: 'Segoe UI'; 
            font-size: 18px; 
            font-weight: bold;
        """)

        # 3. Indicador de estado
        self.status_label = QLabel("Cargando módulos...")
        self.status_label.setStyleSheet("color: #6B7280; font-size: 12px;")

        card_layout.addWidget(self.icon_label, 0, Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.title_label, 0, Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.status_label, 0, Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(self.card)
        
        # Centrar en el padre
        if parent:
            geo = parent.geometry()
            self.move(
                geo.center().x() - self.width() // 2,
                geo.center().y() - self.height() // 2
            )

# --- BOTÓN DE LANZADOR ---
class LauncherBtn(QToolButton):
    def __init__(self, app_config, parent=None):
        super().__init__(parent)
        self.app_config = app_config
        self.setText(app_config["name"])
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # Configuración Visual
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setIconSize(QSize(54, 54)) # Iconos grandes
        self.setFixedSize(140, 120)     # Botones cuadrados/rectangulares
        
        # Cargar Icono
        icon_path = get_icon_path(app_config["icon"])
        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
        else:
            # Fallback
            pix = QPixmap(54, 54)
            pix.fill(QColor("#E0E0E0"))
            self.setIcon(QIcon(pix))
        
        # Aplicar Estilos
        self._apply_styles()

    def _apply_styles(self):
        """Aplica hoja de estilos QSS moderna."""
        is_exit = self.app_config["name"] == "SALIR"
        
        border_color_hover = "#EF4444" if is_exit else "#F59E0B" # Rojo o Amarillo
        bg_color_hover = "#FEF2F2" if is_exit else "#FFF7ED"
        text_color_hover = "#991B1B" if is_exit else "#B45309"

        self.setStyleSheet(f"""
            QToolButton {{
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                color: #374151;
                font-family: 'Segoe UI';
                font-size: 12px;
                font-weight: bold;
                padding: 10px;
            }}
            QToolButton:hover {{
                border: 2px solid {border_color_hover};
                background-color: {bg_color_hover};
                color: {text_color_hover};
            }}
            QToolButton:pressed {{
                background-color: #F3F4F6;
                border: 1px solid #D1D5DB;
                padding-top: 12px;
                padding-left: 12px;
            }}
        """)
        
        # Efecto de Sombra
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)

# --- VENTANA PRINCIPAL ---
class LauncherWindow(QMainWindow):
    def __init__(self, firebase_manager=None):
        super().__init__()
        self.fm = firebase_manager
        
        self.setWindowTitle("ZOEC LAUNCHER")
        self.setFixedSize(580, 650) # Tamaño ajustado para Grid 3x3
        
        # Estilo global
        self.setStyleSheet("QMainWindow { background-color: #F3F4F6; }")
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self._setup_header()
        self._setup_grid()
        self._setup_footer()

    def _setup_header(self):
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("background-color: #1F2937;")
        
        layout = QVBoxLayout(header)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("ZOEC CIVIL")
        title.setStyleSheet("color: #F59E0B; font-weight: 800; font-size: 16px; letter-spacing: 2px;")
        
        subtitle = QLabel("CENTRO DE CONTROL")
        subtitle.setStyleSheet("color: #9CA3AF; font-size: 10px; letter-spacing: 1px;")
        
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.main_layout.addWidget(header)

    def _setup_grid(self):
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setContentsMargins(40, 40, 40, 40)
        grid.setSpacing(20)
        
        row, col = 0, 0
        
        for app in APPS_CONFIG:
            btn = LauncherBtn(app)
            # Conectar click
            if app["name"] == "SALIR":
                btn.clicked.connect(self.close)
            else:
                btn.clicked.connect(lambda checked, a=app: self._launch_program(a))
            
            grid.addWidget(btn, row, col)
            
            col += 1
            if col > 2: # 3 Columnas (0, 1, 2)
                col = 0
                row += 1
                
        self.main_layout.addWidget(grid_container)

    def _setup_footer(self):
        self.status_bar = QLabel("Sistema listo")
        self.status_bar.setFixedHeight(30)
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_bar.setStyleSheet("""
            background-color: #FFFFFF;
            border-top: 1px solid #E5E7EB;
            color: #6B7280;
            font-size: 11px;
        """)
        self.main_layout.addWidget(self.status_bar)

    def _launch_program(self, app_config):
        """Lógica de búsqueda y ejecución con Loader."""
        exe_name = app_config["exe"]
        prog_name = app_config["name"]
        
        self.status_bar.setText(f"Buscando {prog_name}...")
        self.status_bar.setStyleSheet("background-color: #FFF7ED; color: #D97706; border-top: 1px solid #E5E7EB;")
        QApplication.processEvents()
        
        # Lugares donde buscar el ejecutable
        locations = [
            os.path.join(os.getcwd(), exe_name),           # ./{exe}
            os.path.join(os.getcwd(), "apps", exe_name),   # ./apps/{exe}
            os.path.join(os.getcwd(), "..", exe_name),     # ../{exe}
            os.path.join(os.getcwd(), "..", "apps", exe_name) # ../apps/{exe}
        ]
        
        target_path = None
        
        # Caso especial para comandos del sistema
        if exe_name.lower() == "explorer.exe":
            target_path = "explorer.exe"
        else:
            for loc in locations:
                if os.path.exists(loc):
                    target_path = os.path.abspath(loc)
                    break
        
        if target_path:
            try:
                # 1. Mostrar Loader
                loader = AppLoader(app_config, self)
                loader.show()
                QApplication.processEvents() # Forzar renderizado
                
                # Pequeña pausa estética para que se vea el loader (opcional)
                # QTimer.singleShot(500, lambda: None) 

                self.status_bar.setText(f"Ejecutando {prog_name}...")
                
                # 2. Ejecutar
                if sys.platform == 'win32':
                    subprocess.Popen([target_path], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen([target_path])
                
                # 3. Cerrar loader después de 2.5 segundos
                QTimer.singleShot(2500, loader.close)
                QTimer.singleShot(2500, lambda: self._reset_status())
                
            except Exception as e:
                if 'loader' in locals(): loader.close()
                self._show_error(f"Error al iniciar: {str(e)}")
        else:
            self._show_error(f"No se encontró: {exe_name}")

    def _show_error(self, msg):
        self.status_bar.setText(msg)
        self.status_bar.setStyleSheet("""
            background-color: #FEE2E2; 
            color: #991B1B; 
            font-weight: bold;
            border-top: 1px solid #FCA5A5;
        """)
        QTimer.singleShot(4000, lambda: self._reset_status())

    def _reset_status(self):
        self.status_bar.setText("Sistema listo")
        self.status_bar.setStyleSheet("""
            background-color: #FFFFFF;
            border-top: 1px solid #E5E7EB;
            color: #6B7280;
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LauncherWindow()
    window.show()
    sys.exit(app.exec())