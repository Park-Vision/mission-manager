from manager.decision.decision import Decision
from manager.mission.waypoint import Waypoint
from manager.decision.camera.mock_camera import MockCamera

class DetectorDecision(Decision):
    """Makes the decision if the parking spot is free or taken based on visual object detection"""

    def __init__(self) -> None:
        super().__init__()
        self.camera = MockCamera()
    
    async def decide(self, wp: Waypoint):
        spot_free = True
        photo_path = await self.camera.take_photo()

        self.free_spots.append({"parking_spot_id": wp.spot_id, "occupied": spot_free})
