#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

TAVERN = 0
AIR = -1
WALL = -2

PLAYER1 = 1
PLAYER2 = 2
PLAYER3 = 3
PLAYER4 = 4

AIM = {'North': (-1, 0),
       'East': (0, 1),
       'South': (1, 0),
       'West': (0, -1)}


class HeroTile:
    def __init__(self, id):
        self.id = id


class MineTile:
    def __init__(self, heroId=None):
        self.heroId = heroId


class Hero:
    """The Hero object"""

    def __init__(self, hero):
        try:
            # Training bots have no elo or userId
            self.elo = hero['elo']
            self.user_id = hero['userId']
            self.bot_last_move = hero['lastDir']
        except KeyError:
            self.elo = 0
            self.user_id = 0
            self.last_move = None

        self.bot_id = hero['id']
        self.life = hero['life']
        self.gold = hero['gold']
        self.pos = (hero['pos']['x'], hero['pos']['y'])
        self.spawn_pos = (hero['spawnPos']['x'], hero['spawnPos']['y'])
        self.crashed = hero['crashed']
        self.mine_count = hero['mineCount']
        self.mines = []
        self.name = hero['name'].encode("utf-8")


class Game:
    """The game object that gather
    all game state informations"""

    def __init__(self, state):
        self.state = state
        self.mines = {}
        self.board = Board(state['game']['board'])
        self.heroes = [Hero(state['game']['heroes'][i]) for i in range(len(state['game']['heroes']))]
        self.hero = Hero(state['hero'])
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
                elif obj == TAVERN:
                    self.taverns_locs.add((row, col))

        self.process_data(self.state)

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
            self.spawn_points_locs[(hero['spawnPos']['y'], hero['spawnPos']['x'])] = hero['id']


class Board:
    def __parseTile(self, str):
        if str == '  ':
            return AIR
        if str == '##':
            return WALL
        if str == '[]':
            return TAVERN
        match = re.match('\$([-0-9])', str)
        if match:
            return MineTile(match.group(1))
        match = re.match('\@([0-9])', str)
        if match:
            return HeroTile(match.group(1))

    def __parseTiles(self, tiles):
        vector = [tiles[i:i + 2] for i in range(0, len(tiles), 2)]
        matrix = [vector[i:i + self.size] for i in range(0, len(vector), self.size)]

        return [[self.__parseTile(x) for x in xs] for xs in matrix]

    def __init__(self, board):
        self.size = board['size']
        self.tiles = self.__parseTiles(board['tiles'])

    def passable(self, loc):
        """true if can walk through"""
        x, y = loc
        pos = self.tiles[x][y]
        return (pos != WALL) and (pos != TAVERN) and not isinstance(pos, MineTile)

    def to(self, loc, direction):
        """calculate a new location given the direction"""
        row, col = loc
        d_row, d_col = AIM[direction]
        n_row = row + d_row
        if n_row < 0:
            n_row = 0
        if n_row > self.size:
            n_row = self.size
        n_col = col + d_col
        if n_col < 0:
            n_col = 0
        if n_col > self.size:
            n_col = self.size

        return n_row, n_col
