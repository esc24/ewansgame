#!/usr/bin/env python3

"""
Application to keep score during Ewan's Game. A card game with
bids, a running total and a trump that cycles.

"""
import sys


class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[37m'
    BOLD = '\033[1m'
    BLINK = '\033[5m'
    UNDERLINE = '\033[4m'


class Player:
    """
    Represents a named player along with their score.

    """
    def __init__(self, name):
        self._name = name
        self.score = 0

    def __repr__(self):
        return f'<{self.__class__.__name__}({self.name})>'

    @property
    def name(self):
        return self._name


def create_player(prompt_name):
    name = ''
    while not name:
        name = get_input(f'Enter name of {prompt_name}: ')
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
        self.generator = (i for i in (1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1))
        #self.generator = (i for i in (1, 2))

    def __call__(self):
        return next(self.generator)


def get_input(prompt):
    """Modified raw input that requires a non-empty response."""
    res = None
    while not res:
        res = input(prompt)
    return res


class Game:
    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self.n_cards = NCards()
        self.trumps = Trumps()

    def play_hand(self):
        n = self.n_cards()
        print(colors.GREEN + '\nDeal {} card{}'.format(n, 's' if n != 1 else '') + colors.ENDC)
        print(colors.RED + 'Trumps: {}'.format(self.trumps()) + colors.ENDC)
        bid_one = int(get_input(f"{self.player_one.name}'s bid: "))
        while True:
            bid_two = int(get_input(f"{self.player_two.name}'s bid: "))
            if bid_one + bid_two != n:
                break
            else:
                print('Sum of bids cannot equal the number of cards.')
        print('---')
        tricks_one = tricks_two = 0
        while tricks_one + tricks_two != n:
            tricks_one = int(get_input(f'How many tricks did {self.player_one.name} win?: '))
            tricks_two = int(get_input(f'How many tricks did {self.player_two.name} win?: '))
            if tricks_one + tricks_two != n:
                print(f'Error. Total number of tricks must be {n}. Please reenter results...')
        self.score(self.player_one, bid_one, tricks_one)
        self.score(self.player_two, bid_two, tricks_two)
        print('===')
        print(f'{colors.BLUE}Score: {self.player_one.name}: {self.player_one.score}, '
              f'{self.player_two.name}: {self.player_two.score}{colors.ENDC}')
        print('===')

    def play(self):
        while True:
            try:
                self.play_hand()
            except StopIteration:
                break

        print('\nFinal scores:\n============')
        print(f'{self.player_one.name}: {self.player_one.score}')
        print(f'{self.player_two.name}: {self.player_two.score}')
        print('')
        winner = self.leading_player()
        if winner:
            print(f'{colors.BLUE}{colors.BOLD}The winner is {winner}{colors.ENDC}\n')
        else:
            print(f"{colors.BLUE}{colors.BOLD}It's a draw!!!{colors.ENDC}\n")
            
    @staticmethod
    def score(player, bid, tricks):
        if bid == tricks:
            player.score += 10 + bid

    def leading_player(self):
        if self.player_one.score > self.player_two.score:
            res = self.player_one.name
        elif self.player_one.score < self.player_two.score:
            res = self.player_two.name
        else:
            res = None
        return res


def main():
    print(colors.BLUE)
    print("""
***********************************************
*                                             *
* Ewan's Game                                 *
*                                             *
***********************************************""")
    print(colors.ENDC)
    try:
        player_one = create_player('player 1')
        player_two = create_player('player 2')
        while player_one.name == player_two.name:
            print('Error. Players cannot have the same name. Try a different one...')
            player_two = create_player('player 2')
            
    except KeyboardInterrupt:
        print('Exiting...')
        sys.exit(0)

    game = Game(player_one, player_two)
    try:
    	game.play()
    except KeyboardInterrupt:
        print('Exiting...')
        sys.exit(0)
    

if __name__ == '__main__':
    main()
