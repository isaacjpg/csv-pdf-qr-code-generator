# 🚀 Generador de Códigos QR para URLs - Registro Civil

Un generador automático de códigos QR que convierte códigos de identificación en URLs del portal del Registro Civil de Chile, generando PDFs individuales para cada código.

## ✨ Características

- **Generación automática** de códigos QR desde archivos CSV
- **PDFs personalizados** con diseño profesional
- **Formato A5** optimizado para impresión
- **Nombres únicos** de archivo basados en códigos
- **Manejo de errores** robusto
- **Interfaz simple** y fácil de usar

## 🎯 Caso de Uso

Este proyecto está diseñado específicamente para generar códigos QR que apuntan a la URL del portal del Registro Civil de Chile:

```
https://portal.sidiv.registrocivil.cl/docstatus?RUN={CODIGO}-k&type=CEDULA_EXT&serial=111111111&mrz=111111111111111111111111
```

Donde `{CODIGO}` se reemplaza con cada código del archivo CSV.

## 📋 Requisitos

- Python 3.7+
- Dependencias Python (ver instalación)

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd QR_Generator_V1
```

### 2. Instalar dependencias
```bash
# Opción 1: Con pipx (recomendado)
brew install pipx
pipx install pandas qrcode reportlab Pillow

# Opción 2: Con pip --user
pip3 install --user pandas qrcode reportlab Pillow

# Opción 3: Con Homebrew
brew install python-pandas python-qrcode python-reportlab python-pillow
```

## 📁 Estructura del Proyecto

```
QR_Generator_V1/
├── urlqrgenerator_code.py    # Script principal
├── codigos.csv               # Archivo CSV con códigos
├── pdfs_qr/                  # Carpeta de salida (se crea automáticamente)
├── .gitignore               # Archivos excluidos de Git
└── README.md                # Este archivo
```

## 📊 Formato del CSV

El archivo `codigos.csv` debe tener la siguiente estructura:

```csv
codigo,titulo
00010045,00010045
00010046,00010046
00010047,00010047
...
```

- **`codigo`**: Columna con los códigos de identificación (8 dígitos)
- **`titulo`**: Columna con títulos o descripciones (opcional)

## 🚀 Uso

### Ejecución básica
```bash
python3 urlqrgenerator_code.py
```

### Personalización
Puedes modificar las siguientes variables en la función `main()`:

```python
csv_file = "codigos.csv"      # Tu archivo CSV
output_folder = "pdfs_qr"     # Carpeta de salida
codigo = "codigo"             # Nombre de la columna con códigos
```

## 📱 Salida

El script generará:

- **Un PDF por cada código** en el CSV
- **Nombres únicos**: `qr_00010045.pdf`, `qr_00010046.pdf`, etc.
- **Formato A5** optimizado para impresión
- **Código QR centrado** con el título del código
- **Footer con fecha** de generación

## 🔧 Personalización del PDF

Puedes modificar el diseño del PDF editando la función `create_url_pdf()`:

- **Tamaño de página**: Cambiar `A5` por `A4`, `letter`, etc.
- **Fuentes**: Modificar tipos y tamaños de fuente
- **Colores**: Personalizar colores del QR y texto
- **Layout**: Ajustar posiciones y espaciado

## ⚠️ Solución de Problemas

### Error: "No module named 'pandas'"
```bash
pip3 install --user pandas qrcode reportlab Pillow
```

### Error: "numpy.int64 object has no attribute 'decode'"
✅ **Resuelto**: El script ahora convierte automáticamente los códigos numéricos a string.

### Los PDFs no se generan
- Verifica que el archivo CSV existe y tiene el formato correcto
- Asegúrate de que la columna `codigo` existe en el CSV
- Revisa los permisos de escritura en la carpeta de salida

## 📝 Ejemplo de Uso

1. **Preparar CSV**: Crea tu archivo `codigos.csv` con los códigos
2. **Ejecutar script**: `python3 urlqrgenerator_code.py`
3. **Revisar salida**: Los PDFs se generarán en `pdfs_qr/`
4. **Imprimir**: Los PDFs están optimizados para impresión A5

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Si tienes problemas o preguntas:

- Abre un issue en GitHub
- Revisa la sección de solución de problemas
- Verifica que todas las dependencias estén instaladas

## 🎉 Agradecimientos

- **pandas**: Para el manejo de datos CSV
- **qrcode**: Para la generación de códigos QR
- **reportlab**: Para la creación de PDFs
- **Pillow**: Para el procesamiento de imágenes

---

**Desarrollado con ❤️ para automatizar la generación de códigos QR del Registro Civil**
