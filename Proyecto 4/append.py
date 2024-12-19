import json
from PyPDF2 import PdfReader

# Archivo donde se guardará el corpus
CORPUS_FILE = "corpus.json"

# Cargar el corpus existente
def load_corpus():
    try:
        with open(CORPUS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Guardar artículo en el corpus
def save_to_corpus(article_text, score=5):  # Calificación predeterminada de 5
    corpus = load_corpus()
    corpus.append({"texto": article_text, "calificacion": score})
    with open(CORPUS_FILE, "w", encoding="utf-8") as file:
        json.dump(corpus, file, ensure_ascii=False, indent=4)

# Procesar PDF y agregarlo directamente
def add_pdf_to_corpus(file_path):
    try:
        # Leer el PDF
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        if not text.strip():
            print("El PDF no contiene texto extraíble.")
            return

        # Agregar directamente al corpus
        save_to_corpus(text, score=5)
        print("El PDF fue agregado exitosamente al corpus con calificación 5.")
    except Exception as e:
        print(f"Error al procesar el archivo PDF: {e}")

# Uso del método
if __name__ == "__main__":
    pdf_path = "reforma.pdf"  # Ruta del archivo PDF cargado
    add_pdf_to_corpus(pdf_path)