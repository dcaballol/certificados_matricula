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
    df = pd.read_excel('datos_prematricula.xlsx')
    return df


def buscar_estudiante(df, run):
    """
    Busca un estudiante en la base de datos por RUN
    VERSIÓN MEJORADA - Maneja RUNs con o sin DV correctamente
    
    Args:
        df (DataFrame): Base de datos de estudiantes
        run (str o int): RUN del estudiante (puede incluir puntos y guión)
        
    Returns:
        DataFrame o None: Fila del estudiante si se encuentra, None en caso contrario
    """
    # Limpiar el RUN ingresado
    run_limpio = limpiar_run(str(run))
    
    if not run_limpio or len(run_limpio) < 2:
        return None
    
    # Estrategia 1: Intentar buscar el RUN completo tal cual
    # (usuario puede haber ingresado solo números sin DV)
    try:
        run_completo = int(run_limpio)
        resultado = df[df['SAL_RUN'] == run_completo]
        if len(resultado) > 0:
            return resultado.iloc[0]
    except:
        pass
    
    # Estrategia 2: Asumir que el último dígito es el DV
    # (usuario ingresó RUN con DV)
    try:
        run_sin_dv = int(run_limpio[:-1])
        resultado = df[df['SAL_RUN'] == run_sin_dv]
        if len(resultado) > 0:
            return resultado.iloc[0]
    except:
        pass
    
    # Estrategia 3: Si tiene más de 8 dígitos, probar quitando 2 últimos
    # (por si acaso tiene formato raro)
    if len(run_limpio) > 8:
        try:
            run_sin_2digitos = int(run_limpio[:-2])
            resultado = df[df['SAL_RUN'] == run_sin_2digitos]
            if len(resultado) > 0:
                return resultado.iloc[0]
        except:
            pass
    
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
            st.error("❌ Por favor ingresa un RUN válido")
            st.stop()
        
        # NO validar DV - el sistema lo calculará automáticamente
        
        # Buscar estudiante
        with st.spinner('Buscando estudiante...'):
            estudiante = buscar_estudiante(df, run_input)
        
        if estudiante is None:
            st.error("❌ **NO SE ENCONTRÓ** ningún estudiante con ese RUN en la base de prematrícula 2026")
            st.info(f"🔍 RUN buscado: **{run_input}**")
            
            # Ayuda adicional
            with st.expander("💡 Sugerencias"):
                st.write("""
                - Verifica que el RUN esté escrito correctamente
                - Asegúrate que el estudiante esté en prematrícula 2026
                - Prueba sin puntos ni guión: solo números
                - Contacta al administrador si el problema persiste
                """)
            st.stop()
        else:
            # GUARDAR EN SESSION STATE
            st.session_state['estudiante'] = estudiante
            st.session_state['run_formateado'] = formatear_run(estudiante['SAL_RUN'])
            st.session_state['curso_completo'] = formatear_curso(estudiante['COD_GRADO_GLOSA_PRE'], estudiante['LET_CUR_PRE'])
    
    # MOSTRAR DATOS SI EXISTE EN SESSION STATE
    if 'estudiante' in st.session_state:
        estudiante = st.session_state['estudiante']
        run_formateado = st.session_state['run_formateado']
        curso_completo = st.session_state['curso_completo']
        
        # Mostrar datos del estudiante encontrado
        st.success("✅ **ESTUDIANTE ENCONTRADO**")
        
        # Botón para nueva búsqueda
        if st.button("🔄 Buscar Otro Estudiante", type="secondary"):
            # Limpiar session state
            del st.session_state['estudiante']
            del st.session_state['run_formateado']
            del st.session_state['curso_completo']
            st.rerun()
        
        # Mostrar información en columnas
        st.markdown("### 📋 Datos del Estudiante")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("RUN", run_formateado)
        
        with col2:
            st.metric("Curso", curso_completo)
        
        with col3:
            st.metric("Año Escolar", estudiante['ANO_ESCOLAR'])
        
        # Información del establecimiento
        st.markdown("### 🏫 Establecimiento Educacional")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Nombre:** {estudiante['NOM_RBD']}")
        with col2:
            st.info(f"**RBD:** {estudiante['RBD_PRE']} | **Comuna:** {estudiante['NOM_COM_RBD']}")
        
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
                            generador = GeneradorCertificado('template_certificado.docx')
                            certificado_buffer = generador.generar_certificado(
                                datos_certificado,
                                fecha_emision=datetime.combine(fecha_emision, datetime.min.time())
                            )
                            
                            # Nombre del archivo
                            nombre_archivo = f"Certificado_Matricula_{estudiante['SAL_RUN']}_{datetime.now().strftime('%Y%m%d')}.docx"
                            
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
