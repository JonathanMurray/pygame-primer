#!/usr/bin/env python3
import sys

import pygame
from pygame.surface import Surface

size = (640, 480)
screen: Surface = pygame.display.set_mode(size)
background_color = (100, 100, 255)
screen.fill(background_color)
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
