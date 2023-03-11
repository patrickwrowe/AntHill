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
            simulation = self.simulation.update_sim()

            # print the fps
            if main_ticks % gconf.print_fps_every == 0:
                print(f"## Info: Step: {main_ticks} ##")
                print(f"FPS: {self.pg_setup.clock.get_fps()}")
                print(f"Ants with food: {len(simulation.entity_lists['ants_with_food'])}")
                print(f"Ants without food: {len(simulation.entity_lists['ants_without_food'])}")
                print(f"Drain/Cache food level: {simulation.sim_drain.supply}")

            if main_ticks % gconf.draw_frame_every == 0:
                self.artist.draw_frame(
                    screen=self.pg_setup.screen,
                    clock=self.pg_setup.clock,
                    simulation=simulation,
                )

            # Control the frame rate
            self.pg_setup.clock.tick(gconf.framerate)

            main_ticks += 1

        # Quit Pygame
        shutdown.exit_anthill()


if __name__ == "__main__":
    anthill = AntHill.setup_anthill()
    anthill.run_anthill()
