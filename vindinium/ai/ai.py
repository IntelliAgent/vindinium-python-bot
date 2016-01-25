#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import pathfinding


class AI:
    """Pure random A.I, you may NOT use it to win ;-)"""

    def __init__(self):
        pass

    def process(self, game):
        """Do whatever you need with the Game object game"""
        self.game = game
        self.pathfinding = pathfinding.PathFinding(game)

    def decide(self):
        """Must return a tuple containing in that order:
          1 - path_to_goal :
                  A list of coordinates representing the path to your
                 bot's goal for this turn:
                 - i.e: [(y, x) , (y, x), (y, x)]
                 where y is the vertical position from top and x the
                 horizontal position from left.
          2 - action:
                 A string that will be displayed in the 'Action' place.
                 - i.e: "Go to mine"
          3 - decision:
                 A list of tuples containing what would be useful to understand
                 the choice you're bot has made and that will be printed
                 at the 'Decision' place.
          4- hero_move:
                 A string in one of the following: West, East, North,
                 South, Stay
          5 - nearest_enemy_pos:
                 A tuple containing the nearest enemy position (see above)
          6 - nearest_mine_pos:
                 A tuple containing the nearest mine position (see above)
          7 - nearest_tavern_pos:
                 A tuple containing the nearest tavern position (see above)"""

        actions = ['mine', 'tavern', 'fight']

        decisions = {'mine': [("Mine", 30), ('Fight', 10), ('Tavern', 5)],
                     'tavern': [("Mine", 10), ('Fight', 10), ('Tavern', 50)],
                     'fight': [("Mine", 15), ('Fight', 30), ('Tavern', 10)]}

        champion_path = []
        action = random.choice(actions)
        decision = decisions[action]
        nearest_mine_pos = None
        nearest_hero = None

        f_neighbors = self.game.board.neighbors
        f_distance = self.pathfinding.manhattan_distance
        heroes = self.game.heroes
        mines_loc = self.game.mines_locs.keys()
        taverns_loc = self.game.taverns_locs
        hero_pos = self.game.hero.pos

        distance = 9999

        for hero in heroes:
            if hero.bot_id != self.game.hero.bot_id:
                current_distance = f_distance(hero_pos, hero.pos)
                if current_distance < distance:
                    distance = current_distance
                    nearest_enemy_pos = hero.pos
                    nearest_hero = hero

        distance = 9999
        for mine_pos in mines_loc:
            if self.game.mines_locs[mine_pos] == '-' or self.game.mines_locs[mine_pos] != str(self.game.hero.bot_id):
                current_distance = f_distance(hero_pos, mine_pos)
                if current_distance < distance:
                    distance = current_distance
                    nearest_mine_pos = mine_pos

        distance = 9999
        for taverns_pos in taverns_loc:
            current_distance = f_distance(hero_pos, taverns_pos)
            if current_distance < distance:
                distance = current_distance
                nearest_tavern_pos = taverns_pos

        if self.game.hero.life <= 40 and self.game.hero.mine_count > 2:
            distance = 9999
            for x in f_neighbors(nearest_tavern_pos):
                path = self.pathfinding.find_path(hero_pos, x)
                current_distance = path[1]
                if current_distance < distance:
                    distance = current_distance
                    champion_path = path[0]
                    champion_path.append(nearest_tavern_pos)
                    action = actions[1]

        elif 75 >= self.game.hero.life >= 51 and nearest_hero.life < 50 and nearest_hero.mine_count > 0:
            distance = 9999
            for x in f_neighbors(nearest_enemy_pos):
                path = self.pathfinding.find_path(hero_pos, x)
                current_distance = path[1]
                if current_distance < distance:
                    distance = current_distance
                    champion_path = path[0]
                    champion_path.append(nearest_enemy_pos)
                    action = actions[2]

        elif self.game.hero.life >= 30:
            distance = 9999
            for x in f_neighbors(nearest_mine_pos):
                path = self.pathfinding.find_path(hero_pos, x)
                current_distance = path[1]
                if current_distance < distance:
                    distance = current_distance
                    champion_path = path[0]
                    champion_path.append(nearest_mine_pos)
                    action = actions[0]

        if len(champion_path) > 1:
            champion_path.pop(0)

        print champion_path

        return (champion_path,
                action,
                decision,
                self.game.board.direction(hero_pos, champion_path[0]),
                nearest_enemy_pos,
                nearest_mine_pos,
                nearest_tavern_pos)


if __name__ == "__main__":
    pass
