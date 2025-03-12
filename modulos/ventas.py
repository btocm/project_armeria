import logging
from flask import render_template, request, redirect, send_file, url_for
from fpdf import FPDF
from db import mysql

# Importaciones para análisis de datos y generación de gráficas
import matplotlib
import pandas as pd  # Biblioteca para manipulación de datos
import numpy as np  # Biblioteca para cálculos numéricos
import matplotlib.pyplot as plt  # Herramienta para generar gráficas
matplotlib.use('Agg')  # Configuración para usar matplotlib sin entorno gráfico
from sklearn.linear_model import LinearRegression  # Para análisis de regresión lineal
import io  # Para manejar datos en memoria
import base64  # Para codificar imágenes en base64

# Configuración del sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

CATALOGO_ERRORES = {
    "ErrorIM117_00": "Operación exitosa, no hubo errores.",
    "ErrorIM117_12": "Error al acceder al menú de ventas.",
    "ErrorIM117_13": "Error al renderizar el formulario de reporte de ventas.",
    "ErrorIM117_14": "Error al generar reporte de ventas.",
    "ErrorIM117_11": "Error al generar el archivo PDF.",
    "ErrorIM117_15": "Error al generar la gráfica de ventas."
}

# Rutas de ventas
def rutas_ventas(app):
    # Ruta de menú de ventas
    @app.route('/menu_ventas')
    def menu_ventas():
        try:
            logging.info(f"Acceso al menú de ventas - {CATALOGO_ERRORES['ErrorIM117_00']}")
            cur = mysql.connection.cursor()

            consulta = """
                SELECT armas.nombre_arma AS nombre_arma, SUM(ventas.cantidad) AS total_cantidad
                FROM ventas
                INNER JOIN armas ON ventas.numSerie = armas.numSerie
                GROUP BY armas.nombre_arma
                ORDER BY total_cantidad DESC
            """
            cur.execute(consulta)
            resultados = cur.fetchall()
            cur.close()

            if resultados:
                arma_mas_vendida = resultados[0]['nombre_arma']
                arma_menos_vendida = resultados[-1]['nombre_arma']
            else:
                arma_mas_vendida = "No hay ventas registradas"
                arma_menos_vendida = "No hay ventas registradas"

            return render_template(
                'menu_ventas.html',
                arma_mas_vendida=arma_mas_vendida,
                arma_menos_vendida=arma_menos_vendida
            )
        except Exception as e:
            logging.error(f"ErrorIM117_12: {CATALOGO_ERRORES['ErrorIM117_12']} Detalle: {e}")
            return render_template('error.html', mensaje=CATALOGO_ERRORES['ErrorIM117_12'])

    # Ruta para mostrar el formulario de creación de reportes
    @app.route('/nuevo_reporteV')
    def nuevo_reporteV():
        try:
            logging.info("Acceso al formulario de creación de reportes de ventas")
            return render_template('reporte_ventas.html')
        except Exception as e:
            logging.error(f"ErrorIM117_13: {CATALOGO_ERRORES['ErrorIM117_13']} Detalle: {e}")
            return render_template('error.html', mensaje=CATALOGO_ERRORES['ErrorIM117_13'])

    # Ruta para generar un reporte de ventas en PDF
    @app.route('/generar_reporte_ventas', methods=['POST'])
    def generar_reporte_ventas():
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        logging.info(f"Generando reporte de ventas desde {fecha_inicio} hasta {fecha_fin}")

        try:
            # Consulta a la base de datos para obtener registros dentro del rango de fechas
            cur = mysql.connection.cursor()
            consulta = """SELECT * FROM ventas WHERE fecha BETWEEN %s AND %s"""
            cur.execute(consulta, (fecha_inicio, fecha_fin))
            registros = cur.fetchall()

            # Calcular el total de ventas sumando los valores de la columna 'total'
            total_ventas = sum([registro['total'] for registro in registros])
            cur.close()
        except Exception as e:
            logging.error(f"ErrorIM117_14: {CATALOGO_ERRORES['ErrorIM117_14']} Detalle: {e}")
            return render_template('error.html', mensaje=CATALOGO_ERRORES['ErrorIM117_14'])

        try:
            # Generar un archivo PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(200, 10, 'Reporte de Ventas', 0, 1, 'C')
            pdf.ln(10)

            # Agregar encabezados en la tabla 
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(10, 12, 'ID', 1, 0, 'C')
            pdf.cell(20, 12, 'Fecha', 1, 0, 'C')
            pdf.cell(25, 12, 'Num Serie', 1, 0, 'C')
            pdf.cell(20, 12, 'Cantidad', 1, 0, 'C')
            pdf.cell(27, 12, 'Precio Unitario', 1, 0, 'C')
            pdf.cell(20, 12, 'Total', 1, 0, 'C')
            pdf.cell(32, 12, 'Metodo Pago', 1, 0, 'C')
            pdf.ln()

            # Agregar datos de las ventas al PDF
            pdf.set_font('Arial', '', 8)
            for registro in registros:
                pdf.cell(10, 12, str(registro['id_venta']), 1, 0, 'C')
                pdf.cell(20, 12, registro['fecha'].strftime('%Y-%m-%d') if registro['fecha'] else 'N/A', 1, 0, 'C')
                pdf.cell(25, 12, registro['numSerie'] if registro['numSerie'] else 'N/A', 1, 0, 'C')
                pdf.cell(20, 12, str(registro['cantidad']), 1, 0, 'C')
                pdf.cell(27, 12, str(registro['precio_unitario']), 1, 0, 'C')
                pdf.cell(20, 12, str(registro['total']), 1, 0, 'C')
                pdf.cell(32, 12, registro['metodo_pago'] if registro['metodo_pago'] else 'N/A', 1, 0, 'C')
                pdf.ln()
            
            # Agregar el total de ventas
            pdf.ln(10)
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(200, 12, f'Total de Ventas: ${total_ventas:.2f}', 0, 1, 'C')

            # Guardar PDF temporalmente
            pdf_path = 'reporte_ventas.pdf'
            pdf.output(pdf_path)
            logging.info(f"PDF generado exitosamente: {pdf_path} - {CATALOGO_ERRORES['ErrorIM117_00']}")

            # Descargar el archivo PDF
            return send_file(pdf_path, as_attachment=True)

        except Exception as e:
            logging.error(f"ErrorIM117_11: {CATALOGO_ERRORES['ErrorIM117_11']} Detalle: {e}")
            return render_template('error.html', mensaje=CATALOGO_ERRORES['ErrorIM117_11'])
        
        #return render_template('reporte_ventas.html')

    # Ruta para generar una gráfica de ventas
    @app.route('/generar_grafica', methods=['POST'])
    def generar_grafica():
        try:
            # Obtener el año (fecha) desde el formulario
            year = request.form['year']

            # Consulta a la base de datos para obtener ventas del año (fecha) especificado
            cur = mysql.connection.cursor()
            consulta = """SELECT fecha, total FROM ventas WHERE YEAR(fecha) = %s"""
            cur.execute(consulta, (year,))
            registros = cur.fetchall()
            cur.close()

            # Verificar si hay datos para generar la gráfica
            if not registros:
                logging.warning(f"No se encontraron datos de ventas para el año {year}")
                return render_template('grafica_ventas.html', error=f"No hay datos disponibles para el año {year}", year=year)

            # Convertir los registros en un DataFrame de pandas
            data = pd.DataFrame(registros, columns=['fecha', 'total'])

            # Convertir la columna 'fecha' a datetime
            data['fecha'] = pd.to_datetime(data['fecha'])

            # Extraer el mes y agrupar las ventas por mes
            data['mes'] = data['fecha'].dt.month

            # Agrupar los datos por mes y sumar las ventas
            monthly_sales = data.groupby('mes')['total'].sum().reset_index()

            # Generar la gráfica
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(monthly_sales['mes'], monthly_sales['total'], marker='o', linestyle='-', color='b')
            ax.set_title(f'Ventas Mensuales - {year}')
            ax.set_xlabel('Mes')
            ax.set_ylabel('Total de Ventas')
            ax.set_xticks(range(1, 13))
            ax.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
            ax.grid(True)

            # Guardar la gráfica en un objeto en memoria
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            graph_url = base64.b64encode(img.getvalue()).decode()

            # Cerrar la figura
            plt.close(fig)

            logging.info(f"Gráfica generada exitosamente - {CATALOGO_ERRORES['ErrorIM117_00']}")
            return render_template('grafica_ventas.html', graph_url=graph_url, year=year)
        except Exception as e:
            logging.error(f"ErrorIM117_15: {CATALOGO_ERRORES['ErrorIM117_15']} Detalle: {e}")
            return render_template('error.html', mensaje=CATALOGO_ERRORES['ErrorIM117_15'])

    return app
