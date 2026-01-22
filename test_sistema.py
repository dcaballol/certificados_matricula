"""
Script de prueba para el sistema de certificados
Prueba las funciones principales sin necesidad de ejecutar Streamlit
"""

import pandas as pd
from utils import formatear_run, validar_run, limpiar_run, calcular_dv
from generador_certificado import GeneradorCertificado
from datetime import datetime


def test_utils():
    """Prueba las funciones de utilidades"""
    print("="*80)
    print("PRUEBAS DE UTILIDADES")
    print("="*80)
    
    # Test 1: Calcular DV
    print("\n1. Calculando dígito verificador:")
    test_runs = [12345678, 19560438, 22218556]
    for run in test_runs:
        dv = calcular_dv(run)
        print(f"   RUN {run} → DV: {dv}")
    
    # Test 2: Formatear RUN
    print("\n2. Formateando RUNs:")
    for run in test_runs:
        run_formateado = formatear_run(run)
        print(f"   {run} → {run_formateado}")
    
    # Test 3: Validar RUN
    print("\n3. Validando RUNs:")
    test_runs_completos = ["12345678-5", "19.560.438-0", "222185569"]
    for run in test_runs_completos:
        es_valido = validar_run(run)
        print(f"   {run} → {'✓ Válido' if es_valido else '✗ Inválido'}")
    
    # Test 4: Limpiar RUN
    print("\n4. Limpiando RUNs:")
    for run in test_runs_completos:
        run_limpio = limpiar_run(run)
        print(f"   {run} → {run_limpio}")


def test_busqueda():
    """Prueba la búsqueda de estudiantes"""
    print("\n" + "="*80)
    print("PRUEBAS DE BÚSQUEDA")
    print("="*80)
    
    try:
        # Cargar datos
        print("\n1. Cargando base de datos...")
        df = pd.read_excel('/mnt/user-data/uploads/20260122_Prematricula_2026_por_Estud_-_SANTA_CORINA.xlsx')
        print(f"   ✓ Base de datos cargada: {len(df):,} registros")
        
        # Buscar algunos estudiantes de ejemplo
        print("\n2. Buscando estudiantes de ejemplo:")
        runs_ejemplo = df['SAL_RUN'].head(3).tolist()
        
        for run in runs_ejemplo:
            run_formateado = formatear_run(run)
            resultado = df[df['SAL_RUN'] == run]
            
            if len(resultado) > 0:
                est = resultado.iloc[0]
                print(f"\n   RUN: {run_formateado}")
                print(f"   Establecimiento: {est['NOM_RBD']}")
                print(f"   Curso: {est['COD_GRADO_GLOSA_PRE']} {est['LET_CUR_PRE']}")
                print(f"   RBD: {est['RBD_PRE']}")
        
        print("\n3. Estadísticas:")
        print(f"   Total estudiantes: {len(df):,}")
        print(f"   Establecimientos: {df['NOM_RBD'].nunique()}")
        print(f"   Comunas: {df['NOM_COM_RBD'].nunique()}")
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")


def test_generacion_certificado():
    """Prueba la generación de certificados"""
    print("\n" + "="*80)
    print("PRUEBAS DE GENERACIÓN DE CERTIFICADO")
    print("="*80)
    
    try:
        # Cargar datos
        print("\n1. Cargando datos...")
        df = pd.read_excel('/mnt/user-data/uploads/20260122_Prematricula_2026_por_Estud_-_SANTA_CORINA.xlsx')
        estudiante = df.iloc[0]
        
        # Preparar datos
        print("\n2. Preparando datos del estudiante:")
        run_formateado = formatear_run(estudiante['SAL_RUN'])
        curso = f"{estudiante['COD_GRADO_GLOSA_PRE']} {estudiante['LET_CUR_PRE']}"
        
        datos_certificado = {
            'nombre': 'ESTUDIANTE DE PRUEBA',
            'run': run_formateado,
            'establecimiento': estudiante['NOM_RBD'],
            'rbd': estudiante['RBD_PRE'],
            'curso': curso,
            'año': estudiante['ANO_ESCOLAR']
        }
        
        print(f"   Nombre: {datos_certificado['nombre']}")
        print(f"   RUN: {datos_certificado['run']}")
        print(f"   Establecimiento: {datos_certificado['establecimiento']}")
        print(f"   RBD: {datos_certificado['rbd']}")
        print(f"   Curso: {datos_certificado['curso']}")
        
        # Generar certificado
        print("\n3. Generando certificado...")
        generador = GeneradorCertificado('/mnt/user-data/uploads/Formato_certificado_de_matrícula.docx')
        certificado_buffer = generador.generar_certificado(
            datos_certificado,
            fecha_emision=datetime.now()
        )
        
        # Guardar certificado de prueba
        nombre_archivo = f"certificado_prueba_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        with open(nombre_archivo, 'wb') as f:
            f.write(certificado_buffer.read())
        
        print(f"   ✓ Certificado generado: {nombre_archivo}")
        print(f"   Tamaño: {len(certificado_buffer.getvalue()) / 1024:.2f} KB")
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Ejecuta todas las pruebas"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "SISTEMA DE CERTIFICADOS DE MATRÍCULA" + " "*22 + "║")
    print("║" + " "*25 + "SLEP SANTA CORINA" + " "*37 + "║")
    print("║" + " "*28 + "Script de Prueba" + " "*35 + "║")
    print("╚" + "="*78 + "╝")
    
    test_utils()
    test_busqueda()
    test_generacion_certificado()
    
    print("\n" + "="*80)
    print("PRUEBAS COMPLETADAS")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
