from __future__ import annotations
import attrs

from src.config.sim_conf import sconf
from src.sim.datatypes import entities

@attrs.define
class Ant(entities.Entity):
    pheremones: AntPheremones

    @classmethod
    def basic_ant(cls) -> Ant:
        """Creates yer regular old basic ant"""
        pheremones = AntPheremones()

        # Lets just put the ants in the middle of the screen for now.
        init_pos = entities.EntityPos(sconf.sim_x/2, 
                                      sconf.sim_y/2)

        return cls(pos = init_pos, pheremones = pheremones)


# TODO: Move pheremones to datatypes.py as their own datatype
@attrs.define
class Pheremone:
    supply: float = attrs.field(validator=attrs.validators.ge(0.0))

    @classmethod
    def new_pheremone(cls):
        return cls(supply = 1.0)
    
    def withdraw_pheremone(self, quant):
        """Pheremones behave a bit like fixed amounts
        of liquid. They can be used or distributed but
        they are not in infinite supply."""

        # If there's nothing to withdraw, do nothing
        if self.supply == 0.0:
            return 0.0
        # If there's only a small amount left,
        # Withdraw what can be withdrawn
        elif quant > self.supply:
            residal = self.supply
            self.supply = 0.0
            return residal
        # Else, withdraw everything
        else:
            self.supply -= quant
            return quant
    
    def add_pheremone(self, quant):
        self.supply += quant

@attrs.define
class AntLocationPheremone(Pheremone):
    """ants leave pheremones where they have been."""
    ...

@attrs.define
class FoundFoodPheremone(Pheremone):
    """Pheremone is resupplied on finding food.
    
    Ants leave this trail to indicate to other ants
    where food has been found."""

    @classmethod
    def new_pheremone(cls):
        """Ants begin with no food pheremone."""
        return cls(supply = sconf.init_found_food_pheremone_level)

@attrs.define
class AntPheremones:
    location: AntLocationPheremone = AntLocationPheremone.new_pheremone()
    found_food: FoundFoodPheremone = FoundFoodPheremone.new_pheremone()