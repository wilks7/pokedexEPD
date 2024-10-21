import socket
from DisplayCommand import DisplayCommandHandler
from threading import Thread
from display import display_pokemon, DisplayParameters
import time

class CommandServer(DisplayCommandHandler):
    def __init__(self, port: int):
        super().__init__()
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', self.port))  # Bind to all available IP addresses
        self.server_socket.listen(1)
        self.pokedex_entry = 1  # Start with Pokémon ID 1
        print(f"Command server started on port {self.port}")

    def start(self):
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Accepted connection from {addr}")
                client_handler = Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()
        except KeyboardInterrupt:
            print("Shutting down server...")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        try:
            # Send a clear screen command
            color = 15  # Example color, change as needed
            self.clear_screen(client_socket, color)

            # Optionally, send an image after clearing
            display_params = DisplayParameters(
                resolution=(1872,1404),
                generation=1,
                version="red-blue",
                pokedex_entry=self.pokedex_entry,
                variant=None
            )

            img = display_pokemon(
                display_params.resolution,
                display_params.pokedex_entry,
                display_params.generation,
                display_params.version,
                display_params.variant
            )

            if img:
                time.sleep(1)  # Ensure enough time between the commands
                self.draw_image(client_socket, 0, 0, img)
                time.sleep(1)
                self.pokedex_entry += 1
                if self.pokedex_entry > 151:
                    self.pokedex_entry = 1
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()
            print("Client connection closed.")



if __name__ == "__main__":
    import argparse
    from display import Gen1Parameters

    parser = argparse.ArgumentParser(description="Send a command or start a command server.")
    
    # Arguments for manual sending
    # parser.add_argument("--ip", type=str, help="The IP address of the display.")
    # parser.add_argument("--resolution", type=str, default="1872x1404")
    # parser.add_argument("--generation", type=int, default=1)
    # parser.add_argument("--version", type=str, default="red-blue")
    # parser.add_argument("--pokemon", type=int, default=25)
    # parser.add_argument("--variant", type=str, default=None)

    # Argument for running as a server
    parser.add_argument("--port", type=int, default=8319, help="The port to listen on.")

    args = parser.parse_args()

    server = CommandServer(args.port)
    server.start()

