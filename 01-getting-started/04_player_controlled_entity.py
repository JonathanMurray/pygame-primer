#!/usr/bin/env python3
import pygame
import sys
from pygame.rect import Rect
from pygame.time import Clock

size = (640, 480)
screen = pygame.display.set_mode(size)
boxman_color = (100, 150, 200)
x, y = 50, 300
boxman = Rect(x, y, 128, 128)
movement_speed = 0.2
clock = Clock()
while True:

    # Process Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    # Update
    elapsed_time = clock.tick()
    if pygame.key.get_pressed()[pygame.K_w]:
        y -= elapsed_time * movement_speed
    if pygame.key.get_pressed()[pygame.K_a]:
        x -= elapsed_time * movement_speed
    if pygame.key.get_pressed()[pygame.K_s]:
        y += elapsed_time * movement_speed
    if pygame.key.get_pressed()[pygame.K_d]:
        x += elapsed_time * movement_speed

    # Render
    screen.fill((0, 0, 0))
    boxman.topleft = (x, y)
    pygame.draw.rect(screen, boxman_color, boxman)
    pygame.display.update()
