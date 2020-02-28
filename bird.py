import random
import pygame


class Background:
    def __init__(self, width, height):
        self.sprite = pygame.image.load('resources/sprites/background-day.png').convert()
        self.x, self.y = 0, 0

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

    def update(self):
        pass

    def receive_event(self, event):
        pass


class Bird:
    def __init__(self, width, height, pipe):
        self.sprites = [
            pygame.image.load('resources/sprites/redbird-downflap.png').convert_alpha(),
            pygame.image.load('resources/sprites/redbird-midflap.png').convert_alpha(),
            pygame.image.load('resources/sprites/redbird-upflap.png').convert_alpha(),
        ]
        self.sprite_width, self.sprite_height = self.sprites[0].get_size()
        self.sound_flap = pygame.mixer.Sound('resources/audio/swoosh.wav')
        self.sound_hit = pygame.mixer.Sound('resources/audio/hit.wav')
        self.sound_fall = pygame.mixer.Sound('resources/audio/die.wav')
        self.sound_point = pygame.mixer.Sound('resources/audio/point.wav')
        self.gravity = 0.5
        self.lift = -15
        self.height = height
        self.pipe = pipe
        self._set()

    def _set(self):
        self.points = 0
        self.x = 50
        self.y = self.height / 2
        self.alive = True
        self.velocity = 0
        self.pipe.set()

    def draw(self, screen):
        screen.blit(self.sprites [pygame.time.get_ticks() % 300 // 100], (self.x, self.y))

    def update(self):
        self.velocity += self.gravity
        if self.y < self.height + 20:
            self.y += self.velocity
        if self.alive:
            if self._colliding():
                self._hit()
            if self.y > self.height:
                self._fall()
        if self.x > self.pipe.x and not self.pipe.passed and self.alive:
            self.pipe.passed = True
            self.points += 1
            self.sound_point.play()
            print(self.points)

    def _colliding(self):
        return (self.pipe.x + self.pipe.sprite_width > self.x > self.pipe.x) and \
               (self.y < self.pipe.top or self.y > self.pipe.bottom)

    def receive_event(self, event):
        if event.key == pygame.K_SPACE:
            self._up() if self.alive else self._set()

    def _up(self):
        if self.alive:
            self.sound_flap.play()
            self.velocity += self.lift

    def _fall(self):
        self.sound_fall.play()
        self.alive = False

    def _hit(self):
        self.sound_hit.play()
        self.alive = False


class Pipe:
    def __init__(self, width, height):
        self.speed = 3
        self.sprite = pygame.image.load('resources/sprites/pipe-green.png').convert_alpha()
        self.sprite_width, self.sprite_height = self.sprite.get_size()
        self.spacing = 125
        self.height = height
        self.width = width
        self.set()

    def set(self):
        self.top = random.randint(int(self.height / 7), int(3 / 5 * self.height))
        self.y = self.bottom = self.top + self.spacing
        self.x = self.width
        self.passed = False

    def update(self):
        self.x -= self.speed
        if self._offscreen():
            self.set()

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.bottom))
        screen.blit(pygame.transform.flip(self.sprite, False, True), (self.x, self.top-self.sprite_height))

    def _offscreen(self):
        return self.x + self.sprite_width < 0

    def receive_event(self, event):
        pass
