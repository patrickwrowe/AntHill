import os
import sys

import attrs
import pygame

from src.config.global_conf import gconf
from typing import List

@attrs.define
class PGSetup:
    screen: pygame.Surface
    clock: pygame.time.Clock

    # Resources
    # This ought to be a dict or something.
    images: List[pygame.Surface]

    @classmethod
    def pygame_setup(cls, root_dir: str):
        # Initialize Pygame
        pygame.init()

        # Set up the display
        screen = pygame.display.set_mode((gconf.scrn_wdt, gconf.scrn_ht))
        pygame.display.set_caption("Ant Hill")

        # Set up the clock
        clock = pygame.time.Clock()

        # Load images
        images = PGSetup.load_images(root_dir)

        return cls(screen=screen, clock=clock, images=images)

    @staticmethod
    def load_images(root_dir: str):
        images_dir = os.path.join(root_dir, "resources", "graphics")
        all_image_files = os.listdir(images_dir)

        # load the images from file
        # This doesn't really look great to be honest.
        all_images = [pygame.image.load(os.path.join(images_dir, image_file)).convert_alpha() 
                      for image_file in all_image_files]
        all_images = [pygame.transform.scale(image, (10, 10)) for image in all_images]

        return all_images

@attrs.define
class SystemSetup:
    root_dir: os.PathLike

    @classmethod
    def system_setup(cls):
        """Perform miscellaneous system setup, such as
        ensuring that libraries can be imported by adding
        the antihill root directory to the PYTHONPATH."""

        root_dir = os.getcwd()
        sys.path.append(root_dir)

        print(f"Running in dir: {root_dir}")

        return cls(root_dir=root_dir)
