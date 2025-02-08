import pygame
from screen_config import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
Game(screen,clock)
pygame.quit()
