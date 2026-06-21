class Documento:


    def __init__(self, nombre):

        self.nombre = nombre
        self.texto = ""


    def generar_salida(self):

        print("Procesando documento:", self.nombre)

