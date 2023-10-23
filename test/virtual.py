
from .layout import Layout, Block

from lib.pokeImage import resize_image


import tkinter as tk
from PIL import Image, ImageTk


def display_image(image_path):
    # Create a new tkinter window
    window = tk.Tk()
    window.title("Image Display")

    # Load the image using PIL
    pil_image = Image.open(image_path)
    pil_image = resize_image(pil_image, 256)
    
    # Convert the PIL image to a PhotoImage object
    tk_image = ImageTk.PhotoImage(pil_image)

    # Create a label with the image
    label = tk.Label(window, image=tk_image)
    label.pack()

    # Run the tkinter main loop
    window.mainloop()


# other imports and function definitions

if __name__ == "__main__":
    # Code to run only when this script is executed directly
    # For example, tests or demonstrations of functions in the script
    image_path = "0001.png"
    display_image(image_path)

# Provide the path to your image

