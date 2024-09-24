import cv2
import numpy as np


class Peeler:
    def __init__(self) -> None:
        self.brush_radius = 50
        self.brush_density = 15
        self.decay = 0.01
        self.img_size = 1000
        self.gamma = 1

        self.front_img_org = None
        self.back_img_org = None
        self.front_img = None
        self.back_img = None
        self.mask = None
        self.black = None

        self.updatable = False

    def load_imgs(self, front_path: str, back_path: str):
        front_np = np.fromfile(front_path, np.uint8)
        self.front_img_org = cv2.imdecode(front_np, cv2.IMREAD_COLOR)

        h, w, _ = self.front_img_org.shape
        if w > h:
            aspect_ratio = w / h
            new_w = self.img_size
            new_h = int(self.img_size / aspect_ratio)
        else:
            aspect_ratio = h / w
            new_h = self.img_size
            new_w = int(self.img_size / aspect_ratio)
        self.front_img_org = cv2.resize(self.front_img_org, (new_w, new_h))
        h, w, _ = self.front_img_org.shape

        back_np = np.fromfile(back_path, np.uint8)
        self.back_img_org = cv2.imdecode(back_np, cv2.IMREAD_COLOR)
        self.back_img_org = cv2.resize(self.back_img_org, (w, h))

        self.front_img = self.front_img_org.copy()
        self.back_img = self.back_img_org.copy()

        self.mask = np.zeros((h, w), dtype=np.uint8)
        self.black = np.zeros((h, w), dtype=np.uint8)
        self.updatable = True

    def update_img(self):
        if not self.updatable:
            return np.zeros((512, 512, 3), np.uint8)

        self.decay_mask()
        blended_img = self.alpha_blend()
        return cv2.cvtColor(blended_img, cv2.COLOR_BGR2RGB)

    def draw(self, x: int, y: int):
        draw_mask = np.zeros(self.mask.shape, dtype=np.uint8)
        cv2.circle(
            draw_mask,
            center=(x, y),
            radius=self.brush_radius,
            color=self.brush_density,
            thickness=-1,
        )
        self.mask += draw_mask
        self.mask = np.clip(self.mask, 0, 255)

    def decay_mask(self):
        self.mask = self.decay * self.black + (1 - self.decay) * self.mask

    def alpha_blend(self):
        alpha = self.mask.astype(float) / 255.0
        alpha = cv2.merge([alpha, alpha, alpha])

        front = self.front_img.astype(float)
        back = self.back_img.astype(float)

        blended_img = alpha * back + (1 - alpha) * front
        blended_img = blended_img.astype(np.uint8)
        return blended_img

    def adjust_gamma(self):
        self.back_img = self.back_img_org.copy()
        invGamma = 1.0 / self.gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        self.back_img = cv2.LUT(self.back_img, table)
