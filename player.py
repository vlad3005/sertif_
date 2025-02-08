import pygame
from screen_config import SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self,):
        self.player_color = (0, 128, 255)
        self.player_size = 20
        self.player_x = SCREEN_WIDTH / 2
        self.player_y = SCREEN_HEIGHT - 30
        self.player_speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.player_x>=0:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player_x+self.player_size<=SCREEN_WIDTH:
            self.player_x += self.player_speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.player_color,
                         (self.player_x, self.player_y, self.player_size, self.player_size))
