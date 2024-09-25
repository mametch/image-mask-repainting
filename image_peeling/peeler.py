import os

import cv2
import numpy as np

from image_peeling.inference_sgm import InferenceSegm


class Peeler:
    def __init__(self) -> None:
        self.brush_mode = "Brush"
        self.brush_radius = 50
        self.color_r = 255
        self.color_g = 255
        self.color_b = 255
        self.color_a = 128
        self.img_size = 1000

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

    def alpha_blend(self):
        alpha = self.mask.astype(float) * (self.color_a / 255)
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
        mask = cv2.resize(self.mask, (width, height))

        alpha = mask.astype(float) * (self.color_a / 255)
        alpha = cv2.merge([alpha, alpha, alpha])

        img = self.img_org.astype(float)

        simple_img = np.zeros((height, width, 3))
        simple_img += [self.color_r, self.color_g, self.color_b][::-1]

        blended_img = alpha * simple_img + (1 - alpha) * img
        blended_img = blended_img.astype(np.uint8)
        return blended_img

    def save_img(self, save_mask: bool = True):
        blended_img = self.alpha_blend_org_size()
        root, ext = os.path.splitext(self.img_path)
        save_path = root + "_blend" + ext
        cv2.imwrite(save_path, blended_img)

        if not save_mask:
            return

        height, width, _ = self.img_org.shape
        mask = cv2.resize(self.mask, (width, height))
        mask = mask * 255
        save_path = root + "_mask" + ext
        cv2.imwrite(save_path, mask)
