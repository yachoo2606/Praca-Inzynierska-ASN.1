import os
import sys
import pygame
import numpy
from dotenv import load_dotenv

load_dotenv()
pygame.init()

screen = pygame.display.set_mode((int(os.getenv('WINDOW_WIDTH')), int(os.getenv('WINDOW_HEIGHT'))))

startPos = pygame.Vector2(float(os.getenv('WINDOW_WIDTH')) / 2, 0)
endPos = pygame.Vector2(float(os.getenv('WINDOW_WIDTH')) / 2, float(os.getenv('WINDOW_HEIGHT')))
pygame.draw.line(screen, (255, 0, 0), startPos, endPos)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.flip()
