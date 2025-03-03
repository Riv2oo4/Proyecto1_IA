import numpy as np
import heapq
import os
import time
import pandas as pd

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
    
    return np.array(laberinto), inicio, meta

def get_neighbors(position, maze):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    neighbors = []
    for dr, dc in directions:
        r, c = position[0] + dr, position[1] + dc
        if 0 <= r < maze.shape[0] and 0 <= c < maze.shape[1] and maze[r, c] != '1':
            neighbors.append((r, c))
    return neighbors

def heuristic_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristic_euclidean(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def a_star(maze, start, goal, heuristic):
    start_time = time.time()
    priority_queue = [(0 + heuristic(start, goal), 0, start, [start])]
    visited = set()
    nodos_explorados = 0
    branching_factor_total = 0
    
    while priority_queue:
        _, cost, current, path = heapq.heappop(priority_queue)
        if current in visited:
            continue
        visited.add(current)
        nodos_explorados += 1
        
        if current == goal:
            end_time = time.time()
            tiempo_ejecucion = end_time - start_time
            branching_factor = branching_factor_total / nodos_explorados if nodos_explorados else 0
            return {
                "largo_camino": len(path) - 1,
                "nodos_explorados": nodos_explorados,
                "tiempo_ejecucion": tiempo_ejecucion,
                "branching_factor": branching_factor
            }
        
        neighbors = get_neighbors(current, maze)
        branching_factor_total += len(neighbors)
        for neighbor in neighbors:
            new_cost = cost + 1
            heapq.heappush(priority_queue, (new_cost + heuristic(neighbor, goal), new_cost, neighbor, path + [neighbor]))
    
    return None

ruta_carpeta = "Laberintos"
resultados_manhattan = []
resultados_euclidiana = []

for archivo in os.listdir(ruta_carpeta):
    if archivo.endswith(".txt"):
        ruta_archivo = os.path.join(ruta_carpeta, archivo)
        laberinto, inicio, meta = cargar_laberinto(ruta_archivo)
        
        if inicio and meta:
            resultado_manhattan = a_star(laberinto, inicio, meta, heuristic_manhattan)
            resultado_euclidiana = a_star(laberinto, inicio, meta, heuristic_euclidean)
            
            if resultado_manhattan:
                resultados_manhattan.append([
                    archivo, resultado_manhattan["largo_camino"], resultado_manhattan["nodos_explorados"],
                    resultado_manhattan["tiempo_ejecucion"], resultado_manhattan["branching_factor"]
                ])
            
            if resultado_euclidiana:
                resultados_euclidiana.append([
                    archivo, resultado_euclidiana["largo_camino"], resultado_euclidiana["nodos_explorados"],
                    resultado_euclidiana["tiempo_ejecucion"], resultado_euclidiana["branching_factor"]
                ])

df_manhattan_a_star = pd.DataFrame(resultados_manhattan, columns=["Archivo", "Largo Camino", "Nodos Explorados", "Tiempo (s)", "Branching Factor"])
df_euclidiana_a_star = pd.DataFrame(resultados_euclidiana, columns=["Archivo", "Largo Camino", "Nodos Explorados", "Tiempo (s)", "Branching Factor"])

pd.options.display.float_format = '{:,.6f}'.format  
pd.options.display.width = 150  
pd.set_option('display.max_columns', None) 

print("\nResultados A* para Heuristica Manhattan:")
print(df_manhattan_a_star.to_string(index=False))

print("\nResultados A* para Heuristica Euclidiana:")
print(df_euclidiana_a_star.to_string(index=False))
