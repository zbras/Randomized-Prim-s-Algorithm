import pygame

class Player:
    def __init__(self, app, game):
        self.game = game
        self.color = (255,0,0)
        self.curr_loc = tuple()
        self.prev_loc = tuple()
        self.app = app
        self.visited = set()
        self.tail = (255,150,150)
        self.path = (200,200,200)

        self.set_starting_location()

    def set_starting_location(self):
        self.curr_loc = (0, 1)
        self.prev_loc = (0, 1)

    def draw_player(self):
        self.draw_visited()
        currenct_rect = pygame.draw.rect(
            self.app.screen,
            self.color,
            pygame.Rect(self.curr_loc[1] * (self.game.block_dim), self.curr_loc[0] * (self.game.block_dim), (self.game.block_dim), (self.game.block_dim))
        )
        pygame.display.update(currenct_rect)

    def draw_visited(self):
        for (y, x) in self.visited:
            tail = pygame.draw.rect(
                self.app.screen,
                self.tail,
                pygame.Rect(x * (self.game.block_dim), y * (self.game.block_dim), (self.game.block_dim), (self.game.block_dim))
            )
            pygame.display.update(tail)

    def move_up(self):
        y, x = self.curr_loc
        self.move(y - 1, x)

    def move_down(self):
        y, x = self.curr_loc
        self.move(y + 1, x)

    def move_left(self):
        y, x = self.curr_loc
        self.move(y, x - 1)

    def move_right(self):
        y, x = self.curr_loc
        self.move(y, x + 1)

    def move(self, y, x):
        if self.game.maze.coords[y][x] != self.game.maze.path: return
        self.visited.add(self.curr_loc)
        self.curr_loc = (y, x)
        if self.curr_loc in self.visited:
            self.visited.remove(self.curr_loc)
        if self.curr_loc == (self.game.maze.height - 1, self.game.maze.width - 2):
            self.game.process_mouse_down()

if __name__ == '__main__':
    quit()
