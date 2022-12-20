import pygame
import pygame_menu
from constants import WIDTH, HEIGHT, FONT, LINE_COLOR, SHIP4SIDE, SHIP3SIDE, SHIP2SIDE, SHIP1SIDE
from board import Board
from pygame import mixer
from _thread import *

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 120

pygame.display.set_caption("Battleship")
num_ships = [4, 3, 2, 1]

mixer.init()
backSound = mixer.Sound("music/pirate-music-14288.mp3")
backSound.play(loops=-1)
pressSound = mixer.Sound("music/pressSound2.ogg")

mode = ('Solo', 0)


def draw_setup(win):
    win.blit(FONT.render("Ustaw swoje statki", False, LINE_COLOR), (110, 610))
    win.blit(FONT.render("{} x".format(num_ships[3]), False, LINE_COLOR), (70, 650))
    win.blit(FONT.render("{} x".format(num_ships[2]), False, LINE_COLOR), (70, 700))
    win.blit(FONT.render("{} x".format(num_ships[1]), False, LINE_COLOR), (370, 650))
    win.blit(FONT.render("{} x".format(num_ships[0]), False, LINE_COLOR), (370, 700))
    win.blit(SHIP4SIDE, (130, 650))
    win.blit(SHIP3SIDE, (130, 700))
    win.blit(SHIP2SIDE, (430, 650))
    win.blit(SHIP1SIDE, (430, 700))


def set_ships(mx, my, chosen_ship, board, rotate):
    if 130 < mx < 320 and 650 < my < 690:
        if num_ships[3] != 0 and chosen_ship is None:
            num_ships[3] = num_ships[3] - 1
            return SHIP4SIDE
        else:
            return chosen_ship
    elif 130 < mx < 270 and 700 < my < 740:
        if num_ships[2] != 0 and chosen_ship is None:
            num_ships[2] = num_ships[2] - 1
            return SHIP3SIDE
        else:
            return chosen_ship
    elif 430 < mx < 520 and 650 < my < 690:
        if num_ships[1] != 0 and chosen_ship is None:
            num_ships[1] = num_ships[1] - 1
            return SHIP2SIDE
        else:
            return chosen_ship
    elif 430 < mx < 470 and 700 < my < 740:
        if num_ships[0] != 0 and chosen_ship is None:
            num_ships[0] = num_ships[0] - 1
            return SHIP1SIDE
        else:
            return chosen_ship
    elif 100 < mx < 600 and 100 < my < 600:
        if chosen_ship is not None:
            if board.place_ship(mx, my, chosen_ship, rotate) is False:
                return chosen_ship
        else:
            return chosen_ship
    else:
        return chosen_ship


def game():
    run = True
    clock = pygame.time.Clock()
    chosen_ship = None
    rotate = False
    game_phase = False
    board = Board(WIN)
    turn = board.myNumber

    while run:
        clock.tick(FPS)
        board.draw_board()
        mx, my = pygame.mouse.get_pos()
        if game_phase is False:
            draw_setup(WIN)
        if chosen_ship is not None:
            board.show_possible()
            if rotate is False:
                WIN.blit(chosen_ship, (mx - 20, my - 20))
            else:
                WIN.blit(pygame.transform.rotate(chosen_ship, -90), (mx - 20, my - 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if game_phase is False:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        chosen_ship = set_ships(mx, my, chosen_ship, board, rotate)
                        if (num_ships[0] + num_ships[1] + num_ships[2] + num_ships[3]) == 0 and chosen_ship is None:
                            game_phase = not game_phase
                    if event.button == 3:
                        rotate = not rotate
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 750 < mx < 1250 and 100 < my < 600:
                        board.shoot_the_enemy(mx, my)

        board.draw_ships()
        board.show_hit()
        board.end_game()
        pygame.display.update()
    pygame.quit()


def setMode(val, test):
    global mode
    pressSound.play()
    print(val[0], test)
    mode = val[0]


def playPressSound(val):
    pressSound.play()


def main():
    menu = pygame_menu.Menu('Welcome', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.text_input("Name: ", default="User name", onchange=playPressSound)
    menu.add.selector('Mode: ', [('Solo', 0), ('Multiplayer', 1)], onchange=setMode)
    menu.add.button("Play", game)
    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(WIN)


if __name__ == '__main__':
    main()
