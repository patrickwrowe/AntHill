import attrs
import pygame
from src.sim.datatypes.entities import Entity
from src.sim.datatypes.maps import MapArray
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

    def draw_frame(self, screen: pygame.Surface, entities: List[Entity], map = MapArray):
        
        # Draw to the screen
        screen.fill((255, 255, 255))

        # draw dat map
        self.draw_map(screen=screen, map=map)

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

    def draw_map(self, screen: pygame.Surface, map: MapArray):

        terrain_surface = map.values_as_image

        # Scale the terrain surface to fit the screen
        terrain_surface = pygame.transform.scale(terrain_surface, screen.get_size())

        # Blit the terrain surface onto the screen
        screen.blit(terrain_surface, (0, 0))