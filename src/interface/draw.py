from typing import Dict, List, Type

import attrs
import matplotlib.pyplot as plt
import numpy as np
import pygame

from src.setup import PGSetup
from src.sim.datatypes.entities import Entity
from src.sim.datatypes.items import Item
from src.sim.datatypes.maps import MapArray
from src.sim.items.pheremones import AntLocationPheremone
from src.sim.maps.environment_maps import AltitudeMap
from src.sim.sim import AntHillSim


@attrs.define
class Artist:
    # This should be a dict or something
    images: List[pygame.Surface]

    @classmethod
    def from_config(cls, pg_setup: PGSetup):
        return cls(images=pg_setup.images)

    def draw_frame(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        simulation: AntHillSim,
    ):
        """
        Draws a single frame of the simulation.

        Args:
            screen (pygame.Surface): The pygame screen surface to draw on.
            entities (List[Entity]): The list of entities to draw.
            map Dict(MapArray): The maps.

        Returns:
            None
        """

        # Draw to the screen
        screen.fill((255, 255, 255))

        # draw dat map
        self.draw_map(screen=screen, map=simulation.sim_maps[AltitudeMap])
        self.draw_map(
            screen=screen,
            map=simulation.sim_maps[AntLocationPheremone],
            colormap="autumn",
            show_zero=False,
            alpha=100,
        )

        # self.draw_map(screen=screen, map=simulation.meta_maps["AltitudeAntLocation"], colormap='autumn')

        # Draw items
        self.draw_items(screen=screen, items=simulation.sim_items)

        # Draw dem ants
        self.draw_entities(screen=screen, entities=simulation.sim_entities)

        # Draw fps
        # Disabled as text doesn't seem to work...
        # self.draw_fps(screen=screen, clock=clock)

        # Update the display
        pygame.display.flip()

    def draw_entities(self, screen: pygame.Surface, entities: List[Entity]):
        """
        Draw a list of entities on the given Pygame screen.

        Args:
            screen (pygame.Surface): The Pygame screen to draw the entities on.
            entities (List[Entity]): A list of Entity objects to draw.

        Returns:
            None
        """

        for entity in entities:
            pygame.draw.circle(screen, (0, 0, 0), entity.pos.coords, radius=1)

    def draw_items(self, screen: pygame.Surface, items: List[Item]):
        """
        Draw a list of entities on the given Pygame screen.

        Args:
            screen (pygame.Surface): The Pygame screen to draw the entities on.
            items (List[Item]): A list of Item objects to draw.

        Returns:
            None
        """

        for item in items:
            pygame.draw.circle(screen, (200, 50, 0), item.pos.coords, radius=3)

    def draw_map(
        self,
        screen: pygame.Surface,
        map: MapArray,
        colormap: str = "terrain",
        show_zero: bool = True,
        alpha: int = None,
    ) -> None:
        """
        This function takes a Pygame screen and a MapArray object, and
        draws the map represented by the MapArray on the screen
        using a terrain colormap.

        Args:
            screen (pygame.Surface): The Pygame surface to draw the map on.
            map (MapArray): The MapArray object representing the map to be drawn.
            colormap (str): The Matplotlib colormap to be used to draw the map.

        Returns:
            None.
        """

        # Create a 2D array with terrain colormap
        terrain = plt.get_cmap(colormap)(np.linspace(0, 1, 256))[:, :3] * 255
        terrain = terrain.astype(np.uint8)

        values = map.normalised_values

        # Convert the noise array to a 2D array of color indices
        color_indices = (values * (len(terrain) - 1)).astype(np.int32)

        # Create the terrain image using the color indices
        terrain_image = terrain[color_indices]

        # Convert the terrain image to a pygame surface
        terrain_surface = pygame.surfarray.make_surface(terrain_image)

        # Scale the terrain surface to fit the screen
        # terrain_surface = pygame.transform.scale(terrain_surface, screen.get_size())

        if not show_zero:
            terrain_surface.set_colorkey(terrain[0])

        terrain_surface.set_alpha(alpha)

        # Blit the terrain surface onto the screen
        screen.blit(terrain_surface, (0, 0))

    def draw_fps(self, screen: pygame.Surface, clock: pygame.time.Clock):
        font = pygame.font.Font("freesansbold.ttf", 18)
        fps = str(int(self.clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
        return fps_text
