#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lanzador PyQt6 — Hover animations, lift & micro-interactions improvements

Qué implementé en esta versión:
- Hover animations al pasar el mouse sobre un tile:
  - Icon "pop" (suave aumento de iconSize).
  - Tile "lift" (aumento de blur del shadow + leve aumento de maximumSize para dar sensación de elevación).
  - Label cambia de color al pasar el mouse (usando property + re-polish).
  - Ripple effect al hacer click (ya presente).
- Animaciones agrupadas con QParallelAnimationGroup para coherencia.
- Restauración suave al salir del hover.
- Keyboard navigation y badges (como en la versión anterior).
- Evité el bug previo (usar entero en addWidget stretch).
# CORRECCIÓN DE UX: Se implementa LoadingOverlay y la señal de finalización 
# en LauncherTask para mostrar un indicador de carga.

Notas:
- Ajusta rutas de iconos en load_icons() si tu carpeta de iconos está en otra ubicación.
- Requiere PyQt6 instalado.
"""

import sys
import os
import subprocess
from PyQt6 import QtCore, QtGui, QtWidgets # <--- ÚNICA LÍNEA DE IMPORTACIÓN PRINCIPAL

ICON_SIZE = 72
TILE_W = 160
TILE_H = 150
SIDEBAR_WIDTH = 220

STYLE = f"""
QWidget {{
    background: #0f1417;
    color: #E6EEF6;
    font-family: "Segoe UI";
    font-size: 12px;
}}
QFrame#sidebar {{
    background: #0b0d0f;
    border-right: 1px solid rgba(255,255,255,0.03);
}}
QPushButton#sidebarButton {{
    text-align: left;
    padding: 10px 14px;
    border: none;
    color: #E6EEF6;
    background: transparent;
    border-radius: 6px;
}}
QPushButton#sidebarButton[selected="true"] {{
    background: rgba(46,168,255,0.08);
    border-left: 4px solid #2EA8FF;
    color: #2EA8FF;
}}
QWidget.launcherTile {{
    background: transparent;
    border-radius: 10px;
}}
QWidget.launcherTile[selected="true"] {{
    background: rgba(46,168,255,0.06);
    border: 1px solid rgba(46,168,255,0.12);
}}
QLabel.tileLabel {{
    color: #9AA5B1;
    font-weight: 600;
    font-size: 11px;
}}
QLabel.tileLabel[hover="true"] {{
    color: #ffffff;
}}
QLabel.badge {{
    background: #ff4d4f;
    color: white;
    border-radius: 9px;
    padding: 2px 6px;
    font-size: 10px;
    font-weight: 700;
}}
"""

def resource_path(rel_path: str) -> str:
    try:
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

# ----------------------------
# Ripple overlay (animatable)
# ----------------------------
class RippleOverlay(QtWidgets.QWidget):
    def __init__(self, parent=None, color=QtGui.QColor(255,255,255,80)):
        super().__init__(parent)
        self._radius = 0
        self._opacity = 0.0
        self.color = color
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.hide()

    def paintEvent(self, event):
        if self._opacity <= 0 or self._radius <= 0:
            return
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        c = QtGui.QColor(self.color)
        c.setAlphaF(self._opacity)
        brush = QtGui.QBrush(c)
        p.setBrush(brush)
        p.setPen(QtCore.Qt.PenStyle.NoPen)
        # center in event if needed; currently center of widget
        center = QtCore.QPoint(self.width()//2, self.height()//2)
        p.drawEllipse(center, int(self._radius), int(self._radius))
        p.end()

    @QtCore.pyqtProperty(float)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, v):
        self._radius = v
        self.update()

    @QtCore.pyqtProperty(float)
    def rippleOpacity(self):
        return self._opacity

    @rippleOpacity.setter
    def rippleOpacity(self, v):
        self._opacity = v
        self.update()

    def start(self, max_radius=100, duration=420):
        self.show()
        self.raise_()
        group = QtCore.QParallelAnimationGroup(self)
        a1 = QtCore.QPropertyAnimation(self, b"radius", self)
        a1.setStartValue(0.0)
        a1.setEndValue(max_radius)
        a1.setDuration(int(duration * 0.9))
        a1.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)

        a2 = QtCore.QPropertyAnimation(self, b"rippleOpacity", self)
        a2.setStartValue(0.7)
        a2.setKeyValueAt(0.6, 0.25)
        a2.setEndValue(0.0)
        a2.setDuration(duration)

        group.addAnimation(a1)
        group.addAnimation(a2)

        def on_finish():
            self.hide()
            self.radius = 0
            self.rippleOpacity = 0.0

        group.finished.connect(on_finish)
        group.start(QtCore.QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

# ----------------------------
# Loading Overlay (Añadido para el efecto de carga)
# ----------------------------
class LoadingOverlay(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setHidden(True)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100);")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        self.label = QtWidgets.QLabel("Lanzando programa...")
        self.label.setStyleSheet("color: white; font-size: 14px; font-weight: 700; background: transparent;")
        
        layout.addWidget(self.label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        
    def showEvent(self, event):
        # Ajusta el tamaño para cubrir al padre
        if self.parentWidget():
            self.setGeometry(self.parentWidget().rect())
        super().showEvent(event)
        
    def resizeEvent(self, event):
        # Mantiene el tamaño ajustado al padre
        if self.parentWidget():
            self.setGeometry(self.parentWidget().rect())
        super().resizeEvent(event)
        
# ----------------------------
# Subclase QRunnable (CORRECCIÓN con Señal de Finalización)
# ----------------------------
class LauncherTask(QtCore.QRunnable):
    """Tarea que envuelve el lanzamiento de un subproceso y maneja errores."""

    # Clase auxiliar para señales (QRunnable no puede tener señales directamente)
    class Signals(QtCore.QObject):
        finished = QtCore.pyqtSignal() # Señal emitida al finalizar la ejecución

    def __init__(self, exe_name: str, parent=None):
        super().__init__()
        self.exe_name = exe_name
        self.mainWindow = parent
        self.signals = self.Signals() # Instancia de la clase de señales
        
    @QtCore.pyqtSlot()
    def run(self):
        """El método que se ejecuta cuando se inicia la tarea en el QThreadPool."""
        
        # El bloque finally garantiza que la señal 'finished' se emita siempre.
        try:
            # Asegurar la ruta
            if not os.path.isabs(self.exe_name):
                path = os.path.join(os.getcwd(), self.exe_name)
            else:
                path = self.exe_name
                
            # Lanzamiento del programa
            subprocess.Popen([path], shell=False)
            
        except FileNotFoundError:
            # Invocar show_warning en el hilo principal
            QtCore.QMetaObject.invokeMethod(
                self.mainWindow, 
                "show_warning", 
                QtCore.Qt.ConnectionType.QueuedConnection, 
                QtCore.Q_ARG(str, "No encontrado"), 
                QtCore.Q_ARG(str, f"No se encontró: {self.exe_name}") 
            )
        except Exception as e:
            # Invocar show_critical en el hilo principal
            QtCore.QMetaObject.invokeMethod(
                self.mainWindow, 
                "show_critical", 
                QtCore.Qt.ConnectionType.QueuedConnection, 
                QtCore.Q_ARG(str, "Error"), 
                QtCore.Q_ARG(str, f"Ocurrió un error al lanzar {self.exe_name}:\n{e}") 
            )
        finally:
            # ¡CRÍTICO! Emitir la señal al finalizar, sin importar si hubo error o éxito
            self.signals.finished.emit() 

# ----------------------------
# Launcher Tile with improved hover animations
# ----------------------------
class LauncherTile(QtWidgets.QWidget):
    clicked = QtCore.pyqtSignal(object)  # emits self
    def __init__(self, icon: QtGui.QIcon, label: str, exe: str, parent=None):
        super().__init__(parent)
        self.setObjectName("launcherTile")
        self.setProperty("selected", "false")
        self.exe = exe
        self.icon = icon
        self.label_text = label

        self._icon_size = QtCore.QSize(ICON_SIZE, ICON_SIZE)
        self._build_ui()
        self.setFixedSize(TILE_W, TILE_H)

        # shadow effect
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(14)
        self.shadow.setOffset(0, 6)
        self.shadow.setColor(QtGui.QColor(0,0,0,180))
        # add shadow to internal wrapper so shadow doesn't clip
        self.setGraphicsEffect(self.shadow)

        # ripple
        self.ripple = RippleOverlay(self, QtGui.QColor(255,255,255,100))
        self.ripple.setGeometry(0, 0, TILE_W, TILE_H)

        # hover animation group (pop + lift + label color)
        self._hover_group = QtCore.QParallelAnimationGroup(self)
        # icon size animation
        self._icon_anim = QtCore.QPropertyAnimation(self, b"iconSize")
        self._icon_anim.setDuration(200)
        self._icon_anim.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self._hover_group.addAnimation(self._icon_anim)
        # maximumSize animation (simulate lift without changing layout drastically)
        self._size_anim = QtCore.QPropertyAnimation(self, b"maximumSize")
        self._size_anim.setDuration(200)
        self._size_anim.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self._hover_group.addAnimation(self._size_anim)
        # shadow blur animation
        self._shadow_anim = QtCore.QPropertyAnimation(self.shadow, b"blurRadius")
        self._shadow_anim.setDuration(200)
        self._shadow_anim.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self._hover_group.addAnimation(self._shadow_anim)

        # reverse group for leaving (we'll reuse by setting start/end appropriately)
        self._leave_group = QtCore.QParallelAnimationGroup(self)
        self._leave_icon_anim = QtCore.QPropertyAnimation(self, b"iconSize")
        self._leave_icon_anim.setDuration(180)
        self._leave_icon_anim.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self._leave_group.addAnimation(self._leave_icon_anim)
        self._leave_size_anim = QtCore.QPropertyAnimation(self, b"maximumSize")
        self._leave_size_anim.setDuration(180)
        self._leave_size_anim.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self._leave_group.addAnimation(self._leave_size_anim)
        self._leave_shadow_anim = QtCore.QPropertyAnimation(self.shadow, b"blurRadius")
        self._leave_shadow_anim.setDuration(180)
        self._leave_shadow_anim.setEasingCurve(QtCore.QEasingCurve.Type.InCubic)
        self._leave_group.addAnimation(self._leave_shadow_anim)

        # focus & keyboard
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8,8,8,6)
        layout.setSpacing(6)
        self.toolbtn = QtWidgets.QToolButton()
        self.toolbtn.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.toolbtn.setIcon(self.icon)
        self.toolbtn.setIconSize(self._icon_size)
        self.toolbtn.setText(self.label_text)
        self.toolbtn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        # forward clicks from toolbtn to tile clicked
        self.toolbtn.clicked.connect(lambda: self.clicked.emit(self))
        # label under icon (for hover color change)
        self.lbl = QtWidgets.QLabel(self.label_text)
        self.lbl.setObjectName("tileLabel")
        self.lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.toolbtn, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl)

        # badge
        self.badge = QtWidgets.QLabel("", self)
        self.badge.setObjectName("badge")
        self.badge.setProperty("class", "badge")
        self.badge.setVisible(False)
        self.badge.setStyleSheet("QLabel.badge { background: #ff4d4f; color: white; border-radius: 9px; padding: 2px 6px; font-size: 10px; font-weight: 700; }")
        self.badge.move(self.width() - 36, 8)

    # property to animate icon size (for micro-interaction)
    @QtCore.pyqtProperty(QtCore.QSize)
    def iconSize(self):
        return self._icon_size

    @iconSize.setter
    def iconSize(self, size: QtCore.QSize):
        self._icon_size = size
        self.toolbtn.setIconSize(size)

    def set_selected(self, state: bool):
        self.setProperty("selected", "true" if state else "false")
        self.style().unpolish(self); self.style().polish(self); self.update()
        if state:
            self.setFocus(QtCore.Qt.FocusReason.OtherFocusReason)

    def set_badge(self, value: int):
        if value and value > 0:
            txt = str(value) if value < 100 else "99+"
            self.badge.setText(txt)
            self.badge.adjustSize()
            self.badge.move(self.width() - self.badge.width() - 12, 8)
            self.badge.setVisible(True)
        else:
            self.badge.setVisible(False)

    # Hover enter/leave animations
    def enterEvent(self, ev):
        # populate hover animation start/end
        # icon: grow ~12%
        start_icon = self.toolbtn.iconSize()
        end_icon = QtCore.QSize(int(ICON_SIZE * 1.12), int(ICON_SIZE * 1.12))
        self._icon_anim.stop()
        self._icon_anim.setStartValue(start_icon)
        self._icon_anim.setEndValue(end_icon)
        # size: allow small increase so it appears to lift (doesn't break layout much)
        start_size = self.maximumSize()
        if start_size.width() == 16777215:  # default max
            start_size = QtCore.QSize(TILE_W, TILE_H)
        end_size = QtCore.QSize(int(TILE_W * 1.04), int(TILE_H * 1.04))
        self._size_anim.stop()
        self._size_anim.setStartValue(start_size)
        self._size_anim.setEndValue(end_size)
        # shadow blur increase (lift)
        self._shadow_anim.stop()
        self._shadow_anim.setStartValue(self.shadow.blurRadius())
        self._shadow_anim.setEndValue(26)

        # label color change property
        self.lbl.setProperty("hover", "true")
        self.lbl.style().unpolish(self.lbl); self.lbl.style().polish(self.lbl)

        self._hover_group.start()
        return super().enterEvent(ev)

    def leaveEvent(self, ev):
        # reverse animations back to normal
        start_icon = self.toolbtn.iconSize()
        end_icon = QtCore.QSize(ICON_SIZE, ICON_SIZE)
        self._leave_icon_anim.stop()
        self._leave_icon_anim.setStartValue(start_icon)
        self._leave_icon_anim.setEndValue(end_icon)

        start_size = self.maximumSize()
        end_size = QtCore.QSize(TILE_W, TILE_H)
        self._leave_size_anim.stop()
        self._leave_size_anim.setStartValue(start_size)
        self._leave_size_anim.setEndValue(end_size)

        self._leave_shadow_anim.stop()
        self._leave_shadow_anim.setStartValue(self.shadow.blurRadius())
        self._leave_shadow_anim.setEndValue(14)

        # reset label color property
        self.lbl.setProperty("hover", "false")
        self.lbl.style().unpolish(self.lbl); self.lbl.style().polish(self.lbl)

        self._leave_group.start()
        return super().leaveEvent(ev)

    # click micro-interaction + ripple
    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            # small press shrink (quick)
            target = QtCore.QSize(int(ICON_SIZE * 0.9), int(ICON_SIZE * 0.9))
            anim = QtCore.QPropertyAnimation(self, b"iconSize", self)
            anim.setStartValue(self.toolbtn.iconSize())
            anim.setEndValue(target)
            anim.setDuration(100)
            anim.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
            anim.start(QtCore.QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
            self._press_anim = anim
        return super().mousePressEvent(ev)

    def mouseReleaseEvent(self, ev):
        if ev.button() == QtCore.Qt.MouseButton.LeftButton:
            # restore icon
            anim = QtCore.QPropertyAnimation(self, b"iconSize", self)
            anim.setStartValue(self.toolbtn.iconSize())
            anim.setEndValue(QtCore.QSize(ICON_SIZE, ICON_SIZE))
            anim.setDuration(160)
            anim.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
            anim.start(QtCore.QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
            # ripple
            max_r = max(self.width(), self.height()) * 0.9
            self.ripple.start(max_radius=max_r, duration=420)
            # emit clicked
            self.clicked.emit(self)
        return super().mouseReleaseEvent(ev)

    # keyboard activation + arrow delegation (same approach as before)
    def keyPressEvent(self, ev: QtGui.QKeyEvent):
        if ev.key() in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter, QtCore.Qt.Key.Key_Space):
            # simulate click with small delay
            self.mousePressEvent(QtGui.QMouseEvent(QtCore.QEvent.Type.MouseButtonPress, QtCore.QPointF(self.width()/2,self.height()/2), QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.KeyboardModifier.NoModifier))
            QtCore.QTimer.singleShot(90, lambda: self.mouseReleaseEvent(QtGui.QMouseEvent(QtCore.QEvent.Type.MouseButtonRelease, QtCore.QPointF(self.width()/2,self.height()/2), QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.KeyboardModifier.NoModifier)))
            ev.accept()
            return
        if ev.key() in (QtCore.Qt.Key.Key_Left, QtCore.Qt.Key.Key_Right, QtCore.Qt.Key.Key_Up, QtCore.Qt.Key.Key_Down):
            w = self.window()
            if hasattr(w, "move_focus_from_tile"):
                w.move_focus_from_tile(self, ev.key())
                ev.accept()
                return
        return super().keyPressEvent(ev)

# ----------------------------
# Main Window with keyboard nav & responsive grid
# ----------------------------
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PROGAIN Launcher — Hover Animations")
        self.resize(1280, 720)
        self.setStyleSheet(STYLE)
        self.icons = self.load_icons()
        self.tiles = []
        self.cols = 1
        self._build_ui()
        
        # Añade la capa de carga después de construir la UI
        self.loading_overlay = LoadingOverlay(self) # <-- AÑADIDO

    def load_icons(self):
        names = {
            "prog_progain": "icons/icon_programa-01.png",
            "prog_equipos": "icons/icon_programa-02.png",
            "prog_facturas": "icons/icon_programa-03.png",
            "prog_facturacion_inter": "icons/icon_programa-04.png",
            "prog_licitaciones": "icons/icon_programa-05.png",
        }
        icons = {}
        for k, rel in names.items():
            p = resource_path(rel)
            if os.path.exists(p):
                icons[k] = QtGui.QIcon(p)
            else:
                pix = QtGui.QPixmap(ICON_SIZE, ICON_SIZE)
                pix.fill(QtGui.QColor(0,0,0,0))
                icons[k] = QtGui.QIcon(pix)
        return icons

    def _build_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        h = QtWidgets.QHBoxLayout(central)
        h.setContentsMargins(0,0,0,0)

        # sidebar minimal
        sidebar = QtWidgets.QFrame(objectName="sidebar")
        sidebar.setFixedWidth(SIDEBAR_WIDTH)
        side_layout = QtWidgets.QVBoxLayout(sidebar)
        side_layout.setContentsMargins(12,12,12,12)
        title = QtWidgets.QLabel("PROGAIN")
        title.setStyleSheet("font-weight:800; font-size:18px; color: #2EA8FF")
        side_layout.addWidget(title)
        side_layout.addStretch()
        h.addWidget(sidebar)

        # main area with scrollable responsive grid
        self.container = QtWidgets.QWidget()
        main_v = QtWidgets.QVBoxLayout(self.container)
        main_v.setContentsMargins(20,20,20,20)

        header = QtWidgets.QHBoxLayout()
        lbl = QtWidgets.QLabel("ORGANIT by PROGAIN")
        lbl.setStyleSheet("font-weight:700; font-size:18px;")
        header.addWidget(lbl)
        header.addStretch()
        self.search = QtWidgets.QLineEdit()
        self.search.setPlaceholderText("Buscar...")
        self.search.textChanged.connect(self.relayout_tiles)
        # CORRECCIÓN: pasar entero como stretch (no float)
        header.addWidget(self.search, 1)
        main_v.addLayout(header)
        main_v.addSpacing(12)

        self.grid_container = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(22)
        self.grid_layout.setContentsMargins(10,10,10,10)

        # scroll area
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.grid_container)
        main_v.addWidget(scroll, 1)

        h.addWidget(self.container, 1)

        # create tiles
        botones_info = [
            ("PROGAIN", 'prog_progain', "progain_app.exe"),
            ("EQUIPOS", 'prog_equipos', "alquiler_equipos.exe"),
            ("FACTURAS", 'prog_facturas', "gestion_facturas.exe"),
            ("FACTURAS EMP", 'prog_facturacion_inter', "facturacion_gui.exe"),
            ("LICITACIONES", 'prog_licitaciones', "gestor_licitaciones_db.exe"),
        ]
        for label, icon_key, exe in botones_info:
            t = LauncherTile(self.icons.get(icon_key), label, exe, parent=self.grid_container)
            t.clicked.connect(self.on_tile_clicked)
            self.tiles.append(t)

        # sample badges (demo)
        if len(self.tiles) > 2:
            self.tiles[2].set_badge(3)   # FACTURAS
        if len(self.tiles) > 3:
            self.tiles[3].set_badge(12)  # FACTURAS EMP

        # initial layout
        self.relayout_tiles()
        # put focus on first tile for keyboard nav
        if self.tiles:
            self.tiles[0].setFocus()

    def relayout_tiles(self):
        q = self.search.text().strip().lower()
        visible = []
        for t in self.tiles:
            if not q or q in t.label_text.lower():
                t.setVisible(True)
                visible.append(t)
            else:
                t.setVisible(False)
        # compute columns based on available width
        avail = max(400, self.width() - SIDEBAR_WIDTH - 200)
        col_w = TILE_W + 24
        cols = max(1, avail // col_w)
        self.cols = cols
        # clear layout
        while self.grid_layout.count():
            it = self.grid_layout.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)
        # add visible tiles in grid
        r = c = 0
        for t in visible:
            self.grid_layout.addWidget(t, r, c, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
            c += 1
            if c >= cols:
                c = 0
                r += 1
        self.grid_container.update()

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self.relayout_tiles()

    def move_focus_from_tile(self, tile, key):
        if tile not in self.tiles:
            return
        visible_tiles = [t for t in self.tiles if t.isVisible()]
        try:
            idx = visible_tiles.index(tile)
        except ValueError:
            return
        cols = max(1, self.cols)
        rows = (len(visible_tiles) + cols - 1) // cols
        r = idx // cols
        c = idx % cols
        if key == QtCore.Qt.Key.Key_Left:
            new_idx = idx - 1 if c > 0 else idx
        elif key == QtCore.Qt.Key.Key_Right:
            new_idx = idx + 1 if (c < cols - 1 and idx + 1 < len(visible_tiles)) else idx
        elif key == QtCore.Qt.Key.Key_Up:
            new_idx = idx - cols if r > 0 else idx
        elif key == QtCore.Qt.Key.Key_Down:
            new_idx = idx + cols if (r < rows - 1 and idx + cols < len(visible_tiles)) else idx
        else:
            new_idx = idx
        target = visible_tiles[new_idx]
        target.setFocus()
        for t in self.tiles:
            t.set_selected(t is target)

    def on_tile_clicked(self, tile):
        for t in self.tiles:
            t.set_selected(t is tile)
        self.launch_program(tile.exe)
        
    @QtCore.pyqtSlot() # <-- NUEVO MÉTODO
    def hide_loading_overlay(self):
        """Oculta la capa de carga cuando el programa ha sido lanzado."""
        self.loading_overlay.hide()

    # SLOTS DE CORRECCIÓN: Para recibir mensajes de error del hilo secundario
    @QtCore.pyqtSlot(str, str)
    def show_warning(self, title: str, msg: str):
        """Muestra una advertencia en el hilo principal (GUI)."""
        QtWidgets.QMessageBox.warning(self, title, msg)

    @QtCore.pyqtSlot(str, str)
    def show_critical(self, title: str, msg: str):
        """Muestra un error crítico en el hilo principal (GUI)."""
        QtWidgets.QMessageBox.critical(self, title, msg)

    # FUNCIÓN CORREGIDA: Muestra LoadingOverlay y conecta la señal de finalización
    def launch_program(self, exe_name: str):
        # 1. Muestra la capa de carga y la pone al frente
        self.loading_overlay.show()
        self.loading_overlay.raise_()
        
        # 2. Creamos una instancia de nuestra subclase QRunnable
        r = LauncherTask(exe_name, parent=self)
        
        # 3. Conecta la señal de finalización al método para ocultar el loading
        r.signals.finished.connect(self.hide_loading_overlay) # <-- CONEXIÓN CLAVE
        
        # 4. Iniciamos la tarea en el pool de hilos global
        QtCore.QThreadPool.globalInstance().start(r)

# ----------------------------
# Run
# ----------------------------
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()