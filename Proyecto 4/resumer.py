import requests
from bs4 import BeautifulSoup

# def extraer_texto_relevante(url):

def extraer_texto_relevante(url):
    try:
        response = requests.get(url, verify=False)  # Deshabilita la verificación SSL
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Buscar el contenedor principal del artículo (ajustar según el sitio web)
        articulo = soup.find('article')  
        if not articulo:
            articulo = soup.find('div', class_='main-content')  
        if not articulo:
            articulo = soup  # Si no se encuentra, usar todo el HTML
        
        # Eliminar barras laterales, anuncios y contenido no relevante
        for sidebar in articulo.find_all(['aside', 'nav', 'footer']):
            sidebar.decompose()  # Elimina estos elementos del DOM
        
        for no_relevante in articulo.find_all('div', class_=['sidebar', 'related', 'ads', 'promo', 'banner']):
            no_relevante.decompose()
        
        # Extraer encabezados y párrafos del artículo principal
        contenido = []
        for encabezado in articulo.find_all(['h1', 'h2', 'h3']):
            contenido.append(encabezado.get_text(strip=True))
        for parrafo in articulo.find_all('p'):
            contenido.append(parrafo.get_text(strip=True))
        
        texto_relevante = "\n".join(contenido)
        
        return texto_relevante

    except requests.RequestException as e:
        print(f"Error al acceder a la URL: {e}")
        return None

    
def main():
    # url = "https://www.gob.mx/presidencia/prensa/reforma-al-poder-judicial-es-la-lucha-del-pueblo-de-mexico-contra-la-corrupcion-y-el-nepotismo-presidenta-claudia-sheinbaum"
    
    urls = [
         "http://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S1405-91932017000200085",
        "https://www.diputados.gob.mx/sedia/sia/redipal/CR-24/CR-10-24.pdf",
        "https://escuelajudicial.cjf.gob.mx/publicaciones/revista/29/Filiberto%20Valent%C3%ADn%20Ugalde%20Calder%C3%B3n.pdf",
        "https://archivos.juridicas.unam.mx/www/bjv/libros/1/306/7.pdf",
        "http://www.diputados.gob.mx/sia/coord/refconst_lviii/html/109.htm",
        "https://mexico.justia.com/estatales/ciudad-de-mexico/constitucion-politica-de-la-ciudad-de-mexico/titulo-quinto/capitulo-v/",
        "https://archivos.juridicas.unam.mx/www/bjv/libros/6/2834/5.pdf",
        "https://juridica.ibero.mx/index.php/juridi/article/download/55/37/82",
        "https://home.inai.org.mx/wp-content/documentos/SalaDePrensa/Comunicados/Comunicado%20INAI-283-23.pdf",
        "https://elpais.com/mexico/2024-08-28/organos-autonomos-que-son-y-que-implica-la-reforma-para-desaparecerlos.html",
        "http://sil.gobernacion.gob.mx/Archivos/Documentos/2021/02/asun_4141850_20210223_1614156669.pdf",
        "https://eljuegodelacorte.nexos.com.mx/el-abc-de-la-reforma-a-los-organismos-autonomos/",
        "http://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S0041-86332021000100061",
        "https://coparmex.org.mx/la-desaparicion-de-los-organismos-autonomos-compromete-el-futuro-de-mexico-pone-en-riesgo-el-equilibrio-de-poderes-y-la-democracia/",
        "https://es.wikipedia.org/wiki/%C3%93rganos_constitucionales_aut%C3%B3nomos_de_M%C3%A9xico",
        "https://itait.org.mx/Presentaciones/Autonomia_organos_constitucionales.pdf",
        "http://consejogobiernodigital.edomex.gob.mx/content/%C3%B3rganos-aut%C3%B3nomos",
        "http://www2.scjn.gob.mx/juridica/engroses/2/2012/2/2_137864_940.doc",
        "https://imco.org.mx/desaparicion-de-organos-autonomos/",
        "https://coparmex.org.mx/que-perdemos-con-la-desaparicion-de-los-organismos-autonomos-derechos-transparencia-y-prograso/"
    ]
    
    for i,url in enumerate(urls, start=1):
        print("Extrayendo contenido...")
        texto = extraer_texto_relevante(url)
        
        if texto:
            print(f"art {i}")
            print("\nTexto extraído:")
            print(texto)
            
            archivo = "corpus/corpus.txt"
            with open(archivo, "a", encoding="utf-8") as f:
                f.write(f"{texto}\n---ARTÍCULO---\n")
            print(f"\nEl texto se ha guardado en: {archivo}")
        else:
            print("No se pudo extraer el contenido.")
        

if __name__ == "__main__":
    main()