#!/usr/bin/env python3

"""
Application to keep score during Ewan's Game. A card game with
bids, a running total and a trump that cycles.

"""
import sys


class Player:
    """
    Represents a named player along with their score.

    """
    def __init__(self, name):
        self._name = name
        self._score = 0

    def __repr__(self):
        return f'<{self.__class__.__name__}({self.name})>'

    @property
    def name(self):
        return self._name

    @property
    def score(self):
        return self._score


def create_player(prompt_name):
    name = ''
    while not name:
        name = input(f'Enter name of {prompt_name}: ')
    return Player(name)


class Trumps:
    """
    Callable that returns the trumps for the next hand.

    """
    def __init__(self):
        self.trumps = ('Hearts', 'Clubs', 'Diamonds', 'Spades',
                       'Hearts', 'Clubs', 'None', 'Diamonds',
                       'Spades', 'Hearts', 'Clubs', 'Diamonds', 'Spades')
        self.generator = (t for t in self.trumps)

    def __call__(self):
        return next(self.generator)


class NCards:
    def __init__(self):
        self.generator = (i for i in range(12))

    def __call__(self):
        return next(self.generator)


class Game:
    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self.n_cards = NCards()
        self.trumps = Trumps()

    def play_hand(self):
        n = self.n_cards()
        print('Deal {} cards'.format(n))
        print('Trumps: {}'.format(self.trumps()))
        bid_one = int(input(f"{self.player_one.name}'s bid:"))
        while True:
            bid_two = int(input(f"{self.player_two.name}'s bid:"))
            if bid_one + bid_two != n:
                break
            else:
                print('Sum of bids cannot equal the number of cards.')
        print('---')

    def play(self):
        while True:
            try:
                self.play_hand()
            except StopIteration:
                break

        print('Final scores:\n============')
        print(f'{self.player_one.name}: {self.player_one.score}')
        print(f'{self.player_two.name}: {self.player_two.score}')
        print(f'The winner is {self.leading_player()}')

    def leading_player(self):
        if self.player_one.score > self.player_two.score:
            res = self.player_one.name
        elif self.player_one.score < self.player_two.score:
            res = self.player_two.name
        else:
            res = 'Draw!!'
        return res


def main():
    try:
        player_one = create_player('player 1')
        player_two = create_player('player 2')
    except KeyboardInterrupt:
        print('Exiting...')
        sys.exit(0)

    game = Game(player_one, player_two)
    game.play()


if __name__ == '__main__':
    main()
