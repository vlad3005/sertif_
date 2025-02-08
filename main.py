import pygame
import sqlite3
import random

class  LeaderTop:
    def __init__(self):
        connection = sqlite3.connect('leaders_top.db')
        cursor = connection.cursor()
        cursor.execute('''
                                       CREATE TABLE IF NOT EXISTS Users (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       username TEXT DEFAULT '',
                                       score INTEGER DEFAULT 0
                                       )
                                       ''')
        connection.commit()
        connection.close()

    def insert_nickname(self, username):
        connection = sqlite3.connect('leaders_top.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('''
            INSERT INTO Users (username) VALUES (?)
            ''', (username,))
        connection.commit()
        connection.close()

    def update_score(self, score, username):
        connection = sqlite3.connect('leaders_top.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE Users SET score = ? WHERE username = ? AND score < ?',
                       (score, username, score))
        connection.commit()
        connection.close()

    def get_top(self)->list:
        connection = sqlite3.connect('leaders_top.db')
        cursor = connection.cursor()
        cursor.execute('SELECT username, score FROM Users ORDER BY score DESC')
        results = cursor.fetchall()
        connection.close()
        return results


class InputBox:
    def __init__(self, x, y, width, height, text=''):
        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')
        self.input_box_font = pygame.font.SysFont('Verdana', 15)
        self.rect = pygame.Rect(x, y, width, height)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.input_box_font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.input_box_font.render(self.text, True, self.color)

    def get_text(self)->str:
        return str(self.text)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

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

    def draw(self):
        pygame.draw.rect(screen, self.player_color,
                         (self.player_x, self.player_y, self.player_size, self.player_size))

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

    def draw(self):
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

class Game:
    def __init__(self):
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
            screen.blit(start_ms,
                        (SCREEN_WIDTH // 2 - start_ms.get_width() // 2,
                         SCREEN_HEIGHT // 2 - start_ms.get_height() // 2))
            self.ib.update()
            self.ib.draw()
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
            self.coins_and_bombs.draw()
            self.pl.draw()
            self.draw_score()
            self.draw_time()
            ms = self.font.render("собирай монеты и избегай бомб 30 секунд",
                                  True, (255, 255, 255))
            screen.blit(ms, (SCREEN_WIDTH // 2 - ms.get_width() // 2,
                             SCREEN_HEIGHT // 2 - ms.get_height() // 2))
            pygame.display.update()
            clock.tick(60)

    def screen_update(self):
        screen.fill((0, 0, 0))

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
        screen.blit(score_surface, (10, 10))

    def draw_time(self):
        time_surface = self.font.render(f"Время: {(pygame.time.get_ticks() - self.start_time) / 1000}",
                                        True, (255, 255, 255))
        screen.blit(time_surface, (10, 50))

    def draw_lead_top(self):
        merge = 50
        top_list = 0
        for leaders in self.lt.get_top():
            if top_list == 4:
                break
            ms_leaders = self.font.render(f"{leaders[0]} - {leaders[1]}",
                                          True, (255, 0, 0))
            screen.blit(ms_leaders,
                        (SCREEN_WIDTH // 2 - ms_leaders.get_width() // 2,
                         SCREEN_HEIGHT // 2 - ms_leaders.get_height() // 2 + merge))
            pygame.display.update()
            merge += 50
            top_list += 1

    def lose(self):
        self.lt.update_score(self.score, self.username)
        self.draw_lead_top()

        message_surface = self.font.render("Ты проиграл", True, (255, 0, 0))
        screen.blit(message_surface, (SCREEN_WIDTH // 2 - message_surface.get_width() // 2,
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
        screen.blit(message_surface,
                    (SCREEN_WIDTH // 2 - message_surface.get_width() // 2,
                     SCREEN_HEIGHT // 2 - message_surface.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        exit()


pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
Game()
pygame.quit()
