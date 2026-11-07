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

            
            padres_red = [padre.nombre for padre in nodo.padres]
            padres_tabla = bloque["padres"]

            if sorted(padres_red) != sorted(padres_tabla):
                raise ValueError(
                    "Los padres de " + nodo.nombre +
                    " no coinciden entre los archivos"
                )

            nodo.padres = [
                red.obtener_nodo(nombre)
                for nombre in padres_tabla
            ]

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

                    
        # Validar las tablas de probabilidad
        for nodo in red.nodos.values():

            if len(nodo.tabla) == 0:
                raise ValueError(
                    "El nodo " + nodo.nombre +
                    " no tiene tabla de probabilidades"
                )

            for estados_padres, probabilidades in nodo.tabla.items():

                if set(probabilidades.keys()) != set(nodo.estado):
                    raise ValueError(
                        "Estados incorrectos en la tabla de " +
                        nodo.nombre
                    )

                for valor in probabilidades.values():
                    if valor < 0 or valor > 1:
                        raise ValueError(
                            "Probabilidad fuera del rango [0,1] en " +
                            nodo.nombre
                        )

                suma = sum(probabilidades.values())

                if abs(suma - 1) > 0.000001:
                    raise ValueError(
                        "Las probabilidades de " +
                        nodo.nombre +
                        " no suman 1"
                    )
        
        
        # Verificar todas las combinaciones de los padres
        for nodo in red.nodos.values():

            combinaciones_esperadas = [()]

            for padre in nodo.padres:

                nuevas_combinaciones = []

                for combinacion in combinaciones_esperadas:

                    for estado in padre.estado:

                        nueva = combinacion + (estado,)
                        nuevas_combinaciones.append(nueva)

                combinaciones_esperadas = nuevas_combinaciones

            esperadas = set(combinaciones_esperadas)
            existentes = set(nodo.tabla.keys())

            faltantes = esperadas - existentes
            adicionales = existentes - esperadas

            if faltantes:
                raise ValueError(
                    "Faltan combinaciones en " +
                    nodo.nombre + ": " + str(faltantes)
                )

            if adicionales:
                raise ValueError(
                    "Combinaciones no validas en " +
                    nodo.nombre + ": " + str(adicionales)
                )

        return red