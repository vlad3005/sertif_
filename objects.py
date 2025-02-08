import random
import pygame
from screen_config import SCREEN_WIDTH, SCREEN_HEIGHT

class CoinsAndBombs:
    def __init__(self):
        self.obj = []
        self.speed = 4

    def move(self):
        for i in range(len(self.obj)):
            self.obj[i][1] += self.speed

    def create(self):
        if random.random() < 0.03:
            x = random.randint(0, SCREEN_WIDTH)
            num = random.randint(1, 10)
            if num % 2 == 0:
                self.obj.append([x, 0, False])
            else:
                self.obj.append([x, 0, True])

    def clear(self):
        self.obj = [pos for pos in self.obj if pos[1] < SCREEN_HEIGHT]

    def draw(self, screen):
        for pos in self.obj:
            if pos[2]:
                coin_img = pygame.image.load("gold-coin.png")
                coin_img = pygame.transform.scale(coin_img, (20, 20))
                coin_img_location = coin_img.get_rect()
                coin_img_location.center = pos[0], pos[1]
                screen.blit(coin_img, coin_img_location)
            else:
                bomb_img = pygame.image.load("bomb_circle.png")
                bomb_img = pygame.transform.scale(bomb_img,(30,30))
                bomb_img_location = bomb_img.get_rect()
                bomb_img_location.center = pos[0], pos[1]
                screen.blit(bomb_img,bomb_img_location)