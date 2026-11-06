from lector import Lector


lector = Lector()

red = lector.cargar_red("relaciones.txt","tabla.txt")

red.mostrar_estructura()



#La idea es armar diccionarios con las condiciones que ya sabemos
asignacion = {
    "Rain": "heavy",
    "Maintenance": "yes",
    "Train": "delayed",
    "Appointment": "attend"
}
# TRAER EL NODO QUE QUEREMOS AVERIGUAR

probabilidad = red.calcular_probabilidad_conjunta(asignacion)
