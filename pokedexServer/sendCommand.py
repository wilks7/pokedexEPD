import time
from display import display_pokemon, DisplayParameters
import socket
from DisplayCommand import DisplayCommandHandler

class PokemonDisplaySender(DisplayCommandHandler):
    def __init__(self, ip: str, port: int, display_params: DisplayParameters):
        super().__init__()
        self.ip = ip
        self.port = port
        self.display_params = display_params
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        try:
            self.socket.connect((self.ip, self.port))
            print(f"Connected to {self.ip}:{self.port}")
        except Exception as e:
            print(f"Failed to connect to {self.ip}:{self.port}, Error: {e}")

    def send_pokemon_image(self):
        # Use the display_pokemon function to get the image
        img = display_pokemon(
            self.display_params.resolution,
            self.display_params.pokedex_entry,
            self.display_params.generation,
            self.display_params.version,
            self.display_params.variant
        )
        if img:
            self.clear_screen(self.socket, 15)
            time.sleep(1)
            self.draw_image(self.socket, 0, 0, img)
            time.sleep(1)

    def close(self):
        self.socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    import argparse
    from display import Gen1Parameters

    parser = argparse.ArgumentParser(description="Send a command or start a command server.")
    
    # Arguments for manual sending
    parser.add_argument("--ip", type=str, help="The IP address of the display.")
    parser.add_argument("--resolution", type=str, default="1872x1404")
    parser.add_argument("--generation", type=int, default=1)
    parser.add_argument("--version", type=str, default="red-blue")
    parser.add_argument("--pokemon", type=int, default=25)
    parser.add_argument("--variant", type=str, default=None)

    # Argument for running as a server
    parser.add_argument("--port", type=int, default=8319, help="The port to listen on.")

    args = parser.parse_args()

    # Run as a manual command sender
    if not args.ip:
        print("Error: --ip is required.")
        exit(1)
    
    resolution = tuple(map(int, args.resolution.split('x')))
    params = DisplayParameters(
        resolution=resolution,
        generation=args.generation,
        version=args.version,
        pokedex_entry=args.pokemon,
        variant=args.variant
    )

    # params = Gen1Parameters(resolution=resolution, pokedex_entry=args.pokemon)
    
    sender = PokemonDisplaySender(args.ip, args.port, params)
    sender.send_pokemon_image()
    sender.close()