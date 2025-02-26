import pygame
from settings import *


class Paddle:
    def __init__(self):
        self.width = 100
        self.rect = pygame.Rect((SCREEN_WIDTH // 2 - self.width // 2, SCREEN_HEIGHT - 40), (self.width, PADDLE_HEIGHT))
        self.speed = 10

    def move(self, direction):
        if direction == "LEFT" and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == "RIGHT" and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, "blue", self.rect)