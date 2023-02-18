from __future__ import annotations
import attrs
import pygame

from typing import List, Tuple

HEIGHT = 600
WIDTH = 800

@attrs.define
class EventHandler:

    def handle_events(self) -> List[AntHillEvent]:
        
        events = []

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events.append(CloseEvent())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if 0 <= mouse_pos[0] < HEIGHT and 0 <= mouse_pos[1] < WIDTH:
                        events.append(MouseClickEvent(mouse_pos))

        return tuple(events)

@attrs.define
class AntHillEvent:
    ...

@attrs.define
class CloseEvent(AntHillEvent):
    ...

@attrs.define
class MouseClickEvent(AntHillEvent):
    click_location: Tuple[int, int]