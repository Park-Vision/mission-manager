import argparse
import asyncio

from manager.drone import Drone, DroneStates
from transitions.extensions.asyncio import AsyncMachine


async def run_mission():
    await drone.process_drone_messages()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Drone mission manager")
    parser.add_argument("--kafka", action="store_true")
    parser.add_argument("--no-kafka", dest="kafka", action="store_false")
    parser.set_defaults(kafka=True)

    args = parser.parse_args()

    print(f"Mission manager starting - kafka {args.kafka}")
    drone = Drone(args)
    state_machine = AsyncMachine(
        model=drone, states=DroneStates, initial=DroneStates.INITIAL
    )

    if args.kafka:
        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(
                drone.process_drone_messages(),
                drone.to_PREPARE(),
                drone.kafka_connection.consume_messages(),
            )
        )
    else:
        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(
                drone.process_drone_messages(),
                drone.to_PREPARE(),
            )
        )