# ============================================================
# Proyecto: SEACE + IA (Fase 1)
# Objetivo:
# - Descargar PDF desde URL pública
# - Extraer texto
# - Transformar información
# - Guardar datos estructurados (CSV)
# - Almacenar en base de datos relacional SQLite
# ============================================================

import os
import re
import csv
import sqlite3
import requests
import pdfplumber
from datetime import datetime

# ============================================================
# CONFIGURACION
# ============================================================

PDF_URL = "https://www.osinergmin.gob.pe/seccion/centro_documental/Institucional/Procesos-Seleccion/ES/DSHL/05-I-2021-DSHL/Bases-Integradas-05-I-2021-DSHL.pdf"

PDF_FILE = "bases.pdf"
TEXT_FILE = "bases_extraidas.txt"
CSV_FILE = "procesos.csv"
DB_FILE = "seace.db"

# ============================================================
# 1. DESCARGAR PDF
# ============================================================

def descargar_pdf(url, destino):
    print("[INFO] Descargando PDF...")

    response = requests.get(url)

    if response.status_code == 200:
        with open(destino, "wb") as file:
            file.write(response.content)

        print(f"[OK] PDF descargado: {destino}")
    else:
        raise Exception(f"Error descargando PDF: {response.status_code}")

# ============================================================
# 2. EXTRAER TEXTO DEL PDF
# ============================================================

def extraer_texto_pdf(pdf_path):
    print("[INFO] Extrayendo texto del PDF...")

    texto_completo = ""

    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()

            if texto:
                texto_completo += texto + "\n"

    print("[OK] Texto extraído correctamente")

    return texto_completo

# ============================================================
# 3. GUARDAR TEXTO EN ARCHIVO
# ============================================================

def guardar_texto(texto, archivo):
    with open(archivo, "w", encoding="utf-8") as file:
        file.write(texto)

    print(f"[OK] Texto guardado en: {archivo}")

# ============================================================
# 4. TRANSFORMAR DATOS
# ============================================================

def transformar_datos(texto):
    print("[INFO] Transformando datos...")

    lineas = texto.splitlines()

    datos = {
        "fecha_proceso": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cantidad_lineas": len(lineas),
        "contiene_experiencia": False,
        "contiene_puntaje": False,
        "contiene_requisitos": False
    }

    texto_minuscula = texto.lower()

    # Buscar palabras clave
    if "experiencia" in texto_minuscula:
        datos["contiene_experiencia"] = True

    if "puntaje" in texto_minuscula:
        datos["contiene_puntaje"] = True

    if "requisito" in texto_minuscula:
        datos["contiene_requisitos"] = True

    print("[OK] Datos transformados")

    return datos

# ============================================================
# 5. GUARDAR CSV
# ============================================================

def guardar_csv(datos, archivo_csv):

    archivo_existe = os.path.exists(archivo_csv)

    with open(archivo_csv, "a", newline="", encoding="utf-8") as csvfile:

        campos = datos.keys()

        writer = csv.DictWriter(csvfile, fieldnames=campos)

        if not archivo_existe:
            writer.writeheader()

        writer.writerow(datos)

    print(f"[OK] Datos guardados en CSV: {archivo_csv}")

# ============================================================
# 6. BASE DE DATOS SQLITE
# ============================================================

def crear_base_datos():

    conexion = sqlite3.connect(DB_FILE)

    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS procesos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_proceso TEXT,
            cantidad_lineas INTEGER,
            contiene_experiencia INTEGER,
            contiene_puntaje INTEGER,
            contiene_requisitos INTEGER
        )
    """)

    conexion.commit()
    conexion.close()

    print("[OK] Base de datos inicializada")

# ============================================================
# 7. INSERTAR DATOS EN SQLITE
# ============================================================

def insertar_datos(datos):

    conexion = sqlite3.connect(DB_FILE)

    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO procesos (
            fecha_proceso,
            cantidad_lineas,
            contiene_experiencia,
            contiene_puntaje,
            contiene_requisitos
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        datos["fecha_proceso"],
        datos["cantidad_lineas"],
        int(datos["contiene_experiencia"]),
        int(datos["contiene_puntaje"]),
        int(datos["contiene_requisitos"])
    ))

    conexion.commit()
    conexion.close()

    print("[OK] Datos insertados en SQLite")

# ============================================================
# 8. CONSULTAR DATOS
# ============================================================

def mostrar_datos():

    conexion = sqlite3.connect(DB_FILE)

    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM procesos")

    registros = cursor.fetchall()

    print("\n==============================")
    print("DATOS EN SQLITE")
    print("==============================")

    for fila in registros:
        print(fila)

    conexion.close()

# ============================================================
# MAIN
# ============================================================

def main():

    try:

        # Crear DB
        crear_base_datos()

        # Descargar PDF
        descargar_pdf(PDF_URL, PDF_FILE)

        # Extraer texto
        texto = extraer_texto_pdf(PDF_FILE)

        # Guardar TXT
        guardar_texto(texto, TEXT_FILE)

        # Transformar datos
        datos = transformar_datos(texto)

        # Guardar CSV
        guardar_csv(datos, CSV_FILE)

        # Insertar SQLite
        insertar_datos(datos)

        # Mostrar datos
        mostrar_datos()

        print("\n[FINALIZADO] Proceso completado correctamente")

    except Exception as e:
        print(f"[ERROR] {str(e)}")

# ============================================================
# EJECUCION
# ============================================================

if __name__ == "__main__":
    main()