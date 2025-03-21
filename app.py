import os

from dotenv import load_dotenv
from flask import Flask

from db import mysql
from modulos.almacen import rutas_almacen
from modulos.autentificacion import rutas_autentificacion
from modulos.envios import rutas_envios
from modulos.mantenimineto import rutas_mantenimiento
from modulos.proveedores import rutas_proveedores
from modulos.ventas import rutas_ventas
from utils import Logger

load_dotenv()

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Configuración de la base de datos
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER", "root")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD", "")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB", "im117")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT", 3306))

Logger()
# Iniciar conexión a la base de datos
mysql.init_app(app)

# Registro de las rutas de cada módulo
rutas_autentificacion(app)
rutas_almacen(app)
rutas_mantenimiento(app)
rutas_ventas(app)
rutas_proveedores(app)
rutas_envios(app)

if __name__ == "__main__":
    app.run(debug=True)
