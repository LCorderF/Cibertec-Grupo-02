import os
import csv

class FileManager:
    @staticmethod
    def crear_directorios(*directorios):
        for directorio in directorios:
            if directorio:
                os.makedirs(directorio, exist_ok=True)

        print("[OK] Directorios verificados")

    @staticmethod
    def guardar_texto(texto, archivo):
        with open(archivo, "w", encoding="utf-8") as file:
            file.write(texto)

        print(f"[OK] Texto guardado en: {archivo}")

    @staticmethod
    def guardar_csv(datos, archivo_csv):
        archivo_existe = os.path.exists(archivo_csv)
        with open( archivo_csv, "a", newline="", encoding="utf-8" ) as csvfile:
            writer = csv.DictWriter( csvfile, fieldnames=datos.keys())
            if not archivo_existe:
                writer.writeheader()
            writer.writerow(datos)

        print(f"[OK] Datos guardados en CSV: {archivo_csv}")
