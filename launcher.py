import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, 
    QFrame, QToolButton, QApplication, QGraphicsDropShadowEffect, QMessageBox
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QIcon, QCursor, QColor, QPixmap, QAction

# --- CONFIGURACIÓN DE APLICACIONES ---
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

# --- UTILIDADES ---
def resource_path(relative_path):
    """Obtiene ruta absoluta compatible con PyInstaller y entorno dev."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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
        self._create_icon(app_config["icon"])
        
        # Aplicar Estilos
        self._apply_styles()

    def _create_icon(self, icon_name):
        """Carga el SVG correspondiente desde la carpeta icons/"""
        # Mapeo de nombres de config a archivos SVG reales
        # Asegúrate de que estos archivos existan en la carpeta 'icons'
        icon_map = {
            "construction": "construction.svg",
            "truck": "agriculture.svg",        # Usamos agriculture/truck
            "receipt": "receipt_long.svg",
            "business": "inventory.svg",       # O business.svg
            "gavel": "gavel.svg",
            "calculator": "request_quote.svg", # O calculator.svg
            "folder": "folder_open.svg",
            "settings": "settings.svg",
            "power_settings_new": "power_settings_new.svg"
        }
        
        filename = icon_map.get(icon_name, f"{icon_name}.svg")
        icon_path = resource_path(os.path.join("icons", filename))
        
        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
        else:
            # Fallback si no hay icono: Cuadrado gris con la inicial
            print(f"Advertencia: Icono no encontrado en {icon_path}")
            pix = QPixmap(54, 54)
            pix.fill(QColor("#E0E0E0"))
            self.setIcon(QIcon(pix))

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
        """Lógica de búsqueda y ejecución de programas."""
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
                self.status_bar.setText(f"Ejecutando {prog_name}...")
                
                # Ejecutar de forma independiente (Detached)
                if sys.platform == 'win32':
                    subprocess.Popen([target_path], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    subprocess.Popen([target_path]) # Linux/Mac (fallback)
                
                QTimer.singleShot(2000, lambda: self._reset_status())
                
            except Exception as e:
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