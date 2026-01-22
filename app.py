"""
Sistema de Generación de Certificados de Matrícula
SLEP Santa Corina

Aplicación Streamlit para buscar estudiantes y generar certificados de matrícula
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils import formatear_run, limpiar_run, validar_run, formatear_curso
from generador_certificado import GeneradorCertificado

# Configuración de la página
st.set_page_config(
    page_title="Certificados de Matrícula - SLEP Santa Corina",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3a8a;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #475569;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f0f9ff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #f0fdf4;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #22c55e;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fffbeb;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #fef2f2;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def cargar_datos():
    """Carga los datos de prematrícula desde el archivo Excel"""
    df = pd.read_excel('20260122 Prematricula_2026_por_Estud_-_SANTA_CORINA.xlsx')
    return df


def buscar_estudiante(df, run):
    """
    Busca un estudiante en la base de datos por RUN
    
    Args:
        df (DataFrame): Base de datos de estudiantes
        run (str o int): RUN del estudiante (puede incluir puntos y guión)
        
    Returns:
        DataFrame o None: Fila del estudiante si se encuentra, None en caso contrario
    """
    # Limpiar el RUN ingresado
    run_limpio = limpiar_run(run)
    
    # Extraer solo los números (sin DV)
    if len(run_limpio) > 1:
        run_sin_dv = int(run_limpio[:-1])
    else:
        return None
    
    # Buscar en el DataFrame
    resultado = df[df['SAL_RUN'] == run_sin_dv]
    
    if len(resultado) > 0:
        return resultado.iloc[0]
    return None


def main():
    """Función principal de la aplicación"""
    
    # Header
    st.markdown('<p class="main-header">📜 Certificados de Matrícula</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Servicio Local de Educación Pública Santa Corina</p>', unsafe_allow_html=True)
    
    # Cargar datos
    with st.spinner('Cargando base de datos de estudiantes...'):
        try:
            df = cargar_datos()
            st.sidebar.success(f"✅ Base de datos cargada: {len(df):,} estudiantes")
        except Exception as e:
            st.error(f"❌ Error al cargar la base de datos: {str(e)}")
            return
    
    # Sidebar con información
    with st.sidebar:
        st.markdown("### ℹ️ Instrucciones")
        st.markdown("""
        1. Ingresa el RUN del estudiante
        2. Verifica los datos mostrados
        3. Ingresa el nombre del estudiante
        4. Genera y descarga el certificado
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Estadísticas")
        st.metric("Total estudiantes", f"{len(df):,}")
        st.metric("Establecimientos", df['NOM_RBD'].nunique())
        st.metric("Año escolar", df['ANO_ESCOLAR'].iloc[0])
        
        st.markdown("---")
        st.markdown("### 🔍 Formato RUN")
        st.info("Puedes ingresar el RUN con o sin formato:\n- 12345678-9\n- 12.345.678-9\n- 123456789")
    
    # Área principal
    st.markdown("---")
    
    # Formulario de búsqueda
    col1, col2 = st.columns([3, 1])
    
    with col1:
        run_input = st.text_input(
            "🔍 Ingresa el RUN del estudiante",
            placeholder="Ej: 12.345.678-9 o 123456789",
            help="Puedes ingresar el RUN con o sin formato"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        buscar_btn = st.button("🔎 Buscar", type="primary", use_container_width=True)
    
    # Validación y búsqueda
    if buscar_btn and run_input:
        
        # Limpiar el RUN
        run_limpio = limpiar_run(run_input)
        
        if not run_limpio or len(run_limpio) < 2:
            st.markdown('<div class="error-box">❌ Por favor ingresa un RUN válido</div>', unsafe_allow_html=True)
            return
        
        # Validar RUN (opcional, pero recomendado)
        if not validar_run(run_input):
            st.markdown(f'<div class="warning-box">⚠️ El RUN ingresado no tiene un dígito verificador válido. Verificando de todas formas...</div>', unsafe_allow_html=True)
        
        # Buscar estudiante
        with st.spinner('Buscando estudiante...'):
            estudiante = buscar_estudiante(df, run_input)
        
        if estudiante is None:
            st.markdown('<div class="error-box">❌ No se encontró ningún estudiante con ese RUN en la base de datos de prematrícula 2026</div>', unsafe_allow_html=True)
        else:
            # Mostrar datos del estudiante encontrado
            st.markdown('<div class="success-box">✅ <strong>Estudiante encontrado</strong></div>', unsafe_allow_html=True)
            
            # Formatear datos
            run_formateado = formatear_run(estudiante['SAL_RUN'])
            curso_completo = formatear_curso(estudiante['COD_GRADO_GLOSA_PRE'], estudiante['LET_CUR_PRE'])
            
            # Mostrar información en columnas
            st.markdown("### 📋 Datos del Estudiante")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown("**RUN:**")
                st.markdown(f"<h3>{run_formateado}</h3>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown("**Curso:**")
                st.markdown(f"<h3>{curso_completo}</h3>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown("**Año Escolar:**")
                st.markdown(f"<h3>{estudiante['ANO_ESCOLAR']}</h3>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Información del establecimiento
            st.markdown("### 🏫 Establecimiento Educacional")
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown(f"**Nombre:** {estudiante['NOM_RBD']}")
            st.markdown(f"**RBD:** {estudiante['RBD_PRE']}")
            st.markdown(f"**Comuna:** {estudiante['NOM_COM_RBD']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Formulario para generar certificado
            st.markdown("### 📝 Generar Certificado")
            
            with st.form("form_certificado"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nombre_estudiante = st.text_input(
                        "Nombre completo del estudiante*",
                        placeholder="Ej: MARÍA FERNANDA GONZÁLEZ LÓPEZ",
                        help="Ingresa el nombre tal como debe aparecer en el certificado (en mayúsculas)"
                    )
                
                with col2:
                    fecha_emision = st.date_input(
                        "Fecha de emisión",
                        value=datetime.now(),
                        help="Fecha que aparecerá en el certificado"
                    )
                
                finalidad = st.text_input(
                    "Finalidad del certificado (opcional)",
                    value="Para fines pertinentes",
                    help="Especifica la finalidad del certificado"
                )
                
                generar_btn = st.form_submit_button("📄 Generar Certificado", type="primary", use_container_width=True)
                
                if generar_btn:
                    if not nombre_estudiante or nombre_estudiante.strip() == "":
                        st.error("❌ Por favor ingresa el nombre del estudiante")
                    else:
                        try:
                            with st.spinner('Generando certificado...'):
                                # Preparar datos para el certificado
                                datos_certificado = {
                                    'nombre': nombre_estudiante.upper(),
                                    'run': run_formateado,
                                    'establecimiento': estudiante['NOM_RBD'],
                                    'rbd': estudiante['RBD_PRE'],
                                    'curso': curso_completo,
                                    'año': estudiante['ANO_ESCOLAR']
                                }
                                
                                # Generar certificado
                                generador = GeneradorCertificado('Formato certificado de matrícula.docx')
                                certificado_buffer = generador.generar_certificado(
                                    datos_certificado,
                                    fecha_emision=datetime.combine(fecha_emision, datetime.min.time())
                                )
                                
                                # Nombre del archivo
                                run_sin_formato = run_limpio[:-1]  # Sin DV
                                nombre_archivo = f"Certificado_Matricula_{run_sin_formato}_{datetime.now().strftime('%Y%m%d')}.docx"
                                
                                # Botón de descarga
                                st.success("✅ Certificado generado exitosamente")
                                st.download_button(
                                    label="📥 Descargar Certificado",
                                    data=certificado_buffer,
                                    file_name=nombre_archivo,
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    type="primary",
                                    use_container_width=True
                                )
                                
                                st.balloons()
                        
                        except Exception as e:
                            st.error(f"❌ Error al generar el certificado: {str(e)}")
                            st.exception(e)


if __name__ == "__main__":
    main()
