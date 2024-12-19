from googlesearch import search
import random
import time
import json
import urllib3

# Deshabilitar advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lista de palabras clave
KEYWORDS = [
    "reforma al poder judicial mexico", 
    "explicacion de los organismos autónomos en méxico",
    "legislación a los organismos autónomos republica mexicana",
]

# Retraso aleatorio entre solicitudes
def delay_request():
    delay = random.randint(10, 15)
    print(f"Esperando {delay} segundos antes de la próxima solicitud...")
    time.sleep(delay)

# Función para realizar búsquedas en Google
def search_google(keyword, num_results=20):
    urls = []
    try:
        for result in search(keyword, num_results=num_results):
            urls.append(result)
    except Exception as e:
        print(f"Error en la búsqueda para '{keyword}': {e}")
    return urls

# Proceso principal
def main():
    print("Iniciando búsqueda en Google...")
    resultados = {}

    for keyword in KEYWORDS:
        print(f"Buscando: {keyword}")
        urls = search_google(keyword)
        print(f"Se encontraron {len(urls)} resultados para '{keyword}':")
        
        # Guardar los enlaces en el diccionario
        resultados[keyword] = urls

        # Imprimir los enlaces encontrados
        for i, url in enumerate(urls, start=1):
            print(f"{i}. {url}")
        
        delay_request()

    # Guardar resultados en un archivo JSON
    with open("DocumentosTextoPlano/enlaces.json", "a", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

    print("\nBúsqueda completada. Enlaces guardados en 'enlaces.json'.")

if __name__ == "__main__":
    main()