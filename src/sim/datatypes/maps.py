from __future__ import annotations
import numpy as np
import attrs
import matplotlib.pyplot as plt
import pygame

@attrs.define
class MapArray:
    """
    A map contains information about the tiling
    of the world in a 2D plane spanning the simulation
    cell.
    """

    values: np.ndarray

    @classmethod
    def new_map(cls) -> MapArray:
        raise NotImplementedError()

    @property
    def values_as_image(self):
        # Create a 2D array with terrain colormap
        terrain = plt.get_cmap('terrain')(np.linspace(0, 1, 256))[:, :3] * 255
        terrain = terrain.astype(np.uint8)

        values = self.normalised_values

        # Convert the noise array to a 2D array of color indices
        color_indices = (values * (len(terrain) - 1)).astype(np.int32)

        # Create the terrain image using the color indices
        terrain_image = terrain[color_indices]

        # Convert the terrain image to a pygame surface
        terrain_surface = pygame.surfarray.make_surface(terrain_image)

        return terrain_surface

    @property 
    def normalised_values(self):
        # Scale the noise array to be between 0 and 1
        return (self.values - np.min(self.values)) / (np.max(self.values) - np.min(self.values))