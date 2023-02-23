from __future__ import annotations

import functools

import attrs
import numba
import numpy as np


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

    # It would be great to find some way to cache this and then update it...
    # Doing so gains 20 fps...
    # @functools.lru_cache
    @property
    def normalised_values(self) -> np.ndarray:
        # Scale the noise array to be between 0 and 1

        values = (self.values - np.min(self.values)) / (
            np.max(self.values) - np.min(self.values)
        )
        values = np.nan_to_num(values, 0)
        return values
