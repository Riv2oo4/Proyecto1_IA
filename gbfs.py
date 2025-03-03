import os
import time
import math
import heapq
import pandas as pd

class Nodo:
    def __init__(self, estado, padre=None, costo=0, heuristica=0):
        self.estado = estado  # Coordenadas (fila, columna)
        self.padre = padre  # Nodo padre en la ruta
        self.costo = costo  # Costo acumulado
        self.heuristica = heuristica  # Valor heurístico
    
    def __lt__(self, other):
        return self.heuristica < other.heuristica
    
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
    
    def obtener_vecinos(self, nodo, meta, heuristica_tipo):
        vecinos = []
        fila, columna = nodo.estado
        for movimiento in self.movimientos:
            nueva_fila, nueva_columna = fila + movimiento[0], columna + movimiento[1]
            if self.es_valido(nueva_fila, nueva_columna):
                heuristica = calcular_heuristica((nueva_fila, nueva_columna), meta, heuristica_tipo)
                vecinos.append(Nodo((nueva_fila, nueva_columna), padre=nodo, costo=nodo.costo + 1, heuristica=heuristica))
        return vecinos

def calcular_heuristica(pos, meta, tipo):
    x1, y1 = pos
    x2, y2 = meta
    if tipo == "manhattan":
        return abs(x1 - x2) + abs(y1 - y2)
    elif tipo == "euclidiana":
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return 0

def greedy_bfs(laberinto, inicio, meta, heuristica_tipo):
    inicio_tiempo = time.time()
    
    grafo = Grafo(laberinto)
    nodo_inicio = Nodo(inicio, heuristica=calcular_heuristica(inicio, meta, heuristica_tipo))
    frontera = []
    heapq.heappush(frontera, nodo_inicio)
    visitados = set()
    visitados.add(nodo_inicio)
    nodos_explorados = 0
    branching_factor_total = 0
    camino = []
    
    while frontera:
        nodo_actual = heapq.heappop(frontera)
        nodos_explorados += 1
        
        if nodo_actual.estado == meta:
            fin_tiempo = time.time()
            tiempo_ejecucion = fin_tiempo - inicio_tiempo
            
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
        
        vecinos = grafo.obtener_vecinos(nodo_actual, meta, heuristica_tipo)
        branching_factor_total += len(vecinos)
        
        for vecino in vecinos:
            if vecino not in visitados:
                visitados.add(vecino)
                heapq.heappush(frontera, vecino)
    
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
            resultado_manhattan = greedy_bfs(laberinto, inicio, meta, "manhattan")
            resultado_euclidiana = greedy_bfs(laberinto, inicio, meta, "euclidiana")
            
            if resultado_manhattan and resultado_euclidiana:
                resultados.append([
                    archivo, resultado_manhattan["largo_camino"], resultado_manhattan["nodos_explorados"], resultado_manhattan["tiempo_ejecucion"], resultado_manhattan["branching_factor"],
                    resultado_euclidiana["largo_camino"], resultado_euclidiana["nodos_explorados"], resultado_euclidiana["tiempo_ejecucion"], resultado_euclidiana["branching_factor"]
                ])
            else:
                resultados.append([archivo, "No solucionable"] * 9)
        else:
            resultados.append([archivo, "Error en el archivo"] * 9)

# Guardar en un DataFrame y mostrar resultados
df_resultados = pd.DataFrame(resultados, columns=[
    "Archivo", "Largo Camino (Manhattan)", "Nodos Explorados (Manhattan)", "Tiempo Ejecución (Manhattan)", "Branching Factor (Manhattan)",
    "Largo Camino (Euclidiana)", "Nodos Explorados (Euclidiana)", "Tiempo Ejecución (Euclidiana)", "Branching Factor (Euclidiana)"
])

pd.set_option('display.max_columns', None)  # Muestra todas las columnas
pd.set_option('display.expand_frame_repr', False)  # Evita que se parta en múltiples líneas
pd.set_option('display.max_colwidth', None)  # Evita truncamiento de valores largos

print(df_resultados.to_string(index=False))  
