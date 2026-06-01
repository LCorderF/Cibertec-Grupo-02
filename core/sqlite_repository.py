import sqlite3

class SQLiteRepository:
    def __init__(self, db_file):
        self.db_file = db_file

    def crear_base_datos(self):
        print("[INFO] Inicializando base de datos...")
        with sqlite3.connect(self.db_file) as conexion:
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
        print("[OK] Base de datos inicializada")

    def insertar(self, datos):
        print("[INFO] Insertando datos en SQLite...")
        with sqlite3.connect(self.db_file) as conexion:
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
        print("[OK] Datos insertados en SQLite")

    def consultar(self):
        print("[INFO] Consultando datos almacenados.")
        with sqlite3.connect(self.db_file) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM procesos"
            )
            registros = cursor.fetchall()
        return registros
