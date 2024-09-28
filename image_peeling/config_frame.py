import os

import customtkinter

FONT_TYPE = "meiryo"


class ConfigFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fonts = (FONT_TYPE, 15)
        self.header_name = "ConfigFrame"

        self.row_index = 0
        self.setup_form_file()
        self.setup_form_brush()
        self.setup_form_mask()
        self.setup_form_whole_img()
        self.setup_form_save()

    def setup_form_file(self, start_row=0):
        self.img_path_field = customtkinter.CTkEntry(
            master=self,
            placeholder_text="dir path",
            width=400,
            font=self.fonts,
        )
        self.img_path_field.grid(
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(10, 10),
            sticky="ew",
            columnspan=3,
        )

        row_index = self.add_row_index()
        self.load_button = customtkinter.CTkButton(
            master=self,
            text="Load image",
            command=self.load_button_func,
            font=self.fonts,
        )
        self.load_button.grid(
            row=row_index, column=0, padx=10, pady=(0, 10), sticky="ew"
        )

        self.load_mask_button = customtkinter.CTkButton(
            master=self,
            text="Load mask",
            command=self.load_mask_button_func,
            font=self.fonts,
        )
        self.load_mask_button.grid(
            row=row_index, column=2, padx=10, pady=(0, 10), sticky="ew"
        )

    def setup_form_brush(self):
        self.switch_brush_mode = customtkinter.CTkSegmentedButton(
            self,
            values=["Brush", "Erase", "Paint"],
            command=self.switch_brush_mode_event,
        )
        self.switch_brush_mode.grid(
            row=self.add_row_index(), column=1, padx=10, pady=(50, 10), sticky="ew"
        )

        self.brush_radius_label = customtkinter.CTkLabel(
            self,
            text=f"Brush size {self.master.peeler.brush_radius}",
            font=(FONT_TYPE, 13),
        )
        self.brush_radius_label.grid(
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(0, 0),
            sticky="ew",
            columnspan=3,
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
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(0, 10),
            sticky="ew",
            columnspan=3,
        )

    def setup_form_mask(self):
        self.color_r_label = customtkinter.CTkLabel(
            self,
            text=f"Color R {self.master.peeler.color_r}",
            font=(FONT_TYPE, 13),
        )
        self.color_r_label.grid(
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(50, 0),
            sticky="ew",
            columnspan=3,
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
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(0, 10),
            sticky="ew",
            columnspan=3,
        )

        self.color_g_label = customtkinter.CTkLabel(
            self,
            text=f"Color G {self.master.peeler.color_g}",
            font=(FONT_TYPE, 13),
        )
        self.color_g_label.grid(
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(0, 0),
            sticky="ew",
            columnspan=3,
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
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(0, 10),
            sticky="ew",
            columnspan=3,
        )

        self.color_b_label = customtkinter.CTkLabel(
            self,
            text=f"Color B {self.master.peeler.color_b}",
            font=(FONT_TYPE, 13),
        )
        self.color_b_label.grid(
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(0, 0),
            sticky="ew",
            columnspan=3,
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
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(0, 10),
            sticky="ew",
            columnspan=3,
        )

        self.color_a_label = customtkinter.CTkLabel(
            self,
            text=f"Color A {self.master.peeler.color_a}",
            font=(FONT_TYPE, 13),
        )
        self.color_a_label.grid(
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(0, 0),
            sticky="ew",
            columnspan=3,
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
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(0, 10),
            sticky="ew",
            columnspan=3,
        )

        row_index = self.add_row_index()
        self.dilate_button = customtkinter.CTkButton(
            master=self,
            text="Dilate",
            command=self.dilate_button_func,
            font=self.fonts,
        )
        self.dilate_button.grid(
            row=row_index, column=0, padx=10, pady=(0, 10), sticky="ew"
        )

        self.erode_button = customtkinter.CTkButton(
            master=self,
            text="Erode",
            command=self.erode_button_func,
            font=self.fonts,
        )
        self.erode_button.grid(
            row=row_index, column=2, padx=10, pady=(0, 10), sticky="ew"
        )

        self.ed_strength_label = customtkinter.CTkLabel(
            self,
            text=f"ED Strength {self.master.peeler.ed_strength}",
            font=(FONT_TYPE, 13),
        )
        self.ed_strength_label.grid(
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(0, 0),
            sticky="ew",
            columnspan=3,
        )
        self.ed_strength_slider = customtkinter.CTkSlider(
            master=self,
            from_=3,
            to=21,
            number_of_steps=9,
            hover=False,
            width=300,
            command=self.ed_strength_slider_event,
        )
        self.ed_strength_slider.grid(
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(0, 10),
            sticky="ew",
            columnspan=3,
        )

        self.expand_mask_up_button = customtkinter.CTkButton(
            master=self,
            text="Up",
            command=self.expand_mask_up_func,
            font=self.fonts,
        )
        self.expand_mask_up_button.grid(
            row=self.add_row_index(), column=1, padx=10, pady=(0, 10), sticky="ew"
        )

        row_index = self.add_row_index()
        self.expand_mask_left_button = customtkinter.CTkButton(
            master=self,
            text="Left",
            command=self.expand_mask_left_func,
            font=self.fonts,
        )
        self.expand_mask_left_button.grid(
            row=row_index, column=0, padx=10, pady=(0, 10), sticky="ew"
        )

        self.expand_mask_label = customtkinter.CTkLabel(
            self,
            text="Expand mask",
            font=(FONT_TYPE, 13),
        )
        self.expand_mask_label.grid(
            row=row_index, column=1, padx=10, pady=(0, 0), sticky="ew", columnspan=3
        )

        self.expand_mask_right_button = customtkinter.CTkButton(
            master=self,
            text="Right",
            command=self.expand_mask_right_func,
            font=self.fonts,
        )
        self.expand_mask_right_button.grid(
            row=row_index, column=2, padx=10, pady=(0, 10), sticky="ew"
        )

        self.expand_mask_down_button = customtkinter.CTkButton(
            master=self,
            text="Down",
            command=self.expand_mask_down_func,
            font=self.fonts,
        )
        self.expand_mask_down_button.grid(
            row=self.add_row_index(), column=1, padx=10, pady=(0, 10), sticky="ew"
        )

        self.blur_kernel_size_label = customtkinter.CTkLabel(
            self,
            text=f"Blur kernel size {self.master.peeler.blur_kernel_size}",
            font=(FONT_TYPE, 13),
        )
        self.blur_kernel_size_label.grid(
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(0, 0),
            sticky="ew",
            columnspan=3,
        )
        self.blur_kernel_size_slider = customtkinter.CTkSlider(
            master=self,
            from_=1,
            to=31,
            number_of_steps=15,
            hover=False,
            width=300,
            command=self.blur_kernel_size_slider_event,
        )
        self.blur_kernel_size_slider.grid(
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(0, 10),
            sticky="ew",
            columnspan=3,
        )

    def setup_form_whole_img(self):
        self.img_size_label = customtkinter.CTkLabel(
            self,
            text=f"Image size {self.master.peeler.img_size}",
            font=(FONT_TYPE, 13),
        )
        self.img_size_label.grid(
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(50, 0),
            sticky="ew",
            columnspan=3,
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
            row=self.add_row_index(),
            column=0,
            padx=10,
            pady=(0, 10),
            sticky="ew",
            columnspan=3,
        )

    def setup_form_save(self):
        self.save_button = customtkinter.CTkButton(
            master=self,
            text="Save image",
            command=self.save_img_func,
            font=self.fonts,
        )
        self.save_button.grid(
            row=self.add_row_index(), column=1, padx=10, pady=(50, 10), sticky="ew"
        )

    def load_form_defaults(self):
        self.img_path_field.insert(0, self.master.jsonUtil.config["latest_img_path"])
        self.switch_brush_mode.set("Brush")
        self.brush_radius_slider.set(self.master.peeler.brush_radius)
        self.color_r_slider.set(self.master.peeler.color_r)
        self.color_g_slider.set(self.master.peeler.color_g)
        self.color_b_slider.set(self.master.peeler.color_b)
        self.color_a_slider.set(self.master.peeler.color_a)
        self.ed_strength_slider.set(self.master.peeler.ed_strength)
        self.blur_kernel_size_slider.set(self.master.peeler.blur_kernel_size)
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

    def load_mask_button_func(self):
        img_path = self.img_path_field.get()
        root, ext = os.path.splitext(img_path)
        mask_path = root + "_mask" + ext
        if not os.path.isfile(mask_path):
            print("img is not found.")
            return

        self.master.peeler.load_mask(mask_path)

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

    def erode_button_func(self):
        self.master.peeler.erode_mask()

    def dilate_button_func(self):
        self.master.peeler.dilate_mask()

    def ed_strength_slider_event(self, value):
        value = round(value)
        old_label = self.ed_strength_label.cget("text")
        new_label = f"ED Strength {value}"
        if old_label != new_label:
            self.ed_strength_label.configure(text=new_label)
            self.master.peeler.ed_strength = value

    def expand_mask_up_func(self):
        self.master.peeler.expand_mask("up")

    def expand_mask_down_func(self):
        self.master.peeler.expand_mask("down")

    def expand_mask_left_func(self):
        self.master.peeler.expand_mask("left")

    def expand_mask_right_func(self):
        self.master.peeler.expand_mask("right")

    def blur_kernel_size_slider_event(self, value):
        value = round(value)
        old_label = self.blur_kernel_size_label.cget("text")
        new_label = f"Blur kernel size {value}"
        if old_label != new_label:
            self.blur_kernel_size_label.configure(text=new_label)
            self.master.peeler.blur_kernel_size = value

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

    def gamma_slider_event(self, value):
        old_label = self.gamma_label.cget("text")
        new_label = f"Gamma {value}"
        if old_label != new_label:
            self.gamma_label.configure(text=new_label)
            self.master.peeler.gamma = value
            self.master.peeler.adjust_gamma()

    def save_img_func(self):
        self.master.peeler.save_img()
        self.master.peeler.save_mask(False)
        self.master.peeler.save_mask(True)

    # ----- common function -----
    def add_row_index(self):
        self.row_index += 1
        return self.row_index
