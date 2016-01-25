#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vindinium.ai import ai
from vindinium.bots import BaseBot
from vindinium.models.game import Game

DIRS = ["North", "East", "South", "West", "Stay"]
ACTIONS = ["Go mine", "Go beer", "Go enemy"]


class RusselBot(BaseBot):
    def __init__(self):
        self.running = True
        self.state = {}
        self.game = None
        self.last_mine_count = 0
        self.last_gold = 0
        self.last_life = 0
        self.hero_move = None
        self.hero_last_move = None
        self.action = None
        self.last_action = None
        self.path_to_goal = []
        self.decision = []
        self.nearest_enemy_pos = None
        self.nearest_mine_pos = None
        self.nearest_tavern_pos = None
        self.last_nearest_enemy_pos = None
        self.last_nearest_mine_pos = None
        self.last_nearest_tavern_pos = None
        self.last_pos = None
        self.ai = ai.AI()

    def move(self):
        """Return store data provided by A.I and return selected move"""
        # Store status for later report
        try:
            self.hero_last_move = self.hero_move
            self.last_life = self.game.hero.life
            self.last_action = self.action
            self.last_gold = self.game.hero.gold
            self.last_mine_count = self.game.hero.mine_count
            self.last_pos = self.game.hero.pos
            self.last_nearest_enemy_pos = self.nearest_enemy_pos
            self.last_nearest_mine_pos = self.nearest_mine_pos
            self.last_nearest_tavern_pos = self.nearest_tavern_pos
        except AttributeError:
            # First move has no previous move
            pass
        self.game = Game(self.state)

        ################################################################
        # Put your call to AI code here
        ################################################################

        self.ai.process(self.game)
        self.path_to_goal, \
        self.action, \
        self.decision, \
        self.hero_move, \
        self.nearest_enemy_pos, \
        self.nearest_mine_pos, \
        self.nearest_tavern_pos = self.ai.decide()

        ################################################################
        # /AI
        ################################################################

        return self.hero_move
