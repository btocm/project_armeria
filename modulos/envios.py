from flask import redirect, render_template, request, send_file, url_for

from db import mysql
from utils import Logger

log = Logger()


# Ruta de envíos
def rutas_envios(app):

    # Ruta para el menú de envíos
    @app.route('/menu_envios')
    def menu_envios():
        try:
            log.log_info(pretext="Acceso al menu de envios", error="00")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM envios")
            envios = cur.fetchall()
            cur.close()
            return render_template('menu_envios.html', envios=envios)
        except Exception as e:
            log.log_error(error="05", posttext=e)
            return render_template('error.html')

    # Ruta para registrar un nuevo envío
    @app.route('/nuevo_envio', methods=['POST'])
    def nuevo_envio():
        nombre_cliente = request.form['nombre_cliente']
        cantidad_arma = request.form['cantidad_arma']
        direccion = request.form['direccion']
        fecha = request.form['fecha']

        log.log_info(pretext=f"Intento de agregar nuevo envío: Cliente: {nombre_cliente}, Fecha: {fecha}")
        try:
            cur = mysql.connection.cursor()
            escribir = (
                """INSERT INTO envios (nombre_cliente, cantidad_arma, direccion, fecha) VALUES (%s, %s, %s, %s)"""
            )
            cur.execute(escribir, (nombre_cliente, cantidad_arma, direccion, fecha))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            log.log_error(error="06", posttext=e)
            return render_template('error.html')

        log.log_info(pretext=f"Nuevo envío registrado para el cliente: {nombre_cliente}, Fecha: {fecha}", error="00")
        return redirect(url_for('menu_envios'))

    # Ruta para cambiar el estado de un envío
    @app.route('/cambiar_estado/<int:envio_id>', methods=['POST'])
    def cambiar_estado(envio_id):
        nuevo_estado = request.form['estado']
        log.log_info(pretext=f"Intento de cambiar estado del envío con ID: {envio_id} a {nuevo_estado}")
        try:
            cur = mysql.connection.cursor()
            modificar = """UPDATE envios SET estado = %s WHERE id = %s"""
            cur.execute(modificar, (nuevo_estado, envio_id))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            log.log_error(error="19.1", posttext=e)
            return render_template('error.html')

        log.log_info(pretext=f"Estado del envío con ID: {envio_id} actualizado a {nuevo_estado}", error="00")
        return redirect(url_for('menu_envios'))

    # Ruta para buscar un envío por su ID
    @app.route('/b_envio', methods=['POST'])
    def buscarE():
        envio_id = request.form.get('id')
        log.log_info(pretext=f"Busqueda del envío con ID {envio_id}")
        try:
            cursor = mysql.connection.cursor()
            consulta = """SELECT * FROM envios WHERE id = %s"""
            cursor.execute(consulta, (envio_id,))
            envio = cursor.fetchone()
            cursor.close()
        except Exception as e:
            log.log_error(error="19.2", posttext=e)
            return render_template('error.html')

        if not envio:
            log.log_warning(error="20")
            return render_template('menu_envios.html', envio=None)

        log.log_info(pretext=f"Envío encontrado con ID: {envio_id}", error="00")
        return render_template('menu_envios.html', envio=envio)

    return app
