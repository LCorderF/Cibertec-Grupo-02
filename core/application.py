import os

from core.config_manager import ConfigManager
from core.file_manager import FileManager
from core.pdf_downloader import PDFDownloader
from core.pdf_extractor import PDFExtractor
from core.analisis_resumen import AnalisisDocumento, ResumenDocumento
from core.sqlite_repository import SQLiteRepository



class SeaceIAApplication:


    def __init__(self):
        
        # Instancia de la clase ConfigManager
        self.config = ConfigManager()

        # Instancia de la clase PDFDownloader para descarga de archivos PDF
        self.downloader = PDFDownloader()

        # Instancia de la clase para extracción de texto
        self.extractor = PDFExtractor()

        # Instancia de la clase AnalisisDocumento
        self.analizador = AnalisisDocumento(
            "Documento SEACE"
        )

        # Instancia de la clase ResumenDocumento
        self.resumen = ResumenDocumento(
            "Documento SEACE"
        )

        # Instancia de repositorio SQLite
        self.repository = SQLiteRepository(
            self.config.db_file
        )

        self.texto = ""
        
        self.datos = None
        
        
    # Inicializar estructura del proyecto
    # Usa rutas obtenidas desde ConfigManager
    def inicializar_sistema(self):
        
        try:

            FileManager.crear_directorios(
                self.config.db_path,
                self.config.download_path,
                "data",
                "database"
            )
            
            # Crear base de datos SQLite
            self.repository.crear_base_datos()

            print("[OK] Sistema inicializado")


        except Exception as error:

            print("[ERROR] Inicializando sistema:", error)
            
    
    # Descargar PDF
    def descargar_documento(self):

        try:

            self.downloader.descargar(
                self.config.pdf_url,
                self.config.pdf_file
            )


        except Exception as error:

            print("[ERROR] Descargando PDF:", error)
            
            
    # Extraer texto
    def extraer_documento(self):

        try:

            self.texto = self.extractor.extraer_texto(
                self.config.pdf_file
            )


            FileManager.guardar_texto(
                self.texto,
                self.config.text_file
            )


        except Exception as error:

            print("[ERROR] Extrayendo texto:", error)



    # Analisis del documento
    def analizar_documento(self):

        try:

            if self.texto == "":

                raise Exception(
                    "No existe texto cargado"
                )


            self.datos = self.analizador.analizar(
                self.texto
            )


            self.analizador.generar_salida(
                self.datos
            )


        except Exception as error:

            print("[ERROR] Analizando documento:", error)


    # Resumen del documento
    def mostrar_resumen(self):

        try:

            if self.datos is None:

                raise Exception(
                    "Primero debe analizar el documento"
                )


            self.resumen.generar_salida(
                self.datos
            )


        except Exception as error:

            print("[ERROR] Mostrando resumen:", error)


    # Guardar CSV
    def guardar_resultados(self):

        try:

            if self.datos is None:

                raise Exception(
                    "No hay información para guardar"
                )


            FileManager.guardar_csv(
                self.datos,
                self.config.csv_file
            )


            self.repository.insertar(
                self.datos
            )


        except Exception as error:

            print("[ERROR] Guardando resultados:", error)



    # Guardar Base de Datos
    def consultar_bd(self):

        try:

            registros = self.repository.consultar()


            print("\n===================")
            print("REGISTROS SQLITE")
            print("===================")


            for fila in registros:

                print(fila)


        except Exception as error:

            print("[ERROR] Consultando BD:", error)





          
