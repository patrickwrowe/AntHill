from typing import List, Tuple

import numba
import numpy as np
from numpy import exp
from numpy.random import rand

from src.config.sim_conf import sconf
from src.sim.datatypes import SimPos, entities, maps

_tmp_sim_pos = SimPos(0, 0)


def brownian_motion(sim_entities: List[entities.Entity]) -> None:
    """Moves entities randomly, with no care for
    any of the rules or regulations in the world,
    except for the boundaries of the known universe."""

    for entity in sim_entities:
        entity.pos.update_pos(
            (
                np.random.uniform(-sconf.mmc_move_size, sconf.mmc_move_size),
                np.random.uniform(-sconf.mmc_move_size, sconf.mmc_move_size),
            )
        )


def metropolis_monte_carlo(
    sim_entites: List[entities.Entity], potential: maps.MapArray
) -> None:
    """
    Moves entities according to the Metropolis Monte Carlo
    algorithm.

    Args:
        sim_entites (List[Entity]): A list of entities to be moved.
        potential (MapArray): The potential to be used to move entities
    Returns:
        None
    """

    for entity in sim_entites:
        accepted = False
        n_mmc_iter = 0

        while n_mmc_iter < sconf.mmc_max_attempts and accepted == False:
            move, accepted = metropolis_move(potential=potential, pos=entity.pos)
            n_mmc_iter += 1

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
    move = np.array(new_mmc_move(move_size=move_size))

    # Compute the new position
    # Generate a new SimPos object to see if the move would be accepted
    pos_new = _tmp_sim_pos
    pos_new.x, pos_new.y = pos.x, pos.y
    pos_new.update_pos(move)

    # Compute the change in potential energy
    # factoring this out with numba doesn't seem to help.
    # But we'll leave it as-is for profiling.
    delta_energy = mmc_delta_energy(
        potential=potential.values,
        pos_old=pos.coords,
        pos_new=pos_new.coords,
    )

    # Accept or reject the move based on the Metropolis criterion
    accepted = mmc_accept(delta_energy=delta_energy, temperature=temperature)

    return move, accepted

def inertial_metropolis_monte_carlo(
    sim_entites: List[entities.Entity], potential: maps.MapArray
) -> None:
    """
    Moves entities according to the Metropolis Monte Carlo
    algorithm.

    Args:
        sim_entites (List[Entity]): A list of entities to be moved.
        potential (MapArray): The potential to be used to move entities
    Returns:
        None
    """

    for entity in sim_entites:
        accepted = False
        n_mmc_iter = 0

        while n_mmc_iter < sconf.mmc_max_attempts and accepted == False:
            move, accepted = intertial_metropolis_move(potential=potential, pos=entity.pos)
            n_mmc_iter += 1

            if accepted:
                entity.pos.update_pos(move)


def intertial_metropolis_move(
    potential: maps.MapArray,
    pos: SimPos,
    temperature: float = sconf.mmc_move_temp,
    move_size: float = sconf.inertial_mmc_move_size,
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
    move = np.array(new_mmc_move(move_size=move_size))

    # Something like this produces more coherent motion
    # But is very expensive and probably breaks the metropolis
    # criterion.
    move = np.array(pos.vec) + (move / sconf.inertial_mass)
    move = move_size * move / np.linalg.norm(move)

    # Compute the new position
    # Generate a new SimPos object to see if the move would be accepted
    pos_new = _tmp_sim_pos
    pos_new.x, pos_new.y = pos.x, pos.y
    pos_new.update_pos(move)

    # Compute the change in potential energy
    # factoring this out with numba doesn't seem to help.
    # But we'll leave it as-is for profiling.
    delta_energy = mmc_delta_energy(
        potential=potential.values,
        pos_old=pos.coords,
        pos_new=pos_new.coords,
    )

    # Accept or reject the move based on the Metropolis criterion
    accepted = mmc_accept(delta_energy=delta_energy, temperature=temperature)

    return move, accepted


@numba.jit
def mmc_accept(delta_energy: float, temperature: float) -> bool:
    return delta_energy <= 0 or rand() < exp(-delta_energy / temperature)


@numba.jit
def mmc_delta_energy(
    potential: np.ndarray, pos_old: Tuple[float, float], pos_new: Tuple[float, float]
):
    return (
        potential[int(pos_new[0]), int(pos_new[1])]
        - potential[int(pos_old[0]), int(pos_new[1])]
    )


@numba.jit
def new_mmc_move(move_size: float) -> Tuple[float, float]:
    return move_size * (rand(2) - 0.5)
