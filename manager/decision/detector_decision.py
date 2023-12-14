from collections import namedtuple

from numpy import ndarray
from PIL import Image
from ultralytics import YOLO

from manager.decision.camera.camera import Camera
from manager.decision.decision import Decision
from manager.mission.waypoint import Waypoint
from manager import config

ImageDimensions = namedtuple("ImageDimensions", "width height center_x center_y")


class DetectorDecision(Decision):
    """Makes the decision if the parking spot is free or taken based on visual object detection"""

    def __init__(self, camera: Camera) -> None:
        super().__init__()
        self.camera = camera
        self.model = YOLO("yolov8n.pt")  # pretrained YOLOv8n model

    def visualize_result(result) -> None:
        """Draw boxes to image for testing purposes"""
        im_array = result.plot()
        im = Image.fromarray(im_array[..., ::-1])
        im.show()
        im.save("detection_result.jpg")

    def object_is_big(
        self, box_xyxy: ndarray, image_dimensions: ImageDimensions
    ) -> bool:
        """Returns true if detected object bounding box takes up defined proportion of screen"""
        return (
            abs(box_xyxy[0] - box_xyxy[2]) > image_dimensions.width * config.OBJECT_SIZE_PROPORTION_THRESHOLD_X
            and abs(box_xyxy[1] - box_xyxy[3]) > image_dimensions.height * config.OBJECT_SIZE_PROPORTION_THRESHOLD_Y
        )

    def object_is_central(self, box_xyxy: ndarray, image_dimensions: ImageDimensions) -> bool:
        """Returns true if object bounding box center is within a defined distance to img center"""
        return (
            abs(((box_xyxy[0] + box_xyxy[2]) / 2) - image_dimensions.center_x)
            < image_dimensions.width * config.PHOTO_CENTER_DISTANCE_THRESHOLD_X
            and abs(((box_xyxy[1] + box_xyxy[3]) / 2) - image_dimensions.center_y)
            < image_dimensions.height * config.PHOTO_CENTER_DISTANCE_THRESHOLD_Y
        )

    async def decide(self, wp: Waypoint) -> bool:
        """Decides if spot is taken. Sets result to attribute & returns"""
        spot_free = True
        photo_path = await self.camera.take_photo()

        with Image.open(photo_path) as image:
            image_width, image_height = image.size

        image_dimensions = ImageDimensions(
            image_width, image_height, image_width / 2, image_height / 2
        )

        results = self.model(photo_path)

        # Process results list
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                r = box.xyxy[0].astype(int)

                # Decide if detected object takes parking space
                # It has to be big enough and positioned in the center of image
                if self.object_is_big(r, image_dimensions) and self.object_is_central(
                    r, image_dimensions
                ):
                    spot_free = False

        # Draw picture with boxes for testing
        # self.visualize_result(result)

        self.free_spots.append(
            {"parking_spot_id": wp.spot_id, "occupied": not spot_free}
        )
        return not spot_free
