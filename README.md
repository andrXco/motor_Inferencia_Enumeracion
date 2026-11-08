# Motor de inferencia por enumeración

Programa orientado a objetos en Python para cargar redes bayesianas desde archivos y calcular probabilidades mediante enumeración. Muestra la estructura, las tablas y una traza de los cálculos.

## Ejecución sencilla, sin menú

1. Abrir en Visual Studio Code la carpeta que contiene `main.py`.
2. Seleccionar **Terminal > Nueva terminal**.
3. Ejecutar:

```cmd
python main.py
```

Si Windows no reconoce `python`, intentar:

```cmd
py main.py
```

Para elegir la prueba original explícitamente:

```cmd
python main.py original
```

Para ejecutar la prueba compleja, con congestión y fiebre:

```cmd
python main.py compleja
```

Ambos comandos muestran toda la traza y no abren un menú. Sin nombre de prueba, se ejecuta la original.

### ¿Qué pregunta responde la prueba original?

Según las probabilidades del ejemplo, ¿qué probabilidad hay de gripa si sabemos que hay congestión?

- Estructura: `relaciones_prueba.txt`.
- Tablas: `tabla_prueba.txt`.
- Consulta: `Gripa`.
- Evidencia conocida: `Congestion=yes`.
- Variable oculta que se enumera: `Alergia`.

## Qué debe mostrar la ejecución

1. Archivos seleccionados, consulta y evidencia.
2. Nodos cargados y orden topológico.
3. Estructura: estados, padres e hijos de cada nodo.
4. Tablas de probabilidades.
5. Consulta, evidencia y variables ocultas.
6. Cada combinación de estados y la multiplicación de sus probabilidades.
7. Sumas por estado de la consulta.
8. Total de evidencia `P(E)`, factor de normalización y divisiones.
9. Distribución final y su suma, aproximadamente 1.

## Probar otro caso con el mismo main.py

`main.py` es el único punto de entrada necesario. No se necesita crear un programa Python diferente por cada red. Las pruebas incluidas se eligen con los nombres `original` y `compleja`. Para una red nueva, se pueden indicar sus archivos, consulta y evidencias como opciones del comando.

### Gripa con congestión y fiebre

Pregunta: ¿qué probabilidad hay de gripa si conocemos que hay congestión y fiebre?

```cmd
python main.py compleja
```

Resultado esperado: aproximadamente **88.70 %** para gripa y **11.30 %** para no gripa. Se enumeran `Alergia` y `OtraInfeccion`: cuatro combinaciones por cada estado de `Gripa`, ocho en total.

```text
Suma para Gripa=yes: 0.075032
Suma para Gripa=no: 0.009558
Total P(E): 0.08459
```

### Gripa con congestión, pero sin fiebre

```cmd
python main.py compleja --evidencia Congestion=yes Fiebre=no
```

Resultado esperado: aproximadamente **4.97 %** para gripa y **95.03 %** para no gripa.

### Qué significan las opciones

- `--estructura`: archivo de relaciones entre nodos.
- `--tablas`: archivo de probabilidades.
- `--consulta`: nodo del que se calcula la distribución de probabilidad.
- `--evidencia`: estados que ya conocemos, escritos como `Nodo=estado` y separados por espacios.

Al seleccionar archivos personalizados hay que indicar juntos estructura, tablas y consulta. Si se omite la evidencia, se consulta sin observaciones. En cambio, al ejecutar solo `python main.py`, se utiliza la prueba original con congestión conocida.

Para estados con espacios se usan comillas, por ejemplo `--evidencia "Train=on time"`.

## Cómo crear los TXT de una red

Cada red utiliza dos archivos. Son datos de entrada que exige el proyecto, no programas adicionales.

### Archivo de estructura

Una dependencia por línea:

```text
Gripa -> Congestion
Alergia -> Congestion
```

Los nodos se declaran en el archivo de tablas. Una raíz aislada puede existir aunque no aparezca en ninguna dependencia.

### Archivo de probabilidades

Un bloque por nodo. Una raíz tiene una distribución sin padres:

```text
[NODO]
Gripa
estados: yes, no
padres: -
yes: 0.1
no: 0.9
```

Un nodo dependiente tiene una fila por cada combinación de estados de sus padres:

```text
[NODO]
Congestion
estados: yes, no
padres: Gripa, Alergia
yes, yes | yes: 0.95, no: 0.05
yes, no | yes: 0.8, no: 0.2
no, yes | yes: 0.7, no: 0.3
no, no | yes: 0.05, no: 0.95
```

Este fragmento requiere también un bloque para `Alergia` y el archivo de relaciones correspondiente.

Los nombres y estados deben coincidir exactamente. El orden de las condiciones corresponde al orden de `padres`. Cada distribución debe sumar 1 y tener valores entre 0 y 1. No puede haber ciclos en la red.

## Archivos y responsabilidades

| Archivo | Función |
| --- | --- |
| `main.py` | Carga la configuración, conecta los módulos y muestra el resultado. |
| `lector.py` | Lee las relaciones y tablas y valida los datos. |
| `nodo.py` | Representa nombre, estados, padres, hijos y tabla de un nodo. |
| `red_bayesiana.py` | Recorre la red, muestra su contenido y calcula la inferencia. |
| `relaciones_prueba.txt`, `tabla_prueba.txt` | Red original de gripa, alergia y congestión. |
| `relaciones_gripa_compleja.txt`, `tabla_gripa_compleja.txt` | Red con gripa, alergia, otra infección, congestión y fiebre. |
| `relaciones.txt`, `tabla.txt` | Red de lluvia, mantenimiento, tren y cita. |
| `PRUEBAS_GRIPA.txt` | Explicación ampliada y cálculos esperados de las pruebas de gripa. |
| `probar_gripa.cmd` | Atajo opcional de Windows para la prueba compleja. No es necesario si se utiliza `main.py`. |

`__pycache__` contiene archivos que Python genera automáticamente. No contiene los datos de las redes ni es necesario editarlo.

## Cómo funciona la enumeración

1. Se construyen los nodos y las dependencias.
2. Se cargan y validan las tablas de probabilidad.
3. Se obtiene un orden donde los padres aparecen antes que sus hijos.
4. Se fija cada estado posible del nodo consultado junto con la evidencia.
5. Se generan las combinaciones de las variables ocultas.
6. Para cada combinación completa se multiplica la probabilidad de cada nodo dado el estado de sus padres.
7. Se suman los productos por estado de la consulta.
8. Se divide cada suma entre el total para obtener la distribución condicional.
