# Analizador de Grafo Aciclico Dirigido

Sistema para analizar repositorios Git como grafos aciclicos dirigidos y generar metricas de calidad

## descripcion

analiza la estructura de commits y merges en repositorios git aplicando algoritmos de analisis de grafos para obtener metricas como densidad de ramas paths criticos de entrega entropia de historia del proyecto

## uso

```bash
python src/main.py --repo /path/to/repo
```
## Pregunta A: Algoritmo sobre el grafo de commits git

### graph_analysis.py

Se implementa  que contiene la clase `analizador_dag` esta clase implementa todos los algoritmos necesarios para analizar el grafo de commits de git

Se crea dos diccionarios uno para guardar todos los commits encontrados y otro para guardar los padres de cada commit esto lo que hace es representar la estructura del dag. 

En `obtener_commits_git`se usa el comando git rev-list --all --parents para obtener todos los commits del repositorio junto con sus padres donde procesa cada linea que contiene un commit seguido de sus commits parde si es que lo tuviera.

En `calcular_densidad_ramas`, se implementa una densidad  que calcula el numero total de nodos dividido por el numero maximo de niveles del grafo.

`calcular_path_critico` encuentra un camino simple entre dos commits especificos esto simula encontrar la ruta mas directa entre dos puntos del historial del repositorio.

`calcular_entropia` calcula la entropia de shannon del historial basandose en la proporcion de merges versus fast forwards esto nos da una medida de la complejidad del historial del repositorio

`analizar_repositorio` que es la funcion que orquesta todo el analisis llamando a todas las metricas y devolvuelve un diccionario con los resultados 

En `exportar_json` se guarda las metricas calculadas en un archivo json para poder usarlas en otros sistemas

### test_graph.py

archivo de pruebas unitarias que verifica el funcionamiento del analizador

se implemento 3 pruebas

la clase `test_dag` contiene pruebas para verificar que las funciones de calculo funcionen bien

`test_densidad_basica` se verifica que el calculo de densidad devuelva valores mayores a cero cuando hay commits en el grafo

`test_entropia_simple` con esto verificamos que el calculo de entropia devuelva valores no negativos para los grafos

`test_mock_git` se usa mocks para simular la salida del comando git, esto permite probar el parsing de la salida de git de forma aislada


### tests/fixtures/mini_repo

aqui se contiene un repositorio git miniatura creado para  las pruebas

este repositorio tiene la siguiente estructura:
- commit inicial con archivo.txt
- segundo commit con archivo2.txt  

con esta  permite estructura se prueba diferentes tipos de commits y  los merges lo cual nos ayuda para verificar que las metricas se calculen correctamente

## explicacion
entonces basicament el sistema usa subprocess para ejecutar comandos git directamente esto espara obtener la informacion del repositorio. Los algoritmos implementados son adaptados para manejar la estructura de un repositorio git, donde las metricas son la densidad, entropia y el path critico, donde este es el camino simple entre 2 commits en especifico

## Pregunta B: Micro-suite Python con DI, Facade y Composition





