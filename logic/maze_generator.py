import numpy as np
import pandas as pd
import random

class Maze():
    '''
    Class implementation of the Randomized Prim's Algorithmic method of maze generation.
    This class will generate a two-dimensional numpy array of a provided width and height using the rules outlined by Prim's Algorithm:

        1: Start with a grid of unvisited cells.
        2: Choose a cell at random and mark it as part of the maze (a path cell).
            2.1: Add the cells to the North, South, East, and West (neighbors) to the candidate wall list.
        3: While the wall list is not empty, do the following:
            3.1: Pick a random wall from the list.
                3.1.1: Check if only one of the cells that wall divides is visited.
                    3.1.1.1: If 3.1.1 is satisfied, make the wall and the unvisited cell a path.
                    3.1.1.2: Add the unvisited cell's neighbors to the wall list.
                3.1.2: Remove the randomly chosen wall from the wall list.

    In addition to generating the maze, there are a few methods to clean up the resulting array, so that it may be injected into another process, such as a game state.
    '''

    def __init__(self, width = 120, height = 80):
        # self.unvisited must be equal to 0, as the array is initially generated full of zeros.
        self.unvisited = 0
        # self.wall and self.path can be any integer but 0, and must be different
        self.wall = 1
        self.path = 4
        self.border = self.wall
        self.coords = np.zeros((height, width), dtype = int)
        self.wall_list = []
        self.width = width
        self.height = height

        self.generate_starting_point()
        self.generate_walls()
        self.fill_holes()
        self.remove_full_borders()
        self.generate_start_end()

    def generate_starting_point(self) -> None:
        '''
        Chooses a starting point for maze generation at random.
        '''

        # Make sure that the rows and columns adjacent to the borders are not candidates for the starting point.
        x = random.randint(1, self.width - 2)
        y = random.randint(1, self.height - 2)

        self.add_wall_neighbors(y, x)
        self.make_path(y, x)

    def generate_walls(self) -> None:
        '''
        Main loop for maze generation; see class documentation for algorithm rules.
        '''

        # Loop until there are no candidate walls left.
        while self.wall_list:
            # Convert the candidate wall list object to a list to pull random choice.
            cell = random.choice(self.wall_list)
            x, y = cell[1], cell[0]
            # If North and South neighbors are not 'unvisited' and 'path', check these rules against the East and West neighbors.
            if not self.n_s_neighbors(y, x): self.e_w_neighbors(y, x)
            # Remove the cell from the list of candidate wall cells.
            self.delete_node(y, x)

    def fill_holes(self) -> None:
        '''
        This method fills any holes which have been left unassigned by the algorithm.
        The amount of these cells depends on the maze attributes (width, height), the starting cell location, and the rules of the algorithm.
        There are usually fewer than six unassigned cells per maze generation, and all can be safely assigned as walls.
        '''

        self.coords = np.where(self.coords == 0, 1, self.coords)

    def remove_full_borders(self) -> None:
        '''
        If an odd number is used as the width and/or height of the maze, the algorithm may generate full walls on one or more sides.
        This results in any combination of one or two walls on any of the sides of the maze.
        The starting point may also affect this generation.
        
        This method removes additional walls if they are generated.
        '''

        # Check the bottom row.
        if self.path not in self.coords[self.coords.shape[0] - 2]:
            self.coords = np.delete(self.coords, self.coords.shape[0] - 2, 0)
        # Check the top row.
        if self.path not in self.coords[1]:
            self.coords = np.delete(self.coords, 1, 0)

        # Store second column of maze in x_min, second-to-last column in x_max
        x_min, x_max = self.coords[:, 1], self.coords[:, self.coords.shape[1] - 2]

        # Check the rightmost row.
        if self.path not in x_max:
            self.coords = np.delete(self.coords, self.coords.shape[1] - 2, 1)
        # Check the leftmost row.
        if self.path not in x_min:
            self.coords = np.delete(self.coords, 1, 1)

        # Update the new width and height of the maze, as it may have changed shape.
        self.height, self.width = self.coords.shape

    def generate_start_end(self) -> None:
        '''
        Sets the entrance (top-left) and exit (bottom-right) as paths.
        '''

        self.coords[0][1] = self.path
        self.coords[self.height - 1][self.width - 2] = self.path

    def n_s_neighbors(self, y, x) -> bool:
        '''
        Method for rule 3.1: Check if the wall candidate has a path to its North or South, and an unvisited cell opposite the path.
        If found: make the wall candidate and unvisited cell a path, add the unvisited cell's neighbors to the wall set, and remove the original wall candidate from the wall set.

        Returns:
            True or False depending on whether a match was found.
        '''

        # North and South cell coordinates.
        nx, ny = x, y - 1
        sx, sy = x, y + 1

        # If the neighboring cells are out of bounds, return False
        if ny < 1 or sy > self.height - 2: return False
        # Need to check both instances - whether North is a path and South is unvisited, or vice-versa.
        if self.coords[ny][nx] == self.unvisited and self.coords[sy][sx] == self.path:
            self.make_path(ny, nx)
            self.add_wall_neighbors(ny, nx)
            self.make_path(y, x)
            return True
        if self.coords[ny][nx] == self.path and self.coords[sy][sx] == self.unvisited:
            self.make_path(sy, sx)
            self.add_wall_neighbors(sy, sx)
            self.make_path(y, x)
            return True

        return False

    def e_w_neighbors(self, y, x) -> bool:
        '''
        Method for rule 3.1: Check if the wall candidate has a path to its East or West, and an unvisited cell opposite the path.
        If found: make the wall candidate and unvisited cell a path, add the unvisited cell's neighbors to the wall set, and remove the original wall candidate from the wall set.

        Returns:
            True or False depending on whether a match was found.
        '''

        # East and West cell coordinates.
        ex, ey = x - 1, y
        wx, wy = x + 1, y

        # If the neighboring cells are out of bounds, return False
        if ex < 1 or wx > self.width - 2: return False
        # Need to check both instances - whether East is a path and West is unvisited, or vice-versa.
        if self.coords[ey][ex] == self.unvisited and self.coords[wy][wx] == self.path:
            self.make_path(ey, ex)
            self.add_wall_neighbors(ey, ex)
            self.make_path(y, x)
            return True
        if self.coords[ey][ex] == self.path and self.coords[wy][wx] == self.unvisited:
            self.make_path(wy, wx)
            self.add_wall_neighbors(wy, wx)
            self.make_path(y, x)
            return True

        return False

    def add_wall_neighbors(self, y, x) -> None:
        '''
        This method checks the North, South, East, and West neighbors of the cell given the provided coordinates.
        If any of these are unvisited, they are made into walls.
        '''

        # Adjusted coordinates for North, South, East, and West neighbors.
        neighbors = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for neighbor in neighbors:
            ny = y + neighbor[0]
            nx = x + neighbor[1]
            # If the neighbor hasn't been visited, make it into a wall.
            if self.coords[ny][nx] == self.unvisited:
                self.make_wall(ny, nx)

    def make_wall(self, y, x) -> None:
        '''
        This method assigns a cell given the provided coordinates the corresponding value of a wall, then adds it to the list of candidate walls.
        '''

        self.coords[y][x] = self.wall
        self.wall_list.append((y, x))

    def make_path(self, y, x) -> None:
        '''
        This method assigns a cell given the provided coordinates the corresponding value of a path.
        '''

        self.coords[y][x] = self.path

    def delete_node(self, y, x) -> None:
        '''
        Removes a cell given the provided coordinates from the candidate wall set.
        '''

        self.wall_list.remove((y, x))

    def get_maze_shape(self) -> tuple:
        '''
        Returns the shape of the numpy array that houses the maze coordinates.
        '''

        # .shape returns the height first (interesting...)
        height, width = self.coords.shape
        return width, height

    def output(self) -> tuple:
        '''
        Returns the numpy array containing the maze coordinates.
        '''

        return self.coords

if __name__ == '__main__':

    maze = Maze()

    pd.DataFrame(maze.output()).to_csv('maze.csv', index = False, header = False, sep = ' ')