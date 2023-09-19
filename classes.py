import pygame


class Box:
    def __init__(self, x, y, width, height, color, row, col):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.row = row
        self.col = col

    def drawBox(self, screen, color=None):
        if color is None:
            color = self.color
        pygame.draw.rect(screen, color, self.rect)

    def drawCoordinate(self, screen):
        font = pygame.font.Font(None, 15)
        text = font.render(f"({self.row},{self.col})", True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


class Snake:
    def __init__(self, row, col,color, headX= 0, headY= 0, width=30, height=30,lastpos = None):
        self.row = row
        self.col = col
        self.headX = headX
        self.headY = headY
        self.width = width
        self.height = height
        self.rect = pygame.Rect(row, col,30, 30)    # idk how is this works but it works!
        self.lastPos = 0

    def drawBox(self, screen, color):
        if color is None:
            color = self.color
        pygame.draw.rect(screen, color, self.rect)

    def drawCoordinate(self, screen):
        font = pygame.font.Font(None, 15)
        text = font.render(f"({self.row},{self.col})", True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def move(self):
        if self.row >= 19 and self.headX == 1:
            self.row = 0
        elif self.row <= 0 and self.headX == -1:
            self.row = 19
        else:
            self.row += self.headX

        if self.col >= 19 and self.headY == 1:
            self.col = 0
        elif self.col <= 0 and self.headY == -1:
            self.col = 19
        else:
            self.col += self.headY