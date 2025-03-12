import logging
from flask import render_template, request, redirect, url_for
from db import mysql

# Configuración del sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Catálogo de errores
CATALOGO_ERRORES = {
    "ErrorIM117_00": "Operación exitosa, no hubo errores",
    "ErrorIM117_05": "Error al acceder al menú almacén",
    "ErrorIM117_06": "Error al consultar en la base de datos (buscar equipo).",
    "ErrorIM117_06.1": "Error al escribir en la base de datos (registrar un nuevo equipo).",
    "ErrorIM117_06.2": "Error al actualizar en la base de datos (actualizar info. del equipo).",
    "ErrorIM117_07": "Error: No se encontró el equipo solicitado."
}

# Rutas de almacén
def rutas_almacen(app):

    # Ruta para mostrar el menú del almacén
    @app.route('/menu_almacen')
    def menu_almacen():
        try:
            logging.info(f"Acceso al menú del almacén - {CATALOGO_ERRORES['ErrorIM117_00']}")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM armas")
            armas = cur.fetchall()
            cur.close()
        except Exception as e:
            logging.error(f"ErrorIM117_05: {CATALOGO_ERRORES['ErrorIM117_05']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_05: {CATALOGO_ERRORES['ErrorIM117_05']}")

        return render_template('menu_almacen.html', armas=armas)

    # Ruta para buscar equipo
    @app.route('/b_equipo', methods=['POST'])
    def buscarA():
        nombre_arma = request.form.get('nombre_arma') 
        logging.info(f"Búsqueda de equipo con nombre: {nombre_arma}")
        try:
            cursor = mysql.connection.cursor()

            # Consulta a la BD para obtener equipo por nombre
            consulta = """SELECT * FROM armas WHERE nombre_arma = %s"""
            cursor.execute(consulta, (nombre_arma,))
            arma = cursor.fetchone()
            cursor.close()
        except Exception as e:
            logging.error(f"ErrorIM117_06: {CATALOGO_ERRORES['ErrorIM117_06']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_06: {CATALOGO_ERRORES['ErrorIM117_06']}")

        if not arma:
            mensaje = f"ErrorIM117_07: {CATALOGO_ERRORES['ErrorIM117_07']}: {nombre_arma}"
            logging.warning(mensaje)
            return render_template('menu_almacen.html', mensaje=mensaje, arma=arma)

        logging.info(f"Equipo encontrado: {arma} - {CATALOGO_ERRORES['ErrorIM117_00']}")
        return render_template('menu_almacen.html', arma=arma)

    # Ruta para agregar un nuevo equipo
    @app.route('/nuevo_equipo', methods=['POST'])
    def nuevo_equipo():
        arma = request.form['nombre_arma']
        modelo = request.form['modelo']
        calibre = request.form['calibre']
        numSerie = request.form['numSerie']
        disparo = request.form['sistemaDisparo']
        materiales = request.form['materiales']
        peso = request.form['peso']
        costo = request.form['costo']
        
        logging.info(f"Intento de agregar nuevo equipo: {arma}, Modelo: {modelo}, Número de serie: {numSerie}")
        try:
            cur = mysql.connection.cursor()
            escribir = """INSERT INTO armas (nombre_arma, modelo, calibre, numSerie, sistemaDisparo, materiales, peso, costo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(escribir, (arma, modelo, calibre, numSerie, disparo, materiales, peso, costo))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            logging.error(f"ErrorIM117_06.1: {CATALOGO_ERRORES['ErrorIM117_06.1']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_06.1: {CATALOGO_ERRORES['ErrorIM117_06.1']}")

        logging.info(f"Nuevo equipo agregado: {arma}, Número de serie: {numSerie} - {CATALOGO_ERRORES['ErrorIM117_00']}")
        return redirect(url_for('menu_almacen'))
    
    # Ruta para editar equipo
    @app.route('/editar_equipo/<string:numSerie>', methods=['POST'])
    def editar_equipo(numSerie):
        try:
            arma = request.form['nombre_arma']
            modelo = request.form['modelo']
            calibre = request.form['calibre']
            disparo = request.form['sistemaDisparo']
            materiales = request.form['materiales']
            peso = request.form['peso']
            costo = request.form['costo']

            logging.info(f"Intento de editar equipo con número de serie: {numSerie}")
            cursor = mysql.connection.cursor()
            modificar = """UPDATE armas SET nombre_arma = %s, modelo = %s, calibre = %s, sistemaDisparo = %s, materiales = %s, peso = %s, costo = %s WHERE numSerie = %s"""
            cursor.execute(modificar, (arma, modelo, calibre, disparo, materiales, peso, costo, numSerie))
            mysql.connection.commit()
            cursor.close()

            logging.info(f"Equipo actualizado: {arma}, Número de serie: {numSerie} - {CATALOGO_ERRORES['ErrorIM117_00']}")
            return redirect(url_for('menu_almacen'))
        
        except Exception as e:
            logging.error(f"ErrorIM117_06.2: {CATALOGO_ERRORES['ErrorIM117_06.2']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_06.2: {CATALOGO_ERRORES['ErrorIM117_06.2']}")
        
    # Ruta para cambiar el estado del equipo
    @app.route('/cambiar_estadoA/<string:armas_numSerie>', methods=['POST'])
    def cambiar_estadoA(armas_numSerie):
        nuevo_estado = request.form['estado']
        logging.info(f"Intento de cambiar estado del equipo con número de serie: {armas_numSerie} a {nuevo_estado}")
        
        cur = mysql.connection.cursor()
        modificar = """UPDATE armas SET estado = %s WHERE numSerie = %s"""
        cur.execute(modificar, (nuevo_estado, armas_numSerie))
        mysql.connection.commit()
        cur.close()

        logging.info(f"Estado cambiado para el equipo con número de serie: {armas_numSerie} a {nuevo_estado} - {CATALOGO_ERRORES['ErrorIM117_00']}")
        return redirect(url_for('menu_almacen'))
    
    return app
