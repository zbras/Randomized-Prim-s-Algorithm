import numpy as np
import pandas as pd
import random

class Maze():

    def __init__(self, width = 120, height = 80):
        self.border = 1
        self.zero = 0
        self.path = 4
        self.wall = 1
        self.coords = np.zeros((height, width), dtype = int)
        self.wall_set = set()
        self.visited = set()
        self.legal_spaces = set()
        self.width = width
        self.height = height

        self.generate_borders()
        self.generate_starting_point()
        self.generate_walls()
        self.fill_holes()
        self.remove_full_borders()
        self.generate_start_end()

    def generate_borders(self):
        for y in range(self.height):
            self.coords[y][0] = self.border
            self.coords[y][self.width - 1] = self.border
        for x in range(self.width):
            self.coords[0][x] = self.border
            self.coords[self.height - 1][x] = self.border

    def generate_starting_point(self):
        x = random.randint(1, self.width - 2)
        y = random.randint(1, self.height - 2)
        self.add_wall_neighbors(y, x)
        self.make_path(y, x)

    def generate_walls(self):
        while self.wall_set:
            # Convert to list to pull random choice
            cell = random.choice(list(self.wall_set))
            x, y = cell[1], cell[0]
            # Check that cell isn't a wall already
            if self.coords[y][x] != self.wall: continue
            # Check that cell isn't on border
            if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1: continue
            if not self.n_s_neighbors(y, x): self.e_w_neighbors(y, x)
            self.delete_node(y, x)

    def fill_holes(self):
        self.coords = np.where(self.coords == 0, 1, self.coords)

    def remove_full_borders(self):
        if self.path not in self.coords[self.coords.shape[0] - 2]:
            self.coords = np.delete(self.coords, self.coords.shape[0] - 2, 0)
        if self.path not in self.coords[1]:
            self.coords = np.delete(self.coords, 1, 0)
        x_min, x_max = self.coords[:, 1], self.coords[:, self.coords.shape[1] - 2]
        if self.path not in x_max:
            self.coords = np.delete(self.coords, self.coords.shape[1] - 2, 1)
        if self.path not in x_min:
            self.coords = np.delete(self.coords, 1, 1)
        self.height, self.width = self.coords.shape

    def generate_start_end(self):
        while True:
            x_min, x_max = 1, self.width - 2
            if self.coords[1][x_min] == self.path: break
            if self.coords[self.height - 2][x_max] == self.path: break
            x_min += 1
            x_max -= 1
        self.coords[0][1] = self.path
        self.coords[self.height - 1][x_max] = self.path

    def n_s_neighbors(self, y, x):
        nx, ny = x, y - 1
        sx, sy = x, y + 1
        if self.coords[ny][nx] == self.zero and self.coords[sy][sx] == self.path:
            self.make_path(ny, nx)
            self.add_wall_neighbors(ny, nx)
            self.make_path(y, x)
            return True
        if self.coords[ny][nx] == self.path and self.coords[sy][sx] == self.zero:
            self.make_path(sy, sx)
            self.add_wall_neighbors(sy, sx)
            self.make_path(y, x)
            return True
        return False

    def e_w_neighbors(self, y, x):
        ex, ey = x - 1, y
        wx, wy = x + 1, y
        if self.coords[ey][ex] == self.zero and self.coords[wy][wx] == self.path:
            self.make_path(ey, ex)
            self.add_wall_neighbors(ey, ex)
            self.make_path(y, x)
            return True
        if self.coords[ey][ex] == self.path and self.coords[wy][wx] == self.zero:
            self.make_path(wy, wx)
            self.add_wall_neighbors(wy, wx)
            self.make_path(y, x)
            return True
        return False

    def add_wall_neighbors(self, y, x):
        neighbors = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for neighbor in neighbors:
            ny = y + neighbor[0]
            nx = x + neighbor[1]
            if self.coords[ny][nx] == self.zero:
                self.make_wall(ny, nx)

    def make_wall(self, y, x):
        self.coords[y][x] = self.wall
        self.add_node(y, x)

    def make_path(self, y, x):
        self.coords[y][x] = self.path

    def delete_node(self, y, x):
        self.wall_set.remove((y, x))

    def add_node(self, y, x):
        self.wall_set.add((y, x))

    def get_maze_shape(self) -> tuple:
        height, width = self.coords.shape
        return width, height

    def output(self):
        return self.coords

if __name__ == '__main__':

    maze = Maze()

    pd.DataFrame(maze.output()).to_csv('text.csv', index = False, header = False, sep = ' ')