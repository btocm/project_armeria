from flask import redirect, render_template, request, send_file, url_for
from fpdf import FPDF

from db import mysql
from utils import Logger

from .reporte import ReporteFactory

log = Logger()


# Rutas de mantenimiento
def rutas_mantenimiento(app):

    # Ruta del menú de mantenimiento
    @app.route('/menu_mantenimiento')
    def menu_mantenimiento():
        try:
            log.log_info(pretext="Acceso al menu de mantenimiento", error="00")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM mantenimiento")
            datos = cur.fetchall()
            cur.close()
            return render_template('menu_mantenimiento.html', datos=datos)
        except Exception as e:
            log.log_error(error="05", posttext=e)
            return render_template('error.html')

    # Ruta para mostrar el formulario para una nueva solicitud de mantenimiento
    @app.route('/nueva_solicitud')
    def nueva_solicitud():
        try:
            log.log_info(pretext="Acceso al formulario de nueva solicitud", error="00")
            return render_template('reporte_mantenimiento.html')
        except Exception as e:
            log.log_error(error="05", posttext=e)
            return render_template('error.html')

    # Ruta para generar un reporte en PDF basado en un rango de fechas
    @app.route('/generar_reporte', methods=['POST'])
    def generar_reporte():
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        log.log_info(pretext=f"Generando reporte de mantenimiento desde {fecha_inicio} hasta {fecha_fin}")

        try:
            # Consulta a la base de datos
            cur = mysql.connection.cursor()
            consulta = """SELECT * FROM mantenimiento WHERE fecha BETWEEN %s AND %s"""
            cur.execute(consulta, (fecha_inicio, fecha_fin))
            registros = cur.fetchall()
            cur.close()
            log.log_info(pretext=f"Se encontraron {len(registros)} registros para el rango de fechas proporcionado")
        except Exception as e:
            log.log_error(error="10", posttext=e)
            return render_template('error.html')

        try:
            reporte = ReporteFactory.crear_reporte("mantenimiento")
            pdf = reporte.generar(registros)

            pdf_path = 'reporte_mantenimiento.pdf'
            pdf.output(pdf_path)
            log.log_info(pretext=f"PDF generado exitosamente: {pdf_path}", error="00")

            # Descargar el archivo PDF
            return send_file(pdf_path, as_attachment=True)

        except Exception as e:
            log.log_error(error="11", posttext=e)
            return render_template('error.html')

        # return render_template('reporte_mantenimiento.html')
