import tkinter as tk
from tkinter import Canvas

import customtkinter
from PIL import Image, ImageTk

FONT_TYPE = "meiryo"


class CanvasFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fonts = (FONT_TYPE, 15)
        self.header_name = "CanvasFrame"

        self.setup_form()

    def setup_form(self):
        self.canvas = Canvas(self, width=1080, height=1080, bg="black")
        self.canvas.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW)

    def on_click(self, event):
        x, y = event.x, event.y
        self.master.peeler.draw(x, y)

    def on_drag(self, event):
        x, y = event.x, event.y
        self.master.peeler.draw(x, y)

    def set_img(self, img):
        pil_img = Image.fromarray(img)
        tk_img = ImageTk.PhotoImage(image=pil_img)

        i_w, i_h = pil_img.size
        c_w, c_h = self.canvas.size()
        if c_w != i_w or c_h != i_h:
            self.canvas.config(width=i_w, height=i_h)

        self.canvas.itemconfig(self.image_on_canvas, image=tk_img)
        self.canvas.image = tk_img
