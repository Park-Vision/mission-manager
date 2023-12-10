from abc import ABC, abstractmethod
from datetime import datetime
import logging
import os

class Camera(ABC):
    def __init__(self) -> None:
        self.save_path = "./drone_photos/" + datetime.today().strftime(
            "%H:%M_%Y-%m-%d"
        )
        self.create_save_directory()

    def create_save_directory(self):
        """Create a directory to save photos, and a first line in a txt file with data"""
        try:
            os.makedirs(self.save_path)
        except:
            logging.error("Failed to create directory to save photos.")


    @abstractmethod
    async def take_photo(self) -> str:
        pass
