import time
import argparse
from display import DisplayParameters
from sendCommand import PokemonDisplaySender

def run_generation_1(ip: str, port: int, resolution: tuple, version: str, variant: str = None, interval: int = 60):
    while True:
        for pokedex_entry in range(1, 152):  # Generation 1 entries: 1-151
            # Set the display parameters for the current entry
            params = DisplayParameters(
                resolution=resolution,
                generation=1,
                version=version,
                pokedex_entry=pokedex_entry,
                variant=variant
            )
            # Create a new PokemonDisplaySender instance for each entry
            sender = PokemonDisplaySender(ip, port, params)
            sender.send_pokemon_image()
            sender.close()
            # Wait for the specified interval before moving to the next entry
            time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send commands for Generation 1 Pokédex entries.")
    
    # Arguments for running generation 1
    parser.add_argument("--ip", type=str, help="The IP address of the display.")
    parser.add_argument("--resolution", type=str, default="1872x1404")
    parser.add_argument("--version", type=str, default="red-blue")
    parser.add_argument("--variant", type=str, default=None)
    parser.add_argument("--port", type=int, default=8319, help="The port to connect to.")
    parser.add_argument("--interval", type=int, default=60, help="Interval in seconds between each command.")

    args = parser.parse_args()

    # Run generation 1 sending commands
    if not args.ip:
        print("Error: --ip is required.")
        exit(1)
    
    resolution = tuple(map(int, args.resolution.split('x')))

    run_generation_1(args.ip, args.port, resolution, args.version, args.variant, args.interval)
