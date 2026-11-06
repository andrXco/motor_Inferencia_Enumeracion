class RedBayesiana:

    def __init__(self):
        self.nodos = {}

    def agregar_nodo(self, nodo):
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