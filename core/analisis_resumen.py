from core.Documento import Documento
from datetime import datetime

# Clase Hija 01
class AnalisisDocumento(Documento):


    def __init__(self, nombre):

        super().__init__(nombre)



    def analizar(self, texto):

        self.texto = texto


        texto_minuscula = texto.lower()


        # Funcion de orden superior
        lineas = self.limpiar_lineas(texto)


        resultado = {


            "documento":
            self.nombre,

            "fecha_proceso":
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "cantidad_lineas":
            len(lineas),


            "cantidad_palabras":
            len(texto.split()),


            "cantidad_caracteres":
            len(texto),


            "tiene_cronograma":
            self.buscar_palabra(
                "cronograma",
                texto_minuscula
            ),


            "contiene_experiencia":
            self.buscar_palabra(
                "experiencia",
                texto_minuscula
            ),
            
            "contiene_puntaje":
            self.buscar_palabra(
                "puntaje",
                texto_minuscula
            ),


            "contiene_requisitos":
            self.buscar_palabra(
                "requisitos",
                texto_minuscula
            ),



            "tiene_fecha":
            "/" in texto

        }


        return resultado




    def limpiar_lineas(self, texto):


        lineas = texto.splitlines()


        # Funcion de orden superior
        lineas_validas = list(
            filter(
                lambda linea: len(linea.strip()) > 0,
                lineas
            )
        )


        return lineas_validas




    def buscar_palabra(self, palabra, texto):

        return palabra in texto




    # Polimorfismo
    def generar_salida(self, resultado):


        print("\nANALISIS DEL DOCUMENTO")
        print("---------------------")


        print(
            "Documento:",
            resultado["documento"]
        )


        print(
            "Cantidad de líneas:",
            resultado["cantidad_lineas"]
        )


        print(
            "Cantidad de palabras:",
            resultado["cantidad_palabras"]
        )


        print(
            "Cantidad caracteres:",
            resultado["cantidad_caracteres"]
        )


        print(
            "Documento procesado correctamente"
        )



#Clase Hija 02
class ResumenDocumento(Documento):
    
    def __init__(self, nombre):

        super().__init__(nombre)

    # Polimorfismo
    def generar_salida(self, resultado):


        print("\nRESUMEN DEL DOCUMENTO")
        print("-------------------")


        print(
            "Documento:",
            self.nombre
        )


        self.mostrar_estado(
            "Cronograma",
            resultado["tiene_cronograma"]
        )


        self.mostrar_estado(
            "Experiencia",
            resultado["contiene_experiencia"]
        )


        self.mostrar_estado(
            "Puntaje",
            resultado["contiene_puntaje"]
        )
        
        self.mostrar_estado(
            "Requisitos",
            resultado["contiene_requisitos"]
        )

        self.mostrar_estado(
            "Fecha",
            resultado["tiene_fecha"]
        )


    def mostrar_estado(self, nombre, valor):


        if valor:

            print(
                "✓ Contiene",
                nombre
            )

        else:

            print(
                "✗ No contiene",
                nombre
            )