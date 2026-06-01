import pdfplumber

class PDFExtractor:
    def extraer_texto(self, pdf_path):

        print("[INFO] Extrayendo texto del PDF...")
        paginas = []
        with pdfplumber.open(pdf_path) as pdf:

            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if texto:
                    paginas.append(texto)

        print("[OK] Texto extraído correctamente")
        return "\n".join(paginas)
    