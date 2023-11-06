import enum
import json
from dataclasses import asdict

import asyncio
from albatros.copter import Copter
from albatros.enums import CopterFlightModes

import config
from mission.path import create_path
from api_requests.api_requests import get_parking_spots
from mission.waypoint import process_parking_json
from telemetry.kafka_connection import KafkaConnector


class DroneStates(enum.Enum):
    INITIAL = 0
    PREPARE = 1
    READY = 2
    PATH = 3
    TAKEOFF = 4
    FLIGHT = 5
    RETURN = 6
    RAPORT = 7


class Drone(object):
    def __init__(self, args) -> None:
        self.path = None
        self.albatros_copter = Copter()
        self.use_kafka = args.kafka
        self.ready_for_takeoff = False
        if self.use_kafka:
            command_callbacks = {
                "start": self.handle_start,
                "stop": self.handle_stop,
            }
            self.kafka_connection = KafkaConnector('localhost:9092', command_callbacks)

    def handle_start(self):
        """"React to 'start' signal sent from operator - ready for takeoff"""
        self.ready_for_takeoff = True

    def handle_stop(self):
        """React to 'stop' signal sent from operator - immediately return home"""
        self.to_RETURN()

    async def process_drone_messages(self):
        # TODO real implementation - implement albatros
        while True:
            position = self.albatros_copter.get_corrected_position()
            # print(asdict(position))
            await asyncio.sleep(1)
            if self.use_kafka:
                self.kafka_connection.send_one(json.dumps(asdict(position)))

    async def on_enter_PREPARE(self):
        print("Drone initializing...")

        # wait for GPS signal - wrap synchronous function in executor, to avoid blocking
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.albatros_copter.wait_gps_fix)

        await self.to_READY()

    async def on_enter_READY(self):
        print("Drone ready, waiting for start signal")

        # wait for the operator to send start signal...
        while not self.ready_for_takeoff:
            await asyncio.sleep(1)

        # Received takeoff command
        await self.to_PATH()

    async def on_enter_PATH(self):
        # Create path from waypoints
        waypoints = process_parking_json(get_parking_spots(config.DRONE_ID))
        waypoints.insert(0, config.HOME_WAYPOINT)
        self.path = create_path(waypoints)
        await self.to_TAKEOFF()

    async def on_enter_TAKEOFF(self):
        # Takeoff to set altitude

        target_alt = 15
        # TODO probably fix asyncio here
        self.albatros_copter.arm()
        self.albatros_copter.takeoff(target_alt)
        while (
            current_altitude := self.albatros_copter.get_corrected_position().alt
        ) < target_alt - 0.25:  # tolerance
            print(f"Altitude: {current_altitude} m")
            await asyncio.sleep(1)

        # Target altitude was reached
        await self.to_FLIGHT()

    async def on_enter_FLIGHT(self):
        print("To be implemented")

    async def on_enter_RETURN(self):
        self.albatros_copter.set_mode(CopterFlightModes.RTL)

    async def on_enter_RAPORT(self):
        print("To be implemented")