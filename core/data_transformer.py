from datetime import datetime

class DataTransformer:
    def transformar(self, texto):
        print("[INFO] Transformando datos.")
        texto_lower = texto.lower()
        datos = {
            "fecha_proceso":
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "cantidad_lineas":
                len(texto.splitlines()),

            "contiene_experiencia":
                "experiencia" in texto_lower,

            "contiene_puntaje":
                "puntaje" in texto_lower,

            "contiene_requisitos":
                "requisito" in texto_lower
        }
        print("[OK] Datos transformados")
        return datos
