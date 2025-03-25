from flask import redirect, render_template, request, send_file, url_for

from db import mysql
from utils import Logger

log = Logger()


# Rutas de proveedores
def rutas_proveedores(app):

    # Ruta del menú de proveedores
    @app.route('/menu_proveedores')
    def menu_proveedores():
        try:
            log.log_info(pretext="Acceso al menu de proveedores", error="00")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM pedidos")
            pedidos = cur.fetchall()
            cur.close()
            return render_template('menu_proveedores.html', pedidos=pedidos)
        except Exception as e:
            log.log_error(error="05", posttext=e)
            return render_template('error.html')

    # Ruta para registrar un nuevo pedido
    @app.route('/nuevo_pedido', methods=['POST'])
    def nuevo_pedido():
        try:
            equipo = request.form['equipo']
            cantidad = request.form['cantidad']
            proveedor = request.form['proveedor']
            fecha = request.form['fecha']
            comentarios = request.form['comentarios']

            log.log_info(
                pretext=f"Intento de agregar nuevo pedido: Equipo: {equipo}, Cantidad: {cantidad}, Proveedor: {proveedor}, Fecha: {fecha}"
            )
            cur = mysql.connection.cursor()
            escribir = (
                """INSERT INTO pedidos (equipo, cantidad, proveedor, fecha, comentarios) VALUES (%s, %s, %s, %s, %s)"""
            )
            cur.execute(escribir, (equipo, cantidad, proveedor, fecha, comentarios))
            mysql.connection.commit()
            cur.close()

            log.log_info(pretext=f"Nuevo pedido registrado para el proveedor: {proveedor}, Fecha: {fecha}", error="00")
            return redirect(url_for('menu_proveedores'))
        except Exception as e:
            log.log_error(error="06", posttext=e)
            return render_template('error.html')

    # Ruta para buscar un pedido por su ID
    @app.route('/buscar', methods=['POST'])
    def buscar():
        pedido_id = request.form.get('id')
        log.log_info(pretext=f"Búsqueda de pedido con ID: {pedido_id}")

        cursor = mysql.connection.cursor()

        consulta = """SELECT * FROM pedidos WHERE id = %s"""
        cursor.execute(consulta, (pedido_id,))
        pedido = cursor.fetchone()
        cursor.close()

        if not pedido:
            log.log_warning(error="17.1", posttext=f"Pedido ID: {pedido_id}")
            return render_template('menu_proveedores.html')

        log.log_info(f"Pedido encontrado con ID: {pedido_id}", error="00")
        return render_template('menu_proveedores.html', pedido=pedido)

    return app
