# ZOEC Launcher v2.0

Launcher moderno y profesional para aplicaciones ZOEC con diseño minimalista.

## 🎨 Características

- **Diseño Moderno**: Interface minimalista con paleta de colores profesional
- **Splash Screen**: Pantalla de carga animada con barra de progreso
- **Firebase Ready**: Estructura preparada para integración con Firebase
- **Grid 3x3**: Diseño compacto y organizado de aplicaciones
- **Ventana sin bordes**: Interface limpia con controles personalizados

## 📁 Estructura de Archivos

```
.
├── main.py                     # Punto de entrada principal
├── launcher.py                 # Ventana principal del launcher
├── loader.py                   # Pantalla de carga (splash screen)
├── firebase_config.py          # Configuración de Firebase (simulado)
└── lanzador_programas_PyQT6.py # Versión anterior (legacy)
```

## 🚀 Uso

### Ejecutar el launcher

```bash
python3 main.py
```

### Requisitos

- Python 3.8+
- PyQt6

```bash
pip install PyQt6
```

## 🎯 Aplicaciones Configuradas

1. **Equipos** - Gestión de equipos y maquinaria
2. **Contabilidad** - Sistema contable
3. **RRHH** - Recursos humanos
4. **Taller** - Gestión de taller
5. **Inventario** - Control de inventario
6. **GPS** - Seguimiento GPS
7. **Archivos** - Gestión de archivos
8. **Ajustes** - Configuración del sistema
9. **Salir** - Cerrar el launcher

## 🎨 Paleta de Colores

- **Fondo**: `#F3F4F6` (Gris claro)
- **Botones**: `#FFFFFF` (Blanco)
- **Header**: `#1F2937` (Gris oscuro)
- **Texto Principal**: `#1E40AF` (Azul oscuro)
- **Texto Secundario**: `#6B7280` (Gris medio)
- **Hover**: `#3B82F6` (Azul)
- **Footer**: `#F9FAFB` (Gris muy claro)

## 🔧 Configuración

### Agregar/Modificar Aplicaciones

Editar `APPS_CONFIG` en `launcher.py`:

```python
APPS_CONFIG = [
    {"name": "NombreApp", "exe": "app.exe", "icon": "icon_name"},
    # ...
]
```

### Firebase (Futuro)

La estructura en `firebase_config.py` está lista para implementar:
- Autenticación de usuarios
- Permisos por aplicación
- Configuración remota
- Sincronización de datos

## 📸 Capturas de Pantalla

### Splash Screen
![Loader](https://github.com/user-attachments/assets/01ff938b-0917-4be5-b5d3-2661a6818c02)

### Launcher Principal
![Launcher](https://github.com/user-attachments/assets/30e7910a-8a78-4fdc-b474-415687969453)

## 📝 Notas Técnicas

- Ventana sin bordes del sistema (frameless)
- Draggable: Se puede mover arrastrando cualquier parte
- Tamaño fijo: 380x450px (launcher), 400x250px (loader)
- Animación de progreso suave a 20 FPS
- Iconos dibujados con QPainter (sin dependencias externas)

## 🔜 Mejoras Futuras

- [ ] Implementación real de Firebase
- [ ] Iconos SVG personalizados
- [ ] Temas personalizables
- [ ] Notificaciones in-app
- [ ] Actualizaciones automáticas
- [ ] Estadísticas de uso

## 📄 Licencia

Propietario - ZOEC Civil
