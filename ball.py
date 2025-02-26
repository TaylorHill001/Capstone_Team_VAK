import pygame
import random
from settings import *


class Ball:
    def __init__(self, speed):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.dx = random.choice([-speed, speed])
        self.dy = -speed
        self.speed = speed

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Wall collision
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx *= -1
        if self.rect.top <= 0:
            self.dy *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, "red", self.rect)