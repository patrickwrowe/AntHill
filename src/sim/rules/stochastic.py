from typing import List, Tuple

import numpy as np

from src.config.sim_conf import sconf
from src.sim.datatypes import SimPos, entities, maps


def random_move(sim_entities: List[entities.Entity]):
    """Moves entities randomly, with no care for
    any of the rules or regulations in the world,
    except for the boundaries of the known universe."""

    for entity in sim_entities:
        entity.pos.update_pos((np.random.uniform(-1, 1), np.random.uniform(-1, 1)))


def metropolis_monte_carlo(
    sim_entites: List[entities.Entity], potential: maps.MapArray
):
    """
    Moves entities according to the Metropolis Monte Carlo
    algorithm.
    """

    for entity in sim_entites:
        for i in range(sconf.mmc_max_attempts):
            move, accepted = metropolis_move(potential=potential, pos=entity.pos)
            if accepted:
                entity.pos.update_pos(move)


def metropolis_move(
    potential: maps.MapArray,
    pos: SimPos,
    temperature: float = sconf.mmc_move_temp,
    move_size=sconf.mmc_move_size,
) -> Tuple[Tuple[float, float], bool]:
    """Performs a Metropolis Monte Carlo move on an underlying potential.

    Args:
        potential (ndarray): A 2D NumPy array specifying the underlying potential.
        pos (SimPos): The position of the entity to be moved according to MMC.
        temperature (float): The temperature parameter.
        move_size (float): The size of the move.

    Returns:
        x_new (float): The x-coordinate of the new position.
        y_new (float): The y-coordinate of the new position.
        accepted (bool): True if the move was accepted, False otherwise.
    """

    # Generate a random displacement vector
    move = tuple(move_size * np.random.randn(2))

    # Compute the new position
    # Generate a new SimPos object to see if the move would be accepted
    pos_new = SimPos(x=pos.x, y=pos.y)
    pos_new.update_pos(move)

    # Compute the change in potential energy
    delta_energy = (
        potential.normalised_values[int(pos_new.y), int(pos_new.x)]
        - potential.normalised_values[int(pos.y), int(pos.x)]
    )

    # Accept or reject the move based on the Metropolis criterion
    if delta_energy <= 0 or np.random.rand() < np.exp(-delta_energy / temperature):
        accepted = True
    else:
        accepted = False

    return move, accepted
