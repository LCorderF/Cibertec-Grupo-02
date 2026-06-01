import os

from core.config_manager import ConfigManager
from core.file_manager import FileManager
from core.pdf_downloader import PDFDownloader
from core.pdf_extractor import PDFExtractor
from core.data_transformer import DataTransformer
from core.sqlite_repository import SQLiteRepository

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
        self.downloader.descargar(
            self.config.pdf_url,
            self.config.pdf_file
        )
        texto = self.extractor.extraer_texto(
            self.config.pdf_file
        )
        FileManager.guardar_texto(
            texto,
            self.config.text_file
        )
        datos = self.transformer.transformar(
            texto
        )
        FileManager.guardar_csv(
            datos,
            self.config.csv_file
        )
        self.repository.insertar(datos)
        registros = self.repository.consultar()
        print("\n==============================")
        print("DATOS EN SQLITE")
        print("==============================")

        for fila in registros:
            print(fila)
        print(
            "\n[FINALIZADO] Proceso completado correctamente"
        )
