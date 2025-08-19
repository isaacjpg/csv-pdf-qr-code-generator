import pandas as pd
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4, A5
from reportlab.lib.units import inch
from PIL import Image
import os

from datetime import datetime

class URLQRGenerator:
    def __init__(self, csv_path, output_folder="qr_pdfs"):
        """
        Generador simple de QR PDFs para URLs
        
        Args:
            csv_path: Ruta al archivo CSV
            output_folder: Carpeta donde se guardarán los PDFs
        """
        self.csv_path = csv_path
        self.output_folder = output_folder
        self.df = None
        
        # Crear carpeta de salida si no existe
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    
    def load_csv(self):
        """Carga el archivo CSV"""
        try:
            self.df = pd.read_csv(self.csv_path)
            print(f"✅ CSV cargado: {len(self.df)} URLs encontradas")
            print(f"Columnas: {list(self.df.columns)}")
            return True
        except Exception as e:
            print(f"❌ Error al cargar CSV: {e}")
            return False
    
    def generate_qr_for_url(self, url):
        """
        Genera código QR para una URL
        
        Args:
            url: URL para convertir en QR
        
        Returns:
            PIL Image del código QR
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(str(url))
        qr.make(fit=True)
        
        return qr.make_image(fill_color="black", back_color="white")
    
    def create_url_pdf(self, url, filename, title=None, description=None):
        """
        Crea PDF con QR de URL
        
        Args:
            url: URL para el QR
            filename: Nombre del archivo PDF
            title: Título opcional para el PDF
            description: Descripción opcional
        """
        pdf_path = os.path.join(self.output_folder, filename)
        c = canvas.Canvas(pdf_path, pagesize=A5)
        width, height = A5
        
        # Generar código QR
        qr_image = self.generate_qr_for_url(url)
        
        # Guardar QR temporalmente como archivo
        temp_qr_path = os.path.join(self.output_folder, f"temp_qr_{filename.replace('.pdf', '.png')}")
        qr_image.save(temp_qr_path, format='PNG')
        
        # Configurar layout
        margin = 1 * inch
        qr_size = 3 * inch
        
        # Centrar el QR horizontalmente
        qr_x = (width - qr_size) / 2
        qr_y = height - qr_size - 2 * inch
        
        
        # Insertar código QR centrado
        c.drawImage(temp_qr_path, qr_x, qr_y, width=qr_size, height=qr_size)
        
        # Título principal
        c.setFont("Helvetica-Bold", 24)
        title_text = title if title else "Código QR"
        title_width = c.stringWidth(title_text, "Helvetica-Bold", 24)
        c.drawString((width - title_width) / 2, qr_y - 0.5 * inch, title_text)
        
        
        # Footer con fecha
        c.setFont("Helvetica", 8)
        footer_text = f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        c.drawString(margin, 0.5 * inch, footer_text)
        
        c.save()
        
        # Limpiar archivo temporal
        try:
            os.remove(temp_qr_path)
        except:
            pass
        
        return pdf_path
    
    def generate_all_url_pdfs(self, codigo):
        """
        Genera PDFs para todas las URLs del CSV
        
        Args:
            codigo: Nombre de la columna con los códigos
        """
        if self.df is None:
            print("❌ CSV no cargado. Use load_csv() primero.")
            return
        
        if codigo not in self.df.columns:
            print(f"❌ Columna '{codigo}' no encontrada")
            print(f"Columnas disponibles: {list(self.df.columns)}")
            return
        
        generated_files = []
        print("\n🚀 Generando PDFs...")
        
        for index, row in self.df.iterrows():
            # Convertir el código a string para evitar errores
            codigo_valor = str(row[codigo])
            
            url = (f"https://portal.sidiv.registrocivil.cl/docstatus?"
                   f"RUN={codigo_valor}-k&type=CEDULA_EXT&serial=111111111"
                   f"&mrz=111111111111111111111111")
            
            # Validar URL
            if pd.isna(url) or url == "":
                print(f"⚠️  Fila {index + 1}: URL vacía, omitiendo...")
                continue
            
            # Determinar nombre de archivo único por código
            filename = f"qr_{codigo_valor}.pdf"
            
            # Limpiar nombre de archivo
            filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).strip()
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            
            # Obtener título y descripción, convirtiendo a string
            title = (str(row[codigo]) if codigo and codigo in self.df.columns
                     else None)
            description = (str(row[codigo]) if codigo in self.df.columns
                          else None)
            
            try:
                pdf_path = self.create_url_pdf(url, filename, title,
                                             description)
                generated_files.append(pdf_path)
                print(f"✅ {filename} - {codigo_valor}")
            except Exception as e:
                print(f"❌ Error en fila {index + 1}: {e}")
        
        print(f"\n🎉 Completado: {len(generated_files)} PDFs en "
              f"'{self.output_folder}'")
        return generated_files

def main():
    """Función principal"""
    # Configuración - AJUSTA ESTOS VALORES
    csv_file = "codigos.csv"  # Tu archivo CSV
    output_folder = "pdfs_qr"
    
    # Nombres de columnas - ajusta según tu CSV
    codigo = "codigo"          # Columna con las URLs   
    
    # Crear generador
    generator = URLQRGenerator(csv_file, output_folder)
    
    # Cargar y procesar
    if generator.load_csv():
        generator.generate_all_url_pdfs(
            codigo=codigo
        )

def create_sample_csv():
    """Crea un CSV de ejemplo con URLs"""
    sample_data = {
        'nombre': ['Google', 'GitHub', 'YouTube'],
        'titulo': ['Buscador Google', 'Repositorio GitHub', 'Videos YouTube'],
        'descripcion': ['Motor de búsqueda', 'Código fuente', 'Plataforma de videos'],
        'url': ['https://www.google.com', 'https://github.com', 'https://www.youtube.com']
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv('urls_ejemplo.csv', index=False, encoding='utf-8')
    print("📄 Archivo de ejemplo creado: 'urls_ejemplo.csv'")

if __name__ == "__main__":
    # Si no existe el archivo, crear ejemplo
    if not os.path.exists('urls.csv'):
        create_sample_csv()
        print("\n💡 Se creó un CSV de ejemplo. Puedes editarlo o usar tu propio archivo.")
        print("   Asegúrate de ajustar los nombres de columnas en main() si es necesario.\n")
    
    main()