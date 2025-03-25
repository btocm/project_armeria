from flask import redirect, render_template, request, url_for

from db import mysql
from utils import Logger

log = Logger()


# Rutas de almacén
def rutas_almacen(app):

    # Ruta para mostrar el menú del almacén
    @app.route('/menu_almacen')
    def menu_almacen():
        try:
            log.log_info(pretext="Acceso al menu del almacen", error="00")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM armas")
            armas = cur.fetchall()
            cur.close()
        except Exception as e:
            log.log_error(error="05", posttext=e)
            return render_template('error.html')

        return render_template('menu_almacen.html', armas=armas)

    # Ruta para buscar equipo
    @app.route('/b_equipo', methods=['POST'])
    def buscarA():
        nombre_arma = request.form.get('nombre_arma')
        log.log_info(pretext=f"Busqueda del equipo con nombre {nombre_arma}")
        try:
            cursor = mysql.connection.cursor()

            # Consulta a la BD para obtener equipo por nombre
            consulta = """SELECT * FROM armas WHERE nombre_arma = %s"""
            cursor.execute(consulta, (nombre_arma,))
            arma = cursor.fetchone()
            cursor.close()
        except Exception as e:
            log.log_error(error="06", posttext=e)
            return render_template('error.html')

        if not arma:
            log.log_warning(error="07")
            return render_template('menu_almacen.html')
        log.log_info(error="00", pretext=f"Equipo encontrado: {arma}")
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

        log.log_info(pretext="Intento de agregar nuevo equipo: {arma}, Modelo: {modelo}, N.serie: {numSerie}")
        try:
            cur = mysql.connection.cursor()
            escribir = """INSERT INTO armas (nombre_arma, modelo, calibre, numSerie, sistemaDisparo, materiales, peso, costo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(escribir, (arma, modelo, calibre, numSerie, disparo, materiales, peso, costo))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            log.log_error(error="06.1", posttext=e)
            return render_template('error.html')

        log.log_info(pretext=f"Nuevo equipo agregado: {arma}, Número de serie: {numSerie}")
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

            log.log_info(pretext="Intento de editar equipo con numero de serie: {numSerie}")
            cursor = mysql.connection.cursor()
            modificar = """UPDATE armas SET nombre_arma = %s, modelo = %s, calibre = %s, sistemaDisparo = %s, materiales = %s, peso = %s, costo = %s WHERE numSerie = %s"""
            cursor.execute(modificar, (arma, modelo, calibre, disparo, materiales, peso, costo, numSerie))
            mysql.connection.commit()
            cursor.close()

            log.log_info(pretext=f"Equipo actualizado: {arma}, Número de serie: {numSerie}")
            return redirect(url_for('menu_almacen'))

        except Exception as e:
            log.log_error(error="06.2", posttext=e)
            return render_template('error.html')

    # Ruta para cambiar el estado del equipo
    @app.route('/cambiar_estadoA/<string:armas_numSerie>', methods=['POST'])
    def cambiar_estadoA(armas_numSerie):
        nuevo_estado = request.form['estado']
        log.log_info(
            pretext=f"Intento de cambiar estado del equipo con número de serie: {armas_numSerie} a {nuevo_estado}"
        )

        cur = mysql.connection.cursor()
        modificar = """UPDATE armas SET estado = %s WHERE numSerie = %s"""
        cur.execute(modificar, (nuevo_estado, armas_numSerie))
        mysql.connection.commit()
        cur.close()

        log.log_info(
            pretext=f"Estado cambiado para el equipo con número de serie: {armas_numSerie} a {nuevo_estado}", error="00"
        )
        return redirect(url_for('menu_almacen'))

    return app
