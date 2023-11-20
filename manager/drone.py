import asyncio
import enum
import json
import time
from dataclasses import asdict

from albatros.copter import Copter
from albatros.enums import CopterFlightModes
from transitions.extensions.asyncio import AsyncMachine

from manager import config
from manager.api_requests.api_requests import get_parking_spots
from manager.mission.mission import Mission, MissionStatus
from manager.mission.path import create_path
from manager.mission.waypoint import Waypoint, process_parking_json
from manager.telemetry.kafka_connection import KafkaConnector


class DroneState(enum.Enum):
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
        self.state_machine = AsyncMachine(
            model=self, states=DroneState, initial=DroneState.INITIAL
        )
        self.path = None
        self.albatros_copter = Copter()
        self.use_kafka = args.kafka
        self.ready_for_takeoff = False
        self.home_point = Waypoint()
        self.mission = Mission()

        if self.use_kafka:
            command_callbacks = {
                "start": self.handle_start,
                "stop": self.handle_stop,
            }
            self.kafka_connection = KafkaConnector("localhost:9092", command_callbacks)

    def handle_start(self):
        """ "React to 'start' signal sent from operator - ready for takeoff"""
        self.ready_for_takeoff = True

    def handle_stop(self):
        """React to 'stop' signal sent from operator - immediately return home"""
        self.to_RETURN()

    def send_mission_stage(self):
        """Send current stage enum value to broker"""
        message = {"type": "stage", "stage": int(self.state.value)}
        print(message)
        self.kafka_connection.send_one(json.dumps(message))

    async def process_arducopter_messages(self):
        # TODO real implementation - implement albatros
        while True:
            position = self.albatros_copter.get_corrected_position()
            # print(asdict(position))
            await asyncio.sleep(0.5)
            if self.use_kafka:
                self.kafka_connection.send_one(json.dumps(asdict(position)))

    async def on_enter_PREPARE(self):
        print("Entered PREPARE")
        self.send_mission_stage()

        # wait for GPS signal - wrap synchronous function in executor, to avoid blocking
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.albatros_copter.wait_gps_fix)

        # Set home point which will be used as starting location
        starting_position = self.albatros_copter.get_corrected_position()
        self.home_point = Waypoint(
            lat=starting_position.lat * 1.0e-7, lon=starting_position.lon * 1.0e-7
        )

        # Ser ardupilot flight mode
        self.albatros_copter.set_mode(CopterFlightModes.GUIDED)

        await self.to_READY()

    async def on_enter_READY(self):
        print("Entered ready, waiting for start signal")
        self.send_mission_stage()

        # wait for the operator to send start signal...
        while not self.ready_for_takeoff:
            await asyncio.sleep(1)

        # Received takeoff command
        await self.to_PATH()

    async def on_enter_PATH(self):
        print("Entered PATH, creating optimal route")
        self.send_mission_stage()

        # Create path from waypoints
        waypoints = process_parking_json(get_parking_spots(config.DRONE_ID))
        waypoints.insert(0, self.home_point)
        self.path = create_path(waypoints)
        await self.to_TAKEOFF()

    async def on_enter_TAKEOFF(self):
        """Takeoff to set altitude"""
        print("Entered TAKEOFF")
        self.send_mission_stage()

        self.mission.start_timestamp = int(time.time())
        self.mission.status = MissionStatus.ONGOING

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
        print("Entered FLIGHT")
        await self.to_RETURN()
        self.send_mission_stage()

    async def on_enter_RETURN(self):
        print("Entered RETURN")
        self.send_mission_stage()

        self.albatros_copter.set_mode(CopterFlightModes.RTL)

        # Detect landing
        while (
            current_altitude := self.albatros_copter.get_corrected_position().alt
        ) > 0.25:  # tolerance
            print(f"Altitude: {current_altitude} m")
            await asyncio.sleep(1)

        # Landed
        self.mission.end_timestamp = int(time.time())
        self.mission.status = MissionStatus.FINISHED

        await self.to_RAPORT()

    async def on_enter_RAPORT(self):
        print("Entered RAPORT")
        self.send_mission_stage()

        mission_message = asdict(self.mission)
        mission_message["type"] = "missionResult"
        self.kafka_connection.send_one(json.dumps(mission_message))
