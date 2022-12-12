import pygame
import numpy as np
from network import Network
from constants import BG_COLOR, LINE_COLOR, AVAILABLE_COLOR, UNAVAILABLE_COLOR, LINE_WIDTH, FONT, LETTERS,\
    NUMBERS, BOARD_ROWS, BOARD_COLS, BOX_SIZE, SHIP4SIDE, SHIP3SIDE, SHIP2SIDE, SHIP1SIDE, MISS_COLOR
from ship import Ship


class Board:
    def __init__(self):
        self.board = np.zeros((10, 10))
        self.enemy_board = np.zeros((10, 10))
        self.your_ships_left = 20
        self.enemy_ships_left = 20
        self.ship_to_draw = []
        self.n = Network()
        self.opponent_target = (11, 11)

    @staticmethod
    def draw_board(win):
        win.fill(BG_COLOR)
        for i in range(12):
            pygame.draw.line(win, LINE_COLOR, (50 + 50 * i, 50), (50 + 50 * i, 600), LINE_WIDTH)
            pygame.draw.line(win, LINE_COLOR, (700 + 50 * i, 50), (700 + 50 * i, 600), LINE_WIDTH)
            pygame.draw.line(win, LINE_COLOR, (50, 50 + 50 * i), (600, 50 + 50 * i), LINE_WIDTH)
            pygame.draw.line(win, LINE_COLOR, (700, 50 + 50 * i), (1250, 50 + 50 * i), LINE_WIDTH)

        pygame.draw.line(win, LINE_COLOR, (50, 50), (100, 100), LINE_WIDTH)
        pygame.draw.line(win, LINE_COLOR, (700, 50), (750, 100), LINE_WIDTH)

        for i in range(10):
            win.blit(FONT.render(LETTERS[i], False, LINE_COLOR), ((110 + 50 * i), 60))
            win.blit(FONT.render(LETTERS[i], False, LINE_COLOR), ((760 + 50 * i), 60))
            win.blit(FONT.render(NUMBERS[i], False, LINE_COLOR), (60, (110 + 50 * i)))
            win.blit(FONT.render(NUMBERS[i], False, LINE_COLOR), (710, (110 + 50 * i)))

    def show_possible(self, win):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.board[row][col] == 0:
                    pygame.draw.rect(win, AVAILABLE_COLOR,
                                     pygame.Rect(105 + 50 * row, 105 + 50 * col, BOX_SIZE, BOX_SIZE))
                elif self.board[row][col] == 2:
                    pygame.draw.rect(win, UNAVAILABLE_COLOR,
                                     pygame.Rect(105 + 50 * row, 105 + 50 * col, BOX_SIZE, BOX_SIZE))

    def show_hit(self, win):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.board[row][col] == 3:
                    win.blit(FONT.render(LETTERS[10], False, UNAVAILABLE_COLOR), ((110 + 50 * row), (110 + 50 * col)))
                elif self.board[row][col] == 4:
                    win.blit(FONT.render(LETTERS[11], False, MISS_COLOR), ((110 + 50 * row), (110 + 50 * col)))

    def draw_ships(self, win):
        for i in range(len(self.ship_to_draw)):
            self.ship_to_draw[i].draw(win)

    @staticmethod
    def ship_len(chosen_ship):
        if chosen_ship == SHIP1SIDE:
            return 1
        elif chosen_ship == SHIP2SIDE:
            return 2
        elif chosen_ship == SHIP3SIDE:
            return 3
        elif chosen_ship == SHIP4SIDE:
            return 4

    def check_collision(self, rotate, ship_len, row, col):
        for i in range(ship_len):
            if rotate is False:
                for sRow in range(ship_len):
                    if self.board[sRow + row][col] == 2 or self.board[sRow + row][col] == 1:
                        return False
            else:
                for sCol in range(ship_len):
                    if self.board[row][col + sCol] == 2 or self.board[row][col + sCol] == 1:
                        return False
        return True

    def set_on_board(self, row, col):
        for i in range(3):
            for j in range(3):
                if 0 <= (row - 1 + i) < 10 and 0 <= (col - 1 + j) < 10:
                    self.board[row - 1 + i][col - 1 + j] = 2

    def place_ship(self, mx, my, chosen_ship, rotate):
        ship_len = self.ship_len(chosen_ship)
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if (100 + 50 * row) < mx < (150 + 50 * row) and (100 + 50 * col) < my < (150 + 50 * col):
                    if rotate is False:
                        if (row + ship_len) <= 10 and self.check_collision(rotate, ship_len, row, col):
                            self.ship_to_draw.append(Ship(row, col, rotate, chosen_ship))
                            for sRow in range(ship_len):
                                self.set_on_board(row + sRow, col)
                            for sRow in range(ship_len):
                                self.board[row + sRow][col] = 1
                            return True
                        else:
                            return False
                    else:
                        if (col + ship_len) <= 10 and self.check_collision(rotate, ship_len, row, col):
                            self.ship_to_draw.append(Ship(row, col, rotate, chosen_ship))
                            for sCol in range(ship_len):
                                self.set_on_board(row, col + sCol)
                            for sCol in range(ship_len):
                                self.board[row][col + sCol] = 1
                            return True
                        else:
                            return False

    def shoot_the_enemy(self, mx, my):
        # print(self.board)
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if (750 + 50 * row) < mx < (800 + 50 * row) and (100 + 50 * col) < my < (150 + 50 * col):
                    if self.enemy_board[row][col] == 0:
                        self.enemy_board[row][col] = 1
                        self.n.send(make_pos((row, col)))
                        enemy_target = read_pos(self.n.send(make_pos((row, col))))
                        self.wait_for_opponent(enemy_target)

    def wait_for_opponent(self, enemy_target):
        print(enemy_target)
        if enemy_target is not None:
            if self.board[enemy_target[0]][enemy_target[1]] == 1:
                self.board[enemy_target[0]][enemy_target[1]] = 3
                self.your_ships_left -= 1
            else:
                self.board[enemy_target[0]][enemy_target[1]] = 4

    def end_game(self):
        pass


def read_pos(str):
    if str is not None:
        str = str.split(",")
        return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])
