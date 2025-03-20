import logging
import threading

CATALOGO_ERRORES = {
    "00": "Operación exitosa, no hubo errores.",
    "01": "Error al renderizar la página de inicio de sesión.",
    "02": "El usuario o contraseña son incorrectos.",
    "03": "Error al consultar la base de datos.",
    "04": "Error al cerrar sesión.",
    "05": "Error al acceder al menú almacén",
    "06": "Error al consultar en la base de datos (buscar equipo).",
    "06.1": "Error al escribir en la base de datos (registrar un nuevo equipo).",
    "06.2": "Error al actualizar en la base de datos (actualizar info. del equipo).",
    "07": "Error: No se encontró el equipo solicitado.",
    "08": "Error al acceder al menú mantenimiento.",
    "09": "Error al renderizar el formulario de nueva solicitud.",
    "10": "Error al generar el reporte de mantenimiento.",
    "11": "Error al generar el archivo PDF.",
    "12": "Error al acceder al menú de ventas.",
    "13": "Error al renderizar el formulario de reporte de ventas.",
    "14": "Error al generar reporte de ventas.",
    "11": "Error al generar el archivo PDF.",
    "15": "Error al generar la gráfica de ventas.",
    "16": "Error al acceder al menú proveedores.",
    "17": "Error al escribir en la base de datos (registrar un nuevo pedido).",
    "17.1": "Error al consultar en la base de datos (buscar un pedido).",
    "18": "Error al acceder al menú envíos.",
    "19": "Error al escribir en la base de datos (registrar un nuevo envío).",
    "19.1": "Error al actualizar en la base de datos (cambiar estado del envío).",
    "19.2": "Error al consultar en la base de datos (buscar envío).",
    "20": "No se encontró el envío con el ID especificado."
}


class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        # Verificar si hay una instancia creada
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - $(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(
                    "im117_log.log", encoding="utf-8")
            ])

    def log_error(self, error: int, pretext: str = None, posttext: str = None):
        logging.error(f'ErrorIM117_{error}: {
                      CATALOGO_ERRORES[str(error)]} Detalle: {posttext}')

    def lof_info(self, error: int, pretext: str = None, posttext: str = None):
        logging.info(f'{pretext}')

    # def get_error_title(self, error):
    #     for key, value in CATALOGO_ERRORES.items():
    #         if error == int(key):
    #             return CATALOGO_ERRORES[key]
