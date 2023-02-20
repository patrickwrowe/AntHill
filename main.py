import attrs

from src import setup, shutdown
from src.config.global_conf import gconf
from src.interface import draw, events
from src.sim import sim


@attrs.define
class AntHill:
    system_setup: setup.SystemSetup
    pg_setup: setup.PGSetup
    event_handler: events.EventHandler
    artist: draw.Artist
    simulation: sim.AntHillSim

    @classmethod
    def setup_anthill(cls):
        """Set up the pygame environment required."""

        system_setup = setup.SystemSetup.system_setup()
        pg_setup = setup.PGSetup.pygame_setup(system_setup.root_dir)
        event_handler = events.EventHandler()
        artist = draw.Artist.from_config(pg_setup=pg_setup)
        simulation = sim.BasicAntHillSim.new_sim()

        return cls(
            system_setup=system_setup,
            pg_setup=pg_setup,
            event_handler=event_handler,
            artist=artist,
            simulation=simulation,
        )

    def run_anthill(self):
        main_ticks = 0

        # Main loop
        running = True
        while running:
            # print the fps
            if main_ticks % gconf.print_fps_every == 0:
                print(f"FPS: {self.pg_setup.clock.get_fps()}")

            # Get a tuple of AntHillEvents to begin the loop
            # These deal exclusively with user input
            ah_events = self.event_handler.handle_events()

            # Janky hack for now
            # Want to find an "elegant" way to do this
            # For now we're just wanting to close the window.
            for event in ah_events:
                if isinstance(event, events.CloseEvent):
                    running = False
                elif isinstance(event, events.MouseClickEvent):
                    print(
                        f"mouse clicked at {event.click_location[0]}, \
                          {event.click_location[1]}"
                    )

            # Update game state
            entities, items, map = self.simulation.update_sim()

            self.artist.draw_frame(
                screen=self.pg_setup.screen,
                clock=self.pg_setup.clock,
                entities=entities,
                items=items,
                map=map,
            )

            # Control the frame rate
            self.pg_setup.clock.tick(gconf.framerate)

            main_ticks += 1

        # Quit Pygame
        shutdown.exit_anthill()


if __name__ == "__main__":
    anthill = AntHill.setup_anthill()
    anthill.run_anthill()
