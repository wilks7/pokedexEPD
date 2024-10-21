import socket
import struct
import time
from threading import Thread
from PIL import ImageOps
from display import display_pokemon, DisplayParameters

class DisplayCommandHandler:
    def __init__(self):
        pass

    def clear_screen(self, sock, color, apply=True):
        header = struct.pack('<BBHHHH', 1, color, 0, 0, 1872, 1404)
        sock.sendall(header)
        print("Sent clear screen command")

        if apply:
            header = struct.pack('<BBHHHH', 4, 0, 0, 0, 1872, 1404)
            sock.sendall(header)
            print("Sent apply command to refresh display")

    def draw_image(self, sock, posx, posy, orig_image):
        gray_image = ImageOps.grayscale(orig_image)
        width, height = gray_image.size
        pixels = gray_image.load()
        image = bytearray()
        for y in range(height):
            for x in range(0, width, 2):
                byt = (pixels[x, y] // 17) + ((pixels[x + 1, y] // 17) << 4)
                image.append(byt)
        header = struct.pack('<BBHHHH', 2, 15, posx, posy, width, height)
        sock.sendall(header)
        sock.sendall(image)
        header = struct.pack('<BBHHHH', 4, 0, posx, posy, width, height)
        sock.sendall(header)
        print("Sent draw image command")

