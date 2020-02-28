import pygame
from bird import Background, Bird, Pipe


fps = 60
width = 288
height = 512

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

background = Background(width, height)

digits = [pygame.image.load(f'resources/sprites/{i}.png') for i in range(10)]


def show_score(score):
    score_digits = [int(x) for x in str(score)]
    total_width = 0  # total width of all numbers to be printed
    for digit in score_digits:
        total_width += digits[digit].get_width()
    x_offset = 10
    for digit in score_digits:
        screen.blit(digits[digit], (x_offset, 10))
        x_offset += digits[digit].get_width()


while True:
    pipe = Pipe(width, height)
    bird = Bird(width, height, pipe)

    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                for object in (background, pipe, bird):
                    object.receive_event(event)
        for object in (background, pipe, bird):
            object.update()
            object.draw(screen)
        show_score(bird.points)
        pygame.display.update()
