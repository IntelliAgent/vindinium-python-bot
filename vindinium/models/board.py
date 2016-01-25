import re

import vindinium as vin
from vindinium.models import HeroTile, MineTile

__all__ = ['Board']


class Board(object):
    def __parseTile(self, str):
        if str == '  ':
            return vin.AIR
        if str == '##':
            return vin.WALL
        if str == '[]':
            return vin.TAVERN
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
        return (pos != vin.WALL) and (pos != vin.TAVERN) and not isinstance(pos, MineTile)

    def to(self, loc, direction):
        """calculate a new location given the direction"""
        row, col = loc
        d_row, d_col = vin.AIM[direction]
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

    def direction(self, loc, goal):
        if goal[0] - loc[0] == -1:
            return 'North'
        elif goal[0] - loc[0] == 1:
            return 'South'
        elif goal[1] - loc[1] == -1:
            return 'West'
        elif goal[1] - loc[1] == 1:
            return 'East'
        else:
            return 'Stay'

    def in_bounds(self, pos):
        (x, y) = pos
        return 0 <= x < self.size and 0 <= y < self.size

    def neighbors(self, pos):
        (x, y) = pos
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def __str__(self):
        s = ' '
        s += '-' * (self.size) + '\n'
        for y in xrange(self.size):
            s += '|'
            for x in xrange(self.size):
                s += str(self[x, y] or ' ')
            s += '|\n'
        s += ' ' + '-' * (self.size)
        return s
