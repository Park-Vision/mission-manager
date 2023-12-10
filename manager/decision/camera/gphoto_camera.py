import logging
import os
from datetime import datetime

from manager.decision.camera.camera import Camera


class GphotoCamera(Camera):
    """Handles camera using gphoto2 software"""

    def __init__(self, x: str) -> None:
        super().__init__()

    async def take_photo(self) -> str:
        time_with_second = datetime.today().strftime("%H:%M:%S")
        img_name_with_second = f"{time_with_second}.jpg"
        image_path = f"{self.save_path}/{img_name_with_second}"

        os.system(
            f"gphoto2 --trigger-capture --wait-event-and-download=FILEADDED --filename {image_path}"
        )
        logging.debug(f"Photo taken to: {image_path}")

        return image_path
