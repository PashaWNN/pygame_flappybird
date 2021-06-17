import pygame
from objects import Background, Bird, Pipe, Scene, ScoreCounter

fps = 60
width = 288
height = 512

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')


scene = Scene(width, height, [Background, Pipe, Bird, ScoreCounter])

while True:
    clock.tick(fps)
    for event in pygame.event.get():
        scene.receive_event(event)
    scene.update()
    scene.draw(screen)
    pygame.display.update()
