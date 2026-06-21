import os

from core.config_manager import ConfigManager
from core.file_manager import FileManager
from core.pdf_downloader import PDFDownloader
from core.pdf_extractor import PDFExtractor
from core.data_transformer import DataTransformer
from core.sqlite_repository import SQLiteRepository
from core.pdf_discovery import main as descubrir_lista_pdf


class SeaceIAApplication:
    def __init__(self):
        self.config = ConfigManager()
        self.downloader = PDFDownloader()
        self.extractor = PDFExtractor()
        self.transformer = DataTransformer()
        self.repository = SQLiteRepository(
            self.config.db_file
        )

    def run(self):
        print("\n====================================")
        print("INICIO DEL PROCESO SEACE")
        print("====================================")

        FileManager.crear_directorios(
            self.config.db_path,
            self.config.download_path,
            os.path.dirname(self.config.text_file),
            os.path.dirname(self.config.csv_file)
        )

        self.repository.crear_base_datos()

        # Primer paso: descubrir y generar la lista de PDFs
        archivo_lista = descubrir_lista_pdf()
        print(f"[OK] Lista de PDFs generada: {archivo_lista}")

        urls_pdf = FileManager.leer_lineas(archivo_lista)

        for indice, url_pdf in enumerate(urls_pdf, start=1):
            print(f"\nProcesando PDF {indice}/{len(urls_pdf)}")
            try:
                pdf_file = os.path.join(
                    self.config.download_path,
                    f"Proceso_{indice:03d}.pdf"
                )

                text_file = os.path.join(
                    os.path.dirname(self.config.text_file),
                    f"Proceso_{indice:03d}.txt"
                )

                self.downloader.descargar(
                    url_pdf,
                    pdf_file
                )

                texto = self.extractor.extraer_texto(
                    pdf_file
                )

                FileManager.guardar_texto(
                    texto,
                    text_file
                )

                datos = self.transformer.transformar(
                    texto
                )

                FileManager.guardar_csv(
                    datos,
                    self.config.csv_file
                )

                self.repository.insertar(datos)

            except Exception as e:
                print(f"[ERROR] No se pudo procesar: {url_pdf}")
                print(str(e))

        registros = self.repository.consultar()

        print("\n==============================")
        print("DATOS EN SQLITE")
        print("==============================")

        for fila in registros:
            print(fila)

        print(
            "\n[FINALIZADO] Proceso completado correctamente"
        )
