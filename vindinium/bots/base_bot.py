from vindinium.bots import RawBot
from vindinium.models import Game


class BaseBot(RawBot):
    id = None
    state = None
    game = None
    hero = None

    def _start(self, state):
        '''Wrapper to start method.'''
        self.id = state['hero']['id']
        self.state = state
        self.game = Game(state)
        self.hero = self.game.heroes[self.id - 1]
        self.start()

    def _move(self, state):
        '''Wrapper to move method.'''
        self.state = state
        self.game.update(state)
        return self.move()

    def _end(self):
        '''Wrapper to end method.'''
        self.end()
