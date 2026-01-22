"""
Utilidades para el sistema de certificados de matrícula
SLEP Santa Corina
"""

def calcular_dv(run):
    """
    Calcula el dígito verificador de un RUN chileno
    
    Args:
        run (int o str): RUN sin dígito verificador
        
    Returns:
        str: Dígito verificador (0-9 o K)
    """
    run_str = str(run).replace(".", "").replace("-", "")
    
    if not run_str.isdigit():
        return None
        
    run_int = int(run_str)
    
    multiplicador = 2
    suma = 0
    
    while run_int > 0:
        suma += (run_int % 10) * multiplicador
        run_int //= 10
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2
    
    resto = suma % 11
    dv = 11 - resto
    
    if dv == 11:
        return '0'
    elif dv == 10:
        return 'K'
    else:
        return str(dv)


def formatear_run(run, dv=None):
    """
    Formatea un RUN con puntos y guión
    
    Args:
        run (int o str): RUN sin formato
        dv (str, optional): Dígito verificador. Si no se proporciona, se calcula.
        
    Returns:
        str: RUN formateado (ej: 12.345.678-9)
    """
    run_str = str(run).replace(".", "").replace("-", "")
    
    if not run_str.isdigit():
        return run
    
    # Calcular DV si no se proporciona
    if dv is None:
        dv = calcular_dv(run_str)
    
    # Formatear con puntos
    run_formateado = ""
    contador = 0
    
    for digito in reversed(run_str):
        if contador > 0 and contador % 3 == 0:
            run_formateado = "." + run_formateado
        run_formateado = digito + run_formateado
        contador += 1
    
    return f"{run_formateado}-{dv}"


def limpiar_run(run):
    """
    Limpia un RUN eliminando puntos, guiones y espacios
    
    Args:
        run (str): RUN con formato
        
    Returns:
        str: RUN sin formato (solo números y DV)
    """
    return str(run).replace(".", "").replace("-", "").replace(" ", "").strip()


def extraer_run_y_dv(run_completo):
    """
    Extrae el RUN y el dígito verificador por separado
    
    Args:
        run_completo (str): RUN completo con DV
        
    Returns:
        tuple: (run_sin_dv, dv)
    """
    run_limpio = limpiar_run(run_completo)
    
    if len(run_limpio) < 2:
        return None, None
    
    run_sin_dv = run_limpio[:-1]
    dv = run_limpio[-1]
    
    return run_sin_dv, dv


def validar_run(run_completo):
    """
    Valida si un RUN chileno es válido
    
    Args:
        run_completo (str): RUN completo con DV
        
    Returns:
        bool: True si es válido, False en caso contrario
    """
    run_sin_dv, dv_ingresado = extraer_run_y_dv(run_completo)
    
    if run_sin_dv is None:
        return False
    
    if not run_sin_dv.isdigit():
        return False
    
    dv_calculado = calcular_dv(run_sin_dv)
    
    return dv_ingresado.upper() == dv_calculado.upper()


def formatear_fecha(fecha_str):
    """
    Formatea una fecha en formato legible para el certificado
    
    Args:
        fecha_str (str): Fecha en cualquier formato
        
    Returns:
        str: Fecha formateada (ej: "20 de enero del 2026")
    """
    from datetime import datetime
    
    meses = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    
    try:
        if isinstance(fecha_str, str):
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        else:
            fecha = fecha_str
        
        dia = fecha.day
        mes = meses[fecha.month]
        año = fecha.year
        
        return f"{dia} de {mes} del {año}"
    except:
        return fecha_str


def formatear_curso(grado, letra):
    """
    Formatea el curso con el grado y la letra
    
    Args:
        grado (str): Grado (ej: "6° básico")
        letra (str): Letra del curso (ej: "C")
        
    Returns:
        str: Curso formateado (ej: "6° básico C")
    """
    if letra and letra.strip():
        return f"{grado} {letra.upper()}"
    return grado
