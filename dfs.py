import os
import time
import pandas as pd

class PilaLIFO:
    def __init__(self):
        self.datos = []

    def EMPTY(self):
        return len(self.datos) == 0

    def POP(self):
        return self.datos.pop() if not self.EMPTY() else None

    def ADD(self, elemento):
        self.datos.append(elemento)

class Nodo:
    def __init__(self, estado, padre=None, costo=0):
        self.estado = estado  # Coordenadas (fila, columna)
        self.padre = padre  # Nodo padre en la ruta
        self.costo = costo  # Costo acumulado

    def __eq__(self, other):
        return self.estado == other.estado

    def __hash__(self):
        return hash(self.estado)

class Grafo:
    def __init__(self, laberinto):
        self.laberinto = laberinto
        self.filas = len(laberinto)
        self.columnas = len(laberinto[0])
        self.movimientos = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Arriba, Derecha, Abajo, Izquierda

    def es_valido(self, fila, columna):
        return 0 <= fila < self.filas and 0 <= columna < self.columnas and self.laberinto[fila][columna] != '1'

    def obtener_vecinos(self, nodo):
        vecinos = []
        fila, columna = nodo.estado
        for movimiento in self.movimientos:
            nueva_fila, nueva_columna = fila + movimiento[0], columna + movimiento[1]
            if self.es_valido(nueva_fila, nueva_columna):
                vecinos.append(Nodo((nueva_fila, nueva_columna), padre=nodo, costo=nodo.costo + 1))
        return vecinos

def dfs(laberinto, inicio, meta):
    inicio_tiempo = time.time()

    grafo = Grafo(laberinto)
    nodo_inicio = Nodo(inicio)
    pila = PilaLIFO()
    pila.ADD(nodo_inicio)
    visitados = set()
    visitados.add(nodo_inicio)
    nodos_explorados = 0
    branching_factor_total = 0
    camino = []

    while not pila.EMPTY():
        nodo_actual = pila.POP()
        nodos_explorados += 1

        if nodo_actual.estado == meta:
            fin_tiempo = time.time()
            tiempo_ejecucion = fin_tiempo - inicio_tiempo

            # Reconstruir el camino
            while nodo_actual:
                camino.append(nodo_actual.estado)
                nodo_actual = nodo_actual.padre
            camino.reverse()

            branching_factor = branching_factor_total / nodos_explorados if nodos_explorados else 0
            return {
                "largo_camino": len(camino) - 1,
                "nodos_explorados": nodos_explorados,
                "tiempo_ejecucion": tiempo_ejecucion,
                "branching_factor": branching_factor,
            }

        vecinos = grafo.obtener_vecinos(nodo_actual)
        branching_factor_total += len(vecinos)

        for vecino in reversed(vecinos):  # Se invierte el orden para simular pila (LIFO)
            if vecino not in visitados:
                visitados.add(vecino)
                pila.ADD(vecino)

    return None  # No se encontró solución

def cargar_laberinto(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        laberinto = [list(line.strip()) for line in f.readlines()]

    inicio, meta = None, None
    for i in range(len(laberinto)):
        for j in range(len(laberinto[i])):
            if laberinto[i][j] == '2':
                inicio = (i, j)
            elif laberinto[i][j] == '3':
                meta = (i, j)

    return laberinto, inicio, meta

# Procesar todos los laberintos en la carpeta "Laberintos"
ruta_carpeta = "Laberintos"
resultados = []

for archivo in os.listdir(ruta_carpeta):
    if archivo.endswith(".txt"):
        ruta_archivo = os.path.join(ruta_carpeta, archivo)
        laberinto, inicio, meta = cargar_laberinto(ruta_archivo)

        if inicio and meta:
            resultado = dfs(laberinto, inicio, meta)
            if resultado:
                resultados.append([archivo, resultado["largo_camino"], resultado["nodos_explorados"], resultado["tiempo_ejecucion"], resultado["branching_factor"]])
            else:
                resultados.append([archivo, "No solucionable", "No solucionable", "No solucionable", "No solucionable"])
        else:
            resultados.append([archivo, "Error en el archivo", "Error en el archivo", "Error en el archivo", "Error en el archivo"])

# Mostrar resultados en consola
df_resultados = pd.DataFrame(resultados, columns=["Archivo", "Largo del Camino", "Nodos Explorados", "Tiempo de Ejecución (s)", "Branching Factor"])
pd.set_option('display.max_columns', None)  # Muestra todas las columnas
pd.set_option('display.expand_frame_repr', False)  # Evita que se parta en múltiples líneas
pd.set_option('display.max_colwidth', None)  # Evita truncamiento de valores largos

print(df_resultados.to_string(index=False))  
