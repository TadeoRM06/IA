from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re
import json
import urllib3

# Deshabilitar advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lista de palabras clave
KEYWORDS = [
    "reforma judicial", "fiscalías", "organismos autónomos",
    "transparencia", "rendición de cuentas", "independencia judicial",
    "México", "Poder Judicial", "violencia electoral", "autonomía", "magistrados"
]

# Archivo donde se guardará el corpus
CORPUS_FILE = "/naturalLen/corpus.json"

# Encabezados para las solicitudes HTTP
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

# Función para buscar en Google
def search_google(keyword, num_results=15):
    urls = []
    try:
        for result in search(keyword, num_results=num_results):
            urls.append(result)
    except Exception as e:
        print(f"Error en la búsqueda para '{keyword}': {e}")
    return urls

# Función para realizar scraping
def scrape_url(url):
    try:
        response = requests.get(url, headers=HEADERS, verify=False, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return " ".join([p.get_text().strip() for p in soup.find_all("p") if len(p.get_text().strip()) > 50])
    except Exception as e:
        print(f"Error al procesar {url}: {e}")
        return ""

# Función para calificar artículos
def score_article(article_text):
    normalized_text = article_text.lower()
    score = 0
    for keyword in KEYWORDS:
        if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', normalized_text):
            score += 1
    if len(article_text.split()) > 300:
        score += 1
    return score

# Clasificar artículo
def classify_article(article_text, threshold=3):
    score = score_article(article_text)
    return score >= threshold, score

# Cargar y guardar el corpus
def load_corpus():
    try:
        with open(CORPUS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_to_corpus(article_text, score):
    corpus = load_corpus()
    corpus.append({"texto": article_text, "calificacion": score})
    with open(CORPUS_FILE, "w", encoding="utf-8") as file:
        json.dump(corpus, file, ensure_ascii=False, indent=4)

# Proceso principal
def main():
    print("Iniciando búsqueda en Google...")
    all_urls = []
    for keyword in KEYWORDS:
        print(f"Buscando: {keyword}")
        urls = search_google(keyword)
        print(f"Se encontraron {len(urls)} resultados para '{keyword}'")
        all_urls.extend(urls)

    print(f"Un total de {len(all_urls)} URLs encontradas. Realizando scraping...")

    for url in all_urls:
        article_text = scrape_url(url)
        if article_text:
            is_relevant, score = classify_article(article_text)
            if is_relevant:
                save_to_corpus(article_text, score)
                print(f"Artículo relevante guardado con calificación {score}")
            else:
                print(f"Artículo no relevante con calificación {score}")

    print("Proceso completado. Corpus actualizado.")

if __name__ == "__main__":
    main()