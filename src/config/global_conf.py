import attrs


@attrs.define
class GlobalConfig:
    scrn_ht: int = 600
    scrn_wdt: int = 800
    headless: bool = True

    framerate = 240
    print_fps_every = 25


gconf = GlobalConfig()
