from abc import ABC, abstractmethod
from fpdf import FPDF

class Reporte(ABC):
    def get_base_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(200, 10, 'Reporte de Ventas', 0, 1, 'C')
        pdf.ln(10)
        return pdf
    
    @abstractmethod
    def generar(self, datos):
        pass

class ReporteMantenimiento(Reporte):
    def generar(self, datos):
        pdf = self.get_base_pdf()
        pdf.cell(200, 10, 'Reporte de Mantenimiento', 0, 1, 'C')
        
        # Datos especificos del reporte de Mantenimiento
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(10, 10, 'ID', 1)
        pdf.cell(26, 10, 'Nombre Arma', 1)
        pdf.cell(35, 10, 'Tipo Servicio', 1)
        pdf.cell(85, 10, 'Descripcion Falla', 1)
        pdf.cell(20, 10, 'Fecha', 1)
        pdf.ln()

        # Generar datos
        pdf.set_font('Arial', '', 8)
        for registro in datos:
            pdf.cell(10, 10, str(registro['id']), 1)
            pdf.cell(26, 10, registro['nombreA'] if registro['nombreA'] else 'N/A', 1)
            pdf.cell(35, 10, registro['tipoServicio'] if registro['tipoServicio'] else 'N/A', 1)
            pdf.cell(85, 10, registro['descripcionFalla'] if registro['descripcionFalla'] else 'N/A', 1)
            pdf.cell(20, 10, registro['fecha'].strftime('%Y-%m-%d') if registro['fecha'] else 'N/A', 1)
            pdf.ln()

        return pdf

class ReporteVentas(Reporte):
    def generar(self, datos):
        pdf = self.get_base_pdf()
        pdf.cell(200, 10, 'Reporte de Ventas', 0, 1, 'C')

        # Datos especificos del reporte de Mantenimiento
        pdf.cell(10, 12, 'ID', 1, 0, 'C')
        pdf.cell(20, 12, 'Fecha', 1, 0, 'C')
        pdf.cell(25, 12, 'Num Serie', 1, 0, 'C')
        pdf.cell(20, 12, 'Cantidad', 1, 0, 'C')
        pdf.cell(27, 12, 'Precio Unitario', 1, 0, 'C')
        pdf.cell(20, 12, 'Total', 1, 0, 'C')
        pdf.cell(32, 12, 'Metodo Pago', 1, 0, 'C')
        pdf.ln()

        # Generar datos 
        pdf.set_font('Arial', '', 8)
        for registro in datos:
            pdf.cell(10, 12, str(registro['id_venta']), 1, 0, 'C')
            pdf.cell(20, 12, registro['fecha'].strftime('%Y-%m-%d') if registro['fecha'] else 'N/A', 1, 0, 'C')
            pdf.cell(25, 12, registro['numSerie'] if registro['numSerie'] else 'N/A', 1, 0, 'C')
            pdf.cell(20, 12, str(registro['cantidad']), 1, 0, 'C')
            pdf.cell(27, 12, str(registro['precio_unitario']), 1, 0, 'C')
            pdf.cell(20, 12, str(registro['total']), 1, 0, 'C')
            pdf.cell(32, 12, registro['metodo_pago'] if registro['metodo_pago'] else 'N/A', 1, 0, 'C')
            pdf.ln()
        return pdf

class ReporteFactory:
    @staticmethod
    def crear_reporte(tipo: str) -> Reporte:
        if tipo == "mantenimiento":
            return ReporteMantenimiento()
        elif tipo == "ventas":
            return ReporteVentas()
        else:
            raise ValueError(f"Tipo de reporte desconocido: {tipo}")