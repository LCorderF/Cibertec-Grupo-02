from core.application import SeaceIAApplication



def menu():

    try:

        app = SeaceIAApplication()

        app.inicializar_sistema()



        while True:


            print("\n==============================")
            print("          SEACE IA")
            print("==============================")

            print("1. Descargar PDF")
            print("2. Extraer texto")
            print("3. Analizar documento")
            print("4. Mostrar resumen")
            print("5. Guardar resultados")
            print("6. Consultar BD")
            print("7. Salir")


            try:

                opcion = int(
                    input("\nSeleccione opción: ")
                )


            except ValueError:

                print(
                    "[ERROR] Debe ingresar un número"
                )

                continue



            if opcion == 1:

                app.descargar_documento()



            elif opcion == 2:

                app.extraer_documento()



            elif opcion == 3:

                app.analizar_documento()



            elif opcion == 4:

                app.mostrar_resumen()



            elif opcion == 5:

                app.guardar_resultados()



            elif opcion == 6:

                app.consultar_bd()



            elif opcion == 7:

                print(
                    "Sistema finalizado"
                )

                break



            else:

                print(
                    "[ERROR] Opción fuera de rango"
                )



    except Exception as error:

        print(
            "[ERROR GENERAL DEL SISTEMA]",
            error
        )



if __name__ == "__main__":

    menu()