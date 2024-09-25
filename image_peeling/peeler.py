import os

import cv2
import numpy as np

from image_peeling.inference_sgm import InferenceSegm


class Peeler:
    def __init__(self) -> None:
        self.brush_mode = "Brush"
        self.brush_radius = 30
        self.color_r = 0
        self.color_g = 0
        self.color_b = 0
        self.color_a = 170
        self.ed_strength = 7
        self.blur_kernel_size = 11
        self.img_size = 1700

        self.img_path = ""
        self.img_org = None
        self.img = None
        self.mask = None

        self.updatable = False

        self.infer = InferenceSegm()

    def load_img(self, img_path: str):
        self.img_path = img_path
        img_np = np.fromfile(img_path, np.uint8)
        self.img_org = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        img_org_rgb = cv2.cvtColor(self.img_org, cv2.COLOR_BGR2RGB)
        self.mask = self.infer.inference(img_org_rgb)

        self.resize_img()
        self.updatable = True

    def load_mask(self, mask_path: str):
        mask_np = np.fromfile(mask_path, np.uint8)
        self.mask = cv2.imdecode(mask_np, cv2.IMREAD_GRAYSCALE)
        self.mask = (self.mask / 255).astype(np.uint8)
        self.resize_img()

    def resize_img(self):
        self.img = self.img_org.copy()

        h, w, _ = self.img.shape
        if w > h:
            aspect_ratio = w / h
            new_w = self.img_size
            new_h = int(self.img_size / aspect_ratio)
        else:
            aspect_ratio = h / w
            new_h = self.img_size
            new_w = int(self.img_size / aspect_ratio)

        self.img = cv2.resize(self.img, (new_w, new_h))
        self.mask = cv2.resize(self.mask, (new_w, new_h))

    def update_img(self):
        if not self.updatable:
            return np.zeros((512, 512, 3), np.uint8)

        blended_img = self.alpha_blend()
        return cv2.cvtColor(blended_img, cv2.COLOR_BGR2RGB)

    def draw(self, x: int, y: int):
        if self.brush_mode == "Brush":
            brush_color = 1
        elif self.brush_mode == "Erase":
            brush_color = 0
        else:
            brush_color = 1

        cv2.circle(
            self.mask,
            center=(x, y),
            radius=self.brush_radius,
            color=brush_color,
            thickness=-1,
        )

    def erode_mask(self):
        kernel = np.ones((self.ed_strength, self.ed_strength), np.uint8)
        self.mask = cv2.erode(self.mask, kernel)

    def dilate_mask(self):
        kernel = np.ones((self.ed_strength, self.ed_strength), np.uint8)
        self.mask = cv2.dilate(self.mask, kernel)

    def save_img(self):
        blended_img = self.alpha_blend_org_size()
        root, ext = os.path.splitext(self.img_path)
        save_path = root + "_blend" + ext
        cv2.imwrite(save_path, blended_img)

    def save_mask(self, is_ed: bool = False):
        height, width, _ = self.img_org.shape
        mask = cv2.resize(self.mask, (width, height))
        mask = mask * 255

        root, ext = os.path.splitext(self.img_path)
        if is_ed > 0:
            kernel = np.ones((self.ed_strength, self.ed_strength), np.uint8)
            d_mask = cv2.dilate(mask, kernel, self.ed_strength)
            d_save_path = root + f"_mask{self.ed_strength}" + ext
            cv2.imwrite(d_save_path, d_mask)
        else:
            save_path = root + "_mask" + ext
            cv2.imwrite(save_path, mask)

    def alpha_blend(self):
        mask = self.get_antialiasing_mask()
        alpha = mask.astype(float) * (self.color_a / 255)
        alpha = cv2.merge([alpha, alpha, alpha])

        img = self.img.astype(float)
        height, width, _ = self.img.shape

        simple_img = np.zeros((height, width, 3))
        simple_img += [self.color_r, self.color_g, self.color_b][::-1]

        blended_img = alpha * simple_img + (1 - alpha) * img
        blended_img = blended_img.astype(np.uint8)
        return blended_img

    def alpha_blend_org_size(self):
        height, width, _ = self.img_org.shape
        mask = self.get_antialiasing_mask()
        mask = cv2.resize(mask, (width, height))

        alpha = mask.astype(float) * (self.color_a / 255)
        alpha = cv2.merge([alpha, alpha, alpha])

        img = self.img_org.astype(float)

        simple_img = np.zeros((height, width, 3))
        simple_img += [self.color_r, self.color_g, self.color_b][::-1]

        blended_img = alpha * simple_img + (1 - alpha) * img
        blended_img = blended_img.astype(np.uint8)
        return blended_img

    def get_antialiasing_mask(self):
        if self.blur_kernel_size <= 1:
            return self.mask

        mask = self.mask * 255
        mask = cv2.GaussianBlur(mask, (self.blur_kernel_size, self.blur_kernel_size), 0)
        return mask / 255
