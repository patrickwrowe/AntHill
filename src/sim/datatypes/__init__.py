from typing import Tuple

import attr

from src.config.sim_conf import sconf

import numba

@attr.define
class SimPos:
    x: float
    y: float

    vec: Tuple[float, float] = (0, 0)

    @property
    def coords(self) -> Tuple:
        return (self.x, self.y)

    def update_pos(self, vec: Tuple[float, float]) -> None:
        self.x, self.y, self.vec = _update_pos(x = self.x, y = self.y, vec = vec, boundary_x=sconf.default_map_resolution_x, boundary_y=sconf.default_map_resolution_y)

@numba.jit
def _update_pos(x: float, y: float, vec: Tuple[float, float], boundary_x: int, boundary_y: int) -> Tuple[float, float]:
    """Update the position and the direction vector based on the move."""

    old_x, old_y = x, y
    x = _update_coord(x, vec[0], boundary_x)
    y = _update_coord(y, vec[1], boundary_y)
    vec = (x - old_x, y - old_y)

    return x, y, vec

@numba.jit
def _update_coord(
    val: float, step: float, boundary: int
) -> Tuple[float, bool]:
    """Update the coordinates with some vector"""

    boundary -= 1

    newpos = val + step

    if 0 <= newpos <= boundary:
        return newpos
    elif newpos < 0:
        return 0
    elif newpos > boundary:
        return boundary
    else:
        return None