__all__ = ['Hero']


class Hero(object):
    """The Hero object"""

    def __init__(self, hero):
        self.user_id = hero.get('userId')
        self.elo = hero.get('elo')
        self.bot_id = hero['id']
        self.life = hero['life']
        self.last_dir = hero.get('lastDir')
        self.gold = hero['gold']
        self.pos = (hero['pos']['x'], hero['pos']['y'])
        self.spawn_pos = (hero['spawnPos']['x'], hero['spawnPos']['y'])
        self.crashed = hero['crashed']
        self.mine_count = hero['mineCount']
        self.mines = []
        self.name = hero['name'].encode("utf-8")
