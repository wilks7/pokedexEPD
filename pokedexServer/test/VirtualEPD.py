from tkinter import Tk, Canvas
from PIL import ImageTk

class VirtualEPD:
    def __init__(self, resolution, rotation=0):
        self.width, self.height = resolution
        self.rotation = rotation

    def display(self, image):
        root = Tk()      
        canvas = Canvas(root, width=self.width, height=self.height)      
        canvas.pack()      
        tk_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=tk_image)      
        
        root.mainloop()   


