import pygame
import heapq

pygame.init()

# Configuraciones iniciales
ANCHO_VENTANA = 600  # Ancho de la ventana
FILAS = 9  # Número de filas y columnas del grid
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))  # Inicialización de la ventana de Pygame
pygame.display.set_caption("Visualización del Algoritmo A*")

# Colores personalizados
FONDO = (40, 40, 50)  # Color de fondo del grid (tonos oscuros: gris oscuro)
LINEAS = (70, 70, 80)  # Color de las líneas del grid (gris un poco más claro que el fondo)
COLOR_INICIO = (50, 200, 200)  # Color del nodo de inicio (cian)
COLOR_FIN = (255, 70, 70)  # Color del nodo de fin (rojo)
COLOR_RUTA = (50, 150, 50)  # Color de la ruta más corta (verde)
COLOR_PARED = (100, 100, 120)  # Color de los nodos que representan paredes (gris medio)
COLOR_VISITADO = (200, 50, 200)  # Color de los nodos visitados durante la búsqueda (morado)
COLOR_NODO = (80, 80, 90)  # Color de los nodos no visitados (gris oscuro)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = FONDO
        self.ancho = ancho
        self.total_filas = total_filas

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == COLOR_PARED

    def restablecer(self):
        self.color = FONDO

    def hacer_inicio(self):
        self.color = COLOR_INICIO

    def hacer_pared(self):
        self.color = COLOR_PARED

    def hacer_fin(self):
        self.color = COLOR_FIN

    def do_route(self):
        self.color = COLOR_RUTA

    def hacer_visitado(self):
        self.color = COLOR_VISITADO

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho - 2, self.ancho - 2))  # Márgenes ajustados

# Crear grid (matriz de nodos)
def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

# Dibujar las líneas del grid
def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, LINEAS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, LINEAS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

# Dibujar el grid y los nodos en la ventana
def dibujar(ventana, grid, filas, ancho):
    ventana.fill(FONDO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)
    dibujar_grid(ventana, filas, ancho)
    dibujar_leyenda(ventana, ancho)
    pygame.display.update()

# Leyenda de teclas y controles
def dibujar_leyenda(ventana, ancho):
    fuente = pygame.font.SysFont("arial", 18)
    leyenda = [
        "Click Izquierdo: Inicio / Fin / Pared",
        "Click Derecho: Eliminar Nodo",
        "Enter: Iniciar A*",
        "ESC: Salir"
    ]
    for i, texto in enumerate(leyenda):
        render = fuente.render(texto, True, (255, 255, 255))
        ventana.blit(render, (10, ancho - 100 + i * 20))

# Obtener la posición del mouse en términos de filas y columnas
def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

# Algoritmo A* (A Star)
def astar(draw, grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}

    g_score = {nodo: float("inf") for fila in grid for nodo in fila}
    g_score[start] = 0
    f_score = {nodo: float("inf") for fila in grid for nodo in fila}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.hacer_fin()
            return True

        for neighbor, cost in get_neighbors(grid, current):
            temp_g_score = g_score[current] + cost

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.hacer_visitado()

        draw()

        if current != start:
            current.hacer_visitado()

    return False

# Heurística (distancia de Manhattan)
def h(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

# Reconstruir la ruta más corta
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.do_route()
        draw()

# Obtener vecinos de un nodo (incluye diagonales)
def get_neighbors(grid, nodo):
    neighbors = []
    row, col = nodo.get_pos()

    directions = [
        (-1, 0, 1),  # Arriba
        (1, 0, 1),   # Abajo
        (0, -1, 1),  # Izquierda
        (0, 1, 1),   # Derecha
        (-1, -1, 1.414),  # Diagonal arriba-izquierda
        (-1, 1, 1.414),   # Diagonal arriba-derecha
        (1, -1, 1.414),   # Diagonal abajo-izquierda
        (1, 1, 1.414),    # Diagonal abajo-derecha
    ]

    for dr, dc, cost in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and not grid[r][c].es_pared():
            neighbors.append((grid[r][c], cost))

    return neighbors

# Función principal
def main(ventana, filas, ancho):
    grid = crear_grid(filas, ancho)
    start = None
    end = None
    run = True

    while run:
        dibujar(ventana, grid, filas, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, filas, ancho)
                nodo = grid[fila][col]
                if not start and nodo != end:
                    start = nodo
                    start.hacer_inicio()
                elif not end and nodo != start:
                    end = nodo
                    end.hacer_fin()
                elif nodo != start and nodo != end:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, filas, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == start:
                    start = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and start and end:
                    astar(lambda: dibujar(ventana, grid, filas, ancho), grid, start, end)


    pygame.quit()


if __name__ == "__main__":  # Correct usage of __name__
    main(VENTANA, FILAS, ANCHO_VENTANA)
