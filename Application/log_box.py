import pygame
from constants import LINE_COLOR, LINE_WIDTH, FONT


class LogBox:
    def __init__(self, screen):
        self.log_to_draw = ["test tekstu", "zobaczmy długość", "encoded asn: b'0\\x06\\x02\\x01\\x00\\x02\\x01\\x00' len= 8"]
        self.WIN = screen
        self.log_font = pygame.font.SysFont('arial', 14)

    def draw_box(self):
        pygame.draw.line(self.WIN, LINE_COLOR, (700, 625),  (700, 775), LINE_WIDTH)
        pygame.draw.line(self.WIN, LINE_COLOR, (1250, 625),  (1250, 775), LINE_WIDTH)
        pygame.draw.line(self.WIN, LINE_COLOR, (700, 625),  (1250, 625), LINE_WIDTH)
        pygame.draw.line(self.WIN, LINE_COLOR, (700, 775), (1250, 775), LINE_WIDTH)
        if len(self.log_to_draw) < 8:
            for i in range(len(self.log_to_draw)):
                self.WIN.blit(self.log_font.render(self.log_to_draw[i], True, LINE_COLOR), (710, (630 + 17 * i)))
        else:
            for i in range(8):
                self.WIN.blit(self.log_font.render(self.log_to_draw[len(self.log_to_draw) - 8 + i], True, LINE_COLOR),
                              (710, (630 + 17 * i)))


