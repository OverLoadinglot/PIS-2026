from abc import ABC, abstractmethod


class EventPublisher(ABC):
    @abstractmethod
    def publish_all(self, events):
        raise NotImplementedError
