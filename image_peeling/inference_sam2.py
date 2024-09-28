import cv2
import numpy as np
from ultralytics import SAM


class SAM2:
    def __init__(self) -> None:
        self.model = SAM("weights/sam2_l.pt")
        # self.model.info()

    def inference(self, img, points):
        results = self.model(img, points=points, labels=[1])

        mask = results[0].masks.data[0].cpu().numpy()
        mask = mask.astype(np.uint8)

        # マスクがなぜか右にズレるので微調整
        shifted_mask = np.zeros_like(mask)
        shifted_mask[:, :-1] = mask[:, 1:]
        return shifted_mask


if __name__ == "__main__":
    sam2 = SAM2()

    img = cv2.imread(
        "d:/Dropbox/explode/_stable_diffusion/diff/230821_k01c_18_BACK.png"
    )
    points = [[int(480 / 2), int(720 / 2)]]
    mask = sam2.inference(img, points)
    mask *= 255

    mask = cv2.merge([mask, mask, mask])
    blended_img = 0.5 * mask.astype(float) + 0.5 * img.astype(float)
    blended_img = blended_img.astype(np.uint8)
    cv2.imwrite("test.png", blended_img)
