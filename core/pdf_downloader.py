import requests

class PDFDownloader:
    def descargar(self, url, destino):
        print("[INFO] Descargando PDF...")
        response = requests.get( url, timeout=30 )
        response.raise_for_status()
        with open(destino, "wb") as file:
            file.write(response.content)

        print(f"[OK] PDF descargado: {destino}")
