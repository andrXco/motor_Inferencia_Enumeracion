class Nodo:

    def __init__(self, nombre, estados):
        self.nombre=nombre
        self.estado=estados
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
         self.tabla[clave]=probabilidades

    #La estructura de cada fila es: NombreNodo|EstadosPadres|Probabilidades

    def obtenerProbabilidad(self, estado, asignacion):
        estados_padres = []

        for padre in self.padres:
            estados_padres.append(asignacion[padre.nombre])
        clave = tuple(estados_padres)
        return self.tabla[clave][estado]

    