import tkinter as tk
from tkinter import PhotoImage

class Window:
    def __init__(self, image):
        self.image = image
        self.root = tk.Tk()
        self.widgets()
        self.root.mainloop()
    def widgets(self):
        self.img = PhotoImage(file=self.image)
        label = tk.Label(self.root, image=self.img)
        label.pack()
image = "C:\\Users\\eee\\Downloads\\Screenshot 2023-12-21 164646.png"
Window(image)