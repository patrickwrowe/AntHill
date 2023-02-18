import attrs
import pygame
import sys
import os

from src.config.global_conf import gconf

@attrs.define
class PGSetup:

    screen: pygame.Surface
    clock: pygame.time.Clock

    @classmethod
    def pygame_setup(cls):

        # Initialize Pygame
        pygame.init()
        
        # Set up the display
        screen = pygame.display.set_mode((gconf.scrn_wdt, gconf.scrn_ht))
        pygame.display.set_caption("Ant Hill")

        # Set up the clock
        clock = pygame.time.Clock()

        return cls(screen=screen, 
                       clock=clock)

@attrs.define
class SystemSetup:

    root_dir: os.PathLike

    @classmethod
    def system_setup(cls):
        """Perform miscellaneous system setup, such as
        ensuring that libraries can be imported by adding
        the antihill root directory to the PYTHONPATH."""

        root_dir = os.path.dirname(os.getcwd())
        print(root_dir)
        sys.path.append(root_dir)

        return cls(root_dir = root_dir)