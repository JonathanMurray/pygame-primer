#!/usr/bin/env python3
import sys

import pygame
from pygame.surface import Surface

size = (640, 480)
screen: Surface = pygame.display.set_mode(size)
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
color_index = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            color_index = (color_index + 1) % len(colors)

    screen.fill(colors[color_index])
    pygame.display.update()
