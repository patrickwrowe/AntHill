from __future__ import annotations
import attrs
import pygame

from typing import List, Tuple

from src.config.global_conf import gconf


@attrs.define
class EventHandler:
    def handle_events(self) -> List[AntHillEvent]:
        events = []

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events.append(self.handle_exit_event(event))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                events.append(self.handle_mouse_events(event))

        return tuple(events)

    @staticmethod
    def handle_mouse_events(event) -> AntHillEvent:
        if event.button == 1:  # left mouse button
            return MouseClickEvent.from_pygame_get_pos()
        else:
            return None

    @staticmethod
    def handle_exit_event(event) -> AntHillEvent:
        return CloseEvent()


@attrs.define
class AntHillEvent:
    ...


@attrs.define
class CloseEvent(AntHillEvent):
    ...


@attrs.define
class MouseClickEvent(AntHillEvent):
    click_location: Tuple[int, int]

    @classmethod
    def from_pygame_get_pos(cls):
        """returns a mouse click event if the mouse click is
        within the pygame screen"""

        click_location = pygame.mouse.get_pos()
        if (
            0 <= click_location[0] < gconf.scrn_ht
            and 0 <= click_location[1] < gconf.scrn_wdt
        ):
            return cls(click_location)
        else:
            return None
