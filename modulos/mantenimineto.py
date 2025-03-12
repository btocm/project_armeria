import logging
from flask import render_template, request, redirect, send_file, url_for
from fpdf import FPDF
from db import mysql

# Configuración del sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

CATALOGO_ERRORES = {
    "ErrorIM117_00": "Operación exitosa, no hubo errores.",
    "ErrorIM117_08": "Error al acceder al menú mantenimiento.",
    "ErrorIM117_09": "Error al renderizar el formulario de nueva solicitud.",
    "ErrorIM117_10": "Error al generar el reporte de mantenimiento.",
    "ErrorIM117_11": "Error al generar el archivo PDF."
}

# Rutas de mantenimiento
def rutas_mantenimiento(app):

    # Ruta del menú de mantenimiento
    @app.route('/menu_mantenimiento')
    def menu_mantenimiento():
        try:
            logging.info(f"Acceso al menú de mantenimiento - {CATALOGO_ERRORES['ErrorIM117_00']}")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM mantenimiento")
            datos = cur.fetchall()
            cur.close()
            return render_template('menu_mantenimiento.html', datos=datos)
        except Exception as e:
            logging.error(f"ErrorIM117_08: {CATALOGO_ERRORES['ErrorIM117_08']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_08: {CATALOGO_ERRORES['ErrorIM117_08']}")

    # Ruta para mostrar el formulario para una nueva solicitud de mantenimiento
    @app.route('/nueva_solicitud')
    def nueva_solicitud():
        try:
            logging.info(f"Acceso al formulario de nueva solicitud - {CATALOGO_ERRORES['ErrorIM117_00']}")
            return render_template('reporte_mantenimiento.html')
        except Exception as e:
            logging.error(f"ErrorIM117_09: {CATALOGO_ERRORES['ErrorIM117_09']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_09: {CATALOGO_ERRORES['ErrorIM117_09']}")

    # Ruta para generar un reporte en PDF basado en un rango de fechas
    @app.route('/generar_reporte', methods=['POST'])
    def generar_reporte():
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        logging.info(f"Generando reporte de mantenimiento desde {fecha_inicio} hasta {fecha_fin}")

        try:
            # Consulta a la base de datos
            cur = mysql.connection.cursor()
            consulta = """SELECT * FROM mantenimiento WHERE fecha BETWEEN %s AND %s"""
            cur.execute(consulta, (fecha_inicio, fecha_fin))
            registros = cur.fetchall()
            cur.close()
            logging.info(f"Se encontraron {len(registros)} registros para el rango de fechas proporcionado")
        except Exception as e:
            logging.error(f"ErrorIM117_10: {CATALOGO_ERRORES['ErrorIM117_10']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_10: {CATALOGO_ERRORES['ErrorIM117_10']}")

        try:
            # Generar el PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(200, 10, 'Reporte de Mantenimiento', 0, 1, 'C')
            pdf.ln(10)

            # Agregar encabezados
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(10, 10, 'ID', 1)
            pdf.cell(26, 10, 'Nombre Arma', 1)
            pdf.cell(35, 10, 'Tipo Servicio', 1)
            pdf.cell(85, 10, 'Descripcion Falla', 1)
            pdf.cell(20, 10, 'Fecha', 1)
            pdf.ln()

            # Agregar datos
            pdf.set_font('Arial', '', 8)
            for registro in registros:
                pdf.cell(10, 10, str(registro['id']), 1)
                pdf.cell(26, 10, registro['nombreA'] if registro['nombreA'] else 'N/A', 1)
                pdf.cell(35, 10, registro['tipoServicio'] if registro['tipoServicio'] else 'N/A', 1)
                pdf.cell(85, 10, registro['descripcionFalla'] if registro['descripcionFalla'] else 'N/A', 1)
                pdf.cell(20, 10, registro['fecha'].strftime('%Y-%m-%d') if registro['fecha'] else 'N/A', 1)
                pdf.ln()

            pdf_path = 'reporte_mantenimiento.pdf'
            pdf.output(pdf_path)
            logging.info(f"PDF generado exitosamente: {pdf_path} - {CATALOGO_ERRORES['ErrorIM117_00']}")
        
            # Descargar el archivo PDF
            return send_file(pdf_path, as_attachment=True)
        
        except Exception as e:
            logging.error(f"ErrorIM117_11: {CATALOGO_ERRORES['ErrorIM117_11']} Detalle: {e}")
            return render_template('error.html', mensaje=f"ErrorIM117_11: {CATALOGO_ERRORES['ErrorIM117_11']}")
    
        # return render_template('reporte_mantenimiento.html')
