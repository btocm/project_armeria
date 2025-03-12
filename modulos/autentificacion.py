import logging
from flask import render_template, request, redirect, url_for, session
from db import mysql

# Configuración del sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("im117_log.log", encoding="utf-8")  # Guardar logs en un archivo
        #logging.StreamHandler()  # Opcional: Mostrar logs en consola
    ]
)

# Catálogo de errores
CATALOGO_ERRORES = {
    "ErrorIM117_00": "Operación exitosa, no hubo errores.",
    "ErrorIM117_01": "Error al renderizar la página de inicio de sesión.",
    "ErrorIM117_02": "El usuario o contraseña son incorrectos.",
    "ErrorIM117_03": "Error al consultar la base de datos.",
    "ErrorIM117_04": "Error al cerrar sesión.",
}

# Rutas de autentificación
def rutas_autentificacion(app):

    # Ruta para mostrar el menú inicio de sesión
    @app.route('/')
    def index():
        try:
            logging.info(f"Se accedió a la página de inicio de sesión - {CATALOGO_ERRORES['ErrorIM117_00']}")
            return render_template('index.html')
        except Exception as e:
            logging.error(f"ErrorIM117_01: {CATALOGO_ERRORES['ErrorIM117_01']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_01: {CATALOGO_ERRORES['ErrorIM117_01']}")

    # Ruta para iniciar sesión
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            usuario = request.form['usuario']
            password = request.form['password']
            logging.info(f"Intento de inicio de sesión para el usuario: {usuario}")

            try:
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
                user = cur.fetchone()
                cur.close()
            except Exception as e:
                logging.error(f"ErrorIM117_03: {CATALOGO_ERRORES['ErrorIM117_03']} Detalle: {e}")
                return render_template('error.html', mensaje=f"ErrorIM117_03: {CATALOGO_ERRORES['ErrorIM117_03']}")

            if user and user['password'] == password:
                session['user'] = user
                logging.info(f"Inicio de sesión exitoso para el usuario: {usuario} con rol: {user['rol']} - {CATALOGO_ERRORES['ErrorIM117_00']}")

                # Redirección basada en el rol del usuario
                rutas_por_rol = {
                    'almacen': 'menu_almacen',
                    'mantenimiento': 'menu_mantenimiento',
                    'ventas': 'menu_ventas',
                    'proveedores': 'menu_proveedores',
                    'envios': 'menu_envios'
                }
                return redirect(url_for(rutas_por_rol.get(user['rol'], 'index')))
            else:
                logging.warning(f"ErrorIM117_02: {CATALOGO_ERRORES['ErrorIM117_02']} Usuario: {usuario}")
                return render_template('index.html', mensaje=f"ErrorIM117_02: {CATALOGO_ERRORES['ErrorIM117_02']}")

        return render_template('index.html')

    # Ruta para cerrar sesión
    @app.route('/logout', methods=['POST'])
    def logout():
        # try:
            if 'user' in session:
                usuario = session['user']['usuario']
                logging.info(f"El usuario {usuario} cerró sesión - {CATALOGO_ERRORES['ErrorIM117_00']}")
                session.pop('user', None)
            else:
                logging.warning(f"ErrorIM117_04: {CATALOGO_ERRORES['ErrorIM117_04']}")
                return render_template('error.html', mensaje=f"ErrorIM117_04: {CATALOGO_ERRORES['ErrorIM117_04']}")

            return redirect(url_for('index'))

    return app
