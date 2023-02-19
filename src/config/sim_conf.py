import attrs


@attrs.define
class SimConf:

    # Initial simulation settings.
    init_num_basic_ants: int = 1000
    init_num_basic_food: int = 10

    # Simulation dimensions are not locked
    # To the screen dimensions.
    sim_x: int = 800
    sim_y: int = 600

    # Pheremone Settings
    init_found_food_pheremone_level: float = 0.0
    init_location_pheremone_level: float = 1.0

    # Food Settings
    max_basic_food_supply: float = 1.0
    min_basic_food_supply: float = 0.1

    # Default map resolution
    default_map_resolution_x = sim_x
    default_map_resolution_y = sim_y

    # Environmental Variables
    init_temp: int = 298

    # Altitude
    perlin_num_octaves: int = 5
    perlin_persistence: float = 0.5
    perlin_lacunarity: float = 2.0
    perlin_random_seed: int = 101

sconf = SimConf()
