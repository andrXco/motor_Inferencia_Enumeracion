class RedBayesiana:

    def __init__(self):
        self.nodos = {}

    def agregar_nodo(self, nodo):
        if nodo.nombre in self.nodos:
            raise ValueError("Nodo duplicado: " + nodo.nombre)
        self.nodos[nodo.nombre] = nodo

    def obtener_nodo(self, nombre):
        if nombre not in self.nodos:
            raise ValueError("No existe el nodo: " + nombre)
        return self.nodos[nombre]

    def agregar_dependencia(self, nombre_padre, nombre_hijo):

        padre = self.obtener_nodo(nombre_padre)
        hijo = self.obtener_nodo(nombre_hijo)

        if padre == hijo:
            raise ValueError("Un nodo no puede ser padre de si mismo")

        if padre in hijo.padres:
            raise ValueError("La dependencia ya existe")

        if self.existe_camino(hijo, padre):
            raise ValueError("La dependencia genera un ciclo")

        padre.agregar_hijo(hijo)
        hijo.agregar_padre(padre)

    def existe_camino(self, origen, destino):
        pendientes = [origen]
        visitados = []
        while pendientes:
            actual = pendientes.pop()
            if actual == destino:
                return True
            if actual not in visitados:
                visitados.append(actual)
                for hijo in actual.hijos:
                    pendientes.append(hijo)
        return False

    def obtener_raices(self):
        raices = []
        for nodo in self.nodos.values():
            if len(nodo.padres) == 0:
                raices.append(nodo)
        return raices

    def orden_topologico(self):

        grados = {}

        for nodo in self.nodos.values():
            grados[nodo] = len(nodo.padres)

        pendientes = self.obtener_raices()
        orden = []

        while pendientes:

            actual = pendientes.pop(0)
            orden.append(actual)

            for hijo in actual.hijos:

                grados[hijo] -= 1

                if grados[hijo] == 0:
                    pendientes.append(hijo)

        if len(orden) != len(self.nodos):
            raise ValueError("La red contiene un ciclo")

        return orden

    def mostrar_estructura(self):

        print("\nESTRUCTURA DE LA RED BAYESIANA")

        for nodo in self.orden_topologico():

            padres = []

            for padre in nodo.padres:
                padres.append(padre.nombre)

            hijos = []

            for hijo in nodo.hijos:
                hijos.append(hijo.nombre)

            print("\nNodo:", nodo.nombre)
            print("Estados:", nodo.estado)
            print("Padres:", padres)
            print("Hijos:", hijos)

    def mostrar_tablas(self):
        print("\nTABLAS DE PROBABILIDAD")

        for nodo in self.orden_topologico():
            print("\nNodo:", nodo.nombre)

            for estados_padres, probabilidades in nodo.tabla.items():

                if len(nodo.padres) > 0:
                    print("Condiciones:")

                    for i in range(len(nodo.padres)):
                        print(
                            " ",
                            nodo.padres[i].nombre,
                            "=",
                            estados_padres[i]
                        )

                for estado in nodo.estado:
                    print(" ", estado, ":", probabilidades[estado])

    def calcular_probabilidad_conjunta(self, asignacion):

        probabilidad = 1

        print("\nDETALLE DE MULTIPLICACION")

        for nodo in self.orden_topologico():

            nombre = nodo.nombre
            estado = asignacion[nombre]

            valor = nodo.obtenerProbabilidad(
                estado,
                asignacion
            )

            condiciones = []

            for padre in nodo.padres:
                condiciones.append(
                    padre.nombre + "=" + asignacion[padre.nombre]
                )

            if len(condiciones) == 0:
                print("P(", nombre, "=", estado, ") =", valor)
            else:
                print(
                    "P(", nombre, "=", estado,
                    "|", ", ".join(condiciones),
                    ") =", valor
                )

            probabilidad *= valor

        print("Producto =", round(probabilidad, 6))

        return probabilidad
    
    def enumerar_y_sumar(self, asignacion):

        combinaciones = [asignacion.copy()]

        for nodo in self.orden_topologico():

            if nodo.nombre not in asignacion:

                nuevas_combinaciones = []

                for combinacion in combinaciones:

                    for estado in nodo.estado:

                        nueva = combinacion.copy()
                        nueva[nodo.nombre] = estado

                        nuevas_combinaciones.append(nueva)

                combinaciones = nuevas_combinaciones

        suma = 0

        for combinacion in combinaciones:

            probabilidad = self.calcular_probabilidad_conjunta(
                combinacion
            )

            print("Combinacion:", combinacion)
            print("Probabilidad:", round(probabilidad, 4))

            suma += probabilidad

        return suma


    def inferencia_por_enumeracion(self, nombre_consulta, evidencia):

        nodo = self.obtener_nodo(nombre_consulta)

        if not isinstance(evidencia, dict):
            raise ValueError("La evidencia debe ser un diccionario")

        if nombre_consulta in evidencia:
            raise ValueError(
                "La variable consultada no debe estar incluida en la evidencia"
            )

        for nombre, estado in evidencia.items():
            observado = self.obtener_nodo(nombre)

            if estado not in observado.estado:
                raise ValueError(
                    "Estado inválido para " + nombre + ". Válidos: "
                    + str(observado.estado)
                )

        ocultas = [
            otro.nombre for otro in self.orden_topologico()
            if otro.nombre != nombre_consulta and otro.nombre not in evidencia
        ]

        print("\nINFERENCIA POR ENUMERACIÓN")
        print("Consulta X:", nombre_consulta)
        print("Evidencia E:", evidencia or "(sin evidencia)")
        print("Variables ocultas Y:", ocultas or "(ninguna)")
        print("Se calcula: P(X | E) = α Σ_Y P(X, E, Y)")

        resultados = {}

        for estado in nodo.estado:

            asignacion = evidencia.copy()
            asignacion[nombre_consulta] = estado

            print("\nEvaluando:", nombre_consulta, "=", estado)

            suma = self.enumerar_y_sumar(asignacion)

            resultados[estado] = suma

            print("Suma para", estado, "=", suma)

        total = 0

        for estado in resultados:
            total += resultados[estado]

        if total == 0:
            raise ValueError("No es posible normalizar: probabilidad de evidencia igual a 0")

        print("\nNORMALIZACION")

        for estado in resultados:

            resultados[estado] = resultados[estado] / total

            print(
                nombre_consulta, "=", estado,
                ":", resultados[estado]
            )

        return resultados

