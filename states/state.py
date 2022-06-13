class State():

    def __init__(self, game):

        self.game = game
        self.prev_state = None

    def update(self, delta_time, actions):

        pass

    def render(self, surface):

        pass

    def process_mouse_down(self, position):

        pass

    def process_mouse_up(self, position):

        pass

    def process_key_up(self):

        pass

    def process_key_down(self):

        pass

    def process_key_left(self):

        pass

    def process_key_right(self):

        pass

    def enter_state(self):

        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]

        self.game.state_stack.append(self)

    def exit_state(self):

        self.game.state_stack.pop()

if __name__ == '__main__':
    quit()