import math

class Nodo:

    def __init__(self, nombre, estados):
        self.nombre = nombre.strip()
        self.estado = [estado.strip() for estado in estados]

        if not self.nombre:
            raise ValueError("El nombre del nodo no puede estar vacío")

        if not self.estado or any(not estado for estado in self.estado):
            raise ValueError("El nodo debe tener estados válidos")

        if len(set(self.estado)) != len(self.estado):
            raise ValueError(f"Hay estados repetidos en {self.nombre}")

        self.padres=[]
        self.hijos=[]
        self.tabla={}

    def agregar_padre(self, padre):
        if padre not in self.padres:
            self.padres.append(padre)

    def agregar_hijo(self, hijo):
            if hijo not in self.hijos:
                self.hijos.append(hijo)

    def agregarFilaATabla(self, estados_padres, probabilidades):
         clave=tuple(estados_padres)

         if clave in self.tabla:
             raise ValueError(f"Fila duplicada en {self.nombre}: {clave}")

         if set(probabilidades) != set(self.estado):
             raise ValueError(
                 f"Los estados de la tabla de {self.nombre} no coinciden"
             )

         for valor in probabilidades.values():
             if not math.isfinite(valor) or valor < 0 or valor > 1:
                 raise ValueError(
                     f"Probabilidad inválida en la tabla de {self.nombre}"
                 )

         if not math.isclose(sum(probabilidades.values()), 1, abs_tol=1e-6):
             raise ValueError(
                 f"Las probabilidades de {self.nombre} no suman 1"
             )

         self.tabla[clave]=probabilidades

    #La estructura de cada fila es: NombreNodo|EstadosPadres|Probabilidades

    def obtenerProbabilidad(self, estado, asignacion):
        estados_padres = []

        for padre in self.padres:
            estados_padres.append(asignacion[padre.nombre])
        clave = tuple(estados_padres)
        return self.tabla[clave][estado]

    
