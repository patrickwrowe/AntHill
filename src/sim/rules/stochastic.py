from src.sim.datatypes import entities

from typing import List

import numpy as np

def random_move(sim_entities: List[entities.Entity]):
    """Moves entities randomly, with no care for
    any of the rules or regulations in the world,
    except for the boundaries of the known universe."""

    for entity in sim_entities:
        entity.pos.update_pos((np.random.uniform(-1, 1),
                               np.random.uniform(-1, 1)))