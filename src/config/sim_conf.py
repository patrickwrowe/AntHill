import attrs


@attrs.define
class SimConf:
    # Initial simulation settings.
    init_num_basic_ants: int = 100
    init_num_basic_food: int = 10

    # Simulation dimensions are not locked
    # To the screen dimensions.
    sim_x: int = 800
    sim_y: int = 600

    # Types of simulation moves to make when
    # Updating the simulation state
    random_move: bool = True
    mmc_move: bool = False

    # Settings for specific movement rules
    # Metropolis Monte-Carlo
    mmc_move_size: float = 0.5
    mmc_move_temp: float = 0.0001
    mmc_max_attempts: int = 5

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
    # Settings for good looking map
    perlin_num_octaves: int = 20
    perlin_persistence: float = 0.5  # 0.7
    perlin_lacunarity: float = 2.5
    perlin_random_seed: int = 101

    # Good for easy testing of moves - nice n' smooth.
    # perlin_num_octaves: int = 1
    # perlin_persistence: float = 0.5  # 0.7
    # perlin_lacunarity: float = 2
    # perlin_random_seed: int = 101


sconf = SimConf()
