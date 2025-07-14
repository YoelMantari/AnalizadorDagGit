# Preguntas Teoricas

## 1. Grafo de commits como DAG

### a. Demuestra que no existen ciclos en el grafo de commits de git

Git almacena commits como objetos inmutables identificados por hash sha cada commit referencia a sus padres mediante estos hashes inmutables.
Cuando se crea un commit nuevo siempre apunta hacia commits anteriores en el tiempo nunca hacia commits futuros, esta estructura temporal garantiza que no pueden existir ciclos porque un commit no puede ser padre de si mismo ni de sus ancestros, los merges crean nuevas relaciones pero siempre desde commits mas recientes hacia commits mas antiguos manteniendo la direccion temporal

### b. Analiza la complejidad de la busqueda del critical merge path

En un dag con n nodos y m aristas el algoritmo de dijkstra tiene complejidad o(m + n log n) 

para encontrar el critical merge path necesitamos recorrer desde el commit head hasta el tag objetivo

en el peor caso visitamos todos los nodos y aristas del grafo por lo que la complejidad es o(m + n log n)

en repositorios git reales m suele ser cercano a n porque cada commit tiene pocos padres por lo que se aproxima a o(n log n)

## 2. DI DIP e ISP

### a. Dependency injection y principios solid

el micro-suite respeta dependency inversion principle porque las clases dependen de abstracciones no de implementaciones concretas, commit_stats_service recibe json_reader como parametro en lugar de importar directamente una clase de archivo, changelog_writer depende de release_notes_service a traves de su interfaz publica no de su implementacion interna, respeta interface segregation principle porque cada servicio expone solo los metodos que necesitan sus clientes, reporting_suite solo usa get_stats de stats_service y write_markdown de writer sin acoplarse a metodos innecesarios. Esta estructura permite inyectar mocks en las pruebas y cambiar implementaciones sin modificar el codigo