import pygame
import random
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width, screen_height = 288, 624

screen = pygame.display.set_mode((screen_width, screen_height - 20))
pygame.display.set_caption('Flappy Bird')

font = pygame.font.SysFont('Bauhaus93', 60)
white = (255, 255, 255)

ground_scroll = 0
scroll_speed = 1
flying = False
game_over = False
pipe_gap = 150
pipe_freq = 2500
last_pipe = pygame.time.get_ticks() - pipe_freq
score = 0
pass_pipe = False

bg = pygame.image.load("flappy-bird-assets-master/sprites/background-day.png")
ground_img = pygame.image.load("flappy-bird-assets-master/sprites/base.png")
reset_button = pygame.image.load("flappy-bird-assets-master/sprites/message.png")

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = screen_width // 8
    flappy.rect.y = screen_height // 2
    score = 0
    return score


class Bird(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        self.flappy_animation_img = []
        self.index = 0
        self.counter = 0

        for num in range(1, 4):
            bird_img = pygame.image.load(f"flappy-bird-assets-master/sprites/yellowbird-{num}.png")
            self.flappy_animation_img.append(bird_img)
        self.image = self.flappy_animation_img[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.jumped = False



    def update(self):

        if flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 500:
                self.rect.y += int(self.vel)

        if not game_over:
            if pygame.mouse.get_pressed()[0] and self.jumped == False:
                self.jumped = True
                self.vel = -8
            if not pygame.mouse.get_pressed()[0] and self.jumped == True:
                self.jumped = False


            self.counter += 1
            flap_cd = 7

            if self.counter > flap_cd:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.flappy_animation_img):
                    self.index = 0
            self.image = self.flappy_animation_img[self.index]

            self.image = pygame.transform.rotate(self.flappy_animation_img[self.index], -self.vel*2)
        else:
            self.image = pygame.transform.rotate(self.flappy_animation_img[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("flappy-bird-assets-master/sprites/pipe-green.png")
        self.rect = self.image.get_rect()

        if position == -1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - (pipe_gap // 2)]

        if position == 1:
            self.rect.topleft = [x, y + (pipe_gap // 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x: int, y: int, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False
        position = pygame.mouse.get_pos()

        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(screen_width // 8, screen_height // 2)

bird_group.add(flappy)

button = Button(51, 150, reset_button)

running = True
while running:

    clock.tick(fps)

    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    screen.blit(ground_img, (ground_scroll, screen_height - 122))

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score),font, white, (screen_width // 2) - 15, screen_height // 12)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top <= 0:
        game_over = True

    if flappy.rect.bottom >= 495:
        game_over = True
        flying = False

    if not game_over and flying:

        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_freq:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, (screen_height // 2) + pipe_height - 61,  -1)
            top_pipe = Pipe(screen_width, (screen_height // 2) + pipe_height - 61, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 48:
            ground_scroll = 0

        pipe_group.update()

    if game_over:
        if button.draw():
            game_over = False
            score = reset_game()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()
