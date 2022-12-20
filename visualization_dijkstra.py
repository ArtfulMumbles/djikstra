from os import sys
import pygame
import numpy as np

N = 50
vertices_no = 0
vertices = []
graph = []
grid = []
walls = [0 for i in range(N**2)]


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (127, 127, 127)
WINDOW_HEIGHT = 900
WINDOW_WIDTH = 900


def main():
    global SCREEN, CLOCK, grid, graph
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    START = 0
    END = 0
    setup(N)

    map_creator = True
    mousedown = False
    last_changed = (0, 0)
    while map_creator:
        drawGrid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousedown = True
                
            elif event.type == pygame.MOUSEBUTTONUP:
                mousedown = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    map_creator = False
                    
        if mousedown:
            x, y = pygame.mouse.get_pos()
            x = int(x // (WINDOW_HEIGHT / N))
            y = int(y // (WINDOW_HEIGHT / N))
            
            if x != last_changed[0] or y != last_changed[1]:
                if grid[x][y] == 0:
                    grid[x][y] = 2
                else:
                    grid[x][y] = 0
                last_changed = (x, y)
                
        pygame.display.update()

    start_end = True
    count = 0
    while start_end:
        drawGrid()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x = int(x // (WINDOW_HEIGHT / N))
                y = int(y // (WINDOW_HEIGHT / N))
                if count == 0:
                    START = x*N + y
                    grid[x][y] = 1
                    count = 1
                elif count == 1:
                    END = x*N + y
                    grid[x][y] = 3
                    count = 2
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and count == 2:
                    start_end = False
 
                
        pygame.display.update()

    graph = make_matrix()
    
    path = Dijkstra(START, END)
    print(path)
    for n in path:
        grid[n // N][n % N] = 1
    
    while True:
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def setup(N):
    global grid    
    grid = [[0 for i in range(N)] for j in range(N)]
      
    for i in range(N**2):
        add_vertex(i)
        
    

def drawGrid():
    blockSize = WINDOW_HEIGHT / N #Set the size of the grid block

    SCREEN.fill(BLACK)
    for x in range(N):
        for y in range(N):
            rect = pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize)
            if grid[x][y] == 1:
                pygame.draw.rect(SCREEN, GREEN, rect, 0)
            elif grid[x][y] == 2:
                pygame.draw.rect(SCREEN, RED, rect, 0)
            elif grid[x][y] == 3:
                pygame.draw.rect(SCREEN, YELLOW, rect, 0)
                
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

def drawSquare(x, y, color):
    blockSize = WINDOW_HEIGHT / N #Set the size of the grid block
    rect = pygame.Rect(x * blockSize, y * blockSize, blockSize, blockSize)    
    pygame.draw.rect(SCREEN, color, rect, 0)
            

def add_vertex(v):
    global graph
    global vertices_no
    global vertices
    if v in vertices:
        print("Vertex ", v, " already exists")
    else:
        vertices_no += 1
        vertices.append(v)

def make_matrix():
    global walls
    M = [[0 for i in range(N**2)] for j in range(N**2)]
    for r in range(N):
        for c in range(N):
            i = r*N + c
            # Two inner diagonals
            if c > 0: M[i-1][i] = M[i][i-1] = 1
            # Two outer diagonals
            if r > 0: M[i-N][i] = M[i][i-N] = 1
            
    for x in range(N):
        for y in range(N):
            if grid[x][y] == 2:
                for k in range(N**2):
                    sto = x*N + y
                    M[k][sto] = 0
                    
                    
    return M

def Dijkstra(initial, dest):
    print("Running Dijkstra's Algorithm")
    
    global graph, grid, walls

    slope = (255) / (np.sqrt(N**2 + N**2) - 1)
    end_x = dest // N
    end_y = dest % N

    visited = []
    tent_dist = []
    
    for i in range(vertices_no):
        if walls[i] == 1:
            visited.append(1)
        else:
            visited.append(0)
        tent_dist.append(10000000)
        
    tent_dist[vertices.index(initial)] = 0

    current_node = vertices.index(initial)

    running = True
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.time.wait(0)
        for i in range(vertices_no):
            if graph[current_node][i] != 0 and visited[i] == 0:
                    if tent_dist[current_node] + graph[current_node][i] < tent_dist[i]:
                        tent_dist[i] = tent_dist[current_node] + graph[current_node][i]
        visited[current_node] = 1

        x = current_node // N
        y = current_node % N
        dist = np.sqrt((x-end_x)**2 + (y-end_y)**2)
        drawSquare(x, y, list(map(lambda i: int(slope * (i)), (dist, dist, dist))))
        pygame.display.update()

        
        if visited[vertices.index(dest)] == 1:
            shortest_path = []
            current_node = vertices.index(dest)
            moving = True
            shortest_path.append(dest)
            while(moving):
                min_dist = 10000
                min_vertex = 0
                for i in range(vertices_no):
                    if graph[i][current_node] != 0:
                        if tent_dist[i] < min_dist:
                            min_dist = tent_dist[i]
                            min_vertex = i
                shortest_path.insert(0, vertices[min_vertex])
                current_node = min_vertex
                if tent_dist[current_node] == 0:
                    moving = False
                
            return shortest_path
            
        min_dist = 10000
        min_vertex = 0
        for i in range(vertices_no):
            if visited[i] == 0 and tent_dist[i] < min_dist:
                min_vertex = i
                min_dist = tent_dist[i]
                
        current_node = min_vertex


main()
    
