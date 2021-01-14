import pygame
import sys
import os
from random import randint, choice

pygame.init()
pygame.display.set_caption('Space invaders')
enemy = ['enemy_ship1.png', 'enemy_ship2.png', 'enemy_ship3.png']

explosion = ['image_part_001.png', 'image_part_002.png', 'image_part_003.png', 'image_part_004.png', 'image_part_005.png',
             'image_part_006.png', 'image_part_007.png', 'image_part_008.png', 'image_part_009.png', 'image_part_010.png',
             'image_part_011.png', 'image_part_012.png', 'image_part_013.png', 'image_part_014.png']
timer = 2000
wave = 0
player_hp = 500
score = 0
lives = 5

pause = False
pygame.time.set_timer(pygame.USEREVENT, timer)


class Game:
    def __init__(self):
        pass

    def collide(self):
        for i in enemy_sprites:
            pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, filename, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("data", filename)).convert_alpha()
        if filename == 'enemy_ship1.png':
            self.hp = 100
            self.score = 50
        elif filename == 'enemy_ship2.png':
            self.hp = 150
            self.score = 75
        elif filename == 'enemy_ship3.png':
            self.hp = 200
            self.score = 100
        self.counter_shot = 50
        self.shot_speed = 1
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -100
        self.speed_enemy = 3
        self.add(group)
        self.name = filename

    def update(self, *args):
        self.counter_shot -= self.shot_speed
        global player_hp, score, lives
        if self.rect.y + self.speed_enemy < 700:
            self.rect.y += self.speed_enemy
        else:
            self.kill()
            lives -= 1

        for i in range(len(shots)):
            i1 = int(str(i))
            i = shots[i1]
            if i == '.':
                continue
            x, y, speed = i.get_x(), i.get_y(), i.get_speed()
            if self.rect.x < x < self.rect.x + 100 and self.rect.y < y < self.rect.y + 100 and speed < 0:
                self.hp -= damage
                expl = Explosion((self.rect.x + 50, self.rect.y + 50), 'small')
                explosions.append(expl)
                all_sprites.add(expl)
                if self.hp <= 0:
                    expl = Explosion((self.rect.x + 50, self.rect.y + 50), 'lg')
                    explosions.append(expl)
                    all_sprites.add(expl)
                    score += self.score
                    self.kill()
                shots[i1].delet()
                shots[i1] = '.'

        while '.' in shots:
            shots.remove('.')

        if self.rect.x < player_x + 50 < self.rect.x + 100 and self.rect.y < player_y + 50 < self.rect.y + 100:
            player_hp -= 50
            score += self.score
            expl = Explosion((self.rect.x + 50, self.rect.y + 50), 'lg')
            explosions.append(expl)
            all_sprites.add(expl)
            self.kill()

        if player_x - 50 <= self.rect.x <= player_x + 100 and self.counter_shot < 0:
            self.counter_shot = 100
            if self.name == 'enemy_ship1.png':
                shot = Shot(self.rect.x, self.rect.y, 10)
                shots.append(shot)
            elif self.name == 'enemy_ship2.png':
                shot = Shot(self.rect.x - 10, self.rect.y, 10)
                shots.append(shot)
                shot = Shot(self.rect.x + 10, self.rect.y, 10)
                shots.append(shot)
            elif self.name == 'enemy_ship3.png':
                shot = Shot(self.rect.x, self.rect.y, 10)
                shots.append(shot)
                shot = Shot(self.rect.x - 20, self.rect.y, 10)
                shots.append(shot)
                shot = Shot(self.rect.x + 20, self.rect.y, 10)
                shots.append(shot)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.image = pygame.image.load(os.path.join("data", explosion[self.frame])).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.size = size
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.size == 'small':
                self.frame += 1
            if self.frame == len(explosion) - 1:
                self.kill()
            else:
                center = self.rect.center
                if self.frame >= 14:
                    self.kill()
                else:
                    if self.size == 'small':
                        self.image = pygame.image.load(os.path.join("data", explosion[self.frame])).convert_alpha()
                        self.image = pygame.transform.scale(self.image, (40, 40))
                        self.rect = self.image.get_rect()
                        self.rect.center = center
                    else:
                        self.image = pygame.image.load(os.path.join("data", explosion[self.frame])).convert_alpha()
                        self.rect = self.image.get_rect()
                        self.rect.center = center


class Shot:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.sprite = pygame.sprite.Sprite()
        if self.speed < 0:
            self.sprite.image = load_image("shot_1.png")
        else:
            self.sprite.image = load_image("shot_2.png")
        self.sprite.rect = self.sprite.image.get_rect()
        all_sprites.add(self.sprite)
        self.sprite.rect.x = self.x + 45
        self.sprite.rect.y = self.y - 10

    def Move(self):
        self.sprite.rect.y += self.speed
        if self.sprite.rect.y + self.speed < -20:
            all_sprites.remove(self.sprite)
        elif self.sprite.rect.y + self.speed > 800:
            all_sprites.remove(self.sprite)

    def delet(self):
        all_sprites.remove(self.sprite)

    def get_y(self):
        return int(self.sprite.rect.y)

    def get_x(self):
        return int(self.sprite.rect.x)

    def get_speed(self):
        return int(self.speed)


def createship(group):
    name = choice(enemy)
    x = randint(100, 800)
    return Enemy(x, name, group)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    return image


def s():
    for i in range(len(shots)):
        r = shots[i]
        if r == '.':
            continue
        r.Move()
        if r.get_y() < -20:
            shots[i] = '.'
    while '.' in shots:
        shots.remove('.')


image = load_image("фон.png")
global all_sprites
all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("spaceship_1.png")
sprite.image = pygame.transform.scale(sprite.image, (100, 100))
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
global explosions
explosions = []
sprite.rect.x = 5
sprite.rect.y = 550
image = pygame.transform.scale(image, (1000, 700))
board = Game()
screen = pygame.display.set_mode((1300, 700))

enemy_gr = pygame.sprite.Group()
createship(enemy_gr)

expose_gr = pygame.sprite.Group()

font = pygame.font.Font(None, 60)
text = font.render("Score: {}".format(score), True, (255, 0, 0))
text_x = 1040
text_y = 40
text1 = font.render("{}".format('Wave:'), True, (255, 0, 0))
text1_x = 1040
text1_y = 100
text2 = font.render("Health: {}".format(player_hp), True, (255, 0, 0))
text2_x = 1040
text2_y = 160
text3 = font.render("{}".format('Lives:'), True, (255, 0, 0))
text3_x = 1040
text3_y = 220

global shots
shots = []

screen.blit(image, (0, 0))
clock = pygame.time.Clock()
fps = 60
speed = 10
global damage
damage = 50
global damage_enemy
damage_enemy = 10
counter_shot = 100
shot_speed = 5
regeneration = 1  # кол-во хп восстанавливаемого в секунду
regeneration_cooldown = 60
running = True

while running:
    clock.tick(fps)
    regeneration_cooldown -= 1
    if regeneration_cooldown == 0:
        if pause:
            regeneration_cooldown += 1
            pass
        else:
            regeneration_cooldown = 60
            player_hp += regeneration
            if player_hp > 500:
                player_hp = 500
    counter_shot -= shot_speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT and not pause:
            createship(enemy_gr)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if not pause:
                    pause = True
                else:
                    pause = False

    keys = pygame.key.get_pressed()
    if pause:
        continue
    if keys[pygame.K_LEFT]:
        if sprite.rect.x - speed > 0:
            sprite.rect.x -= speed
    if keys[pygame.K_RIGHT]:
        if sprite.rect.x + speed < 900:
            sprite.rect.x += speed
    if keys[pygame.K_UP]:
        if sprite.rect.y - speed > 0:
            sprite.rect.y -= speed
    if keys[pygame.K_DOWN]:
        if sprite.rect.y + speed < 610:
            sprite.rect.y += speed
    if keys[pygame.K_q]:
        sprite.image = load_image("spaceship_2.png")
        sprite.image = pygame.transform.scale(sprite.image, (100, 100))

    if keys[pygame.K_w]:
        if counter_shot < 0:
            shot = Shot(sprite.rect.x, sprite.rect.y, -10)
            shots.append(shot)
            shot = Shot(sprite.rect.x - 20, sprite.rect.y, -10)
            shots.append(shot)
            shot = Shot(sprite.rect.x + 20, sprite.rect.y, -10)
            shots.append(shot)
            counter_shot = 100
    s()
    player_x, player_y = sprite.rect.x, sprite.rect.y

    screen.fill((0, 0, 0))
    screen.blit(image, (0, 0))

    screen.blit(image, (0, 0))
    pygame.draw.line(screen, (255, 255, 255),
                     (1000, 0),
                     (1000, 700), 10)

    text = font.render("Score: {}".format(score), True, (255, 0, 0))
    text1 = font.render("{}".format('Wave:'), True, (255, 0, 0))
    text2 = font.render("Health: {}".format(player_hp), True, (255, 0, 0))
    text3 = font.render("Lives: {}".format(lives), True, (255, 0, 0))

    screen.blit(text, (text_x, text_y))
    screen.blit(text1, (text1_x, text1_y))
    screen.blit(text2, (text2_x, text2_y))
    screen.blit(text3, (text3_x, text3_y))
    for i in explosions:
        i.update()

    for i in range(len(shots)):
            i1 = int(str(i))
            i = shots[i1]
            x, y, fly_speed = i.get_x(), i.get_y(), i.get_speed()
            if sprite.rect.x < x < sprite.rect.x + 100 and sprite.rect.y < y < sprite.rect.y + 100 and fly_speed > 0:
                player_hp -= damage_enemy
                expl = Explosion((sprite.rect.x + 50, sprite.rect.y + 50), 'small')
                explosions.append(expl)
                all_sprites.add(expl)
                shots[i1].delet()
                shots[i1] = '.'

    enemy_gr.draw(screen)
    all_sprites.draw(screen)
    enemy_gr.update()
    pygame.display.flip()

pygame.quit()
