"""
Generador de Certificados de Matrícula
SLEP Santa Corina
"""

from docx import Document
from datetime import datetime
import io


class GeneradorCertificado:
    """Clase para generar certificados de matrícula personalizados"""
    
    def __init__(self, template_path):
        """
        Inicializa el generador con la ruta del template
        
        Args:
            template_path (str): Ruta al archivo .docx template
        """
        self.template_path = template_path
    
    def generar_certificado(self, datos_estudiante, fecha_emision=None):
        """
        Genera un certificado de matrícula personalizado
        
        Args:
            datos_estudiante (dict): Diccionario con los datos del estudiante
                - nombre: Nombre completo
                - run: RUN formateado
                - establecimiento: Nombre del establecimiento
                - rbd: Código RBD
                - curso: Curso completo (ej: "6° básico C")
                - año: Año escolar
            fecha_emision (datetime, optional): Fecha de emisión del certificado
            
        Returns:
            io.BytesIO: Documento Word en memoria
        """
        # Cargar el template
        doc = Document(self.template_path)
        
        # Usar fecha actual si no se proporciona
        if fecha_emision is None:
            fecha_emision = datetime.now()
        
        # Formatear fecha
        fecha_formateada = self._formatear_fecha(fecha_emision)
        
        # Reemplazar en párrafos
        for para in doc.paragraphs:
            self._reemplazar_en_texto(para, datos_estudiante, fecha_formateada)
        
        # Reemplazar en tablas (si las hay)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        self._reemplazar_en_texto(para, datos_estudiante, fecha_formateada)
        
        # Guardar en memoria
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        return buffer
    
    def _reemplazar_en_texto(self, para, datos, fecha):
        """
        Reemplaza los placeholders en un párrafo
        
        Args:
            para: Párrafo de python-docx
            datos (dict): Datos del estudiante
            fecha (str): Fecha formateada
        """
        # Obtener el texto completo del párrafo
        texto_original = para.text
        
        # Lista de reemplazos a realizar
        reemplazos = {
            'SOFIA MENDEZ FLOREZ': datos.get('nombre', '').upper(),
            '27.571.150-0': datos.get('run', ''),
            'ESCUELA CARLOS CONDELL DE LA HAZA': datos.get('establecimiento', '').upper(),
            '8521': str(datos.get('rbd', '')),
            '6° básico C': datos.get('curso', ''),
            '2026': str(datos.get('año', 2026)),
            '20 de enero del 2026': fecha
        }
        
        # Aplicar reemplazos
        texto_nuevo = texto_original
        for viejo, nuevo in reemplazos.items():
            if viejo in texto_nuevo:
                texto_nuevo = texto_nuevo.replace(viejo, str(nuevo))
        
        # Si hubo cambios, actualizar el párrafo manteniendo el formato
        if texto_nuevo != texto_original:
            # Guardar el formato del primer run
            if para.runs:
                formato_original = {
                    'bold': para.runs[0].bold,
                    'italic': para.runs[0].italic,
                    'underline': para.runs[0].underline,
                    'font_name': para.runs[0].font.name if para.runs[0].font.name else None,
                    'font_size': para.runs[0].font.size
                }
                
                # Limpiar el párrafo
                for run in para.runs:
                    run.text = ''
                
                # Añadir el texto nuevo con el formato original
                nuevo_run = para.runs[0] if para.runs else para.add_run()
                nuevo_run.text = texto_nuevo
                
                # Aplicar formato
                if formato_original.get('bold'):
                    nuevo_run.bold = True
                if formato_original.get('italic'):
                    nuevo_run.italic = True
                if formato_original.get('underline'):
                    nuevo_run.underline = True
                if formato_original.get('font_name'):
                    nuevo_run.font.name = formato_original['font_name']
                if formato_original.get('font_size'):
                    nuevo_run.font.size = formato_original['font_size']
    
    def _formatear_fecha(self, fecha):
        """
        Formatea una fecha para el certificado
        
        Args:
            fecha (datetime): Fecha a formatear
            
        Returns:
            str: Fecha formateada (ej: "20 de enero del 2026")
        """
        meses = {
            1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
            5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
            9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
        }
        
        dia = fecha.day
        mes = meses[fecha.month]
        año = fecha.year
        
        return f"{dia} de {mes} del {año}"
    
    @staticmethod
    def preparar_datos_estudiante(row):
        """
        Prepara los datos de un estudiante desde un DataFrame row
        
        Args:
            row: Fila de pandas DataFrame
            
        Returns:
            dict: Datos formateados para el certificado
        """
        from utils import formatear_run, formatear_curso
        
        # Formatear RUN con DV
        run_formateado = formatear_run(row['SAL_RUN'])
        
        # Formatear curso
        curso = formatear_curso(
            row['COD_GRADO_GLOSA_PRE'],
            row['LET_CUR_PRE']
        )
        
        return {
            'nombre': row.get('NOMBRE_ESTUDIANTE', 'NOMBRE NO DISPONIBLE'),
            'run': run_formateado,
            'establecimiento': row['NOM_RBD'],
            'rbd': row['RBD_PRE'],
            'curso': curso,
            'año': row['ANO_ESCOLAR']
        }
