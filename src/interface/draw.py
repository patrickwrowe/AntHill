import pygame
from src.sim.datatypes.entities import Entity
from typing import List

def draw_frame(screen: pygame.Surface, entities: List[Entity]):
    # Draw to the screen
    screen.fill((255, 255, 255))

    for entity in entities:
        pygame.draw.circle(screen,
                           (0, 0, 0),
                            entity.pos.coords,
                            radius=1)

    # Update the display
    pygame.display.flip()
