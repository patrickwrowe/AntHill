from typing import Tuple

import attr

from src.config.sim_conf import sconf

@attr.define
class SimPos:
    x: float
    y: float

    vec: Tuple[float, float] = (0, 0)

    @property
    def coords(self) -> Tuple:
        return (self.x, self.y)

    def update_pos(self, vec: Tuple[float, float]) -> None:
        """Update the position and the direction vector based on the move."""

        old_x, old_y = self.x, self.y
        self.x = self._update_coord(self.x, vec[0], sconf.sim_x)
        self.y = self._update_coord(self.y, vec[1], sconf.sim_y)
        self.vec = (self.x - old_x, self.y - old_y)

    def _update_coord(self, val, step, boundary):
        """Update the coordinates with some vector """
        newpos = val + step

        if 0 <= newpos <= boundary:
            return newpos
        elif newpos < 0:
            return 0
        elif newpos > boundary:
            return boundary
        else:
            raise ValueError(f"Entity has produced nonsensical new position: {newpos}")