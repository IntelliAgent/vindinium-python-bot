import logging
import sys
import webbrowser

import requests

__all__ = ['Client']


class Client(object):
    def __init__(self, key,
                 mode='training',
                 n_turns=300,
                 server='http://vindinium.org',
                 open_browser=False):
        self.key = key
        self.mode = mode
        self.n_turns = n_turns
        self.server = server
        self.open_browser = open_browser
        self.timeout_move = 15
        self.timeout_connection = 10 * 60

        self.__session = None

    def run(self, bot):
        try:
            # Connect
            state = self.__connect()
            bot._start(state)
            play_url = state['playUrl']

            # Move
            finished = False
            while not finished:
                action = bot._move(state)
                sys.stdout.write("Going to {}.\n".format(action))
                sys.stdout.flush()
                state = self.__move(play_url, action)
                finished = state['game']['finished']

            return state['viewUrl']

        finally:
            # End
            bot._end()
            self.__disconnect()

    def __connect(self):
        # Create requests session
        self.__session = requests.session()

        # Set up parameters
        server = self.server
        if self.mode == 'arena':
            params = {'key': self.key}
            endpoint = '/api/arena'
        else:
            params = {'key': self.key, 'turns': self.n_turns, 'map': 'm2'}
            endpoint = '/api/training'

        # Connect
        logging.info('Trying to connect to %s%s', server, endpoint)
        r = self.__session.post(server + endpoint, params, timeout=10 * 60)

        # Get response
        if r.status_code == 200:
            state = r.json()
            logging.info('Connected! Playing game at: %s', state['viewUrl'])

            # Open browser if ``open_browser`` is True
            if self.open_browser:
                webbrowser.open(state['viewUrl'])

            return state
        else:
            logging.error('Error when connecting to server, message: "%s"', r.text)
            raise IOError('Connection error, check log for the message.')

    def __move(self, url, action):
        r = self.__session.post(url, {'dir': action}, timeout=self.timeout_move)

        if r.status_code == 200:
            return r.json()

        else:
            logging.error('Connection error during game, message: "(%d) %s"', r.status_code, r.text)
            raise IOError('Connection error, check log for the message.')

    def __disconnect(self):
        '''Close the session.'''
        if (self.__session):
            self.__session.close()
