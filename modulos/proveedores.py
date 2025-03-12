import logging
from flask import render_template, request, redirect, send_file, url_for
from db import mysql

# Configuración del sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

CATALOGO_ERRORES = {
    "ErrorIM117_00": "Operación exitosa, no hubo errores.",
    "ErrorIM117_16": "Error al acceder al menú proveedores.",
    "ErrorIM117_17": "Error al escribir en la base de datos (registrar un nuevo pedido).",
    "ErrorIM117_17.1": "Error al consultar en la base de datos (buscar un pedido).",
}

# Rutas de proveedores
def rutas_proveedores(app):

    # Ruta del menú de proveedores
    @app.route('/menu_proveedores')
    def menu_proveedores():
        try:
            logging.info(f"Acceso al menú de proveedores - {CATALOGO_ERRORES['ErrorIM117_00']}")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM pedidos")
            pedidos = cur.fetchall()
            cur.close()
            return render_template('menu_proveedores.html', pedidos=pedidos)
        except Exception as e:
            logging.error(f"ErrorIM117_16: {CATALOGO_ERRORES['ErrorIM117_16']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_16: {CATALOGO_ERRORES['ErrorIM117_16']}")

    # Ruta para registrar un nuevo pedido
    @app.route('/nuevo_pedido', methods=['POST'])
    def nuevo_pedido():
        try:
            equipo = request.form['equipo']
            cantidad = request.form['cantidad']
            proveedor = request.form['proveedor']
            fecha = request.form['fecha']
            comentarios = request.form['comentarios']

            logging.info(f"Intento de agregar nuevo pedido: Equipo: {equipo}, Cantidad: {cantidad}, Proveedor: {proveedor}, Fecha: {fecha}")
            cur = mysql.connection.cursor()
            escribir = """INSERT INTO pedidos (equipo, cantidad, proveedor, fecha, comentarios) VALUES (%s, %s, %s, %s, %s)"""
            cur.execute(escribir, (equipo, cantidad, proveedor, fecha, comentarios))
            mysql.connection.commit()
            cur.close()

            logging.info(f"Se registró un nuevo pedido: Proveedor: {proveedor}, Fecha: {fecha} - {CATALOGO_ERRORES['ErrorIM117_00']}")
            return redirect(url_for('menu_proveedores'))
        except Exception as e:
            logging.error(f"ErrorIM117_17: {CATALOGO_ERRORES['ErrorIM117_17']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_17: {CATALOGO_ERRORES['ErrorIM117_17']}")

    # Ruta para buscar un pedido por su ID
    @app.route('/buscar', methods=['POST'])
    def buscar():
        pedido_id = request.form.get('id')
        logging.info(f"Búsqueda de pedido con ID: {pedido_id}")

        cursor = mysql.connection.cursor()

        consulta = """SELECT * FROM pedidos WHERE id = %s"""
        cursor.execute(consulta, (pedido_id,))
        pedido = cursor.fetchone()
        cursor.close()

        if not pedido:
            mensaje = f"No se encontró ningún pedido con el ID {pedido_id}."
            logging.warning(f"ErrorIM117_17.1: {CATALOGO_ERRORES['ErrorIM117_17.1']} Detalle: Pedido ID: {pedido_id}")
            return render_template('menu_proveedores.html', mensaje=mensaje)

        logging.info(f"Pedido encontrado con ID: {pedido_id} - {CATALOGO_ERRORES['ErrorIM117_00']}")
        return render_template('menu_proveedores.html', pedido=pedido)
        
    return app
