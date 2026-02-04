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


class LauncherBtn:
    # existing methods...
    def _create_icon(self, icon_name):
        if icon_name == "construction":
            # Draw a construction helmet and crane
            pass
        elif icon_name == "truck":
            # Draw a truck/heavy vehicle
            pass
        elif icon_name == "receipt":
            # Draw a receipt/document with lines
            pass
        elif icon_name == "business":
            # Draw a business building with windows
            pass
        elif icon_name == "calculator":
            # Draw a calculator with buttons
            pass
        elif icon_name == "folder":
            # Draw a folder icon
            pass

    def _launch_program(self, program_name):
        locations = ["./", "apps/", "../", "../apps/"]
        for location in locations:
            # Search for executables in each location
            pass
    # existing methods...