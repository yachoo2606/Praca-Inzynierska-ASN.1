import pygame
from constants import SHIP1SIDE, SHIP2SIDE, SHIP3SIDE, SHIP4SIDE, SHIP1UP, SHIP2UP, SHIP3UP, SHIP4UP


class Ship:
    def __init__(self, start_row, start_col, rotate, chosen_ship):
        self.start_row = start_row
        self.start_col = start_col
        self.rotate = rotate
        self.ship_image = chosen_ship

    def draw(self, win):
        if self.rotate is False:
            win.blit(self.ship_image, (105 + 50 * self.start_row, 105 + 50 * self.start_col))
        else:
            win.blit(pygame.transform.rotate(self.ship_image, -90), (105 + 50 * self.start_row, 105 + 50 * self.start_col))

    def __repr__(self):
        return str(self.ship_image)
