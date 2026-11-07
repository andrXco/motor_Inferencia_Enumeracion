from lector import Lector

lector = Lector()

red = lector.cargar_red(
    "relaciones_prueba.txt",
    "tabla_prueba.txt"
)

red.mostrar_estructura()
red.mostrar_tablas()

print("Nodos cargados:", list(red.nodos.keys()))

print("\nPRUEBA 4: NUEVA RED BAYESIANA")

evidencia = {
    "Congestion": "yes"
}

resultado = red.inferencia_por_enumeracion(
    "Gripa",
    evidencia
)

print("\nRESULTADO FINAL")

for estado in resultado:
    print(estado, ":", round(resultado[estado], 4))

