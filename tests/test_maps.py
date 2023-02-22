import numpy as np
import pytest

from src.config.sim_conf import sconf
from src.sim.datatypes import SimPos, items, entities
from src.sim.datatypes.maps import MapArray
from src.sim.maps.consumables_maps import ConsumableMap
from src.sim.maps.environment_maps import AltitudeMap

# Overwrite to ensure test environment is correct
sconf.perlin_num_octaves = 20
sconf.perlin_persistence = 0.5
sconf.perlin_lacunarity = 2.5
sconf.perlin_random_seed = 101


def test_new_map():
    with pytest.raises(NotImplementedError):
        MapArray.new_map()


def test_normalised_values():
    # Test with all positive values
    values = np.array([[1, 2], [3, 4]])
    map_array = MapArray(values)
    assert np.allclose(
        map_array.normalised_values, np.array([[0, 0.33333333], [0.66666667, 1]])
    )

    # Test with all negative values
    values = np.array([[-1, -2], [-3, -4]])
    map_array = MapArray(values)
    assert np.allclose(
        map_array.normalised_values, np.array([[1, 0.66666667], [0.33333333, 0]])
    )

    # Test with a mix of positive and negative values
    values = np.array([[1, -2], [3, -4]])
    map_array = MapArray(values)
    assert np.allclose(
        map_array.normalised_values, np.array([[0.71428571, 0.28571429], [1, 0]])
    )

    # Test with a zero array
    values = np.zeros((2, 2))
    map_array = MapArray(values)
    assert np.allclose(map_array.normalised_values, values)

    # one more pass
    values = np.array([[10, 4], [20, 0]])
    map_array = MapArray(values=values)

    # Test that the normalised values are between 0 and 1
    norm_values = map_array.normalised_values
    assert np.all(norm_values >= 0) and np.all(norm_values <= 1)

    # Test that the minimum value in the normalised array is 0
    assert np.min(norm_values) == 0

    # Test that the maximum value in the normalised array is 1
    assert np.max(norm_values) == 1

    # Test that the values are correctly normalised
    assert np.allclose(norm_values, np.array([[0.5, 0.2], [1, 0]]))


def test_new_map():
    consumable = items.Consumable(pos=SimPos(x=0, y=0), supply=10)
    map_array = ConsumableMap.new_map(consumable)

    # Check that the map has the expected shape and type
    assert isinstance(map_array, MapArray)
    assert map_array.values.shape == (
        sconf.default_map_resolution_x,
        sconf.default_map_resolution_y,
    )

    # Check that the consumable attribute is set correctly
    assert map_array.consumable == consumable

    # Check that all values in the map are zero
    assert np.allclose(
        map_array.values,
        np.zeros((sconf.default_map_resolution_x, sconf.default_map_resolution_y)),
    )

    # check withdrawing from the consumable map
    entity_list = [entities.Entity(pos=SimPos(10, 10),
                                   consumables={items.Consumable: items.Consumable(pos=SimPos(x=0, y=0), supply=11)}),
                    entities.Entity(pos=SimPos(15, 15),
                                    consumables={items.Consumable: items.Consumable(pos=SimPos(x=0, y=0), supply=10)})
                   ]

    # Test withdrawing one from each entity
    withdrawn_map = map_array.withdraw_from_entities(withdraw_entities=entity_list, value=1.0)
    assert withdrawn_map.sum() == 2.0
    assert entity_list[0].consumables[items.Consumable].supply == 10.0
    assert entity_list[1].consumables[items.Consumable].supply == 9.0
    assert map_array.values.sum() == 2.0
    assert map_array.values[int(entity_list[0].pos.x)][int(entity_list[0].pos.y)] == 1.0
    assert map_array.values[int(entity_list[1].pos.x)][int(entity_list[1].pos.y)] == 1.0


    # Test withdrawing the remaining 9 from one
    withdrawn_map = map_array.withdraw_from_entities(withdraw_entities=entity_list, value=9.0)
    assert withdrawn_map.sum() == 18.0
    assert entity_list[0].consumables[items.Consumable].supply == 1.0
    assert entity_list[1].consumables[items.Consumable].supply == 0.0
    assert map_array.values.sum() == 20.0
    assert map_array.values[int(entity_list[0].pos.x)][int(entity_list[0].pos.y)] == 10.0
    assert map_array.values[int(entity_list[1].pos.x)][int(entity_list[1].pos.y)] == 10.0

    # Test withdrawing the remaining one more
    withdrawn_map = map_array.withdraw_from_entities(withdraw_entities=entity_list, value=1.0)
    assert withdrawn_map.sum() == 1.0
    assert entity_list[0].consumables[items.Consumable].supply == 0.0
    assert entity_list[1].consumables[items.Consumable].supply == 0.0
    assert map_array.values.sum() == 21.0
    assert map_array.values[int(entity_list[0].pos.x)][int(entity_list[0].pos.y)] == 11.0
    assert map_array.values[int(entity_list[1].pos.x)][int(entity_list[1].pos.y)] == 10.0

    # Test withdrawing the remaining one more
    withdrawn_map = map_array.withdraw_from_entities(withdraw_entities=entity_list, value=1.0)
    assert withdrawn_map.sum() == 0.0
    assert entity_list[0].consumables[items.Consumable].supply == 0.0
    assert entity_list[1].consumables[items.Consumable].supply == 0.0
    assert map_array.values.sum() == 21.0
    assert map_array.values[int(entity_list[0].pos.x)][int(entity_list[0].pos.y)] == 11.0
    assert map_array.values[int(entity_list[1].pos.x)][int(entity_list[1].pos.y)] == 10.0

@pytest.fixture
def altitude_map():
    return AltitudeMap.new_map()


def test_new_altitude_map(altitude_map):
    assert isinstance(altitude_map, AltitudeMap)
    assert altitude_map.values.shape == (
        sconf.default_map_resolution_x,
        sconf.default_map_resolution_y,
    )


def test_perlin_noise_2d():
    shape = (100, 100)
    noise_arr = AltitudeMap.perlin_noise_2d(shape)

    assert isinstance(noise_arr, np.ndarray)
    assert noise_arr.shape == shape
    assert np.min(noise_arr) >= -1.0
    assert np.max(noise_arr) <= 1.0


def test_perlin_noise_2d_seed():
    shape = (100, 100)
    noise_arr1 = AltitudeMap.perlin_noise_2d(shape, seed=0)
    noise_arr2 = AltitudeMap.perlin_noise_2d(shape, seed=0)

    assert np.allclose(noise_arr1, noise_arr2)


def test_perlin_noise_2d_octaves():
    shape = (100, 100)
    noise_arr1 = AltitudeMap.perlin_noise_2d(shape, octaves=3)
    noise_arr2 = AltitudeMap.perlin_noise_2d(shape, octaves=5)

    assert not np.allclose(noise_arr1, noise_arr2)


def test_perlin_noise_2d_persistence():
    shape = (100, 100)
    noise_arr1 = AltitudeMap.perlin_noise_2d(shape, persistence=0.5)
    noise_arr2 = AltitudeMap.perlin_noise_2d(shape, persistence=0.9)

    assert not np.allclose(noise_arr1, noise_arr2)


def test_perlin_noise_2d_lacunarity():
    shape = (100, 100)
    noise_arr1 = AltitudeMap.perlin_noise_2d(shape, lacunarity=2.0)
    noise_arr2 = AltitudeMap.perlin_noise_2d(shape, lacunarity=4.0)

    assert not np.allclose(noise_arr1, noise_arr2)
