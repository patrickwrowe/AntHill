from __future__ import annotations
import numpy as np
import attrs

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
