import pygame
pygame.init()

WIDTH = 1300
HEIGHT = 800
LINE_WIDTH = 10
BOARD_ROWS = 10
BOARD_COLS = 10
BOX_SIZE = 40
# rgb
BG_COLOR = (64, 210, 255)
LINE_COLOR = (255, 255, 255)
AVAILABLE_COLOR = (0, 255, 0)
UNAVAILABLE_COLOR = (255, 0, 0)
MISS_COLOR = (0, 0, 0)
# letters
LETTERS = "ABCDEFGHIJXO"
NUMBERS = "0123456789"
FONT = pygame.font.SysFont('comicssans', 60)

# assets
SHIP1UP = pygame.transform.scale(pygame.image.load("ships/ship1.png"), (40, 40))
SHIP1SIDE = pygame.transform.rotate(SHIP1UP, -90)
SHIP2UP = pygame.transform.scale(pygame.image.load("ships/ship2.png"), (40, 90))
SHIP2SIDE = pygame.transform.rotate(SHIP2UP, -90)
SHIP3UP = pygame.transform.scale(pygame.image.load("ships/ship3.png"), (40, 140))
SHIP3SIDE = pygame.transform.rotate(SHIP3UP, -90)
SHIP4UP = pygame.transform.scale(pygame.image.load("ships/ship4.png"), (40, 190))
SHIP4SIDE = pygame.transform.rotate(SHIP4UP, -90)
