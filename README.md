# 📜 Sistema de Certificados de Matrícula
## SLEP Santa Corina

Sistema web desarrollado con Streamlit para buscar estudiantes por RUN y generar certificados de matrícula personalizados en formato Word (.docx).

---

## 🎯 Características

- ✅ **Búsqueda rápida por RUN**: Busca estudiantes en la base de datos de prematrícula 2026
- 🔍 **Validación de RUN**: Valida automáticamente el dígito verificador
- 📊 **Visualización de datos**: Muestra información completa del estudiante y establecimiento
- 📝 **Generación automática**: Crea certificados personalizados en formato Word
- 💾 **Descarga instantánea**: Descarga el certificado listo para imprimir
- 🎨 **Interfaz amigable**: Diseño intuitivo y profesional

---

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

---

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
# Si tienes git instalado
git clone [url-del-repositorio]
cd certificados-matricula

# O simplemente descargar y extraer los archivos
```

### 2. Crear un entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 📂 Estructura del Proyecto

```
certificados-matricula/
│
├── app.py                                    # Aplicación principal Streamlit
├── generador_certificado.py                  # Módulo para generar certificados
├── utils.py                                  # Funciones auxiliares (RUN, formato, etc.)
├── requirements.txt                          # Dependencias del proyecto
├── README.md                                 # Este archivo
│
├── data/                                     # Carpeta para datos
│   ├── 20260122_Prematricula_2026_por_Estud_-_SANTA_CORINA.xlsx
│   └── Formato_certificado_de_matrícula.docx
│
└── certificados_generados/                   # Carpeta para guardar certificados (opcional)
```

---

## 🎮 Uso

### 1. Preparar los archivos de datos

Asegúrate de tener:
- **Base de datos de estudiantes**: `20260122_Prematricula_2026_por_Estud_-_SANTA_CORINA.xlsx`
- **Template del certificado**: `Formato_certificado_de_matrícula.docx`

Coloca estos archivos en la carpeta `data/` o actualiza las rutas en `app.py`:

```python
# Línea 71 en app.py
df = pd.read_excel('data/20260122_Prematricula_2026_por_Estud_-_SANTA_CORINA.xlsx')

# Línea 256 en app.py
generador = GeneradorCertificado('data/Formato_certificado_de_matrícula.docx')
```

### 2. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### 3. Usar la aplicación

1. **Buscar estudiante**:
   - Ingresa el RUN del estudiante (con o sin formato)
   - Haz clic en "Buscar"

2. **Verificar datos**:
   - Revisa la información del estudiante
   - Verifica el establecimiento y curso

3. **Generar certificado**:
   - Ingresa el nombre completo del estudiante
   - Selecciona la fecha de emisión
   - (Opcional) Especifica la finalidad del certificado
   - Haz clic en "Generar Certificado"

4. **Descargar**:
   - Descarga el certificado generado en formato Word
   - Abre el documento para verificar y/o imprimir

---

## 🔧 Personalización

### Modificar el template del certificado

Edita el archivo `Formato_certificado_de_matrícula.docx` según tus necesidades. Los siguientes campos se reemplazarán automáticamente:

- `SOFIA MENDEZ FLOREZ` → Nombre del estudiante
- `27.571.150-0` → RUN del estudiante
- `ESCUELA CARLOS CONDELL DE LA HAZA` → Nombre del establecimiento
- `8521` → RBD del establecimiento
- `6° básico C` → Curso del estudiante
- `2026` → Año escolar
- `20 de enero del 2026` → Fecha de emisión

### Cambiar colores y estilos

Modifica la sección de estilos CSS en `app.py` (líneas 22-60) para personalizar los colores de la interfaz.

---

## 📊 Columnas del Excel

El archivo Excel debe contener las siguientes columnas:

| Columna | Descripción |
|---------|-------------|
| `SAL_RUN` | RUN del estudiante (sin DV) |
| `RBD_PRE` | Código RBD del establecimiento |
| `NOM_RBD` | Nombre del establecimiento |
| `COD_GRADO_GLOSA_PRE` | Grado (ej: "6° básico") |
| `LET_CUR_PRE` | Letra del curso (ej: "C") |
| `ANO_ESCOLAR` | Año escolar |
| `NOM_COM_RBD` | Nombre de la comuna |

---

## 🛠️ Solución de Problemas

### Error: "ModuleNotFoundError"

```bash
# Asegúrate de tener el entorno virtual activado e instala las dependencias
pip install -r requirements.txt
```

### Error: "FileNotFoundError"

Verifica que las rutas a los archivos Excel y Word sean correctas en `app.py`.

### El certificado no se genera correctamente

- Verifica que el template Word contenga los placeholders exactos
- Revisa que los datos del estudiante estén completos
- Revisa los logs de error en la terminal

### Problemas con el RUN

El sistema acepta RUNs en varios formatos:
- `12345678-9`
- `12.345.678-9`
- `123456789`

---

## 🔐 Consideraciones de Privacidad

- El sistema NO almacena nombres de estudiantes en la base de datos
- Los certificados se generan en memoria y se descargan directamente
- No se guardan copias de los certificados en el servidor
- El nombre del estudiante debe ingresarse manualmente para cada certificado

---

## 📝 Notas Importantes

1. **Base de datos**: La base de datos se carga en memoria al iniciar la aplicación para búsquedas rápidas
2. **Cache**: Los datos se cachean para mejorar el rendimiento
3. **Validación**: El sistema valida el dígito verificador del RUN pero permite continuar si es inválido
4. **Formato**: Los certificados mantienen el formato del template original

---

## 👨‍💻 Desarrollo

### Ejecutar en modo desarrollo

```bash
streamlit run app.py --server.runOnSave true
```

### Agregar nuevas funcionalidades

El proyecto está modularizado para facilitar el desarrollo:

- `app.py`: Interfaz y lógica de la aplicación
- `generador_certificado.py`: Lógica de generación de documentos Word
- `utils.py`: Funciones auxiliares reutilizables

---

## 📄 Licencia

Este proyecto fue desarrollado para el Servicio Local de Educación Pública Santa Corina.

---

## 🤝 Soporte

Para reportar problemas o solicitar nuevas funcionalidades, contacta al equipo de desarrollo de SLEP Santa Corina.

---

## 📚 Recursos Adicionales

- [Documentación de Streamlit](https://docs.streamlit.io/)
- [Documentación de python-docx](https://python-docx.readthedocs.io/)
- [Documentación de pandas](https://pandas.pydata.org/docs/)

---

**Desarrollado con ❤️ para SLEP Santa Corina**
