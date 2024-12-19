import os
import requests
from bs4 import BeautifulSoup
from googlesearch import search

def search_pdfs(keywords, num_results=10):
    query = f"{keywords} filetype:pdf"
    urls = []
    for url in search(query, num_results=num_results):
        if url.endswith(".pdf"):
            urls.append(url)
    return urls

def download_pdf(url, output_dir):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        filename = os.path.join(output_dir, url.split("/")[-1])
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Descargado: {filename}")
    except requests.RequestException as e:
        print(f"Error al descargar {url}: {e}")

if __name__ == "__main__":
    output_dir = "G:/Lenguje Natural/Docs"
    os.makedirs(output_dir, exist_ok=True)
    print("Buscando PDFs...")
    pdf_urls = search_pdfs("Reforma poder judicial debate", num_results=10)
    
    if pdf_urls:
        print(f"Se encontraron {len(pdf_urls)} PDFs. Descargando...")
        for pdf_url in pdf_urls:
            download_pdf(pdf_url, output_dir)
    else:
        print("No se encontraron PDFs.")