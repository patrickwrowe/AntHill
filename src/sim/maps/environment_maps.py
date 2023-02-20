from __future__ import annotations

import attrs
import matplotlib.pyplot as plt
import numpy as np
from noise import pnoise2

from src.config.sim_conf import sconf
from src.sim.datatypes import items, maps


@attrs.define
class TemperatureMap(maps.MapArray):
    @classmethod
    def new_map(cls) -> TemperatureMap:
        # For example, initalise a map over the simulation with a
        # default temperature of 298K.
        values = sconf.init_temp * np.ones(
            (sconf.default_map_resolution_x, sconf.default_map_resolution_y)
        )

        return cls(values=values)


@attrs.define
class AltitudeMap(maps.MapArray):
    @classmethod
    def new_map(cls) -> AltitudeMap:
        values = AltitudeMap.perlin_noise_2d(
            shape=(sconf.default_map_resolution_x, sconf.default_map_resolution_y)
        )

        return cls(values=values)

    @staticmethod
    def perlin_noise_2d(
        shape,
        octaves=sconf.perlin_num_octaves,
        persistence=sconf.perlin_persistence,
        lacunarity=sconf.perlin_lacunarity,
        seed=sconf.perlin_random_seed,
    ):
        """Generates 2D Perlin noise with given shape and parameters."""

        if seed is not None:
            np.random.seed(seed)

        rows, cols = shape
        x = np.linspace(0, sconf.perlin_scale_x, num=cols, endpoint=False)
        y = np.linspace(0, sconf.perlin_scale_y, num=rows, endpoint=False)
        xv, yv = np.meshgrid(x, y, indexing="ij")
        noise_arr = np.zeros(shape)
        for o in range(octaves):
            octave_factor = persistence**o
            frequency = lacunarity**o
            scaled_x = xv * frequency
            scaled_y = yv * frequency

            if seed is not None:
                # Add random offsets to the input coordinates for each octave
                offset_x = np.random.uniform(-1000, 1000)
                offset_y = np.random.uniform(-1000, 1000)
                scaled_x += offset_x
                scaled_y += offset_y

            # The "noise" library is using C and wants you to check on a per-sample
            # Basis. Use np.vectorize to get a version of the function which
            # lets you pass numpy arrays instead of sets of floats.
            noise_arr += np.vectorize(pnoise2)(scaled_y, scaled_x).T * octave_factor

        return noise_arr
