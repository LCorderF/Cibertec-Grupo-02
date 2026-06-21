import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import os


PAGINAS_INICIALES = [
    "https://www.osinergmin.gob.pe/seccion/institucional/Paginas/procesos-seleccion-dse.aspx",
    "https://www.osinergmin.gob.pe/seccion/institucional/institucional/procesos-seleccion/division-supervision-regional",
    "https://www.osinergmin.gob.pe/seccion/institucional/institucional/procesos-seleccion/gerencia-supervision-minera"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def obtener_links_pdf(url):
    """
    Devuelve todos los enlaces PDF encontrados en una página.
    """
    pdfs = set()

    try:
        r = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )

        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a", href=True):

            href = a["href"].strip()

            if ".pdf" in href.lower():
                pdf_url = urljoin(url, href)
                pdfs.add(pdf_url)

    except Exception as e:
        print(f"Error leyendo {url}")
        print(e)

    return pdfs


def validar_pdf(url):
    """
    Verifica que el enlace exista y sea un PDF.
    """

    try:
        r = requests.head(
            url,
            headers=HEADERS,
            timeout=20,
            allow_redirects=True
        )

        if r.status_code != 200:
            return False

        content_type = r.headers.get(
            "Content-Type",
            ""
        ).lower()

        if "pdf" in content_type:
            return True

        if url.lower().endswith(".pdf"):
            return True

    except:
        pass

    return False


def generar_nombre_archivo():
    fecha = datetime.now().strftime("%Y%m%d")

    correlativo = 1

    while True:

        nombre = (
            f"ListaProceso_PDF_{fecha}-"
            f"{correlativo:03d}.txt"
        )

        if not os.path.exists(nombre):
            return nombre

        correlativo += 1


def descubrir_pdfs(maximo=50):
    """
    Descubre hasta 'maximo' PDFs válidos.
    """

    encontrados = set()

    for pagina in PAGINAS_INICIALES:

        print(f"Analizando: {pagina}")

        pdfs = obtener_links_pdf(pagina)

        for pdf in pdfs:

            if pdf in encontrados:
                continue

            print(f"Validando: {pdf}")

            if validar_pdf(pdf):

                encontrados.add(pdf)

                print(
                    f"[{len(encontrados)}] OK"
                )

            if len(encontrados) >= maximo:
                return sorted(encontrados)

    return sorted(encontrados)


def guardar_lista(lista):
    """
    Guarda los enlaces encontrados y retorna
    el nombre del archivo generado.
    """

    nombre = generar_nombre_archivo()

    with open(
        nombre,
        "w",
        encoding="utf-8"
    ) as f:

        for item in lista:
            f.write(item + "\n")

    return nombre


def main():

    lista = descubrir_pdfs(50)

    print(
        f"PDF válidos encontrados: "
        f"{len(lista)}"
    )

    archivo_generado = guardar_lista(lista)

    """
    print(
        f"Archivo generado: "
        f"{archivo_generado}"
    )
    """

    return archivo_generado


if __name__ == "__main__":

    nombre_archivo = main()

    print(
        f"Valor de retorno: "
        f"{nombre_archivo}"
    )