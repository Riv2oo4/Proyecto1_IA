import numpy as np
import heapq
from collections import deque
import time
from tabulate import tabulate

def cargar_laberinto(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            return np.array([list(map(int, linea.strip().replace(',', ''))) for linea in archivo if linea.strip()])
    except ValueError:
        print("Error al procesar el laberinto.")
        return None

def get_neighbors(position, maze):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    return [(r, c) for dr, dc in directions if 0 <= (r := position[0] + dr) < maze.shape[0] and 0 <= (c := position[1] + dc) < maze.shape[1] and maze[r, c] != 1]

def medir_rendimiento(algoritmo, maze, start, goal, heuristic=None):
    start_time = time.time()
    path, nodos_recorridos = algoritmo(maze, start, goal, heuristic) if heuristic else algoritmo(maze, start, goal)
    return len(path) if path else 0, time.time() - start_time, nodos_recorridos

def bfs(maze, start, goal):
    queue, visited, nodos_recorridos = deque([(start, [start])]), set(), 0
    while queue:
        current, path = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        nodos_recorridos += 1
        if current == goal:
            return path, nodos_recorridos
        queue.extend((neighbor, path + [neighbor]) for neighbor in get_neighbors(current, maze))
    return None, nodos_recorridos

def dfs(maze, start, goal):
    stack, visited, nodos_recorridos = [(start, [start])], set(), 0
    while stack:
        current, path = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        nodos_recorridos += 1
        if current == goal:
            return path, nodos_recorridos
        stack.extend((neighbor, path + [neighbor]) for neighbor in get_neighbors(current, maze))
    return None, nodos_recorridos

def greedy_search(maze, start, goal, heuristic):
    priority_queue, visited, nodos_recorridos = [(heuristic(start, goal), start, [start])], set(), 0
    while priority_queue:
        _, current, path = heapq.heappop(priority_queue)
        if current in visited:
            continue
        visited.add(current)
        nodos_recorridos += 1
        if current == goal:
            return path, nodos_recorridos
        for neighbor in get_neighbors(current, maze):
            heapq.heappush(priority_queue, (heuristic(neighbor, goal), neighbor, path + [neighbor]))
    return None, nodos_recorridos

def a_star(maze, start, goal, heuristic):
    priority_queue, visited, nodos_recorridos = [(0 + heuristic(start, goal), 0, start, [start])], set(), 0
    while priority_queue:
        _, cost, current, path = heapq.heappop(priority_queue)
        if current in visited:
            continue
        visited.add(current)
        nodos_recorridos += 1
        if current == goal:
            return path, nodos_recorridos
        for neighbor in get_neighbors(current, maze):
            heapq.heappush(priority_queue, (cost + 1 + heuristic(neighbor, goal), cost + 1, neighbor, path + [neighbor]))
    return None, nodos_recorridos

def heuristic_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristic_euclidean(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

nombre_archivo = "Laberintos/Laberinto3-3.txt"
laberinto = cargar_laberinto(nombre_archivo)

if laberinto is not None:
    start_positions = [(r, c) for r in range(laberinto.shape[0]) for c in range(laberinto.shape[1]) if laberinto[r, c] == 2]
    goal_positions = [(r, c) for r in range(laberinto.shape[0]) for c in range(laberinto.shape[1]) if laberinto[r, c] == 3]
    
    if start_positions and goal_positions:
        start, goal = start_positions[0], goal_positions[0]
        algoritmos = {
            "BFS": (bfs, None), "DFS": (dfs, None),
            "Greedy Manhattan": (greedy_search, heuristic_manhattan),
            "Greedy Euclidean": (greedy_search, heuristic_euclidean),
            "A*_Manhattan": (a_star, heuristic_manhattan),
            "A*_Euclidean": (a_star, heuristic_euclidean)
        }
        
        resultados = [[nombre, *medir_rendimiento(algoritmo, laberinto, start, goal, heuristica)] for nombre, (algoritmo, heuristica) in algoritmos.items()]
        print(tabulate(resultados, headers=["Algoritmo", "Pasos", "Tiempo (s)", "Nodos Recorridos"], tablefmt="grid"))