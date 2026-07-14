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

import sys

import pygame

_, failed = pygame.init()
assert not failed


class Score:

    def __init__(self):
        self.player = 0
        self.enemy = 0

    def reset(self):
        self.player = 0
        self.enemy = 0

    def render(self, font: pygame.Font) -> list[pygame.Surface]:
        """Return player and enemy scores respectively"""
        return [
            font.render(str(self.player), True, (50, 50, 50)),
            font.render(str(self.enemy), True, (50, 50, 50)),
        ]


class Game:
    window_size: tuple[int, int] = 1920, 1080

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(self.window_size)
        self.font = pygame.font.Font("Fonts/Kenney Future.ttf", 80)
        pygame.display.set_caption("Pong")

        self.sound_won = pygame.mixer.Sound("Sounds/SoundCoin.wav")
        self.sound_hit_a = pygame.mixer.Sound("Sounds/SoundLand1.wav")
        self.sound_hit_b = pygame.mixer.Sound("Sounds/SoundLand2.wav")
        self.sound_start_level = pygame.mixer.Sound("Sounds/SoundStartLevel.wav")

        self.ball = Ball()
        self.paddle_a = Paddle(Paddle.size[0] / 2, self.window_size[0] / 2 - Paddle.size[1] / 2)
        self.paddle_b = Paddle(
            self.window_size[0] - Paddle.size[0] / 2,
            self.window_size[1] / 2 - Paddle.size[1] / 2,
        )

        self.score = Score()
        self.score_text = self.score.render(self.font)

        self.delta = 0.0
        self.clock = pygame.time.Clock()

    def update(self, delta):
        self.ball.rect.x += self.ball.direction[0] * self.ball.speed * self.delta
        self.ball.rect.y += self.ball.direction[1] * self.ball.speed * self.delta

        if self.ball.rect.bottom > self.window_size[1] or self.ball.rect.top < 0:
            self.ball.direction[1] = -self.ball.direction[1]
        if self.ball.rect.right < 0:
            self.ball.reset_position()
            self.score.enemy += 1
            self.sound_won.play()
            if self.score.enemy == 3:
                self.score.reset()
                self.sound_start_level.play()
            self.score_text = self.score.render(self.font)
        elif self.ball.rect.left > self.window_size[0]:
            self.ball.reset_position()
            self.score.player += 1
            self.sound_won.play()
            if self.score.player == 3:
                self.score.reset()
                self.sound_start_level.play()
            self.score_text = self.score.render(self.font)
        if self.ball.rect.colliderect(self.paddle_a.rect):
            self.ball.switch_direction()
            self.sound_hit_a.play()
        elif self.ball.rect.colliderect(self.paddle_b.rect):
            self.ball.switch_direction()
            self.sound_hit_b.play()

        self.paddle_a.update(delta)
        self.paddle_b.update(delta)

    def draw(self, surface: pygame.Surface):
        surface.fill((20, 20, 20))

        surface.blit(
            self.score_text[0],
            (
                self.window_size[0] / 5 - self.score_text[0].width / 2,
                self.window_size[1] / 2 - self.score_text[0].height / 2,
            ),
        )

        surface.blit(
            self.score_text[1],
            (
                (self.window_size[0] - (self.window_size[0] / 5)) - self.score_text[1].width / 2,
                self.window_size[1] / 2 - self.score_text[1].height / 2,
            ),
        )

        self.paddle_a.draw(surface)
        self.paddle_b.draw(surface)
        self.ball.draw(surface)

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.paddle_b.direction = -1
                if event.key == pygame.K_DOWN:
                    self.paddle_b.direction = 1
                if event.key == pygame.K_w:
                    self.paddle_a.direction = -1
                if event.key == pygame.K_s:
                    self.paddle_a.direction = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.paddle_b.direction = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    self.paddle_a.direction = 0

        self.update(self.delta)
        self.draw(self.screen)
        pygame.display.flip()

        self.delta = self.clock.tick(60)


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
            if self.rect.bottom >= Game.window_size[1]:
                return
        self.rect.y += self.direction * self.speed * delta


class Ball:
    size = 50
    speed = 0.6

    def __init__(self):
        self.image = pygame.Surface((self.size, self.size))
        self.direction = [1, 1]
        self.rect = self.image.get_rect(
            center=(
                Game.window_size[0] / 2 - self.size / 2,
                Game.window_size[1] / 2 - self.size / 2,
            )
        )
        pygame.draw.circle(self.image, "#FFFFFF", (self.size // 2, self.size // 2), self.size / 2)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def reset_position(self):
        self.rect.x = Game.window_size[0] // 2 - self.size // 2
        self.rect.y = Game.window_size[1] // 2 - self.size // 2

    def switch_direction(self):
        self.direction[0] = -self.direction[0]


def main():
    game = Game()
    game.sound_start_level.play()

    while True:
        game.loop()


if __name__ == "__main__":
    main()
