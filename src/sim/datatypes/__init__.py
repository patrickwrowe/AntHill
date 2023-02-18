import attr
from typing import Tuple


@attr.define
class SimPos:
    x: float
    y: float

    @property
    def coords(self) -> Tuple:
        return tuple(self.x, self.y)
