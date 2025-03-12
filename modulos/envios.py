import logging
from flask import render_template, request, redirect, send_file, url_for
from db import mysql

# Configuración del sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Catálogo de errores
CATALOGO_ERRORES = {
    "ErrorIM117_00": "Operación exitosa, no hubo errores.",
    "ErrorIM117_18": "Error al acceder al menú envíos.",
    "ErrorIM117_19": "Error al escribir en la base de datos (registrar un nuevo envío).",
    "ErrorIM117_19.1": "Error al actuaizar en la base de datos (cambiar estado del envío).",
    "ErrorIM117_19.2": "Error al consultar en la base de datos (buscar envío).",
    "ErrorIM117_20": "No se encontró el envío con el ID especificado."
}

# Ruta de envíos
def rutas_envios(app):

    # Ruta para el menú de envíos
    @app.route('/menu_envios')
    def menu_envios():
        try:
            logging.info(f"Acceso al menú de envíos - {CATALOGO_ERRORES['ErrorIM117_00']}")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM envios")
            envios = cur.fetchall()
            cur.close()
            return render_template('menu_envios.html', envios=envios)
        except Exception as e:
            logging.error(f"ErrorIM117_18: {CATALOGO_ERRORES['ErrorIM117_18']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_18: {CATALOGO_ERRORES['ErrorIM117_18']}")

    # Ruta para registrar un nuevo envío
    @app.route('/nuevo_envio', methods=['POST'])
    def nuevo_envio():
        nombre_cliente = request.form['nombre_cliente']
        cantidad_arma = request.form['cantidad_arma']
        direccion = request.form['direccion']
        fecha = request.form['fecha']

        logging.info(f"Intento de agregar nuevo envío: Cliente: {nombre_cliente}, Fecha: {fecha}")
        try:
            cur = mysql.connection.cursor()
            escribir = """INSERT INTO envios (nombre_cliente, cantidad_arma, direccion, fecha) VALUES (%s, %s, %s, %s)"""
            cur.execute(escribir, (nombre_cliente, cantidad_arma, direccion, fecha))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            logging.error(f"ErrorIM117_19: {CATALOGO_ERRORES['ErrorIM117_19']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_19: {CATALOGO_ERRORES['ErrorIM117_19']}")

        logging.info(f"Nuevo envío registrado para el cliente: {nombre_cliente}, Fecha: {fecha} - {CATALOGO_ERRORES['ErrorIM117_00']}")
        return redirect(url_for('menu_envios'))

    # Ruta para cambiar el estado de un envío
    @app.route('/cambiar_estado/<int:envio_id>', methods=['POST'])
    def cambiar_estado(envio_id):
        nuevo_estado = request.form['estado']
        logging.info(f"Intento de cambiar estado del envío con ID: {envio_id} a {nuevo_estado}")
        try:
            cur = mysql.connection.cursor()
            modificar = """UPDATE envios SET estado = %s WHERE id = %s"""
            cur.execute(modificar, (nuevo_estado, envio_id))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            logging.error(f"ErrorIM117_19.1: {CATALOGO_ERRORES['ErrorIM117_19.1']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_19.1: {CATALOGO_ERRORES['ErrorIM117_19.1']}")

        logging.info(f"Estado del envío con ID: {envio_id} actualizado a {nuevo_estado} - {CATALOGO_ERRORES['ErrorIM117_00']}")
        return redirect(url_for('menu_envios'))

    # Ruta para buscar un envío por su ID
    @app.route('/b_envio', methods=['POST'])
    def buscarE():
        envio_id = request.form.get('id')
        logging.info(f"Búsqueda de envío con ID: {envio_id}")
        try:
            cursor = mysql.connection.cursor()
            consulta = """SELECT * FROM envios WHERE id = %s"""
            cursor.execute(consulta, (envio_id,))
            envio = cursor.fetchone()
            cursor.close()
        except Exception as e:
            logging.error(f"ErrorIM117_19.2: {CATALOGO_ERRORES['ErrorIM117_19.2']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_19.2: {CATALOGO_ERRORES['ErrorIM117_19.2']}")

        if not envio:
            mensaje = f"ErrorIM117_20: {CATALOGO_ERRORES['ErrorIM117_20']}"
            logging.warning(mensaje)
            return render_template('menu_envios.html', mensaje=mensaje, envio=None)

        logging.info(f"Envío encontrado con ID: {envio_id} - {CATALOGO_ERRORES['ErrorIM117_00']}")
        return render_template('menu_envios.html', envio=envio)

    return app
