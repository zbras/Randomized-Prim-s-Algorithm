import pygame, time, os
from states.game_state import Game

class App():

    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Randomized Prim\'s Algorithm')
        pygame.mouse.set_visible(False)

        self.running, self.playing = True, True
        self.delta_time, self.prev_time = 0, 0
        self.actions = {
            'tab': False,
            'escape': False,
            'start': False,
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        self.state_stack = []

        self.load_assets()
        self.load_states()

    def game_loop(self):

        while self.playing:
            self.get_delta_time()
            self.get_events()

            if self.actions['escape']:
                self.exit_game()

            if self.actions['up']:
                self.state_stack[-1].process_key_up()

            if self.actions['down']:
                self.state_stack[-1].process_key_down()

            if self.actions['left']:
                self.state_stack[-1].process_key_right()

            if self.actions['right']:
                self.state_stack[-1].process_key_left()

            self.update()
            self.render()
            self.reset_keys()

    def get_events(self):

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.actions['down'] = True
                if event.key == pygame.K_UP:
                    self.actions['up'] = True
                if event.key == pygame.K_LEFT:
                    self.actions['right'] = True
                if event.key == pygame.K_RIGHT:
                    self.actions['left'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.actions['down'] = False
                if event.key == pygame.K_UP:
                    self.actions['up'] = False
                if event.key == pygame.K_LEFT:
                    self.actions['left'] = False
                if event.key == pygame.K_RIGHT:
                    self.actions['right'] = False

            if event.type == pygame.QUIT:
                self.exit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.actions['escape'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.actions['escape'] = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                self.state_stack[-1].process_mouse_down(position)

            elif event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                self.state_stack[-1].process_mouse_up(position)

    def update(self):

        self.state_stack[-1].update(self.delta_time, self.actions)

    def render(self):

        self.state_stack[-1].render(self.surface)
        pygame.display.flip()

    def get_delta_time(self):

        now = time.time()
        self.delta_time = now - self.prev_time
        self.prev_time = now

    def load_assets(self):

        pass

    def load_states(self):

        self.game_screen = Game(self)
        self.state_stack.append(self.game_screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def exit_game(self):

        self.running, self.playing = False, False

        quit()


if __name__ == '__main__':

    os.system('cls' if os.name == 'nt' else 'clear')
    app = App()

    while app.running:
        app.game_loop()