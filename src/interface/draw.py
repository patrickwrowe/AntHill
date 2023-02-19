import attrs
import pygame
from src.sim.datatypes.entities import Entity
from src.setup import PGSetup
from typing import List

import numpy as np

@attrs.define
class Artist:

    # This should be a dict or something
    images: List[pygame.Surface]

    @classmethod
    def from_config(cls, pg_setup: PGSetup):
        return cls(images = pg_setup.images)

    def draw_frame(self, screen: pygame.Surface, entities: List[Entity]):
        
        # Draw to the screen
        screen.fill((255, 255, 255))

        # Draw dem ants
        self.draw_entities(screen=screen, entities=entities)

        # Update the display
        pygame.display.flip()

    def draw_entities(self, screen: pygame.Surface, entities: List[Entity]):
        for entity in entities:
            pygame.draw.circle(screen,
                            (0, 0, 0),
                                entity.pos.coords,
                                radius=1)
            
            # This is probably HORRIBLY inefficient.
            # Definitely ought to optimise this - disabling for now in favour of dots.
            # coords = tuple(np.array(entity.pos.coords) - np.array(self.images[0].get_rect().center))
            # screen.blit(self.images[0], coords)