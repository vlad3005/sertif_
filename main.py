import pygame
import  sqlite3
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
        cursor.execute('UPDATE Users SET score = ? WHERE username = ? AND score < ?', (score, username, score))
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
        self.player_x = screen_width/2
        self.player_y = screen_height-30
        self.player_speed = 5
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.player_x>=0:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player_x+20<=screen_width:
            self.player_x += self.player_speed
    def draw(self):
        pygame.draw.rect(screen, self.player_color, (self.player_x, self.player_y, self.player_size, self.player_size))

class Game:
    def __init__(self):
        self.start = False
        self.score = 0
        self.username = ""
        self.coins_and_bombs = []
        self.coins_and_bombs_speed = 4
        self.font = pygame.font.SysFont("Arial", 36)
        ib = InputBox(screen_width // 2 - 100, screen_height // 2 + 50, 140, 32)
        pl = Player()
        self.lt = LeaderTop()
        running = True

        while not self.start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start = True
                    running = False
                ib.handle_event(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start = True

                        self.username = ib.get_text()
                        self.lt.insert_nickname(self.username)
            self.screen_update()
            start_ms = self.font.render("Введите ник и нажмите enter", True, (255, 255, 255))
            screen.blit(start_ms, (screen_width // 2 - start_ms.get_width() // 2,
                                   screen_height // 2 - start_ms.get_height() // 2))
            ib.update()

            ib.draw()
            pygame.display.update()

        self.screen_update()
        pygame.display.update()

        self.start_time = pygame.time.get_ticks()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            time = (pygame.time.get_ticks() - self.start_time)/1000

            pl.move(pygame.key.get_pressed())
            self.move()
            self.create()
            self.clear()
            self.screen_update()
            self.collision(pl.player_x, pl.player_y)
            if time >30:
                self.win()
            self.draw()
            pl.draw()
            self.draw_score()
            self.draw_time()
            ms = self.font.render("собирай монеты и избегай бомб 30 секунд", True, (255, 255, 255))
            screen.blit(ms, (screen_width // 2 - ms.get_width() // 2,
                             screen_height // 2 - ms.get_height() // 2))
            pygame.display.update()
            clock.tick(60)

    def move(self):
        for i in range(len(self.coins_and_bombs)):
            self.coins_and_bombs[i][1] += self.coins_and_bombs_speed

    def create(self):
        if random.random() < 0.03:
            x = random.randint(0, screen_width)
            num = random.randint(1, 10)
            if num % 2 == 0:
                self.coins_and_bombs.append([x, 0, False])
            else:
                self.coins_and_bombs.append([x, 0, True])

    def clear(self):
        self.coins_and_bombs = [pos for pos in self.coins_and_bombs if pos[1] < screen_height]

    def screen_update(self):
        screen.fill((0, 0, 0))

    def draw(self):
        for pos in self.coins_and_bombs:
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

    def collision(self, player_x, player_y):
        for pos in self.coins_and_bombs:
            if pos[2]:
                if abs(pos[0] - player_x) <= 20 and abs(pos[1] - player_y) <= 15:
                    self.score += 1
                    self.coins_and_bombs.remove(pos)
            else:
                if abs(pos[0] - player_x) <= 20 and abs(pos[1] - player_y) <= 15:
                    self.lose()

    def draw_score(self):
        score_surface = self.font.render(f"Монеты: {self.score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

    def draw_time(self):
        time_surface = self.font.render(f"Время: {(pygame.time.get_ticks() - self.start_time) / 1000}", True, (255, 255, 255))
        screen.blit(time_surface, (10, 50))
    def lose(self):
        message_surface = self.font.render("Ты проиграл", True, (255, 0, 0))
        screen.blit(message_surface, (screen_width // 2 - message_surface.get_width() // 2,
                                      screen_height // 2 - message_surface.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        exit()

    def win(self):
        self.lt.update_score(self.score, self.username)
        merge = 50
        top_list = 0
        for leaders in self.lt.get_top():
            if top_list ==4:
                break
            ms_leaders = self.font.render(f"{leaders[0]} - {leaders[1]}", True, (255, 0, 0))
            screen.blit(ms_leaders, (screen_width // 2 - ms_leaders.get_width() // 2 ,  screen_height // 2 - ms_leaders.get_height()//2+ merge))
            pygame.display.update()
            merge+=50
            top_list+=1

        message_surface = self.font.render(f"Ты победил! Монеты: {self.score}", True, (255, 0, 0))
        screen.blit(message_surface, (screen_width // 2 - message_surface.get_width() // 2,
                                           screen_height // 2 - message_surface.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        exit()

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
Game()
pygame.quit()