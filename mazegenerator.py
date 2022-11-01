#  N = sirka, M = vyska
#  maze[M][N]
import random
import numpy as np

def carve_maze(grid: np.ndarray, size: int) -> np.ndarray:
    output_grid = np.empty([size * 3, size * 3], dtype=str)
    output_grid[:] = 0

    i = 0
    j = 0
    while i < size:
        w = i * 3 + 1
        while j < size:
            k = j * 3 + 1
            toss = grid[i, j]
            output_grid[w, k] = 1
            if toss == 0 and k + 2 < size * 3:
                output_grid[w, k + 1] = 1
                output_grid[w, k + 2] = 1
            if toss == 1 and w - 2 >= 0:
                output_grid[w - 1, k] = 1
                output_grid[w - 2, k] = 1

            j = j + 1

        i = i + 1
        j = 0

    return output_grid

def preprocess_grid(grid:np.ndarray, size:int) -> np.ndarray:
    # fix first row and last column to avoid digging outside the maze external borders
    first_row = grid[0]
    first_row[first_row == 1] = 0
    grid[0] = first_row
    for i in range(1,size):
        grid[i,size-1] = 1
    return grid


def genmaze(size, s):
    n=1
    p=0.5
    grid = np.random.binomial(n, p, size=(size,size))
    maze = carve_maze(preprocess_grid(grid,size), size)
    maze[s[1]][s[0]] = 'S'
    return maze











