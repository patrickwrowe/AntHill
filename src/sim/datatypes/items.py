from __future__ import annotations

import attrs

from src.sim.datatypes import SimPos


@attrs.define
class Item:
    """Base class for non-sentient
    collectible items in the sim.

    Attributes:
        pos (SimPos): The position of the item
    """

    pos: SimPos


@attrs.define
class Consumable(Item):
    """Base class for an item which
    is consumable, e.g. pheremones and food."""

    supply: float = attrs.field(validator=attrs.validators.ge(0.0))

    def withdraw(self, quant):
        """Food has a finite supply"""
        # If there's nothing to withdraw, do nothing
        if self.supply == 0.0:
            return 0.0
        # If there's only a small amount left,
        # Withdraw what can be withdrawn
        elif quant > self.supply:
            residual = self.supply
            self.supply = 0.0
            return residual
        # Else, withdraw everything
        else:
            self.supply -= quant
            return quant

    def deposit(self, quant):
        self.supply += quant
