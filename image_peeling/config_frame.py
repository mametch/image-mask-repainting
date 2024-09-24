import os

import customtkinter

FONT_TYPE = "meiryo"


class ConfigFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fonts = (FONT_TYPE, 15)
        self.header_name = "ConfigFrame"
        self.current_file_id = 0

        self.setup_form()

    def setup_form(self):
        # ----- file configs -----
        self.prev_button = customtkinter.CTkButton(
            master=self,
            text="Prev",
            command=self.prev_button_func,
            font=self.fonts,
        )
        self.prev_button.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="ew")

        self.current_id_label = customtkinter.CTkLabel(
            self, text=f"{self.current_file_id + 1}", font=(FONT_TYPE, 13)
        )
        self.current_id_label.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="ew")

        self.next_button = customtkinter.CTkButton(
            master=self,
            text="Next",
            command=self.next_button_func,
            font=self.fonts,
        )
        self.next_button.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="ew")

        self.img_dir_field = customtkinter.CTkEntry(
            master=self,
            placeholder_text="dir path",
            width=400,
            font=self.fonts,
        )
        self.img_dir_field.grid(
            row=1, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )

        self.load_button = customtkinter.CTkButton(
            master=self,
            text="Load images",
            command=self.load_button_func,
            font=self.fonts,
        )
        self.load_button.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="ew")

        # ----- brush configs -----
        self.brush_radius_label = customtkinter.CTkLabel(
            self,
            text=f"Brush size {self.master.peeler.brush_radius}",
            font=(FONT_TYPE, 13),
        )
        self.brush_radius_label.grid(
            row=3, column=0, padx=10, pady=(50, 10), sticky="ew", columnspan=3
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

        self.brush_density_label = customtkinter.CTkLabel(
            self,
            text=f"Brush density {self.master.peeler.brush_density}",
            font=(FONT_TYPE, 13),
        )
        self.brush_density_label.grid(
            row=5, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )
        self.brush_density_slider = customtkinter.CTkSlider(
            master=self,
            from_=1,
            to=255,
            number_of_steps=254,
            hover=False,
            width=300,
            command=self.brush_density_slider_event,
        )
        self.brush_density_slider.grid(
            row=6, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )

        self.decay_label = customtkinter.CTkLabel(
            self, text=f"Decay {self.master.peeler.decay}", font=(FONT_TYPE, 13)
        )
        self.decay_label.grid(
            row=7, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )
        self.decay_slider = customtkinter.CTkSlider(
            master=self,
            from_=0.0,
            to=0.05,
            number_of_steps=10,
            hover=False,
            width=300,
            command=self.decay_slider_event,
        )
        self.decay_slider.grid(
            row=8, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )

        # ----- whole image config -----
        self.img_size_label = customtkinter.CTkLabel(
            self,
            text=f"Image size {self.master.peeler.img_size}",
            font=(FONT_TYPE, 13),
        )
        self.img_size_label.grid(
            row=9, column=0, padx=10, pady=(50, 10), sticky="ew", columnspan=3
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
            row=10, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )

        self.gamma_label = customtkinter.CTkLabel(
            self,
            text=f"Gamma {self.master.peeler.gamma}",
            font=(FONT_TYPE, 13),
        )
        self.gamma_label.grid(
            row=11, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )
        self.gamma_slider = customtkinter.CTkSlider(
            master=self,
            from_=0.5,
            to=2.5,
            number_of_steps=8,
            hover=False,
            width=300,
            command=self.gamma_slider_event,
        )
        self.gamma_slider.grid(
            row=12, column=0, padx=10, pady=(0, 10), sticky="ew", columnspan=3
        )

    def load_form_defaults(self):
        self.set_current_id_label()
        self.img_dir_field.insert(0, self.master.jsonUtil.config["latest_dir_path"])
        self.brush_radius_slider.set(self.master.peeler.brush_radius)
        self.brush_density_slider.set(self.master.peeler.brush_density)
        self.decay_slider.set(self.master.peeler.decay)
        self.img_size_slider.set(self.master.peeler.img_size)
        self.gamma_slider.set(self.master.peeler.gamma)
        self.load_button_func()

    # ----- event function -----
    def prev_button_func(self):
        if self.current_file_id <= 0:
            return

        self.current_file_id -= 1
        self.set_current_id_label()
        self.load_imgs()

    def next_button_func(self):
        if self.current_file_id >= self.master.imgFileManager.get_length() - 1:
            return

        self.current_file_id += 1
        self.set_current_id_label()
        self.load_imgs()

    def load_button_func(self):
        dir_path = self.img_dir_field.get()
        if not os.path.isdir(dir_path):
            print("dir is not found.")
            return

        self.master.imgFileManager.load_img_paths(dir_path)
        if self.master.imgFileManager.get_length() <= 0:
            print("img not found.")
            return

        self.current_file_id = 0
        self.set_current_id_label()
        self.load_imgs()

        self.master.jsonUtil.config["latest_dir_path"] = dir_path
        self.master.jsonUtil.save_json()

    def brush_radius_slider_event(self, value):
        value = round(value)
        old_label = self.brush_radius_label.cget("text")
        new_label = f"Brush size {value}"
        if old_label != new_label:
            self.brush_radius_label.configure(text=new_label)
            self.master.peeler.brush_radius = value

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

    # ----- common function -----
    def set_current_id_label(self):
        denominator = self.master.imgFileManager.get_length()
        self.current_id_label.configure(
            text=f"{self.current_file_id + 1}/{denominator}"
        )

    def load_imgs(self):
        front_path, back_path = self.master.imgFileManager.get_by_index(
            self.current_file_id
        )
        self.master.peeler.load_imgs(front_path, back_path)
        self.master.peeler.adjust_gamma()
