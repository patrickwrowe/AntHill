from __future__ import annotations

from typing import List

import attrs
import numpy as np

from src.config.sim_conf import sconf
from src.sim.datatypes import maps
import functools

@attrs.define
class MetaMap(maps.MapArray):
    """A metamap contains information on a number of 
    submaps. And provides a linear combination of these
    values as the result of its return value."""
    
    sub_maps: List[maps.MapArray]
    coefficients: List[float]

    @classmethod
    def new_map(cls, sub_maps: List[maps.MapArray], coefficients: List[float]) -> MetaMap:

        MetaMap.validate_submaps(sub_maps=sub_maps, coefficients=coefficients)
        values = MetaMap._compose_submaps(sub_maps=sub_maps, coefficients=coefficients)

        return cls(values = values, sub_maps = sub_maps, coefficients=coefficients)

    @staticmethod
    def validate_submaps(sub_maps: List[maps.MapArray], coefficients: List[float]) -> None:
        # Check that the maps all have the same shape.
        map_shapes = np.array([map.values.shape for map in sub_maps])
        assert all(map_shapes[:, 0] == map_shapes[0, 0])
        assert all(map_shapes[:, 1] == map_shapes[0, 1])
        assert len(coefficients) == len(sub_maps)

    @staticmethod
    def _compose_submaps(sub_maps: List[maps.MapArray], coefficients: List[float]):
        
        values = np.zeros(sub_maps[0].values.shape)

        for sub_map, coefficient in zip(sub_maps, coefficients):
            values += coefficient * sub_map.values
        
        return values

    def recompose_submaps(self):
        self.values = MetaMap._compose_submaps(sub_maps = self.sub_maps, coefficients = self.coefficients)
