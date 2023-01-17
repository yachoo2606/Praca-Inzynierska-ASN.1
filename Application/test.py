import unittest
import pygame.display
from board import Board
from constants import *
from log_box import LogBox


class TestBoard(unittest.TestCase):
    board = None

    @classmethod
    def setUpClass(cls):
        # WIN, ADDRESS.get_value(), log_box
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        log_box = LogBox(WIN)

        cls.board = Board(WIN, "127.0.0.1", log_box)

    @classmethod
    def tearDownClass(cls):
        cls.shared_resource = None

    def test_check_full_destroy_oneElementShip(self):
        """
        Test that checking for sunk the one element ship
        """

        self.board.board[0][1] = 1
        self.board.board[0][0] = 2
        self.board.board[1][0] = 2
        self.board.board[1][1] = 2
        self.board.board[1][2] = 2
        self.board.board[0][3] = 2

        self.assertTrue(self.board.check_full_destroy(0, 1), "Should be True")

    def test_check_full_destroy_twoElementShip_noSunk_horizontal(self):
        """
        Test that checking for not sunk the two element ship
        """

        self.board.board[0][1] = 1
        self.board.board[0][2] = 1
        self.board.board[0][0] = 2
        self.board.board[1][0] = 2
        self.board.board[1][1] = 2
        self.board.board[1][2] = 2
        self.board.board[1][3] = 2
        self.board.board[0][3] = 2

        self.assertFalse(self.board.check_full_destroy(0, 1), "Should be False")

    def test_check_full_destroy_twoElementShip_sunk_horizontal(self):
        """
        Test that checking for not sunk the two element ship
        """

        self.board.board[0][1] = 1
        self.board.board[0][2] = 3
        self.board.board[0][0] = 2
        self.board.board[1][0] = 2
        self.board.board[1][1] = 2
        self.board.board[1][2] = 2
        self.board.board[1][3] = 2
        self.board.board[0][3] = 2

        self.assertTrue(self.board.check_full_destroy(0, 1), "Should be True")

    def test_check_full_destroy_twoElementShip_noSunk_vertical(self):
        """
        Test that checking for not sunk the two element ship
        """

        self.board.board[0][1] = 1
        self.board.board[1][1] = 1
        self.board.board[0][0] = 2
        self.board.board[1][0] = 2
        self.board.board[2][0] = 2
        self.board.board[2][1] = 2
        self.board.board[2][2] = 2
        self.board.board[1][2] = 2
        self.board.board[0][2] = 2

        self.assertFalse(self.board.check_full_destroy(0, 1), "Should be False")

    def test_check_full_destroy_twoElementShip_sunk_vertical(self):
        """
        Test that checking for not sunk the two element ship
        """

        self.board.board[0][1] = 1
        self.board.board[1][1] = 3
        self.board.board[0][0] = 2
        self.board.board[1][0] = 2
        self.board.board[2][0] = 2
        self.board.board[2][1] = 2
        self.board.board[2][2] = 2
        self.board.board[1][2] = 2
        self.board.board[0][2] = 2

        self.assertTrue(self.board.check_full_destroy(0, 1), "Should be True")


if __name__ == '__main__':
    unittest.main()
