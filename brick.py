import pygame
from settings import *


class Brick:    
    color_ranking = ["blue", "green", "yellow", "orange", "red"]
    def __init__(self, x, y, row):        
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.rank = ROWS - row + 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.color_ranking[self.rank - 1], self.rect)
        pygame.draw.rect(screen, "black", self.rect, 2)

    def get_brick_score(self, scoring_ratio):
        score = self.rank * scoring_ratio
        return score

def create_bricks():
    bricks = []
    for row in range(ROWS):
        for col in range(COLS):
            x = col * (BRICK_WIDTH + 10) + 35
            y = row * (BRICK_HEIGHT + 10) + 50
            bricks.append(Brick(x, y, row + 1))
    return bricks