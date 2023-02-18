from __future__ import annotations
import attrs
import pygame

from typing import List

@attrs.define
class EventHandler:

    def handle_events(self) -> List[AntHillEvent]:
        
        events = []

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events.append(CloseEvent)

        return tuple(events)

@attrs.define
class AntHillEvent:
    ...

@attrs.define
class CloseEvent(AntHillEvent):
    ...