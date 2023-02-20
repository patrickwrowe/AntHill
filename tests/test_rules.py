import pytest
import numpy as np

from src.sim.datatypes.entities import Entity
from src.sim.datatypes.maps import MapArray
from src.config.sim_conf import sconf
from src.sim.datatypes import SimPos
from src.sim.rules.stochastic import random_move, metropolis_monte_carlo, metropolis_move

def test_random_move():
    # Set up entities for testing
    entity1 = Entity(pos=SimPos(0, 0))
    entity2 = Entity(pos=SimPos(1, 1))
    entity3 = Entity(pos=SimPos(-1, -1))
    entities = [entity1, entity2, entity3]

    # Test that entities are moved randomly
    np.random.seed(0)
    random_move(entities)
    assert entity1.pos != SimPos(0, 0)
    assert entity2.pos != SimPos(1, 1)
    assert entity3.pos != SimPos(-1, -1)

def test_metropolis_move():

    # Create a test potential
    test_potential = MapArray(np.array([
        [1, 1, 1],
        [1, 2, 1],
        [1, 1, 1]
    ]))

    # Test moving to a neighboring cell with lower potential
    test_pos = SimPos(1, 1)
    move, accepted = metropolis_move(test_potential, test_pos, temperature=0.0, move_size=1)
    assert np.all(np.array(move) < 1)
    assert accepted == True

    # And at high temperature
    test_pos = SimPos(1, 1)
    move, accepted = metropolis_move(test_potential, test_pos, temperature=1.0, move_size=1)
    assert np.all(np.array(move) < 1)
    assert accepted == True

    # Test moving to a neighboring cell with higher potential

    # Create a test potential
    test_potential = MapArray(2 * np.ones((sconf.default_map_resolution_x, sconf.default_map_resolution_y)))

    center_x = int(sconf.default_map_resolution_x / 2)
    center_y = int(sconf.default_map_resolution_y / 2)

    test_potential.values[center_x, center_y] = 1

    test_pos = SimPos(center_x, center_y)
    for i in range(10):
        move, accepted = metropolis_move(test_potential, test_pos, temperature=0.0, move_size=1)
        assert np.all(np.array(move) < 1)

        # it might move around but it will never move to a place with a higher potential
        assert test_potential.values[int(test_pos.x), int(test_pos.y)] == 1

    # Test moving to a neighboring cell with higher potential -> At high temp this should pass
    test_pos = SimPos(center_x, center_y)
    move, accepted = metropolis_move(test_potential, test_pos, temperature=10, move_size=1)
    assert np.all(np.array(move) < 1)
    assert accepted == True

    # Test moving to a cell outside the boundaries of the potential
    test_pos = SimPos(center_x, center_y)
    move, accepted = metropolis_move(test_potential, test_pos, temperature=1, move_size=sconf.default_map_resolution_x * 100)
    assert test_pos.x < sconf.default_map_resolution_x
    assert test_pos.y < sconf.default_map_resolution_y

def test_metropolis_monte_carlo():

    # Test that the function runs without errors
    potential = MapArray(np.ones((10, 10)))
    sim_entities = [Entity(pos=SimPos(x=4, y=4))]
    metropolis_monte_carlo(sim_entites=sim_entities, potential=potential)

    # Test that entities have moved
    initial_positions = [entity.pos.coords for entity in sim_entities]
    metropolis_monte_carlo(sim_entites=sim_entities, potential=potential)
    final_positions = [entity.pos.coords for entity in sim_entities]
    assert initial_positions != final_positions