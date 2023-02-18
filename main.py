import attrs
import pygame
import sys

from src.interface import events, draw
from src import setup, shutdown

@attrs.define
class AntHill:

    pgsetup: setup.PGSetup
    event_handler: events.EventHandler

    @classmethod
    def setup_anthill(cls):
        """Set up the pygame environment required."""

        pgsetup = setup.PGSetup.pygame_setup()
        event_handler = events.EventHandler()

        return cls(pgsetup, event_handler)

    def run_anthill(self):

        # Main loop
        running = True
        while running:
            
            # Events
            ah_events = self.event_handler.handle_events()

            # Janky hack for now
            # Probably want to find an "elegant" way to do this
            for event in ah_events:
                if isinstance(event, events.CloseEvent):
                    running = False
                elif isinstance(event, events.MouseClickEvent):
                    print(f"mouse clicked at {event.click_location[0]}, {event.click_location[1]}")

            # Update game state
            # ...

            draw.draw_frame(self.pgsetup.screen)

            # Control the frame rate
            self.pgsetup.clock.tick(60)

        # Quit Pygame
        shutdown.exit_anthill()

if __name__ == "__main__":
    
    anthill = AntHill.setup_anthill()
    anthill.run_anthill()
