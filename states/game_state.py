import pygame
from states.state import State
from logic.maze import Maze
from logic.player import Player

class Game(State):

    def __init__(self, app):

        State.__init__(self, app)
        self.app = app

        self.maze_width = 100
        self.maze_height = 70
        self.block_dim = 10
        self.wall_color = (100,100,100)
        self.path_color = (200,200,200)

        self.maze = Maze(self.maze_width, self.maze_height)

        self.screen_width = self.maze.width * self.block_dim
        self.screen_height = self.maze.height * self.block_dim
        self.app.surface = pygame.Surface((self.screen_width, self.screen_height))
        #self.app.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.app.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.NOFRAME)
        self.player = Player(self.app, self)
        self.pause_render = False

    def update(self, delta_time, actions) -> None:

        self.render(self.app.screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def render(self, surface):

        if not self.pause_render:
            surface.fill(self.path_color)
            maze = self.maze.output()
            width, height = self.maze.get_maze_shape()
            row = 0
            col = 0

            for x in range(0, width):
                for y in range(0, height):
                    if maze[y][x] == self.maze.wall: color = self.wall_color
                    if maze[y][x] == self.maze.path: color = self.path_color
                    pygame.draw.rect(
                        surface,
                        color,
                        pygame.Rect(row * (self.block_dim), col * (self.block_dim), (self.block_dim), (self.block_dim))
                    )
                    col += 1
                col = 0
                row += 1
            self.pause_render = not self.pause_render

        self.player.draw_player()

    def process_mouse_down(self, position = None):

        self.maze = Maze(self.maze_width, self.maze_height)
        self.player = Player(self.app, self)
        self.render(self.app.surface)
        self.pause_render = not self.pause_render

    def process_key_up(self):
        self.player.move_up()

    def process_key_down(self):
        self.player.move_down()

    def process_key_left(self):
        self.player.move_left()

    def process_key_right(self):
        self.player.move_right()

if __name__ == '__main__':
    quit()
