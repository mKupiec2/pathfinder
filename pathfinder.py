import pygame  # pip install pygame
from queue import PriorityQueue
import tkinter as tk


WIDTH = 800
ROWS = 50
WIN = pygame.display.set_mode((1000, WIDTH))
pygame.font.init()
pygame.display.set_caption("Pathfinding in Python")

# COLORS
#################################
RED = (255, 0, 0)               #
GREEN = (0, 255, 0)             #
BLUE = (0, 0, 255)              #
WHITE = (255, 255, 255)         #
BLACK = (0, 0, 0)               #
GREY = (128, 128, 128)          #
YELLOW = (255, 255, 0)          #
PURPLE = (128, 0, 128)          #
ORANGE = (255, 168, 0)          #
TURQUOISE = (64, 224, 255)      #
#################################


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    """
    The heuristic function. Calculate the estimated distance between `p1` and `p2`
    :param p1: Start node position
    :param p2: End node position
    :return: the estimated distance between `p1` and `p2`
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    """
    Reconstruct the path calculated by the algorithm
    :param came_from: Previous node
    :param current:  Current node
    :param draw: Function draw()
    """
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def a_start(draw, grid, start, end):
    """
    A* pathfinding algorithm that finds the shortest possible path
    :param draw: Function draw()
    :param grid: Array containing all node objects
    :param start: Start node object
    :param end: End node object
    :return: Returns False if there is no path possible, returns True if found the shortest path
    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    end.make_end()

        draw()

        if current != start:
            current.make_closed()

    return False


def dijkstra(draw, grid, start, end):
    """
    Dijkstra pathfinding algorithm that finds the shortest path possible. Less efficient than A*
    :param draw: Function draw()
    :param grid: Array containing all node objects
    :param start: Start node object
    :param end: End node object
    :return: Returns False if there is no path possible, returns True if found the shortest path
    """
    count = 0
    queue = PriorityQueue()
    queue.put((0, count, start))
    came_from = {}
    dist = {node: float("inf") for row in grid for node in row}
    dist[start] = 0

    open_set_hash = {start}

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_dist = dist[current] + 1

            if temp_dist < dist[neighbor]:
                came_from[neighbor] = current
                dist[neighbor] = temp_dist
                if neighbor not in open_set_hash:
                    count += 1
                    queue.put((dist[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        end.make_end()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    """
    Function that makes the grid array containing all node objects
    :param rows: Amount of rows in grid
    :param width: Width of grid
    :return: array containing all node objects
    """
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    """
    Draw grid in the window
    :param win: Window to draw grid in
    :param rows: Amount of rows in grid
    :param width: Width of grid
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows + 1):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    """
    Draw buttons, grid, nodes on the screen
    :param win: Window to draw in
    :param grid: Array containing all node objects
    :param rows: Amount of rows in grid
    :param width: Width of grid
    """
    win.fill(WHITE)
    pygame.draw.rect(WIN, GREY, (850, 200, 100, 50))
    pygame.draw.rect(WIN, GREY, (850, 300, 100, 50))
    pygame.draw.rect(WIN, GREY, (850, 400, 100, 50))
    my_font = pygame.font.SysFont('Calibri', 35)
    my_font2 = pygame.font.SysFont('Calibri', 28)
    text_surface = my_font.render('Start', False, (0, 0, 0))
    WIN.blit(text_surface, (868, 209))
    text_surface2 = my_font2.render('Settings', False, (0, 0, 0))
    WIN.blit(text_surface2, (856, 312))
    text_surface = my_font.render('Reset', False, (0, 0, 0))
    WIN.blit(text_surface, (861, 409))

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    """
    Get the row and col that the user clicked on
    :param pos: Mouse position
    :param rows: Amount of rows in grid
    :param width: Width of grid
    :return: Clicked row and col
    """
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def choose_window():
    """
    Display the tutorial window
    """
    global window
    global chosen
    chosen = False
    window = tk.Tk()
    window.geometry("500x300+700+300")
    window.title("Tutorial")
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)
    window.columnconfigure(3, weight=1)
    window.columnconfigure(4, weight=1)

    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    window.rowconfigure(2, weight=1)
    window.rowconfigure(3, weight=1)
    window.rowconfigure(4, weight=1)
    window.rowconfigure(5, weight=1)

    label = tk.Label(window, text="Choose your algorithm")
    label.grid(row=0, column=0, columnspan=5)

    button_frame = tk.Frame(window)
    but1 = tk.Button(button_frame, text='A*', command=call_a_star)
    but2 = tk.Button(button_frame, text='Dijkstra', command=call_dijkstra)
    but1.grid(row=0, column=0)
    but2.grid(row=0, column=1)
    button_frame.grid(row=1, column=2, sticky='n')

    window.mainloop()


def call_a_star():
    """
    Choose the A* algorithm
    """
    global algorithm, chosen
    algorithm = "a*"
    chosen = True
    window.destroy()


def call_dijkstra():
    """
    Choose the dijkstra algorithm
    """
    global algorithm, chosen
    algorithm = "dijkstra"
    chosen = True
    window.destroy()


def main(win, width):
    """
    Contains the main loop that runs the whole app
    :param win: Window to draw in
    :param width: Width of the grid
    """
    global ROWS
    choose_window()
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    done = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] <= 800 and pos[1] <= 800:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    if not start and node != end:
                        start = node
                        start.make_start()

                    elif not end and node != start:
                        end = node
                        end.make_end()

                    elif node != end and node != start:
                        node.make_barrier()

                if 850 < pos[0] < 950 and 200 < pos[1] < 250:
                    if start and end and not done:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)

                        if chosen:
                            if algorithm == "a*":
                                a_start(lambda: draw(win, grid, ROWS, width), grid, start, end)
                            elif algorithm == "dijkstra":
                                dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)
                            done = True
                        else:
                            choose_window()

                if 850 < pos[0] < 950 and 300 < pos[1] < 350:
                    choose_window()

                if 850 < pos[0] < 950 and 400 < pos[1] < 450:
                    start = None
                    end = None
                    done = False
                    grid = make_grid(ROWS, width)

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                if pos[0] <= 800 and pos[1] <= 800:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

    pygame.quit()


if __name__ == '__main__':
    main(WIN, WIDTH)
