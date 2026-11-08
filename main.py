"""Entrada del motor. Ejecutar python main.py --help para ver las opciones."""

import argparse
from pathlib import Path

from lector import Lector


def localizar_archivo(nombre_archivo):
    ruta = Path(nombre_archivo).expanduser()
    if not ruta.is_absolute() and not ruta.exists():
        ruta = Path(__file__).resolve().parent / ruta
    if not ruta.is_file():
        raise ValueError(f"No existe el archivo: {ruta.resolve()}")
    return ruta.resolve()


def cargar_red(archivo_estructura, archivo_probabilidades):
    return Lector().cargar_red(
        localizar_archivo(archivo_estructura),
        localizar_archivo(archivo_probabilidades),
    )


def mostrar_resultado(consulta, evidencia, resultado):
    print("\nRESULTADO FINAL")
    print("Consulta X:", consulta)
    print("Evidencia E:", evidencia or "(sin evidencia)")
    for estado, probabilidad in resultado.items():
        print(f"P({consulta}={estado} | E) = {probabilidad:.10g}"
              f" ({probabilidad * 100:.4f} %)")
    print(f"Suma de la distribucion final: {sum(resultado.values()):.10g}")
    print("PRUEBA COMPLETADA: inferencia calculada sin errores detectados.")


def ejecutar(archivo_estructura, archivo_probabilidades, consulta, evidencia):
    print("\nCONFIGURACION DE LA PRUEBA")
    print("Estructura solicitada:", archivo_estructura)
    print("Tablas solicitadas:", archivo_probabilidades)
    print("Consulta:", consulta)
    print("Evidencia:", evidencia or "(sin evidencia)")
    estructura = localizar_archivo(archivo_estructura)
    tablas = localizar_archivo(archivo_probabilidades)

    red = cargar_red(estructura, tablas)
    print("\nCARGA VALIDADA")
    print("Nodos cargados:", list(red.nodos))
    print("Orden topologico:", [n.nombre for n in red.orden_topologico()])

    red.mostrar_estructura()
    red.mostrar_tablas()

    resultado = red.inferencia_por_enumeracion(consulta, evidencia)
    mostrar_resultado(consulta, evidencia, resultado)
    return resultado


def leer_evidencia(elementos):
    evidencia = {}
    for elemento in elementos:
        nombre, separador, estado = elemento.partition("=")
        nombre, estado = nombre.strip(), estado.strip()
        if not separador or not nombre or not estado:
            raise ValueError(f"Evidencia invalida: {elemento!r}. Usa Nodo=estado.")
        if nombre in evidencia:
            raise ValueError(f"Evidencia repetida para el nodo: {nombre}")
        evidencia[nombre] = estado
    return evidencia


def main():
    parser = argparse.ArgumentParser(
        description="Motor de inferencia por enumeracion con traza completa.",
        epilog="Sin opciones se ejecuta Gripa dada Congestion=yes. "
               "Con archivos personalizados, omitir --evidencia significa sin evidencia.",
    )
    parser.add_argument("prueba", nargs="?", choices=("original", "compleja"),
                        help="Nombre corto de la prueba; por defecto se usa original")
    parser.add_argument("--estructura", help="Archivo de dependencias Padre -> Hijo")
    parser.add_argument("--tablas", help="Archivo con los bloques de probabilidad")
    parser.add_argument("--consulta", help="Nombre exacto del nodo consultado")
    parser.add_argument("--evidencia", nargs="*", metavar="Nodo=estado",
                        help='Observaciones separadas por espacios; usa comillas si contienen espacios')
    opciones = parser.parse_args()
    seleccion = (opciones.estructura, opciones.tablas, opciones.consulta)
    if any(valor is not None for valor in seleccion):
        if opciones.prueba is not None:
            parser.error("Elige un nombre de prueba o archivos personalizados, no ambos.")
        if not all(seleccion):
            parser.error("Indica juntos --estructura, --tablas y --consulta.")
        estructura, tablas, consulta = seleccion
        elementos = opciones.evidencia or []
    else:
        pruebas = {
            "original": (
                "relaciones_prueba.txt", "tabla_prueba.txt", "Gripa",
                ["Congestion=yes"],
            ),
            "compleja": (
                "relaciones_gripa_compleja.txt", "tabla_gripa_compleja.txt", "Gripa",
                ["Congestion=yes", "Fiebre=yes"],
            ),
        }
        nombre_prueba = opciones.prueba or "original"
        estructura, tablas, consulta, evidencia_predeterminada = pruebas[nombre_prueba]
        elementos = (evidencia_predeterminada if opciones.evidencia is None
                     else opciones.evidencia)
        print("PRUEBA SELECCIONADA:", nombre_prueba)
    try:
        evidencia = leer_evidencia(elementos)
    except ValueError as error:
        parser.error(str(error))
    try:
        ejecutar(estructura, tablas, consulta, evidencia)
    except (OSError, UnicodeError, ValueError, KeyError) as error:
        print("Error:", error)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
