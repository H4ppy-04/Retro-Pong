"""
Author: Joshua Rose (joshuarose099 (at) gmail (dot) com)
Description: This is a 2-player pong game that I made. This is PVP (Player
    versus player), so there is no AI or machine to play against. For the controls
    player A can use W and S to control the up and down movements (respectively) of
    the paddle on the left-hand side of the screen. Inversely, player B can use the
    UP and DOWN arrow keys to control the respective up and down movement of the
    paddle on the right-hand side of the screen. First to 3 points wins.

Credits: Kenney.nl under the CC0 license for assets.
"""

import pygame

_, failed = pygame.init()
assert not failed

window_size = 1920, 1080
screen = pygame.display.set_mode(window_size)
font = pygame.font.Font("Fonts/Kenney Future.ttf", 80)
pygame.display.set_caption("Pong")

sound_won = pygame.Sound("Sounds/SoundCoin.wav")
sound_hit_a = pygame.Sound("Sounds/SoundLand1.wav")
sound_hit_b = pygame.Sound("Sounds/SoundLand2.wav")
sound_start_level = pygame.Sound("Sounds/SoundStartLevel.wav")


class Paddle:
    size = 30, 90
    speed = 0.7

    def __init__(self, x, y):
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = 0
        pygame.draw.rect(self.image, "#FFFFFF", (0, 0, *self.size), 0, 10)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def update(self, delta: float):
        if self.direction == -1:
            if self.rect.top <= 0:
                return
        elif self.direction == 1:
            if self.rect.bottom >= window_size[1]:
                return
        self.rect.y += self.direction * self.speed * delta


class Score:
    player = 0
    enemy = 0

    def reset(self):
        self.player = 0
        self.enemy = 0

    def render(self) -> list[pygame.Surface]:
        """Return player and enemy scores respectively"""
        return [
            font.render(str(self.player), True, (50, 50, 50)),
            font.render(str(self.enemy), True, (50, 50, 50)),
        ]


score = Score()
score_text = score.render()


class Ball:
    size = 50
    speed = 0.6

    def __init__(self):
        self.image = pygame.Surface((self.size, self.size))
        self.direction = [1, 1]
        self.rect = self.image.get_rect(
            center=(
                window_size[0] / 2 - self.size / 2,
                window_size[1] / 2 - self.size / 2,
            )
        )
        pygame.draw.circle(
            self.image, "#FFFFFF", (self.size // 2, self.size // 2), self.size / 2
        )

    def update(self, delta: float):
        global score_text
        self.rect.x += self.direction[0] * self.speed * delta
        self.rect.y += self.direction[1] * self.speed * delta

        if self.rect.bottom > window_size[1] or self.rect.top < 0:
            self.direction[1] = -self.direction[1]
        if self.rect.right < 0:
            self.reset_position()
            score.enemy += 1
            sound_won.play()
            if score.enemy == 3:
                score.reset()
                sound_start_level.play()
            score_text = score.render()
        if self.rect.left > window_size[0]:
            self.reset_position()
            score.player += 1
            sound_won.play()
            if score.player == 3:
                score.reset()
                sound_start_level.play()
            score_text = score.render()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def reset_position(self):
        self.rect.x = window_size[0] / 2 - self.size / 2
        self.rect.y = window_size[1] / 2 - self.size / 2

    def switch_direction(self):
        self.direction[0] = -self.direction[0]


running = True

ball = Ball()
paddle_a = Paddle(Paddle.size[0] / 2, window_size[0] / 2 - Paddle.size[1] / 2)
paddle_b = Paddle(
    window_size[0] - Paddle.size[0] / 2, window_size[0] / 2 - Paddle.size[1] / 2
)

delta = 0.0
clock = pygame.time.Clock()

sound_start_level.play()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddle_b.direction = -1
            if event.key == pygame.K_DOWN:
                paddle_b.direction = 1
            if event.key == pygame.K_w:
                paddle_a.direction = -1
            if event.key == pygame.K_s:
                paddle_a.direction = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                paddle_b.direction = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                paddle_a.direction = 0

    screen.fill((20, 20, 20))

    screen.blit(
        score_text[0],
        (
            window_size[0] / 5 - score_text[0].width / 2,
            window_size[1] / 2 - score_text[0].height / 2,
        ),
    )

    screen.blit(
        score_text[1],
        (
            (window_size[0] - (window_size[0] / 5)) - score_text[1].width / 2,
            window_size[1] / 2 - score_text[1].height / 2,
        ),
    )

    ball.draw(screen)
    ball.update(delta)

    if ball.rect.colliderect(paddle_a.rect):
        ball.switch_direction()
        sound_hit_a.play()
    elif ball.rect.colliderect(paddle_b.rect):
        ball.switch_direction()
        sound_hit_b.play()

    paddle_a.draw(screen)
    paddle_b.draw(screen)

    paddle_a.update(delta)
    paddle_b.update(delta)

    pygame.display.flip()
    delta = clock.tick(60)

pygame.quit()
exit(0)
