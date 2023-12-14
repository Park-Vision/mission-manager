import argparse
import asyncio

from manager import config
from manager.drone import Drone


async def run_mission():
    await drone.process_arducopter_messages()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Drone mission manager")
    parser.add_argument("--kafka", action="store_true")
    parser.add_argument("--no-kafka", dest="kafka", action="store_false")
    parser.set_defaults(kafka=True)

    # Drone id, key and altitude can be specified in command line, but when not specified use default values from file
    parser.add_argument('--id', nargs='?', default=config.DRONE_ID)
    parser.add_argument('--key', nargs='?', default=config.DRONE_KEY)
    parser.add_argument('--altitude', nargs='?', default=config.PHOTO_ALTITUDE)

    args = parser.parse_args()

    print(f"Mission manager starting - kafka {args.kafka}")
    drone = Drone(args)

    if args.kafka:
        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(
                drone.process_arducopter_messages(),
                drone.to_PREPARE(),
                drone.kafka_connection.consume_messages(),
            )
        )
    else:
        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(
                drone.process_arducopter_messages(),
                drone.to_PREPARE(),
            )
        )
