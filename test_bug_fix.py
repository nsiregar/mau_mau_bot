import unittest

from game import Game
from player import Player
import card as c


class Test(unittest.TestCase):

    game = None

    def setUp(self):
        self.game = Game(None)

    def test_sim_bluff_refa(self):
        refa = Player(self.game, "Refa")
        can = Player(self.game, "Can")

        self.game.last_card = c.Card(c.YELLOW, '4')

        refa.cards = [c.Card(c.GREEN, '7')]

        can.cards = [c.Card(c.GREEN, '4')]

        refa.playable_cards()
        refa.cards.append(c.Card(None, None, c.DRAW_FOUR))
        refa.playable_cards()
        refa.play(c.Card(None, None, c.DRAW_FOUR))
        self.game.choose_color(c.GREEN)
        self.assertFalse(refa.bluffing)
        self.assertFalse(self.game.current_player.prev.bluffing)

if __name__ == '__main__':
    unittest.main()