import asyncio
import random

from manager.decision.decision import Decision
from manager.mission.waypoint import Waypoint


class MockDecision(Decision):
    """Randomizes the decision if the parking spot is free or taken"""

    def __init__(self) -> None:
        super().__init__()
    
    async def decide(self, wp: Waypoint):
        # simulate processing time
        await asyncio.sleep(1)
        self.free_spots.append({"parking_spot_id": wp.spot_id, "occupied": random.choice([True, False])})
