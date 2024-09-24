import os

import customtkinter

FONT_TYPE = "meiryo"


class ConfigFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fonts = (FONT_TYPE, 15)
        self.header_name = "ConfigFrame"

        self.setup_form()

    def setup_form(self):
        # ----- file configs -----
        self.img_path_field = customtkinter.CTkEntry(
            master=self,
            placeholder_text="dir path",
            width=400,
            font=self.fonts,
        )
        self.img_path_field.grid(
            row=0, column=0, padx=10, pady=(10, 10), sticky="ew", columnspan=3
        )

        self.load_button = customtkinter.CTkButton(
            master=self,
            text="Load image",
            command=self.load_button_func,
            font=self.fonts,
        )
        self.load_button.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

        # ----- brush configs -----
        self.switch_brush_mode = customtkinter.CTkSegmentedButton(
            self, values=["Brush", "Erase"], command=self.switch_brush_mode_event
        )
        self.switch_brush_mode.grid(
            row=2, column=1, padx=10, pady=(50, 10), sticky="ew"
        )

        self.brush_radius_label = customtkinter.CTkLabel(
            self,
            text=f"Brush size {self.master.peeler.brush_radius}",
            font=(FONT_TYPE, 13),
        )
        self.brush_radius_label.grid(
            row=3, column=0, padx=10, pady=(10, 10), sticky="ew", columnspan=3
        )
        self.brush_radius_slider = customtkinter.CTkSlider(
            master=self,
            from_=10,
            to=100,
            number_of_steps=9,
            hover=False,
            width=300,
            command=self.brush_radius_slider_event,
        )
        self.brush_radius_slider.grid(
            row=4, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )

        # ----- mask configs -----
        self.color_r_label = customtkinter.CTkLabel(
            self,
            text=f"Color R {self.master.peeler.color_r}",
            font=(FONT_TYPE, 13),
        )
        self.color_r_label.grid(
            row=5, column=0, padx=10, pady=(50, 10), sticky="ew", columnspan=3
        )
        self.color_r_slider = customtkinter.CTkSlider(
            master=self,
            from_=0,
            to=255,
            number_of_steps=255,
            hover=False,
            width=300,
            command=self.color_r_slider_event,
        )
        self.color_r_slider.grid(
            row=6, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )

        self.color_g_label = customtkinter.CTkLabel(
            self,
            text=f"Color G {self.master.peeler.color_g}",
            font=(FONT_TYPE, 13),
        )
        self.color_g_label.grid(
            row=7, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )
        self.color_g_slider = customtkinter.CTkSlider(
            master=self,
            from_=0,
            to=255,
            number_of_steps=255,
            hover=False,
            width=300,
            command=self.color_g_slider_event,
        )
        self.color_g_slider.grid(
            row=8, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )

        self.color_b_label = customtkinter.CTkLabel(
            self,
            text=f"Color B {self.master.peeler.color_b}",
            font=(FONT_TYPE, 13),
        )
        self.color_b_label.grid(
            row=9, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )
        self.color_b_slider = customtkinter.CTkSlider(
            master=self,
            from_=0,
            to=255,
            number_of_steps=255,
            hover=False,
            width=300,
            command=self.color_b_slider_event,
        )
        self.color_b_slider.grid(
            row=10, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )

        self.color_a_label = customtkinter.CTkLabel(
            self,
            text=f"Color A {self.master.peeler.color_a}",
            font=(FONT_TYPE, 13),
        )
        self.color_a_label.grid(
            row=11, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )
        self.color_a_slider = customtkinter.CTkSlider(
            master=self,
            from_=0,
            to=255,
            number_of_steps=255,
            hover=False,
            width=300,
            command=self.color_a_slider_event,
        )
        self.color_a_slider.grid(
            row=12, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )

        # ----- whole image config -----
        self.img_size_label = customtkinter.CTkLabel(
            self,
            text=f"Image size {self.master.peeler.img_size}",
            font=(FONT_TYPE, 13),
        )
        self.img_size_label.grid(
            row=13, column=0, padx=10, pady=(50, 10), sticky="ew", columnspan=3
        )
        self.img_size_slider = customtkinter.CTkSlider(
            master=self,
            from_=500,
            to=2000,
            number_of_steps=10,
            hover=False,
            width=300,
            command=self.img_max_slider_event,
        )
        self.img_size_slider.grid(
            row=14, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )

        # ----- save button -----
        self.save_button = customtkinter.CTkButton(
            master=self,
            text="Save image",
            command=self.save_img_func,
            font=self.fonts,
        )
        self.save_button.grid(row=15, column=1, padx=10, pady=(50, 10), sticky="ew")

    def load_form_defaults(self):
        self.img_path_field.insert(0, self.master.jsonUtil.config["latest_img_path"])
        self.switch_brush_mode.set("Brush")
        self.brush_radius_slider.set(self.master.peeler.brush_radius)
        self.color_r_slider.set(self.master.peeler.color_r)
        self.color_g_slider.set(self.master.peeler.color_g)
        self.color_b_slider.set(self.master.peeler.color_b)
        self.color_a_slider.set(self.master.peeler.color_a)
        self.img_size_slider.set(self.master.peeler.img_size)
        self.load_button_func()

    # ----- event function -----
    def load_button_func(self):
        img_path = self.img_path_field.get()
        if not os.path.isfile(img_path):
            print("img is not found.")
            return

        self.master.peeler.load_img(img_path)
        self.master.jsonUtil.config["latest_img_path"] = img_path
        self.master.jsonUtil.save_json()

    def switch_brush_mode_event(self, value):
        self.master.peeler.brush_mode = value

    def brush_radius_slider_event(self, value):
        value = round(value)
        old_label = self.brush_radius_label.cget("text")
        new_label = f"Brush size {value}"
        if old_label != new_label:
            self.brush_radius_label.configure(text=new_label)
            self.master.peeler.brush_radius = value

    def color_r_slider_event(self, value):
        value = round(value)
        old_label = self.color_r_label.cget("text")
        new_label = f"Color r {value}"
        if old_label != new_label:
            self.color_r_label.configure(text=new_label)
            self.master.peeler.color_r = value

    def color_g_slider_event(self, value):
        value = round(value)
        old_label = self.color_g_label.cget("text")
        new_label = f"Color g {value}"
        if old_label != new_label:
            self.color_g_label.configure(text=new_label)
            self.master.peeler.color_g = value

    def color_b_slider_event(self, value):
        value = round(value)
        old_label = self.color_b_label.cget("text")
        new_label = f"Color b {value}"
        if old_label != new_label:
            self.color_b_label.configure(text=new_label)
            self.master.peeler.color_b = value

    def color_a_slider_event(self, value):
        value = round(value)
        old_label = self.color_a_label.cget("text")
        new_label = f"Color a {value}"
        if old_label != new_label:
            self.color_a_label.configure(text=new_label)
            self.master.peeler.color_a = value

    def brush_density_slider_event(self, value):
        value = round(value)
        old_label = self.brush_density_label.cget("text")
        new_label = f"Brush density {value}"
        if old_label != new_label:
            self.brush_density_label.configure(text=new_label)
            self.master.peeler.brush_density = value

    def decay_slider_event(self, value):
        old_label = self.decay_label.cget("text")
        new_label = f"Decay {value}"
        if old_label != new_label:
            self.decay_label.configure(text=new_label)
            self.master.peeler.decay = value

    def img_max_slider_event(self, value):
        value = round(value)
        old_label = self.img_size_label.cget("text")
        new_label = f"Image max size {value}"
        if old_label != new_label:
            self.img_size_label.configure(text=new_label)
            self.master.peeler.img_size = value
            self.load_imgs()

    def gamma_slider_event(self, value):
        old_label = self.gamma_label.cget("text")
        new_label = f"Gamma {value}"
        if old_label != new_label:
            self.gamma_label.configure(text=new_label)
            self.master.peeler.gamma = value
            self.master.peeler.adjust_gamma()

    def save_img_func(self):
        self.master.peeler.save_img()

    # ----- common function -----
