from nodo import Nodo
from red_bayesiana import RedBayesiana

class Lector:
    def cargar_red(self, archivo_estructura, archivo_probabilidades):
        red = RedBayesiana()
        bloques = []
        bloque = None
        archivo = open(archivo_probabilidades, "r")

        for linea in archivo:
            linea = linea.strip()
            if linea == "":
                continue
            if linea == "[NODO]":
                if bloque != None:
                    bloques.append(bloque)
                bloque = {
                    "nombre": "",
                    "estados": [],
                    "padres": [],
                    "filas": []
                }
            elif bloque != None:
                if bloque["nombre"] == "":
                    bloque["nombre"] = linea

                elif linea.startswith("estados:"):

                    texto = linea.split(":", 1)[1]
                    bloque["estados"] = [estado.strip() for estado in texto.split(",")]

                elif linea.startswith("padres:"):
                    texto = linea.split(":", 1)[1].strip()
                    if texto != "-": 
                        bloque["padres"] = [padre.strip() for padre in texto.split(",")
                        ]
                else:
                    bloque["filas"].append(linea)
        if bloque != None:
            bloques.append(bloque)
        archivo.close()

        for bloque in bloques:

            nodo = Nodo(
                bloque["nombre"],
                bloque["estados"]
            )

            red.agregar_nodo(nodo)

        # Leer las dependencias
        archivo = open(archivo_estructura, "r")

        for linea in archivo:

            linea = linea.strip()

            if linea == "":
                continue

            padre, hijo = linea.split("->")

            red.agregar_dependencia(
                padre.strip(),
                hijo.strip()
            )

        archivo.close()

        # Cargar las tablas de probabilidad
        for bloque in bloques:

            nodo = red.obtener_nodo(bloque["nombre"])

            padres_red = []

            for padre in nodo.padres:
                padres_red.append(padre.nombre)

            # Nodo independiente
            if len(nodo.padres) == 0:

                probabilidades = {}

                for fila in bloque["filas"]:

                    estado, valor = fila.split(":", 1)

                    probabilidades[estado.strip()] = float(valor.strip())

                nodo.agregarFilaATabla([],probabilidades)

            # Nodo dependiente
            else:

                for fila in bloque["filas"]:

                    condicion, distribucion = fila.split("|", 1)

                    estados_padres = [estado.strip() for estado in condicion.split(",")]

                    probabilidades = {}

                    valores = distribucion.split(",")

                    for valor in valores:

                        estado, probabilidad = valor.split(":", 1)

                        probabilidades[estado.strip()] = float( probabilidad.strip())

                    nodo.agregarFilaATabla(estados_padres,probabilidades)
        return red