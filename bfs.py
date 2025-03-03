import os
import time
import pandas as pd
import numpy as np
from collections import deque

class Grafo:
    def __init__(self, laberinto):
        self.laberinto = np.array(laberinto) 
        self.filas, self.columnas = self.laberinto.shape
        self.movimientos = [(-1, 0), (0, 1), (1, 0), (0, -1)]  

    def es_valido(self, fila, columna, visitados):
        return 0 <= fila < self.filas and 0 <= columna < self.columnas and self.laberinto[fila, columna] != '1' and (fila, columna) not in visitados

def reconstruir_camino(padres, inicio, meta):
    camino = []
    nodo = meta
    while nodo is not None:
        camino.append(nodo)
        nodo = padres.get(nodo)
    return list(reversed(camino))

def bfs(laberinto, inicio, meta):
    inicio_tiempo = time.time()
    
    grafo = Grafo(laberinto)
    cola = deque([inicio])  
    visitados = set([inicio])
    padres = {inicio: None}  
    nodos_explorados = 0
    nodos_generados = 0  

    while cola:
        nodo_actual = cola.popleft()
        nodos_explorados += 1

        if nodo_actual == meta:
            camino = reconstruir_camino(padres, inicio, meta)
            fin_tiempo = time.time()
            branching_factor = nodos_generados / nodos_explorados if nodos_explorados > 0 else 0  

            return {
                "largo_camino": len(camino) - 1,  
                "nodos_explorados": nodos_explorados,
                "nodos_generados": nodos_generados,
                "branching_factor": branching_factor,
                "tiempo_ejecucion": fin_tiempo - inicio_tiempo,
            }

        for movimiento in grafo.movimientos:
            nueva_fila, nueva_columna = nodo_actual[0] + movimiento[0], nodo_actual[1] + movimiento[1]
            nueva_posicion = (nueva_fila, nueva_columna)
            
            if grafo.es_valido(nueva_fila, nueva_columna, visitados):
                visitados.add(nueva_posicion)  
                padres[nueva_posicion] = nodo_actual  
                cola.append(nueva_posicion)
                nodos_generados += 1  

    return None  

def cargar_laberinto(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        laberinto = [list(line.strip()) for line in f.readlines()]  

    laberinto = np.array(laberinto)  
    inicio = tuple(map(int, np.argwhere(laberinto == '2')[0]))
    meta = tuple(map(int, np.argwhere(laberinto == '3')[0]))

    return laberinto, inicio, meta

ruta_carpeta = "Laberintos"
resultados = []

for archivo in os.listdir(ruta_carpeta):
    if archivo.endswith(".txt"):
        ruta_archivo = os.path.join(ruta_carpeta, archivo)
        laberinto, inicio, meta = cargar_laberinto(ruta_archivo)

        if inicio and meta:
            resultado = bfs(laberinto, inicio, meta)
            if resultado:
                resultados.append([
                    archivo, 
                    resultado["largo_camino"], 
                    resultado["nodos_explorados"], 
                    resultado["nodos_generados"], 
                    resultado["branching_factor"], 
                    resultado["tiempo_ejecucion"]
                ])
            else:
                resultados.append([archivo, "No solucionable", "No solucionable", "No solucionable", "No solucionable", "No solucionable"])
        else:
            resultados.append([archivo, "Error en el archivo", "Error en el archivo", "Error en el archivo", "Error en el archivo", "Error en el archivo"])

df_resultados = pd.DataFrame(resultados, columns=[
    "Archivo", "Largo del Camino", "Nodos Explorados", "Nodos Generados", "Branching Factor", "Tiempo de Ejecucion (s)"
])
pd.set_option('display.max_columns', None)  
pd.set_option('display.expand_frame_repr', False)  
pd.set_option('display.max_colwidth', None)  

print(df_resultados.to_string(index=False))
