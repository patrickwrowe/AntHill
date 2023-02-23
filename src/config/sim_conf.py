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

    # Types of simulation moves to make when
    # Updating the simulation state
    brownian_motion: bool = False
    mmc_move: bool = True

    # Settings for specific movement rules
    # Metropolis Monte-Carlo
    # *2 here for optimisation purposes
    mmc_move_size: float = 1.0 * 2
    mmc_move_temp: float = 0.03
    mmc_max_attempts: int = 5

    # Pheremone Settings
    init_found_food_pheremone_level: float = 0.0
    init_location_pheremone_level: float = 10.0
    withdraw_pheremones_every: int = 100
    pheremone_withdraw_quant: float = 0.01

    # Food Settings
    max_basic_food_supply: float = 1.0
    min_basic_food_supply: float = 0.1

    # Default map resolution
    default_map_resolution_x = sim_x
    default_map_resolution_y = sim_y

    # misc maps
    recompose_submaps_every: int = 100

    # Environmental Variables
    init_temp: int = 298

    # Altitude
    # Settings for good looking map
    perlin_num_octaves: int = 20
    perlin_persistence: float = 0.5  # 0.7
    perlin_lacunarity: float = 2.5
    perlin_random_seed: int = 101
    perlin_scale_x: int = 3
    perlin_scale_y: int = perlin_scale_x

    # Good for easy testing of moves - nice n' smooth.
    # perlin_num_octaves: int = 1
    # perlin_persistence: float = 0.5  # 0.7
    # perlin_lacunarity: float = 2
    # perlin_random_seed: int = 101


sconf = SimConf()
