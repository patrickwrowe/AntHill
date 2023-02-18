import attrs
import pygame

from typing import Any

@attrs.define
class PGSetup:

    screen: pygame.Surface
    clock: pygame.time.Clock

    @classmethod
    def pygame_setup(cls):

        # Initialize Pygame
        pygame.init()

        # Set up the display
        width = 800
        height = 600
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Ant Hill")

        # Set up the clock
        clock = pygame.time.Clock()

        return PGSetup(screen=screen, 
                       clock=clock)