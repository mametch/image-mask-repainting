import customtkinter

from image_peeling.canvas_frame import CanvasFrame
from image_peeling.config_frame import ConfigFrame
from image_peeling.img_file_manager import ImgFileManager
from image_peeling.json_util import JsonUtil
from image_peeling.peeler import Peeler

FONT_TYPE = "meiryo"
AFTER_MS = 33


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")

        self.jsonUtil = JsonUtil("config.json")
        self.peeler = Peeler()
        self.imgFileManager = ImgFileManager()

        self.fonts = (FONT_TYPE, 15)
        self.geometry("1300x1000")
        self.title("Image Peeling")
        self.setup_form()

        self.load_form_defaults()
        self.after(AFTER_MS, self.update_img)

    def setup_form(self):
        self.config_frame = ConfigFrame(master=self)
        self.config_frame.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.canvas_frame = CanvasFrame(master=self)
        self.canvas_frame.grid(row=0, column=1, padx=20, pady=20, sticky="w")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def load_form_defaults(self):
        self.config_frame.load_form_defaults()

    def update_img(self):
        img = self.peeler.update_img()
        self.canvas_frame.set_img(img)

        self.after(AFTER_MS, self.update_img)


if __name__ == "__main__":
    app = App()
    app.mainloop()
