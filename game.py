import pygame
import random

class RewardsBombs():
    def __init__(self):
        pygame.init()
        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Призы и бомбы")
        self.clock = pygame.time.Clock()
        self.green_pos = [self.screen_width // 2, self.screen_height - 30]
        self.red_positions = []
        self.red_speed = 2
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 24)
        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.green_pos[0] - 20 >= 0:
                            self.green_pos[0] -= 20
                    elif event.key == pygame.K_RIGHT:
                        if self.green_pos[0] + 20 <= self.screen_width:
                            self.green_pos[0] += 20
                    elif event.key == pygame.K_UP:
                        if self.green_pos[1] - 20 >= 0:
                            self.green_pos[1] -= 20
                    elif event.key == pygame.K_DOWN:
                        if self.green_pos[1] + 20 <= self.screen_height:
                            self.green_pos[1] += 20

            # движение красных бомб
            for i in range(len(self.red_positions)):
                self.red_positions[i][1] += self.red_speed

            # создание бомб и призов
            if random.random() < 0.02:
                x = random.randint(0, self.screen_width)
                num = random.randint(1, 10)
                if num % 2 == 0:
                    self.red_positions.append([x, 0, False])
                else:
                    self.red_positions.append([x, 0, True])

            # проверка столкновений с игроком
            for pos in self.red_positions:
                if pos[2]:
                    if abs(pos[0] - self.green_pos[0]) <= 20 and abs(pos[1] - self.green_pos[1]) <= 20:
                        self.score += 1
                        self.red_positions.remove(pos)
                else:
                    if (pos[0] - self.green_pos[0]) ** 2 + (pos[1] - self.green_pos[1]) ** 2 < 400:
                        self.game_over()

            # убираем бомбы за пределами окна
            self.red_positions = [pos for pos in self.red_positions if pos[1] < self.screen_height]
            self.screen.fill((0, 0, 0))

            for pos in self.red_positions:
                if pos[2]:
                    pygame.draw.polygon(self.screen, (0, 0, 255), [[pos[0], pos[1]-10], [pos[0]+10, pos[1]+10], [pos[0]-10, pos[1]+10]])
                else:
                    pygame.draw.circle(self.screen, (255, 0, 0), pos[:2], 10)

            pygame.draw.circle(self.screen, (0, 255, 0), self.green_pos, 10)

            self.draw_score()
            pygame.display.update()
            self.clock.tick(60)

    def draw_score(self):
        score_surface = self.font.render(f"Призы: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

    def game_over(self):
        message_surface = self.font.render(f"Игра закончена! Призы: {self.score}", True, (255, 0, 0))
        self.screen.blit(message_surface, (self.screen_width // 2 - message_surface.get_width() // 2, self.screen_height // 2 - message_surface.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(3000)
        pygame.quit()
        exit()

RewardsBombs()




# import pygame
# import random
#
# pygame.init()
# screen_width = 640
# screen_height = 480
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption('Лабиринт')
#
# black = (0,0,0)
# white = (255,255,255)
# red = (255,0,0)
# blue = (0,0,255)
# green = (0,255,0)
#
# # параметры стен и дверей
# line_width = 10
# line_gap = 40
# line_offset = 20
# door_width = 20
# door_gap = 40
# max_openings_per_line = 5
#
# # параметры и стартовая позиция игрока
# player_radius = 10
# player_speed = 5
# player_x = screen_width - 12
# player_y = screen_height - line_offset
#
# # рисуем стены и двери
# lines = []
# for i in range(0, screen_width, line_gap):
#     #rect = pygame.Rect(i, 0, line_width, screen_height)
#     num_openings = random.randint(1, max_openings_per_line)
#     if num_openings == 1:
#         # одна дверь посередине стены
#         door_pos = random.randint(line_offset + door_width, screen_height - line_offset - door_width)
#         lines.append(pygame.Rect(i, 0, line_width, door_pos - door_width))
#         lines.append(pygame.Rect(i, door_pos + door_width, line_width, screen_height - door_pos - door_width))
#     else:
#         # несколько дверей
#         opening_positions = [0] + sorted([random.randint(line_offset + door_width, screen_height - line_offset - door_width) for _ in range(num_openings-1)]) + [screen_height]
#         for j in range(num_openings):
#             lines.append(pygame.Rect(i, opening_positions[j], line_width, opening_positions[j+1]-opening_positions[j]-door_width))
#
# clock = pygame.time.Clock()
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             quit()
#
#     # передвижение игрока
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT] and player_x > player_radius:
#         player_x -= player_speed
#     elif keys[pygame.K_RIGHT] and player_x < screen_width - player_radius:
#         player_x += player_speed
#     elif keys[pygame.K_UP] and player_y > player_radius:
#         player_y -= player_speed
#     elif keys[pygame.K_DOWN] and player_y < screen_height - player_radius:
#         player_y += player_speed
#
#     # проверка столкновений игрока со стенами
#     player_rect = pygame.Rect(player_x - player_radius, player_y - player_radius, player_radius * 2, player_radius * 2)
#     for line in lines:
#         if line.colliderect(player_rect):
#             # в случае столкновения возвращаем игрока назад
#             if player_x > line.left and player_x < line.right:
#                 if player_y < line.top:
#                     player_y = line.top - player_radius
#                 else:
#                     player_y = line.bottom + player_radius
#             elif player_y > line.top and player_y < line.bottom:
#                 if player_x < line.left:
#                     player_x = line.left - player_radius
#                 else:
#                     player_x = line.right + player_radius
#     screen.fill(black)
#
#     for line in lines:
#         pygame.draw.rect(screen, green, line)
#     pygame.draw.circle(screen, red, (player_x, player_y), player_radius)
#     pygame.display.update()
#     clock.tick(60)