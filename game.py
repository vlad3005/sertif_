import pygame
from database import LeaderTop
from input_box import InputBox
from player import Player
from objects import CoinsAndBombs
from screen_config import SCREEN_WIDTH, SCREEN_HEIGHT

class Game:
    def __init__(self, screen, clock):
        self.start = False
        self.start_time = 0
        self.score = 0
        self.username = ""
        self.font = pygame.font.SysFont("Arial", 36)
        self.ib = InputBox(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 140, 32)
        self.pl = Player()
        self.lt = LeaderTop()
        self.coins_and_bombs = CoinsAndBombs()
        self.running = True
        self.screen = screen
        self.clock = clock

        self.start_screen()
        self.play()

    def start_screen(self):
        while not self.start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start = True
                    self.running = False
                self.ib.handle_event(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start = True
                        self.username = self.ib.get_text()
                        self.lt.insert_nickname(self.username)
            self.screen_update()
            start_ms = self.font.render("Введите ник и нажмите enter",
                                        True, (255, 255, 255))
            self.screen.blit(start_ms,
                        (SCREEN_WIDTH // 2 - start_ms.get_width() // 2,
                         SCREEN_HEIGHT // 2 - start_ms.get_height() // 2))
            self.ib.update()
            self.ib.draw(self.screen)
            pygame.display.update()

        self.screen_update()
        pygame.display.update()

        self.start_time = pygame.time.get_ticks()

    def play(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            time = (pygame.time.get_ticks() - self.start_time)/1000

            self.pl.move(pygame.key.get_pressed())
            self.coins_and_bombs.move()
            self.coins_and_bombs.create()
            self.coins_and_bombs.clear()
            self.screen_update()
            self.collision(self.pl.player_x, self.pl.player_y)
            if time >30:
                self.win()
            self.coins_and_bombs.draw(self.screen)
            self.pl.draw(self.screen)
            self.draw_score()
            self.draw_time()
            ms = self.font.render("собирай монеты и избегай бомб 30 секунд",
                                  True, (255, 255, 255))
            self.screen.blit(ms, (SCREEN_WIDTH // 2 - ms.get_width() // 2,
                             SCREEN_HEIGHT // 2 - ms.get_height() // 2))
            pygame.display.update()
            self.clock.tick(60)

    def screen_update(self):
        self.screen.fill((0, 0, 0))

    def collision(self, player_x, player_y):
        for pos in self.coins_and_bombs.obj:
            if pos[2]:
                if abs(pos[0] - player_x) <= 20 and abs(pos[1] - player_y) <= 15:
                    self.score += 1
                    self.coins_and_bombs.obj.remove(pos)
            else:
                if abs(pos[0] - player_x) <= 20 and abs(pos[1] - player_y) <= 15:
                    self.lose()

    def draw_score(self):
        score_surface = self.font.render(f"Монеты: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

    def draw_time(self):
        time_surface = self.font.render(f"Время: {(pygame.time.get_ticks() - self.start_time) / 1000}",
                                        True, (255, 255, 255))
        self.screen.blit(time_surface, (10, 50))

    def draw_lead_top(self):
        merge = 50
        top_list = 0
        for leaders in self.lt.get_top():
            if top_list == 4:
                break
            ms_leaders = self.font.render(f"{leaders[0]} - {leaders[1]}",
                                          True, (255, 0, 0))
            self.screen.blit(ms_leaders,
                        (SCREEN_WIDTH // 2 - ms_leaders.get_width() // 2,
                         SCREEN_HEIGHT // 2 - ms_leaders.get_height() // 2 + merge))
            pygame.display.update()
            merge += 50
            top_list += 1

    def lose(self):
        self.lt.update_score(self.score, self.username)
        self.draw_lead_top()

        message_surface = self.font.render("Ты проиграл", True, (255, 0, 0))
        self.screen.blit(message_surface, (SCREEN_WIDTH // 2 - message_surface.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - message_surface.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        exit()

    def win(self):
        self.lt.update_score(self.score, self.username)
        self.draw_lead_top()

        message_surface = self.font.render(f"Ты победил! Монеты: {self.score}",
                                           True, (255, 0, 0))
        self.screen.blit(message_surface,
                    (SCREEN_WIDTH // 2 - message_surface.get_width() // 2,
                     SCREEN_HEIGHT // 2 - message_surface.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        exit()