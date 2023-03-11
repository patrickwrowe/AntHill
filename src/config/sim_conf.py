import attrs


@attrs.define
class SimConf:
    # Initial simulation settings.
    init_num_basic_ants: int = 500
    init_num_basic_food: int = 20

    # Simulation dimensions are not locked
    # To the screen dimensions.
    sim_x: int = 800
    sim_y: int = 600

    # Basic parameters
    item_collect_dist = 5
    drain_item_scale_mod = 2

    # Types of simulation moves to make when
    # Updating the simulation state
    brownian_motion: bool = False
    mmc_move: bool = True

    # Settings for specific movement rules
    # Metropolis Monte-Carlo
    # *2 here for optimisation purposes
    mmc_move_size: float = 2.0 * 2
    mmc_move_temp: float = 0.003
    mmc_max_attempts: int = 5

    # Pheremone Settings
    init_found_food_pheremone_level: float = 100.0
    init_location_pheremone_level: float = 100.0
    withdraw_pheremones_every: int = 25
    pheremone_withdraw_quant: float = 0.01
    pheremone_map_gauss_sigma: float = 0.5

    # Food Settings
    max_basic_food_supply: float = 100.0
    min_basic_food_supply: float = 10

    # item settings
    withdraw_items_every: int = 500
    item_withdraw_quant: float = 0.01

    # Default map resolution
    default_map_resolution_x = sim_x
    default_map_resolution_y = sim_y

    # misc maps
    recompose_submaps_every: int = 30

    # Environmental Variables
    init_temp: int = 298

    # Altitude
    # Settings for good looking map
    perlin_num_octaves: int = 20
    perlin_persistence: float = 0.5  # 0.7
    perlin_lacunarity: float = 2.5
    perlin_random_seed: int = 4
    perlin_scale_x: int = 3
    perlin_scale_y: int = perlin_scale_x

    # Smoothin' good for debugging
    perlin_gauss_sigma: float = 1.0

    # Good for easy testing of moves - nice n' smooth.
    # perlin_num_octaves: int = 1
    # perlin_persistence: float = 0.5  # 0.7
    # perlin_lacunarity: float = 2
    # perlin_random_seed: int = 101


sconf = SimConf()
