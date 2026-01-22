# 🚀 Guía Rápida de Inicio

## Inicio Rápido (3 pasos)

### Windows

1. **Descargar** todos los archivos del proyecto
2. **Colocar los datos** en la misma carpeta:
   - `20260122_Prematricula_2026_por_Estud_-_SANTA_CORINA.xlsx`
   - `Formato_certificado_de_matrícula.docx`
3. **Hacer doble clic** en `iniciar.bat`

### Linux/Mac

1. **Descargar** todos los archivos del proyecto
2. **Colocar los datos** en la misma carpeta:
   - `20260122_Prematricula_2026_por_Estud_-_SANTA_CORINA.xlsx`
   - `Formato_certificado_de_matrícula.docx`
3. **Abrir terminal** en la carpeta y ejecutar:
   ```bash
   ./iniciar.sh
   ```

---

## ⚠️ Importante: Actualizar Rutas

Si colocaste los archivos de datos en una carpeta diferente, debes actualizar las rutas en `app.py`:

### Línea 71 - Ruta del Excel
```python
# Cambiar esta línea:
df = pd.read_excel('/mnt/user-data/uploads/20260122_Prematricula_2026_por_Estud_-_SANTA_CORINA.xlsx')

# Por (si los datos están en carpeta 'data'):
df = pd.read_excel('data/20260122_Prematricula_2026_por_Estud_-_SANTA_CORINA.xlsx')

# O (si están en la misma carpeta):
df = pd.read_excel('20260122_Prematricula_2026_por_Estud_-_SANTA_CORINA.xlsx')
```

### Línea 256 - Ruta del Template Word
```python
# Cambiar esta línea:
generador = GeneradorCertificado('/mnt/user-data/uploads/Formato_certificado_de_matrícula.docx')

# Por (si los datos están en carpeta 'data'):
generador = GeneradorCertificado('data/Formato_certificado_de_matrícula.docx')

# O (si están en la misma carpeta):
generador = GeneradorCertificado('Formato_certificado_de_matrícula.docx')
```

---

## 📝 Uso Básico

1. **Buscar estudiante**: Ingresa el RUN (con o sin formato)
   - Ejemplos válidos: `12345678-9`, `12.345.678-9`, `123456789`

2. **Verificar datos**: Revisa que los datos mostrados sean correctos

3. **Generar certificado**:
   - Ingresa el nombre del estudiante en MAYÚSCULAS
   - Selecciona la fecha de emisión
   - Haz clic en "Generar Certificado"

4. **Descargar**: Descarga el archivo Word y listo para imprimir

---

## 🔧 Solución de Problemas Comunes

### "No se encontró el archivo Excel"
- Verifica que el archivo esté en la carpeta correcta
- Actualiza la ruta en `app.py` línea 71

### "No se encontró el template Word"
- Verifica que el archivo esté en la carpeta correcta
- Actualiza la ruta en `app.py` línea 256

### "ModuleNotFoundError"
```bash
# Instalar dependencias manualmente:
pip install streamlit pandas openpyxl python-docx
```

### No se abre el navegador automáticamente
- Abre manualmente: http://localhost:8501

---

## 💡 Consejos

- ✅ El nombre del estudiante debe ir en MAYÚSCULAS
- ✅ Puedes buscar con RUN formateado o sin formato
- ✅ Los certificados se descargan directamente, no se guardan en el servidor
- ✅ Puedes generar múltiples certificados sin cerrar la aplicación

---

## 📞 Soporte

Para más ayuda, consulta el archivo `README.md` completo.
