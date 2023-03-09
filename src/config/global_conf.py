import attrs


@attrs.define
class GlobalConfig:
    scrn_ht: int = 600
    scrn_wdt: int = 800
    headless: bool = True

    framerate = 240
    print_fps_every = 25
    draw_frame_every = 1

    update_colormap_image_every = 50


gconf = GlobalConfig()
