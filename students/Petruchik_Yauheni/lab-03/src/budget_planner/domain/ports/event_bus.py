from abc import ABC, abstractmethod
from typing import Callable, List
from ..models.events import DomainEvent

class EventBus(ABC):
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        pass

    @abstractmethod
    def subscribe(self, event_type: type, handler: Callable[[DomainEvent], None]) -> None:
        pass