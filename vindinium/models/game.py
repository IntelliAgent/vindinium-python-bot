__all__ = ['Game']
import vindinium as vin
from vindinium.models import Hero, Board, Tavern, MineTile, HeroTile


class Game(object):
    """The game object that gather
    all game state informations"""

    def __init__(self, state):
        self.state = state
        self.mines = {}
        self.board = Board(state['game']['board'])
        self.heroes = [Hero(state['game']['heroes'][i]) for i in range(len(state['game']['heroes']))]
        self.hero = Hero(state['hero'])
        self.taverns = []
        self.mines_locs = {}
        self.spawn_points_locs = {}
        self.taverns_locs = set([])
        self.heroes_locs = {}
        self.walls_locs = []
        self.url = None
        self.turn = None
        self.max_turns = None
        self.finished = None
        self.board_size = state['game']['board']['size']
        self.turn = state['game']['turn']
        self.max_turns = state['game']['maxTurns']
        self.finished = state['game']['finished']
        for row in range(len(self.board.tiles)):
            for col in range(len(self.board.tiles[row])):
                obj = self.board.tiles[row][col]
                if isinstance(obj, MineTile):
                    self.mines_locs[(row, col)] = obj.heroId
                elif isinstance(obj, HeroTile):
                    self.heroes_locs[(row, col)] = obj.id
                elif obj == vin.TAVERN:
                    self.taverns_locs.add((row, col))
                    self.taverns.append(Tavern(row, col))

        self.process_data(self.state)

    def update(self, state):
        size = state['game']['board']['size']
        tiles = state['game']['board']['tiles']
        heroes = state['game']['heroes']

        self.turn = state['game']['turn']

        for hero, hero_state in zip(self.heroes, heroes):
            hero.crashed = hero_state['crashed']
            hero.mine_count = hero_state['mineCount']
            hero.gold = hero_state['gold']
            hero.life = hero_state['life']
            hero.last_dir = hero_state.get('lastDir')
            hero.x = hero_state['pos']['y']
            hero.y = hero_state['pos']['x']

        for mine in self.mines:
            char = tiles[mine.x * 2 + mine.y * 2 * size + 1]
            mine.owner = None if char == '-' else int(char)

    def process_data(self, state):
        """Parse the game state"""
        self.set_url(state['viewUrl'])
        self.process_game(state['game'])

    def set_url(self, url):
        """Set the game object url var"""
        self.url = url

    def process_game(self, game):
        """Process the game data"""
        process = {'heroes': self.process_heroes}

        for key in game:
            if key in process:
                process[key](game[key])

    def process_heroes(self, heroes):
        """Add heroes"""
        for hero in heroes:
            self.spawn_points_locs[(hero['spawnPos']['x'], hero['spawnPos']['y'])] = hero['id']

    def has_enemy_pos(self, pos):
        enemy_heroes = filter(lambda x: x != self.hero.bot_id, self.heroes)
        for hero in enemy_heroes:
            if hero.pos == pos:
                return True
        return False

    def life_hero_at_pos(self, pos):
        enemy_heroes = filter(lambda x: x != self.hero.bot_id, self.heroes)
        for hero in enemy_heroes:
            if hero.pos == pos:
                return hero.life
        return 0

    def cost(self, current, goal):
        if self.has_enemy_pos(goal):
            return 1 + self.life_hero_at_pos(goal)
        for x in self.board.neighbors(goal):
            if self.has_enemy_pos(x):
                return 1 + self.life_hero_at_pos(goal) // 2
        else:
            return 1

    def get_hero_by_pos(self, pos):
        return filter(lambda x: x.hero.pos == pos, self.heroes)


