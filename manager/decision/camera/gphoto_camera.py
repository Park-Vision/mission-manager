from datetime import datetime
import logging
import os

from manager.decision.camera.camera import Camera


class GphotoCamera(Camera):
    """Handles camera using gphoto2 software"""
    def __init__(self, x: str) -> None:
        super().__init__()
    
    async def take_photo(self) -> str:
        img_name_with_second = f"{datetime.today().strftime("%H:%M:%S")}.jpg"
        image_path = f"{self.save_path}/{img_name_with_second}"

        os.system(
            f"gphoto2 --trigger-capture --wait-event-and-download=FILEADDED --filename {image_path}"
        )
        logging.debug(f"Photo taken to: {image_path}")

        return image_path
