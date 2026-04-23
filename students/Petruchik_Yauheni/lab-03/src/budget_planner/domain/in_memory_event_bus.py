from typing import Dict, List, Callable
from ..domain.models.events import DomainEvent
from ..domain.ports.event_bus import EventBus

class InMemoryEventBus(EventBus):
    def __init__(self):
        self._handlers: Dict[type, List[Callable]] = {}

    def subscribe(self, event_type: type, handler: Callable[[DomainEvent], None]) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event: DomainEvent) -> None:
        event_type = type(event)
        for handler in self._handlers.get(event_type, []):
            handler(event)