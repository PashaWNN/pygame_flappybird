import random
from typing import Type, Collection

import pygame


class GameObject:

    images = []

    def __init__(self, scene):
        self.scene = scene
        self.sprites = [
            pygame.image.load(s).convert_alpha()
            for s in self.images
        ]
        self.x = 0
        self.y = 0

    def receive_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        sprites = self.sprites
        if sprites:
            screen.blit(self.sprites[pygame.time.get_ticks() % 100 * len(sprites) // 100], (self.x, self.y))


class Background(GameObject):
    images = ['resources/sprites/background-day.png']


class Bird(GameObject):
    images = [
        'resources/sprites/redbird-downflap.png',
        'resources/sprites/redbird-midflap.png',
        'resources/sprites/redbird-upflap.png'
    ]

    def __init__(self, scene):
        super().__init__(scene)
        self.sprite_width, self.sprite_height = self.sprites[0].get_size()
        self.sound_flap = pygame.mixer.Sound('resources/audio/swoosh.wav')
        self.sound_hit = pygame.mixer.Sound('resources/audio/hit.wav')
        self.sound_fall = pygame.mixer.Sound('resources/audio/die.wav')
        self.sound_point = pygame.mixer.Sound('resources/audio/point.wav')
        self.gravity = 0.5
        self.lift = -15
        self.pipe = self.scene.get_object('pipe')
        self._set()

    def _set(self):
        self.points = 0
        self.x = 50
        self.y = self.scene.height / 2
        self.alive = True
        self.velocity = 0
        self.pipe.set()

    def update(self):
        self.velocity += self.gravity
        if self.y < self.scene.height + 20:
            self.y += self.velocity
        if self.alive:
            if self._colliding():
                self._hit()
            if self.y > self.scene.height:
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


class Pipe(GameObject):
    images = ['resources/sprites/pipe-green.png']
    def __init__(self, scene):
        super().__init__(scene)
        self.speed = 3
        self.sprite_width, self.sprite_height = self.sprites[0].get_size()
        self.spacing = 125
        self.top = 0
        self.passed = False
        self.y = 0
        self.set()

    def set(self):
        self.top = random.randint(int(self.scene.height / 7), int(3 / 5 * self.scene.height))
        self.y = self.bottom = self.top + self.spacing
        self.x = self.scene.width
        self.passed = False

    def update(self):
        self.x -= self.speed
        if self._offscreen():
            self.set()

    def draw(self, screen):
        screen.blit(self.sprites[0], (self.x, self.bottom))
        screen.blit(pygame.transform.flip(self.sprites[0], False, True), (self.x, self.top-self.sprite_height))

    def _offscreen(self):
        return self.x + self.sprite_width < 0


class ScoreCounter(GameObject):
    images = [
        f'resources/sprites/{i}.png'
        for i in range(10)
    ]

    def __init__(self, scene):
        super().__init__(scene)
        self.bird = self.scene.get_object('bird')

    def draw(self, screen):
        score_digits = [int(x) for x in str(self.bird.points)]
        total_width = 0  # total width of all numbers to be printed
        for digit in score_digits:
            total_width += self.sprites[digit].get_width()
        x_offset = 10
        for digit in score_digits:
            screen.blit(self.sprites[digit], (x_offset, 10))
            x_offset += self.sprites[digit].get_width()


class Scene:
    def __init__(self, width: int, height: int, objects: Collection[Type[GameObject]]):
        self._objects = {}
        self.width = width
        self.height = height
        for obj in objects:
            self._objects[obj.__name__.lower()] = obj(self)

    def get_object(self, name):
        return self._objects.get(name)

    def receive_event(self, event):
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            for object_ in self._objects.values():
                object_.receive_event(event)

    def update(self):
        for object_ in self._objects.values():
            object_.update()

    def draw(self, screen):
        for object_ in self._objects.values():
            object_.draw(screen)
