import asyncio
import enum
import json
import time
from dataclasses import asdict

from albatros.copter import Copter
from albatros.enums import CopterFlightModes
from albatros.nav.position import PositionGPS, distance_between_points
from transitions.extensions.asyncio import AsyncMachine

from manager.config import PHOTO_ALTITUDE
from manager.mission.mission import Mission, MissionStatus
from manager.mission.path import create_path
from manager.mission.waypoint import Waypoint, process_parking_message
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
        self.waypoints = []

        if self.use_kafka:
            command_callbacks = {
                "start": self.handle_start,
                "stop": self.handle_stop,
            }
            self.kafka_connection = KafkaConnector("localhost:9092", command_callbacks)

    def handle_start(self, msg: dict):
        """ "React to 'start' signal sent from operator - ready for takeoff"""
        self.waypoints = process_parking_message(msg)

        self.ready_for_takeoff = True

    def handle_stop(self, msg: dict):
        """React to 'stop' signal sent from operator - immediately return home"""
        self.to_RETURN()

    def send_mission_stage(self):
        """Send current stage enum value to broker"""
        if self.use_kafka:
            message = {"type": "stage", "stage": int(self.state.value)}
            self.kafka_connection.send_one(json.dumps(message))

    async def fly_to_single_point(self, waypoint: Waypoint) -> None:
        # because mavlink sends coordinates in scaled form as integers
        # we use function which scales WGS84 coordinates by 7 decimal places (degE7)
        target = PositionGPS.from_float_position(lat=waypoint.position[0], lon=waypoint.position[1], alt=PHOTO_ALTITUDE)

        self.albatros_copter.fly_to_gps_position(target.lat, target.lon, target.alt)

        while True:
            current_position = self.albatros_copter.get_corrected_position()
            dist = distance_between_points(current_position, target)

            print(f"Distance to target: {dist} m")
            if dist < 0.25: # tolerance
                return
            await asyncio.sleep(1)


    async def process_arducopter_messages(self):
        while True:
            self.send_mission_stage()
            # TODO real implementation - implement albatros

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
        self.waypoints.insert(0, self.home_point)
        self.path = create_path(self.waypoints)
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
        self.send_mission_stage()

        for waypoint in self.waypoints:
            await self.fly_to_single_point(waypoint)

        await self.to_RETURN()


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

        self.ready_for_takeoff = False
        await self.to_PREPARE()
