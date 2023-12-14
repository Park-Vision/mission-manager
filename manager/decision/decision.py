from abc import ABC, abstractmethod

from manager.mission.waypoint import Waypoint


class Decision(ABC):
    def __init__(self) -> None:
        self.free_spots = []

    @abstractmethod
    async def decide(self, wp: Waypoint) -> bool:
        pass
