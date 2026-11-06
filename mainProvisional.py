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
appointment = red.obtener_nodo("Appointment")


#Aqui ponemos el numero para guardar la probabilidad que nos va a salir
probabilidad = 1

for nombre in asignacion:

    nodo = red.obtener_nodo(nombre)

    probabilidad *= nodo.obtenerProbabilidad(asignacion[nombre],asignacion)

print("\nProbabilidad conjunta:", probabilidad) #ESTE ES EL EJERCICIO QUE HICIMOS EN CLASE