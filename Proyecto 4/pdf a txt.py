import PyPDF2
import os

def pdf_a_txt(pdf_ruta, txt_ruta):
    try:
        # Aseguramos que las rutas sean absolutas
        pdf_ruta = os.path.abspath(pdf_ruta)
        txt_ruta = os.path.abspath(txt_ruta)
        
        # Abre el archivo PDF en modo lectura binaria
        with open(pdf_ruta, 'rb') as pdf_file:
            lector = PyPDF2.PdfReader(pdf_file)
            texto = ""

            # Extrae el texto de cada página
            for pagina in lector.pages:
                texto += pagina.extract_text()

        # Guarda el texto extraído en un archivo .txt
        with open(txt_ruta, 'w', encoding='utf-8') as txt_file:
            txt_file.write(texto)

        print(f"Texto extraído correctamente y guardado en {txt_ruta}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Rutas de entrada y salida (especifica directamente las rutas aquí)
ruta_pdf = r"E:\Lenguje Natural\lenguajeNatural\DocumentosTextoPlano\reforma2.pdf"
ruta_txt = r"E:\Lenguje Natural\lenguajeNatural\DocumentosTextoPlano\data2.txt"

pdf_a_txt(ruta_pdf, ruta_txt)
