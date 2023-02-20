from __future__ import annotations
import numpy as np
import attrs
import functools

@attrs.define(slots=False)
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

    @functools.cached_property 
    def normalised_values(self):
        # Scale the noise array to be between 0 and 1

        values = (self.values - np.min(self.values)) / (np.max(self.values) - np.min(self.values))
        values = np.nan_to_num(values, 0)

        return values